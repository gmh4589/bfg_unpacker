
import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal

from source.ui.main_ui_init import MainWindow
from source.ui import localize
from source.reapers import (pathologic, aurora_engine, seven_s_seven, celestia, doom_wad, zip_archive, locres,
                            arx_fatalis, phyre, zpl2png)
from source import delete


class QProcessList(MainWindow):

    def __init__(self):
        super().__init__()
        sys.stdout = EmittingStream(text_written=self.append_text)
        self.root_dir = os.path.abspath(__file__).split('source')[0]
        self.file_name = ''
        self.head = b''

        # QProcesses connect
        self.arx = arx_fatalis.PakExtractor()
        self.aurora = aurora_engine.ERFUnpacker()
        self.celestia = celestia.Celestia()
        self.delete_thread = delete.DeleteThread()
        self.id_tech = doom_wad.WadExtractor()
        self.locres2txt = locres.Locres2TXT()
        self.txt2locres = locres.TXT2Locres()
        self.mor = pathologic.MorUnpacker()
        self.phyre = phyre.PhyreSave()
        self.x7 = seven_s_seven.Seven()
        self.zip = zip_archive.Zip()
        self.zpl2png = zpl2png.ZPL2PNG()

    def q_connect(self, threed, fn='', header=f'{localize.unpacking}...'):
        threed.file_name = fn
        threed.output_folder = self.out_dir
        self.pb.set_theme(self.setting["Main"]["theme"])
        self.pb.header.setText(header)
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.show()
        threed.update_signal.connect(self.update_progress)
        threed.start()

    def update_progress(self, pb_value, p_text, info, process_done):
        self.pb.progressBar.setValue(pb_value)
        self.pb.progress.setText(p_text)
        self.pb.status.setText(info)

        if process_done:
            self.pb.close()


class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        self.text_written.emit(str(text))