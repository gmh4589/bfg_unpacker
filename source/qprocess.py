
import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal

from source.ui.main_ui_init import MainWindow
from source.ui import localize
from source.reapers import (pathologic, aurora_engine, seven_s_seven, celestia, doom_wad, zip_archive, locres,
                            arx_fatalis, phyre, zpl2png, sen_book, quake_pak, qbms, seven_zip, unreal,
                            unity, afs, source_vpk, other_prg, ffmpeg_tool)
from source import delete


class QProcessList(MainWindow):

    def __init__(self):
        super().__init__()
        sys.stdout = EmittingStream(text_written=self.append_text)
        self.root_dir = os.path.abspath(__file__).split('source')[0]
        self.file_name = ''
        self.head = b''

        # QProcesses connect
        self.afs = afs.AFSExtractor()
        self.arx = arx_fatalis.PakExtractor()
        self.aurora = aurora_engine.ERFUnpacker()
        self.celestia = celestia.Celestia()
        self.delete_thread = delete.DeleteThread()
        self.ffmpeg = ffmpeg_tool.Converter()
        self.id_tech = doom_wad.WadExtractor()
        self.locres2txt = locres.Locres2TXT()
        self.txt2locres = locres.TXT2Locres()
        self.mor = pathologic.MorUnpacker()
        self.other_prg = other_prg.OtherProg()
        self.phyre = phyre.PhyreSave()
        self.quake_pak = quake_pak.QPAKExtractor()
        self.qbms = qbms.Q_BMS()
        self.sen_book = sen_book.SenBook()
        self.sen_book_save = sen_book.SenBookSave()
        self.seven_zip = seven_zip.SevenZIP()
        self.source_vpk = source_vpk.VPKExtractor()
        self.unity = unity.Unity()
        self.unreal = unreal.Unreal()
        self.x7 = seven_s_seven.Seven()
        self.zip = zip_archive.Zip()
        self.zpl2png = zpl2png.ZPL2PNG()

    def q_connect(self, nuke, fn='', header=f'{localize.unpacking}...'):
        nuke.file_name = fn
        nuke.output_folder = self.out_dir
        self.pb.set_theme(self.setting["Main"]["theme"])
        self.pb.header.setText(header)
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.show()
        nuke.update_signal.connect(self.update_progress)
        nuke.start()

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
