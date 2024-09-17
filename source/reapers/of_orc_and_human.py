import os
import gzip
import shutil

from source.reaper import Reaper, file_reaper
from source.ui import localize


class OOMExtractor(Reaper):

    @file_reaper
    def run(self):
        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if magic != b'PSSG':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Of orc and human'), True)
                return

            name = os.path.basename(self.file_name)
            file.seek(0x34E)
            name_len = int.from_bytes(file.read(4), byteorder='big')
            f_name = file.read(name_len).decode('utf-8', errors='ignore')
            file.seek(4, 1)
            ogg_long = int.from_bytes(file.read(4), byteorder='big')
            file.seek(4, 1)
            ogg_source = file.read(ogg_long)
            lip_source = file.read()

            with open(os.path.join(self.output_folder, f_name), 'wb') as ogg_file:
                ogg_file.write(ogg_source)

            with open(os.path.join(self.output_folder, name + '.lip'), 'wb') as lip_file:
                lip_file.write(lip_source)

            self.update_pb(1, 1, name)


class OGGPacker(Reaper):

    @file_reaper
    def run(self):
        name, ext = os.path.basename(self.file_name).split('.')
        ogg_name = self.file_name.replace(ext, 'ogg')
        lip_name = self.file_name.replace(ext, 'lip')

        if not os.path.exists(ogg_name) or not os.path.exists(lip_name):
            self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Of orc and human'), True)
            return

        ogg_long = os.path.getsize(ogg_name)
        lip_long = os.path.getsize(lip_name)
        name_len = len(name)
        archive_size = ogg_long + lip_long + name_len + 858
        out_path = os.path.join(self.output_folder, name)

        with open(ogg_name, 'rb') as ogg_file:
            ogg_data = ogg_file.read()

        with open(lip_name, 'rb') as lip_file:
            lip_data = lip_file.read()

        binary_data = (
                b'PSSG' +
                archive_size.to_bytes(4, byteorder='big') +
                (b'\x00\x00\x00\x11\x00\x00\x00\x0b\x00\x00\x00\x01\x00\x00\x00\tAUDIODATA\x00\x00\x00\x02\x00\x00\x00'
                 b'\x01\x00\x00\x00\x0cbinaryObjRef\x00\x00\x00\x02\x00\x00\x00\x0bmarkerCount\x00\x00\x00\x02\x00\x00'
                 b'\x00\x07OGGDATA\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x11LIPSYNC_ANIMATION\x00\x00\x00\x00\x00'
                 b'\x00\x00\x04\x00\x00\x00\x11LIPSYNC_DATABLOCK\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x05width'
                 b'\x00\x00\x00\x04\x00\x00\x00\x06length\x00\x00\x00\x05\x00\x00\x00\tstartTime\x00\x00\x00\x06\x00'
                 b'\x00\x00\x07endTime\x00\x00\x00\x05\x00\x00\x00\x17LIPSYNC_DATABLOCK_VALUE\x00\x00\x00\x00\x00\x00'
                 b'\x00\x06\x00\x00\x00\x0cPSSGDATABASE\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\rspiderVersion\x00'
                 b'\x00\x00\x08\x00\x00\x00\x11spiderFileVersion\x00\x00\x00\t\x00\x00\x00\x15spiderLayeredDatabase\x00'
                 b'\x00\x00\n\x00\x00\x00\x05scale\x00\x00\x00\x0b\x00\x00\x00\x02up\x00\x00\x00\x07\x00\x00\x00\x07'
                 b'LIBRARY\x00\x00\x00\x01\x00\x00\x00\x0c\x00\x00\x00\x04type\x00\x00\x00\x08\x00\x00\x00\x08TYPEINFO'
                 b'\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x08typeName\x00\x00\x00\x0e\x00\x00\x00\ttypeCount\x00'
                 b'\x00\x00\t\x00\x00\x00\x03XXX\x00\x00\x00\x01\x00\x00\x00\x0f\x00\x00\x00\x02id\x00\x00\x00\n\x00'
                 b'\x00\x00\x0cBINARYOBJECT\x00\x00\x00\x01\x00\x00\x00\x10\x00\x00\x00\x0ebinaryDataSize\x00\x00\x00'
                 b'\x0b\x00\x00\x00\nBINARYDATA\x00\x00\x00\x00\x00\x00\x00\x06') +
                (archive_size - 546).to_bytes(4, byteorder='big') +
                (b'\x00\x00\x00L\x00\x00\x00\x07\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x04\x00'
                 b'\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x0c?\x80\x00'
                 b'\x00?\x80\x00\x00?\x80\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x0c\x00\x00\x00\x00?\x80\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x08\x00\x00\x00(\x00\x00\x00$\x00\x00\x00\r\x00\x00\x00\x10\x00\x00\x00\x0c'
                 b'BINARYOBJECT\x00\x00\x00\x0e\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00-\x00\x00'
                 b'\x00)\x00\x00\x00\r\x00\x00\x00\x15\x00\x00\x00\x11LIPSYNC_ANIMATION\x00\x00\x00\x0e\x00\x00\x00\x04'
                 b'\x00\x00\x00\x01\x00\x00\x00\x08\x00\x00\x00#\x00\x00\x00\x1f\x00\x00\x00\r\x00\x00\x00\x0b\x00\x00'
                 b'\x00\x07OGGDATA\x00\x00\x00\x0e\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x07') +
                (ogg_long + name_len + 76).to_bytes(4, byteorder='big') +
                b'\x00\x00\x00\x18\x00\x00\x00\x0c\x00\x00\x00\x10\x00\x00\x00\x0cBINARYOBJECT\x00\x00\x00\n' +
                (ogg_long + name_len + 40).to_bytes(4, byteorder='big') +
                (name_len + 28).to_bytes(4, byteorder='big') +
                b'\x00\x00\x00\x10\x00\x00\x00\x04' +
                (ogg_long - 4).to_bytes(4, byteorder='big') +
                (name_len + 4).to_bytes(4, byteorder='big') +
                (name_len + 8).to_bytes(4, byteorder='big') +
                (name_len + 4).to_bytes(4, byteorder='big') +
                name.encode('utf-8') + b'.ogg' +
                name_len.to_bytes(4, byteorder='big') +
                ogg_long.to_bytes(4, byteorder='big') +
                (b'\0' * 4) +
                ogg_data +
                lip_data
        )

        if self.COMPRESSED:

            with gzip.open(out_path, 'wb') as cf:
                cf.write(binary_data)

            shutil.move(out_path, out_path + '.pgz')
        else:

            with open(out_path, 'wb') as nf:
                nf.write(binary_data)

        self.update_pb(1, 1, name)
