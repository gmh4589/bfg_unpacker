
from icecream import ic
import zlib
from collections import namedtuple

from source.codecs.dds_tools import DDSCreator
from source.reaper import Reaper, file_reaper
#TODO Write it to the end

class RpackUnpack(Reaper, DDSCreator):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b"RP5L", b"RP6L", ], magic, 'Chrome Engine Archive'):
                return

            file.seek(0x14)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            ic(hex(file_count))
            file.seek(0x20)
            FileData = namedtuple('FileData', ['unk1', 'unk2', 'file_type', 'data_offset', 'info_offset', 'unk3'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        int.from_bytes(file.read(4), byteorder="little"),
                        int.from_bytes(file.read(3), byteorder="little"),
                        int.from_bytes(file.read(1), byteorder="little"),
                        int.from_bytes(file.read(4), byteorder="little"),
                        int.from_bytes(file.read(4), byteorder="little"),
                        int.from_bytes(file.read(4), byteorder="little")
                    )
                )
            
            file.seek((file_count * 0x50) + 0x10, 1)
            
            for f in file_data:
                ic(f)

# from icecream import ic
# import zlib
# import struct

# from source.codecs.dds_tools import DDSCreator
# from source.reaper import Reaper, file_reaper


# class RP6L(Reaper, DDSCreator):

#     @file_reaper
#     def run(self):

#         with open(self.file_name, "rb") as file:
#             magic = file.read(4)

#             if not self.magic([b"RP6L", ], magic, 'Chrome Engine Archive'):
#                 return

#             file.seek(8, 1)
#             parts = int.from_bytes(file.read(4), byteorder="little")
#             sections = int.from_bytes(file.read(4), byteorder="little")
#             file.seek(8, 1)
#             file_names = int.from_bytes(file.read(4), byteorder="little")
#             file.seek(4, 1)

#             section = [
#                 {"filetype": int.from_bytes(file.read(4), byteorder="little"),
#                  "offset": int.from_bytes(file.read(4), byteorder="little"),
#                  "fileSize": int.from_bytes(file.read(4), byteorder="little"),
#                  "isPacked": int.from_bytes(file.read(4), byteorder="little"),
#                  "unk1": int.from_bytes(file.read(4), byteorder="little"),
#                  } for _ in range(sections)]

#             filepart = [
#                 {"sectionIndex": int.from_bytes(file.read(1), byteorder="little") + 1,
#                  "unk1": int.from_bytes(file.read(1), byteorder="little"),
#                  "fileIndex": int.from_bytes(file.read(2), byteorder="little") + 1,
#                  "offset": int.from_bytes(file.read(4), byteorder="little"),
#                  "size": int.from_bytes(file.read(4), byteorder="little"),
#                  "unk2": int.from_bytes(file.read(4), byteorder="little"),
#                  } for _ in range(parts)]

#             filemap = [
#                 {"partsCount": int.from_bytes(file.read(1), byteorder="little"),
#                  "unk1": int.from_bytes(file.read(1), byteorder="little"),
#                  "filetype": int.from_bytes(file.read(1), byteorder="little"),
#                  "unk2": int.from_bytes(file.read(1), byteorder="little"),
#                  "fileIndex": int.from_bytes(file.read(4), byteorder="little") + 1,
#                  "firstPart": int.from_bytes(file.read(4), byteorder="little") + 1,
#                  } for _ in range(file_names)]

#             file_name_idx = [int.from_bytes(file.read(4), byteorder="little") for _ in range(file_names)]

#             file_name_off = file.tell()

#         filename = []

#         for i in range(len(file_name_idx)):
#             file.seek(file_name_off + file_name_idx[i])
#             filename.append(file.read(256).decode("utf-8").rstrip("\0"))

#         for i, s in enumerate(section):
#             pack = bool(s["isPacked"])
#             file_size = s["fileSize"]
#             file.seek(s["offset"])
#             data = file.read(file_size)

#             if pack:
#                 s["data"] = zlib.decompress(data)
#             else:
#                 s["data"] = data

#         fmt = {2: 'R8G8B8A8_SNORM', 3: 'R8G8B8A8_SNORM', 14: 'BC2_UNORM', 17: 'BC1_UNORM',
#                18: 'BC2_UNORM', 19: 'BC3_UNORM', 33: 'BC3_UNORM'}
#         ext_list = {16: "msh", 32: "dds", 48: "shd", 64: "anm", 80: "fx"}
#         file_count = len(filemap)

#         for i, m in enumerate(filemap):

#             try:
#                 ext = ext_list[m["filetype"]]
#             except IndexError:
#                 ext = str(m["filetype"])

#             fn = f"{filename[i]}.{ext}"
#             ptr = m["firstPart"]
#             ic(fn)
#             count = m["partsCount"]
#             out = bytearray()

#             while count > 0:
#                 p = filepart[ptr]
#                 s_idx = p["sectionIndex"]
#                 size = p["size"]
#                 s = section[s_idx]
#                 offs = p["offset"]

#                 out.extend(s["data"][offs: offs + size])

#                 ptr += 1
#                 count -= 1

#             out = bytes(out)

#             if ext == 'dds':
#                 width = struct.unpack("H", out[:2])[0]
#                 height = struct.unpack("H", out[2:4])[0]
#                 dxt = struct.unpack("I", out[12:16])[0]
#                 codec = fmt[dxt]
#                 data_file = out[152:]
#                 self.dds_save(width, height, codec, f'{self.output_folder}/{fn}', data_file)
#             else:
#                 with open(f'{self.output_folder}/{fn}', "wb") as w:
#                     w.write(out)

#             self.update_pb(file_count, i, fn)