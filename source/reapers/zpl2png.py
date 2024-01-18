import os
import requests
import shutil
from time import sleep
from icecream import ic

from source.reaper import Reaper
from source.ui import localize


class ZPL2PNG(Reaper):

    def run(self):

        with open(self.file_name, 'r', encoding='utf-8') as zpl_file:
            zpl = zpl_file.read()

        url = f'http://api.labelary.com/v1/printers/8dpmm/labels/{round(58 / 25.4, 2)}x{round(90 / 25.4, 2)}/0/'
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
