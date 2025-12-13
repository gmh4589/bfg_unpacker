
import os
import io
from icecream import ic
from  collections import namedtuple
from source.reaper import Reaper, file_reaper

FileData = namedtuple('FileData',
                       ['offset', 'zip_size', 'unzip_size', 'file_name', 'hash_sum'])
file_list = {}

VolData = namedtuple('VolData', ['vol', 'folders'])
vol_data = []

class Metro(Reaper):

    get_ext = {
        'content': 'dat',
        'sounds': 'ogg',
        'textures': 'tex',
        'videos': 'ogv'
    }

    @file_reaper
    def run(self):
        file_size = os.path.getsize(self.file_name)
        path_to_files = os.path.dirname(self.file_name)

        if 'content.vfx' not in self.file_name:
            file_name = os.path.basename(self.file_name)
            self.file_name = self.file_name.replace(file_name, 'content.vfx')
            file_size = os.path.getsize(self.file_name)

            if not os.path.exists(self.file_name):
                self.magic([b'\1\0\0\0'], b'\0', 'Metro 2033 Redux VFX')
                return
         
        with open(self.file_name, "rb") as vfx_file:
            magic = vfx_file.read(4)

            if not self.magic([b'\1\0\0\0'], magic, 'Metro 2033 VFI'):
                return   
            
            one = int.from_bytes(vfx_file.read(4), 'little')    
            hash_sum = vfx_file.read(16), 'little'
            vol_count = int.from_bytes(vfx_file.read(4), 'little') 
            x3_1 = int.from_bytes(vfx_file.read(4), 'little') 
            x3_2 = int.from_bytes(vfx_file.read(4), 'little') 

            for i in range(vol_count):
                vol_name = self.get_name(vfx_file)
                vols = int.from_bytes(vfx_file.read(4), 'little')  
                folders = []

                for j in range(vols):
                    f = self.get_name(vfx_file)
                    ic(f)
                    folders.append(f)
                
                vol_data.append(VolData(vol=vol_name, folders=folders))
                vfx_file.seek(4, 1)

