import os
import json
from datetime import datetime

from PyQt6.QtCore import QThread
from icecream import ic
from ffmpeg import FFmpeg, Progress
from ffmpeg.errors import FFmpegError

from source.reaper import Reaper, file_reaper, logger
from source.qprocess import QProcessList
from source.ui import localize
from source.setting import setting

def ffmpeg_conv(**kwargs):
    conv = Converter(stng=setting)
    conv.format = kwargs.get('Format', None)
    conv.file_name = kwargs.get('file_name', None)
    conv.ab = kwargs.get('Audio Bitrate', None)
    conv.a_codec = kwargs.get('Audio Codec', None)
    conv.map = kwargs.get('Audio Track', None)
    conv.vf_scale = f"{kwargs.get('Width', None)}:{kwargs.get('High', None)}"
    conv.vb = kwargs.get('Video Bitrate', None)
    conv.v_codec = kwargs.get('Video Codec', None)
    conv.frequency = kwargs.get('Frequency', None)
    conv.channels = kwargs.get('Channels', None)
    conv.speed = kwargs.get('Speed', None)
    conv.info_only = kwargs.get('Info', None)
    proc = QProcessList()
    ic(conv.file_name)

    QThread(proc.q_connect(conv, conv.file_name, header=f'{localize.convert}: {conv.file_name}...')).run()


class ErrorMixin:

    def show_error(self, e):
        print(localize.unsupported_ftype)
        logger('ERROR', f"{localize.unsupported_ftype} {str(e)}")
        self.update_pb(1, 1, self.file_name)


class Converter(Reaper, ErrorMixin):

    def __init__(self, stng=setting, *args, **kwargs):
        super().__init__(stng=stng, *args, **kwargs)
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
    
    def get_seconds(self, time: str):
        duration = time.split(':')

        if len(duration) == 3:
            return int(duration[0]) * 3600 + int(duration[1]) * 60 + float(duration[2])
        elif len(duration) == 1:
            return int(float(time))

    @file_reaper
    def run(self):
        out_path = f'{self.setting['Main']['out_path']}\\{os.path.basename(self.file_name).replace(".", "_")}\\{'.'.join(os.path.basename(self.file_name).split(".")[:-1])}.{self.format}'

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        ic(out_path)

        try:
            probe = FFmpeg(executable='data\\ffmpeg\\ffprobe.exe').input(self.file_name, print_format="json", show_streams=None)
            meta = json.loads(probe.execute())
            # ic(meta)
        except FFmpegError as e:
            print(localize.unsupported_ftype)
            logger('ERROR', f"{localize.unsupported_ftype} {str(e)}")
            self.update_pb(1, 1, self.file_name)
            return
                
        # Get duration for variuos variants
        dur_list = []
        lng_list = ['', '-eng', '-jap', '-rus', '-fra', '-deu', '-kor', '-tur', '-chn']

        for i in range(10):
            try:
                dur_list.append(self.get_seconds(str(meta['streams'][i].get('duration', '0'))))
            except (KeyError, IndexError):
                break

        for lng in lng_list:
            try:
                dur_list.append(self.get_seconds(str(meta['streams'][0]['tags'].get(f'DURATION{lng}', '0'))))
            except (KeyError, IndexError):
                pass

        dur_get = max(dur_list)
        dur_default = 7200  # default 2 hours
        duration = dur_get if dur_get > 0 else dur_default

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
                self.update_pb(duration, duration, out_path)

        @ffmpeg.on("progress")
        def on_progress(progress: Progress):
            now = progress.time.seconds
            self.update_ffmpeg(duration, now, progress)

        @ffmpeg.on("completed")
        def on_completed():
            self.update_pb(duration, duration, out_path)

        try:
            ffmpeg.execute()    
        except FFmpegError as e:
            self.show_error(e)


class MediaInfo(Reaper, ErrorMixin):

    def run(self):
        out_path = f'{self.setting['Main']['out_path']}\\{os.path.basename(self.file_name).replace(".", "_")}\\{os.path.basename(self.file_name)}.media_info.json'
        
        try:
            probe = FFmpeg(executable='data\\ffmpeg\\ffprobe.exe').input(self.file_name, print_format="json", show_streams=None)
            meta = json.loads(probe.execute())
        except FFmpegError as e:
            self.show_error(e)
            return
        
        with open(out_path, "w") as f:
            json.dump(meta, f, indent=4)

        for key, value in meta['streams'][0].items():
            print(f"{key}: {value}")
        
        self.update_pb(1, 1, self.file_name)

