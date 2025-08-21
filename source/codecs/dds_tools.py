from source.reaper import logger


class DDSCreator:

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

    def dds_save(self, width, height, codec, name='', data=None, header=False,
                 cubemap=0, depth=1, mips=0):

        if data is None:
            return b''

        try:
            self.__getattribute__(codec)()
        except (TypeError, AttributeError):
            logger(level='ATTENTION',
                   message=f'Unknown DDS type {codec}! In file {name}\n. File was save as B8G8R8A8_UNORM',
                   show=True)

            self.B8G8R8A8_UNORM()

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

        with open(name, 'wb') as dds_file:
            dds_file.write(header_data + data)

    def A8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x08' + (b'\0' * 15) + b'\xff' + (b'\0' * 3) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x02' + (b'\0' * 3)

    def ATI1(self):
        self.codec = b'ATI1'
        self.codec_data = (b'\0' * 21) + b'\x10' + (b'\0' * 18)
        self.depth = b'\x0a'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def ATI2(self):
        self.codec = b'ATI2'
        self.codec_data = (b'\0' * 21) + b'\x10' + (b'\0' * 18)
        self.depth = b'\x0a'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def AYUV(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'd' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def B4G4R4A4_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 4) + b'\x0f' + (b'\0' * 2) + b'\xf0' + (b'\0' * 3) + b'\x0f' + (b'\0' * 4) + b'\xf0' + (b'\0' * 2) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'A' + (b'\0' * 3)

    def B5G5R5A1_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 4) + b'|' + (b'\0' * 2) + b'\xe0\x03' + (b'\0' * 2) + b'\x1f' + (b'\0' * 4) + b'\x80' + (b'\0' * 2) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'A' + (b'\0' * 3)

    def B5G6R5_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 4) + b'\xf8' + (b'\0' * 2) + b'\xe0\x07' + (b'\0' * 2) + b'\x1f' + (b'\0' * 7) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'@' + (b'\0' * 3)

    def B8G8R8A8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 5) + b'\xff' + (b'\0' * 2) + b'\xff' + (b'\0' * 2) + b'\xff' + (b'\0' * 6) + b'\xff\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'A' + (b'\0' * 3)

    def B8G8R8A8_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'[' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def B8G8R8X8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 5) + b'\xff' + (b'\0' * 2) + b'\xff' + (b'\0' * 2) + b'\xff' + (b'\0' * 7) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'@' + (b'\0' * 3)

    def B8G8R8X8_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b']' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC1_UNORM(self):
        self.codec = b'DXT1'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC1_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'H' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC2_UNORM(self):
        self.codec = b'DXT3'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC2_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'K' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC3_UNORM(self):
        self.codec = b'DXT5'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC3_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'N' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC4_SNORM(self):
        self.codec = b'BC4S'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC4_UNORM(self):
        self.codec = b'BC4U'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC5_SNORM(self):
        self.codec = b'BC5S'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC5_UNORM(self):
        self.codec = b'BC5U'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC6H_SF16(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'`' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC6H_UF16(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'_' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC7_UNORM(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'b' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def BC7_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'c' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\n'
        self.keys = b'\x07'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def G8R8_G8B8_UNORM(self):
        self.codec = b'GRGB'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R10G10B10A2_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x19' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R10G10B10A2_UNORM(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x18' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R10G10B10_XR_BIAS_A2_UNORM(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'Y' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R11G11B10_FLOAT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x1a' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16B16A16_FLOAT(self):
        self.codec = b'q' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16B16A16_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x0e' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16B16A16_SNORM(self):
        self.codec = b'n' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16B16A16_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x0c' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16B16A16_UNORM(self):
        self.codec = b'$' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16_FLOAT(self):
        self.codec = b'p' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'&' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16_SNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 3) + b'\xff\xff' + (b'\0' * 4) + b'\xff\xff' + (b'\0' * 8) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'' + (b'\0' * 2) + b'\x08\x00'

    def R16G16_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'$' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16G16_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 3) + b'\xff\xff' + (b'\0' * 4) + b'\xff\xff' + (b'\0' * 8) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'@' + (b'\0' * 3)

    def R16_FLOAT(self):
        self.codec = b'o' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b';' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16_SNORM(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b':' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'9' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R16_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 3) + b'\xff\xff' + (b'\0' * 14) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'' + (b'\0' * 2) + b'\x02\x00'

    def R32G32B32A32_FLOAT(self):
        self.codec = b't' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32B32A32_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x04' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32B32A32_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x03' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32B32_FLOAT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x06' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32B32_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x08' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32B32_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x07' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32_FLOAT(self):
        self.codec = b's' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x12' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32G32_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x11' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32_FLOAT(self):
        self.codec = b'r' + (b'\0' * 3)
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'+' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R32_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'*' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8B8A8_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b' ' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8B8A8_SNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 3) + b'\xff' + (b'\0' * 4) + b'\xff' + (b'\0' * 4) + b'\xff' + (b'\0' * 4) + b'\xff\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'' + (b'\0' * 2) + b'\x08\x00'

    def R8G8B8A8_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x1e' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8B8A8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b' ' + (b'\0' * 3) + b'\xff' + (b'\0' * 4) + b'\xff' + (b'\0' * 4) + b'\xff' + (b'\0' * 4) + b'\xff\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'A' + (b'\0' * 3)

    def R8G8B8A8_UNORM_SRGB(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'\x1d' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8_B8G8_UNORM(self):
        self.codec = b'RGBG'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'4' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8_SNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 3) + b'\xff' + (b'\0' * 4) + b'\xff' + (b'\0' * 10) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'' + (b'\0' * 2) + b'\x08\x00'

    def R8G8_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'2' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8G8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x10' + (b'\0' * 3) + b'\xff' + (b'\0' * 12) + b'\xff' + (b'\0' * 2) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x01\x00\x02\x00'

    def R8_SINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'@' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8_SNORM(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'?' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8_UINT(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'>' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def R8_UNORM(self):
        self.codec = b'\0' * 4
        self.codec_data = b'\x08' + (b'\0' * 3) + b'\xff' + (b'\0' * 15) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'' + (b'\0' * 2) + b'\x02\x00'

    def R9G9B9E5_SHAREDEXP(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'C' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def Y210(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'l' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def Y216(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'm' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def Y410(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'e' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def Y416(self):
        self.codec = b'DX10'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17) + b'f' + (b'\0' * 3) + b'\x03' + (b'\0' * 7) + b'\x01' + (b'\0' * 7)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

    def YUY2(self):
        self.codec = b'YUY2'
        self.codec_data = (b'\0' * 20) + b'\x08\x10@' + (b'\0' * 17)
        self.depth = b'\x02'
        self.keys = b'\x0f'
        self.pixel_format = b'\x10'
        self.rgb = b'\x04' + (b'\0' * 3)

