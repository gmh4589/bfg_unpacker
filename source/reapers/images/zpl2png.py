import os
import requests
import shutil
from time import sleep

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui import localize


class ZPL2PNG(Reaper):

    def __init__(self, width=None, height=None):
        super().__init__()
        self.width = width
        self.height = height
    
    def run(self):

        if self.width is None and self.height is None:
            self.get_size()

    def get_size(self):
        size_list = ['20x20', '30x20', '30x30', '43x25', '58x30', '58x40', '58x60', 
                     '58x90', '75x120', '100x50', '100x72', '100x150', '150x50']
        
        def callback(selected_value):

            if selected_value in size_list:
                self.width, self.height = selected_value.split('x')
                self.width = int(self.width)
                self.height = int(self.height)
                self.continue_run()
            else:
                self.update_signal.emit(100, '', localize.error, True)

        self.user_choice_signal.emit('Select label size', size_list, callback)

    @file_reaper
    def continue_run(self):
        
        with open(self.file_name, 'r') as zpl_file:
            zpl = zpl_file.read()

        ic(self.width, self.height)
        url = f'http://api.labelary.com/v1/printers/8dpmm/labels/{round(self.width / 25.4, 2)}x{round(self.height / 25.4, 2)}/0/'
        files = {'file': zpl}
        headers = {'Accept': 'image/png'}
        response = requests.post(url, headers=headers, files=files, stream=True)

        if response.status_code == 200:
            response.raw.decode_content = True
            zpl_name = f'{os.path.basename(self.file_name).split(".")[0]}.png'

            with open(os.path.join(self.output_folder, zpl_name), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            print(f'{localize.done} - {self.file_name}')
            ic(self.file_name, 'Done!')

        else:
            print(f'{localize.error}: {response.text}')

        ic(response.status_code)
        self.update_signal.emit(100, '', localize.done, True)
        sleep(1)
