import threading
import os
from subprocess import Popen
from PyQt6.QtCore import QThread, pyqtSignal
from abc import abstractmethod
from tkinter.messagebox import showinfo
from icecream import ic
from datetime import datetime
from pathlib import Path
from tkinter.messagebox import askyesno
from threading import Thread

from source.ui import localize
from source.setting import setting
from source.codecs.zip_methods import ZipMethods
from source.out_reader import OutReader

DEBUG = False if os.path.exists('dev_tools') else True


def logger(level: str, message: str, show: bool = False, messagebox: bool = False) -> None:

    if show:
        print(message)

    with open('log.txt', 'a') as log:
        log.write(f'{datetime.now()} - [{level}]: {message}\n')

    if messagebox:
        showinfo(title=level, message=message)


# class file_reaper:
#     # TODO: DEBUG alwais work, even if DEBUG = False

#     def __init__(self, func):
#         self.func = func 

#     def __get__(self, instance, owner):
#         return lambda *args, **kwargs: self.__call__(instance, *args, **kwargs)

#     def __call__(self, obj, *args, **kwargs):
#         global DEBUG
#         error = None
#         function_name = str(self.func).split(" ")[1]
#         start = datetime.now()

#         try:
#             if DEBUG:
#                 try:
#                     result = self.func(obj, *args, **kwargs)
#                 except Exception as e:
#                     error = e
#                     result = None
#             else:
#                 result = self.func(obj, *args, **kwargs)
#         except Exception as e:
#             error = e
#             result = None

#         end = datetime.now()
#         print(f'{localize.done}\n{localize.duration} {end - start}')

#         if error is None:
#             logger('INFO',
#                    f'\n\tFunction: {function_name}\n\tStart: {start}\n\tEnd: {end}\n\tDuration: {end - start}\n')
#         else:
#             print(f'ERROR IN {function_name}: {error}!!!')
#             logger('ERROR',
#                    f'\n\tFunction: {function_name}\n\tStart: {start}\n\tError: {error}\n')

#         return result

def file_reaper(func_name):

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


class Reaper(QThread):
    update_signal = pyqtSignal(int, str, str, bool) # progress, file count, message, isending
    user_choice_signal = pyqtSignal(str, list, object) # header text, drop menu list, callback
    COMPRESSED = True
    file_name = ''
    path_to_root = os.path.dirname(os.path.abspath(f"{os.path.curdir}\\game_base.db"))
    com_type = None
    new_ext = 'dat'

    def __init__(self):
        super().__init__()
        self.setting = setting
        self.output_folder = self.setting['Main']['out_path']
        os.makedirs(self.output_folder, exist_ok=True)
        
    @abstractmethod
    def run(self):
        pass
    
    def update_pb(self, file_count: int, current_file: int, file_name: str):

        file_count = 1 if file_count == 0 else file_count
        current_file = 1 if current_file == 0 else current_file
        ic(f'{current_file}\\{file_count}: {localize.saving} - {file_name}...')
        print(f'{current_file}\\{file_count}: {localize.saving} - {file_name}...'.replace('<font', ''))
        is_ending = True if current_file + 1 >= file_count else False

        self.update_signal.emit(int(100 / file_count * current_file),
                                f'{current_file + 1}\\{file_count}',
                                f'{localize.saving} - {file_name}...',
                                is_ending)

    @staticmethod
    def folderSize(path, was_files=0):
        file_size = 0
        numfile = 0
        iteration = 0

        for file in Path(path).rglob('*'):

            if os.path.isfile(file):
                file_size += os.path.getsize(file)
                numfile += 1

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

    def magic(self, magic: list, read_magic: bytes | int, message: str) -> bool:

        for m in magic:

            if m == read_magic:
                return True

        else:
            print(localize.not_correct_file.replace('%%', message))
            self.update_signal.emit(100, '', '', True)
            return False
    
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

        if chang_dir:
            os.chdir(self.path_to_root)

    # TODO: Very slow working... 🐌
    def unzip(self, f_name: str,
              c_num: int = 1,
              get_ext: bool = False,
              test: bool = False,
              encrypt: bool = False,
              crypt_method: str = '',
              crypt_key='') -> None:

        out_path = self.output_folder if test else os.environ['TEMP']
        file_size = os.path.getsize(out_path)

        if encrypt:
            # TODO: Need tests
            dump_name = crypt_method + '_enc.dmp'
            script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" '
                      f'-o -a "{crypt_method}{" " + crypt_key if crypt_key else ""}" '
                      f'"{self.path_to_root}\\data\\QuickBMS\\encryption_scan.bms")" '
                      f'"{f_name}" "{out_path}"').replace("/", "\\")
        else:
            dump_name = ZipMethods.codec_indexes()[c_num] + '.dmp'
            script = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" -o -a "{c_num}" '
                      f'"{self.path_to_root}\\data\\QuickBMS\\comtype_scan2.bms" '
                      f'"{f_name}" "{out_path}"').replace("/", "\\")

        dump_file = os.path.join(out_path, dump_name)

        if not test:
            Popen(script).wait()

            try:

                with open(dump_file, 'rb') as dmp:
                    unzip_data = dmp.read()

                try:
                    os.remove(f_name)
                except OSError:
                    pass

                if get_ext:
                    self.new_ext = self.get_ext(unzip_data[:4])
                    f_name = f_name.replace('dat', self.new_ext)

                with open(f_name, 'wb') as out_f:
                    out_f.write(unzip_data)

            except (FileNotFoundError, PermissionError):
                print(localize.filed_to_unzip)
                ic(localize.filed_to_unzip)

        else:
            proc = Popen(script)
            threading.Timer(10, proc.terminate).start()
            proc.wait()

            try:
                dump_size = os.path.getsize(dump_file)

                if dump_size <= file_size:
                    os.remove(dump_file)
                else:

                    with open(dump_file, 'rb') as df:
                        bt = df.read(1)
                        dt = df.read()

                    btc = dt.count(bt) + 1

                    if btc == dump_size:
                        os.remove(dump_file)
            except FileNotFoundError:
                pass

    @staticmethod
    def get_ext(index: bytes) -> str:
        ext_list = {
            # Image Formats
            b'DDS ': 'dds', b'\x89PNG': 'png', b'GIF8': 'gif', b'\xFF\xD8\xFF\xE0': 'jpg', b'\0\0\x02\0': 'tga', b'\0\0\x0a\0': 'tga',
            # Audio Formats
            b'RIFF': 'wav', b'RIFX': 'wav', b'OggS': 'ogg', b'ID3\x04': 'mp3',
            # Archive Formats
            b'PK\x03\x04': 'zip', b'7z\xBC\xAF': '7z',
            # Document formats
            b'\x25PDF': 'pdf', b'<?xm': 'xml', b'{\n  ': 'json', 
            # Video formats
            b'BIKi': 'bik', b'BIKb': 'bik', b'SMK2': 'smk', b'BIK2': 'bk2', b'\0\0\x01\xBA': 'mpeg',
            # 3D formats
            b'BLEN': 'blend', b'STLB': 'stl', b'Kayd': 'fbx', b'ply\x0A': 'ply', b'glTF': 'glb',
            # Programs
            b'MZ\x90\x00': 'exe', b'\xCB\x0D\x0D\x0A': 'pyc', b'\x7fELF': 'elf', b'PE\x00\x00': 'dll', b'LuaQ': 'luac',
            # Data Bases
            b'SQLi': 'db',
        }

        if index[:2] == b'\x78\x9c':
            return 'zlib'
        
        if index[:3] == b'\xEF\xBB\xBF':
            return 'txt'

        try:
            return ext_list[index]
        except (IndexError, KeyError):

            try:
                ext = index[:3].decode('utf-8').lower()
                black_list = '!@\'"#$;:%^&?*(),<>?\\/|{}[]=+    '

                for s in black_list:

                    if s in ext:
                        ext = 'dat'
                        break

                with open(os.path.join(os.environ['TEMP'], f'test.{ext}'), 'wb'):
                    pass

                return ext

            except (UnicodeDecodeError, ValueError, OSError):
                return 'dat'

