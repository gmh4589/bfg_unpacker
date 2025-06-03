import os
from collections import namedtuple
from source.reaper import Reaper, file_reaper


class SpeechUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as speech:
            magic = speech.read(4)

            if not self.magic([b'CPSW', ], magic, 'Red Engine'):
                return

            version = int.from_bytes(speech.read(4), byteorder="little")
            file_count = len(speech.read().split(b'RIFF')) - 1
            speech.seek(0x14)
            FileData = namedtuple('FileData',
                                  ['wav_start', 'wav_size', 'sr2w_start', 'sr2w_size'])
            file_data = []

            for i in range(file_count):
                file_data.append(FileData(
                    int.from_bytes(speech.read(8), byteorder="little"),  # WAV Offset
                    int.from_bytes(speech.read(8), byteorder="little"),  # WAV Size
                    int.from_bytes(speech.read(8), byteorder="little"),  # SR2W Offset
                    int.from_bytes(speech.read(8), byteorder="little")   # SR2W Size
                ))
                speech.seek(8, 1)

            for i, file in enumerate(file_data):
                speech.seek(file.wav_start)
                size = int.from_bytes(speech.read(4), byteorder="little")
                self.file_save(os.path.join(self.output_folder, f"{i}.wav"), speech.read(size))
                speech.seek(file.sr2w_start)
                self.file_save(os.path.join(self.output_folder, f"{i}.sr2w"), speech.read(file.sr2w_size))
                self.update_pb(file_count, i + 1, f"{i}.wav, {i}.sr2w")
