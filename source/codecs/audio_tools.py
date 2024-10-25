
import configparser
import math
import os
from icecream import ic

from source.codecs.wav_list import wav_list

setting = configparser.ConfigParser()
setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')


def wav_save(args):
    ic(args)

    name = args['file_name']
    sample_rate = args['Frequency']
    channels = args['Channels']
    bps = args['Bit'] if 'Bit' in args.keys() else 0
    codec = wav_list[args['Format']]['hex']
    ic(codec)
    bitrate = int((int(sample_rate) * int(bps) * int(channels)) / 8)
    block_align = int(int(bps) * int(channels) / 8)
    offset = args['Offset']

    out_name = os.path.basename(name).split('.')[0]
    new_name = f"{setting['Main']['out_path']}\\{out_name}.wav"
    print('Saved:', new_name)

    with open(name, 'rb') as data_file:
        data_file.seek(int(offset))
        new_data = data_file.read()

    with open(new_name, 'wb') as new_audio:
        new_audio.write(b'RIFF' +
                        (len(new_data) + 0x24).to_bytes(4, byteorder='little') +
                        b'WAVEfmt ' +
                        (0x10).to_bytes(4, byteorder='little') +
                        codec.to_bytes(2, byteorder='little') +
                        int(channels).to_bytes(2, byteorder='little') +
                        int(sample_rate).to_bytes(4, byteorder='little') +
                        bitrate.to_bytes(4, byteorder='little') +
                        block_align.to_bytes(2, byteorder='little') +
                        int(bps).to_bytes(2, byteorder='little') +
                        b'data' +
                        len(new_data).to_bytes(4, byteorder='little') +
                        new_data)


def atrac_save(args):
    ic(args)

    name = args['file_name']
    channels = int(args['Channels'])
    bitrate = int(args['Bitrate'])
    loop = args['Loop']
    offset = args['Offset']
    ext = str(args['Format']).lower()
    chunk_size = 0x20 if bitrate in (72, 144) else 0x34
    codec = 0x270 if bitrate % 9 == 0 else 0xfffe
    c_arg = 1 if codec == 0x270 else 2
    block_align = int(math.ceil(((bitrate * c_arg * 48) / 18) / 16)) * 16
    fact = b'fact\x0C\x00\x00\x00\x00\x80\x01\x00\x00\x04\x00\x00\00\x04\x00\x00'

    if bitrate == 72:
        # TODO: Check for bitrate 72 and 1 channel
        extended_data = b'\x0E\x00\x01\x00\x00\x10\x00\x00\x01\x00\x01\x00\x01\x00\x00\x00'
    elif bitrate == 144:
        extended_data = b'\x0E\x00\x01\x00\x00\x10\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
    else:
        fact = b'fact\x0C\x00\x00\x00\x00\x80\x01\x00\x00\x08\x00\x00\xB8\x08\x00\x00'
        extended_data = (b'\x22\x00\x00\x08\x03\x00\x00\x00\xBF\xAA\x23\xE9\x58\xCB\x71\x44\xA1\x19\xFF\xFA\x01' +
                         b'\xE4\xCE\x62\x01\x00' +
                         (((int(bitrate / 32) * 21) + (1 if bitrate > 100 else 0)) * 256 + 0x48).to_bytes(4, byteorder='little') +
                         (b'\x00' * 6))

    bitrate = int(bitrate / 8) * 1000
    out_name = os.path.basename(name).split('.')[0]
    new_name = f"{setting['Main']['out_path']}\\{out_name}.{ext}"
    print('Saved:', new_name)

    with open(name, 'rb') as data_file:
        data_file.seek(int(offset))
        new_data = data_file.read()

    with open(new_name, 'wb') as new_audio:
        new_audio.write(b'RIFF')
        head = (chunk_size.to_bytes(4, byteorder='little') +    # File size from here to eof
                codec.to_bytes(2, byteorder='little') +         # Codec ID for Atrac, always 0xfffe or 0x720
                channels.to_bytes(2, byteorder='little') +      # Channels count
                0xbb80.to_bytes(4, byteorder='little') +        # Sample rate, always 48000
                bitrate.to_bytes(4, byteorder='little') +       # (Bitrate / 8) * 1000
                block_align.to_bytes(4, byteorder='little') +   # Nearest multiple of 16 in (bitrate * (1 if bitrate % 9 == 0 else 2) * 48) / 18
                extended_data + fact)
        # TODO: Check fact place, add loop support

        if loop:
            head += b''

        new_audio.write((len(new_data) + len(head) + 16).to_bytes(4, byteorder='little') +
                        b'WAVEfmt ' + head + b'data' +
                        len(new_data).to_bytes(4, byteorder='little') +
                        new_data)


# TODO: Наличие сомнительно...
def mp3_save(args):
    ic(args)

    head = (b'\x54\x41\x47\x75\x6E\x6B\x6E\x6F\x77\x6E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x75'
            b'\x6E\x6B\x6E\x6F\x77\x6E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x75\x6E\x6B\x6E\x6F'
            b'\x77\x6E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x32\x32\x30\x33\x32\x30\x32\x32\x75'
            b'\x6E\x6B\x6E\x6F\x77\x6E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    name = args['file_name']
    offset = args['Offset']
    out_name = os.path.basename(name).split('.')[0]
    new_name = f"{setting['Main']['out_path']}\\{out_name}.mp3"

    with open(name, 'rb') as data_file:
        data_file.seek(int(offset))
        new_data = data_file.read()

    with open(new_name, 'wb') as new_audio:
        new_audio.write(head + new_data)


def ps_audio_tools(args):
    ic(args)

    platform = args['Platform']
    mode = args['Mode']
    file_name = ['file_name']

    match platform:
        case 'PS2':
            pass
        case 'PS3':
            pass
        case 'PS4':
            pass
        case 'PSP':
            pass
        case 'PS Vita':
            pass



