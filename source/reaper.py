import shutil
import os
import io
from functools import wraps
from subprocess import Popen
from datetime import datetime
import zlib

from PyQt6.QtCore import QThread, pyqtSignal
from abc import abstractmethod
from icecream import ic
from pathlib import Path
from tkinter.messagebox import showinfo, askyesno
from threading import Thread

from source.ui import localize
from source.setting import setting
from source.codecs.zip_methods import ZipMethods
from source.out_reader import OutReader
from source.get_ext import GetExt

DEBUG = False


def logger(level: str, message: str, show: bool = False, messagebox: bool = False) -> None:

    if show:
        print(message)

    with open('log.txt', 'a') as log:
        log.write(f'{datetime.now()} - [{level}]: {message}\n')

    if messagebox:
        showinfo(title=level, message=message)


def file_reaper(func_name):

    @wraps(func_name)
    def wrapper(*args, **kwargs):
        error = None
        function = str(func_name)
        start = datetime.now()

        if DEBUG:

            try:
                func_name(*args, **kwargs)
            except Exception as e:
                error = e

        else:
            func_name(*args, **kwargs)

        end = datetime.now()
        print(f'{localize.done}\n'
              f'{localize.duration} {end - start}')

        if error is None:
            logger(f'INFO',
                   f'\n\tFunction: {function}\n\tStart: {start}\n\tEnd: {end}\n\tDuration: {end - start}\n')
        else:
            print(f'ERROR IN {function}: {error}!!!')
            logger(f'ERROR',
                   f'\n\tFunction: {function}\n\tStart: {start}\n\tError: {error}\n')

    return wrapper


class Reaper(QThread, GetExt):
    update_signal = pyqtSignal(int, str, str, bool) # progress, file count, message, isending
    user_choice_signal = pyqtSignal(str, list, object) # header text, drop menu list, callback
    COMPRESSED = True
    file_name = ''
    path_to_root = os.path.dirname(os.path.abspath(f"{os.path.curdir}\\game_base.db"))
    com_type = None
    new_ext = 'dat'
    maximum = 100
    script_name = None

    def __init__(self, stng=setting):
        super().__init__()
        self.setting = stng
        self.output_folder = self.setting['Main']['out_path']
        os.makedirs(self.output_folder, exist_ok=True)
        self.out_reader = None
        self.out_print = None
        self.err_print = None
        
    @abstractmethod
    def run(self):
        pass
    
    def update_pb(self, file_count: int, current_file: int, file_name: str):

        file_count = 1 if file_count == 0 else file_count
        current_file = 1 if current_file == 0 else current_file

        ic(f'{current_file}\\{file_count}: {localize.saving} - {file_name}...')
        print(f'{current_file}\\{file_count}: {localize.saving} - {file_name}...'.replace('<font', ''))

        self.update_signal.emit(int(100 / file_count * current_file),
                                f'{current_file}\\{file_count}',
                                f'{localize.saving} - {file_name}...',
                                current_file + 1 >= file_count)
        
    def update_ffmpeg(self, duration: int, current_time: int, progress):
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            p = int(100 / duration * current_time)
            percent = p if p < 95 else 95
            
            self.update_signal.emit(percent, 
                                    f"TIME: {str(progress.time).split('.')[0]}\\{formatted_time}", 
                                    f"SPEED: {progress.speed} | FPS: {progress.fps}", 
                                    False)

    @staticmethod
    def folderSize(path, was_files=0):
        file_size = 0
        numfile = 0
        iteration = 0

        for file in Path(path).rglob('*'):

            if os.path.isfile(file):

                try:
                    file_size += os.path.getsize(file)
                    numfile += 1
                except (FileNotFoundError, FileExistsError):
                    break

            iteration += 1

        return file_size, numfile - was_files, iteration

    @staticmethod
    def multi_vol():
        agree = askyesno(title=localize.message,
                         message=localize.multivol)
        return agree

    @staticmethod
    def file_save(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as nf:
            nf.write(data)
    
    def get_name(self, file_io: io.BytesIO):
        name = ''

        while True:

            sym = file_io.read(1)

            if sym == b'\0':
                break

            try:
                name += sym.decode('utf-8')
            except UnicodeDecodeError:
                pass

        
        return name

    def magic(self, magic: list, read_magic: bytes | int, message: str) -> bool:

        for m in magic:

            if m == read_magic:
                return True

        else:
            print(localize.not_correct_file.replace('%%', message))
            self.update_signal.emit(100, '', '', True)
            return False

    def start_reader(self, proc, out_print=False):
        self.out_reader = OutReader(out_print=out_print)
        Thread(target=self.out_reader.out_reader, args=[proc,], daemon=True).start()
        Thread(target=self.out_reader.err_reader, args=[proc,], daemon=True).start()

    def pipe_reader(self, prg, chang_dir: bool = False):
        out_reader = OutReader()
        pr_err = ''
        pr_out = ''

        Thread(target=out_reader.out_reader, args=[prg,], daemon=True).start()
        Thread(target=out_reader.err_reader, args=[prg,], daemon=True).start()

        while prg.poll() is None:

            try:
                self.update_signal.emit(0, '', f'{".".join(out_reader.output)}...', False)

                if out_reader.err and out_reader.err != pr_err:
                    print(out_reader.err)
                    pr_err = out_reader.err

                if out_reader.out and out_reader.out != pr_out:
                    print(out_reader.out)
                    pr_out = out_reader.out

            except Exception as e:
                ic(e)
                self.update_signal.emit(0, '', '', False)

        out_reader.end = True
        self.update_signal.emit(0, '', '', True)

    def smart_deflate(self, data: bytes) -> bytes:

        # обычный zlib
        try:
            return zlib.decompress(data)
        except zlib.error:
            pass

        # raw deflate
        try:
            return zlib.decompress(data, -15)
        except zlib.error:
            pass

        # deflate noerror
        try:
            obj = zlib.decompressobj(-15)
            return obj.decompress(data)
        except zlib.error:
            pass

        # deflate noerror via QuickBMS
        try:
            temp_path = f"{os.environ['TEMP']}\\bfg_unpacker\\temp_file.dat"

            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            with open(temp_path, 'wb') as tf:
                tf.write(data)

            return self.unzip(temp_path, ZipMethods.DEFLATE_NOERROR, file_move=False)

        except (FileNotFoundError, PermissionError, OSError):
            print("Unknown deflate format")
            return data
            # raise ValueError("Unknown deflate format")
        
    def encrypt(self, f_name: str, crypt_method: str, crypt_key: str | bytes | int,
                get_ext: bool = False, test: bool = False):
        out_path = self.output_folder if test else os.environ['TEMP']

        # TODO: Need tests
        dump_name = crypt_method + '_enc.dmp'
        script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" '
                  f'-o -a "{crypt_method}{" " + crypt_key if crypt_key else ""}" '
                  f'"{self.path_to_root}\\data\\QuickBMS\\encryption_scan.bms")" '
                  f'"{f_name}" "{out_path}"').replace("/", "\\")

    # TODO: Very slow working... 🐌
    def unzip(self, f_name: str, c_num: int = 1, file_move: bool = True, wait: bool = True):
        out_path = f"{os.environ['TEMP']}\\bfg_unpacker\\{os.path.basename(f_name).replace('.', '_')}"

        if not os.path.exists(out_path):
            os.makedirs(out_path)

        script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" '
                  f'-o -a "{c_num}" '
                  f'"{self.path_to_root}\\data\\QuickBMS\\comtype_scan2.bms" '
                  f'"{f_name}" "{out_path}"').replace("/", "\\")

        dump_name = ZipMethods.codec_indexes()[c_num] + '.dmp'
        dump_file = f"{out_path}\\{dump_name}"

        Popen(script).wait() if wait else Popen(script).poll()

        if file_move:
            shutil.move(dump_file, f_name)
            return None
        else:

            with open(dump_file, 'rb') as nf:
                return nf.read()

