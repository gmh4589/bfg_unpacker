import os
import ffmpeg
import psutil
from icecream import ic
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize

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
        self.info_only = False

    def is_file_in_use(self):
        for process in psutil.process_iter(['pid', 'open_files']):

            try:

                for file_info in process.open_files():
                    # ic(file_info.path)

                    if os.path.abspath(file_info.path) == os.path.abspath(self.file_name):
                        return True

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    @file_reaper
    def run(self):
        out_path = f'{self.output_folder}/{os.path.basename(self.file_name).split(".")[-2]}.{self.format}'
        media_info = ffmpeg.probe(self.file_name)
        dur = float(media_info['format']['duration'])
        ic(media_info)
        ic(dur)

        if self.info_only:
            print(media_info)
            return

        ar = (f'"{self.path_to_root}data\\ffmpeg\\ffmpeg.exe" '
              f'-i "{self.file_name}" '
              f'-vcodec {self.v_codec} '
              f'-vb {self.vb} '
              f'-vf scale="{self.vf_scale}" '
              f'-acodec {self.a_codec} '
              f'-ab {self.ab} '
              f'-map 0:0 -map 0:{self.map} '
              f'"{out_path}"')

        ic(ar)

        if 'k' in self.ab:
            ab = int(self.ab[:-1]) * 1000
        elif 'M' in self.ab:
            ab = int(self.ab[:-1]) * 1000000
        else:
            ab = int(self.ab)

        if 'k' in self.vb:
            vb = int(self.vb[:-1]) * 1000
        elif 'M' in self.vb:
            vb = int(self.vb[:-1]) * 1000000
        else:
            vb = int(self.vb)

        size = int(((ab + vb) * dur) / 8)
        ic(size)

        Popen(ar, stdout=PIPE, stderr=PIPE, encoding='utf-8')

        while True:

            try:
                new = os.path.getsize(out_path)
                ic(new)
            except FileNotFoundError:
                new = 0

            percent = int(100/size * new)
            self.update_signal.emit(percent, '', f'{localize.convert} - {self.file_name}...', False)

            # Конечно, костыль, но работает...
            if not self.is_file_in_use(): break
            # TODO: Попытка обратиться к Popen.poll() приводит к зависанию процесса
            # if ff.poll() is not None: break

        self.update_signal.emit(100, '', localize.done, True)
