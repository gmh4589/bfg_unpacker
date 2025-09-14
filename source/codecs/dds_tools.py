
import os
from icecream import ic
from source.reaper import logger
from source.db_connect import DatabaseConnect


class DDSCreator:
    db = DatabaseConnect()
    dds_table = db.get_table('dds_codecs')


    def __init__(self):
        self.codec = b''
        self.codec_data = b''
        self.depth = b''
        self.keys = b''
        self.pixel_format = b''
        self.rgb = b''
        self.rgb_data = b''

    @classmethod
    def codec_list(cls):
        return [c for c in cls.__dict__.keys() if '__' not in c and c.upper() == c]
    
    def __set_data(self, codec, codec_data, depth, keys, pixel_format, rgb):
        self.codec = codec
        self.codec_data = codec_data
        self.depth = depth
        self.keys = keys
        self.pixel_format = pixel_format
        self.rgb = rgb
        ic(codec, codec_data, depth, keys, pixel_format, rgb)
    
    def __get_codec_index(self, codec_name, file_name):

        for i in range(len(self.dds_table)):

            if codec_name == self.dds_table['codec_name'][i]:
                break
        
        else:
            logger(level='ATTENTION',
                message=f'Unknown DDS type {codec_name}! In file {file_name}\n. File was save as B8G8R8A8_UNORM',
                show=True)
            i = 8
        
        return i

    def dds_save(self, width, height, codec='', name='', data=None, header=False, cubemap=0, depth=1, mips=0):

        if data is None:
            return b''

        idx = self.__get_codec_index(codec, name)
        self.__set_data(
            codec=bytes.fromhex(str(self.dds_table['codec'][idx])),
            codec_data=bytes.fromhex(str(self.dds_table['codec_data'][idx])),
            depth=int(self.dds_table['depth'][idx]).to_bytes(1),
            keys=int(self.dds_table['keys'][idx]).to_bytes(1),
            pixel_format=int(self.dds_table['pixel_format'][idx]).to_bytes(1),
            rgb=bytes.fromhex(str(self.dds_table['rgb'][idx]))
        )

        self.rgb_data = self.codec_data[:25]
        self.codec_data = self.codec_data[26:]
        linear_size = max(width, height)
        header_data = (b'DDS\x20\x7C' + (b'\0' * 3) +
                       self.keys +
                       self.pixel_format +
                       self.depth + b'\x00' +
                       height.to_bytes(4, byteorder='little') +
                       width.to_bytes(4, byteorder='little') +
                       linear_size.to_bytes(4, byteorder='little') +
                       depth.to_bytes(4, byteorder='little') +
                       mips.to_bytes(4, byteorder='little') +
                       (b'\x00' * 44) + b'\x20' + (b'\0' * 3) +
                       self.rgb +
                       self.codec +
                       self.rgb_data +
                       cubemap.to_bytes() +
                       self.codec_data)

        if header:
            return header_data

        name = name + '.dds' if '.dds' not in name else name
        os.makedirs(os.path.dirname(name), exist_ok=True)

        with open(name, 'wb') as dds_file:
            dds_file.write(header_data + data)
