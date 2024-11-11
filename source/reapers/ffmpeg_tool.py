import os
import json

from PyQt6.QtCore import QThread
from icecream import ic
from ffmpeg import FFmpeg, Progress

from source.reaper import Reaper, file_reaper, logger
from source.qprocess import QProcessList
from source.ui import localize


def ffmpeg_conv(args: dict):

    conv = Converter()
    conv.format = args.get('Format', None)
    conv.file_name = args.get('file_name', None)
    conv.ab = args.get('Audio Bitrate', None)
    conv.a_codec = args.get('Audio Codec', None)
    conv.map = args.get('Audio Track', None)
    conv.vf_scale = f"{args.get('Width', None)}:{args.get('High', None)}"
    conv.vb = args.get('Video Bitrate', None)
    conv.v_codec = args.get('Video Codec', None)
    conv.frequency = args.get('Frequency', None)
    conv.channels = args.get('Channels', None)
    conv.speed = args.get('Speed', None)
    conv.info_only = args.get('Info', None)
    proc = QProcessList()
    ic(conv.file_name)

    QThread(proc.q_connect(conv, conv.file_name, header=f'{localize.convert}: {conv.file_name}...')).run()


class Converter(Reaper):

    def __init__(self):
        super().__init__()
        self.v_codec = 'hevc'
        self.vb = '5M'
        self.vf_scale = '1920:1080'
        self.a_codec = 'ac3'
        self.ab = '192k'
        self.map = '1'
        self.format = 'mkv'
        self.frequency = '44100'
        self.channels = '2'
        self.speed = '1'
        self.info_only = None

    @file_reaper
    def run(self):
        out_path = f'{self.output_folder}\\{os.path.basename(self.file_name).split(".")[0]}.{self.format}'
        ic(out_path)
        probe = FFmpeg(executable='data\\ffmpeg\\ffprobe.exe').input(self.file_name, print_format="json", show_streams=None)
        meta = json.loads(probe.execute())
        ic(meta)

        if self.info_only is not None:

            for key, value in meta['streams'][0].items():
                print(f"{key}: {value}")
            
            self.update_pb(1, 1, self.file_name)
            return

        frame_rate = int(meta['streams'][0]['r_frame_rate'].split('/')[0])

        try:
            duration = float(meta['streams'][0]['duration'])
        except (KeyError, IndexError):

            try:
                duration = meta['streams'][0]['tags']['DURATION'].split(':')
                duration = float(duration[0]) * 3600 + int(duration[1]) * 60 + float(duration[2])
            except (KeyError, IndexError):
                duration = 0

        frames = int(frame_rate * duration)
        ffmpeg = FFmpeg(executable='data\\ffmpeg\\ffmpeg.exe').option("y").input(self.file_name)

        if self.v_codec is not None:
            ffmpeg.output(
                url=out_path,
                # map=["0:0", f"1:{self.map}"],
                options={"codec:v": self.v_codec,
                         "vb": self.vb,
                         "codec:a": self.a_codec,
                         "ab": self.ab,
                         "filter:v": f"scale={self.vf_scale}",
                         "strict": '-2',
                         }
            )

        elif self.a_codec is not None:
            ffmpeg.output(
                url=out_path,
                options={"codec:a": self.a_codec,
                         "ab": self.ab,
                         "filter:a": f"asetrate={self.frequency} atempo={self.speed}",
                         "strict": '-2',
                         }
            )

        else:
            ffmpeg.output(url=out_path)

        @ffmpeg.on("stderr")
        def on_stderr(line):
            ic(line)
            print(line)
            logger('DEBUG', line)

            if 'Conversion failed!' in line or 'error' in line.lower():
                self.update_pb(frames, frames, out_path)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            self.update_pb(frames, progress.frame, out_path)

        @ffmpeg.on("completed")
        def on_completed():
            self.update_pb(frames, frames, out_path)

        ffmpeg.execute()
