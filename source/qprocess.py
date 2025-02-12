
import os
from icecream import ic

from source.setting import Setting
from source.ui import localize
from source.ui.custom_ui import ProgressBar


class QProcessList(Setting):

    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.head = b''
        self.out_dir = self.setting['Main']['out_path']
        self.proc = None
        self.nuke = None
        self.last_run = None
        self.pb = None
        self.maximum = 100

    def q_connect(self, nuke, fn='', header=f'{localize.unpacking}...', maximum=100):
        self.pb = ProgressBar(maximum=maximum)
        self.maximum = maximum
        self.nuke = nuke
        self.nuke.file_name = fn
        subfolder = bool(int(self.setting['Main']['subfolders']))
        fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}'
        ic(fp)

        try:
            self.nuke.output_folder = fp if subfolder else self.out_dir

            if subfolder:
                os.makedirs(fp, exist_ok=True)

        except AttributeError:
            pass

        self.pb.header.setText(self.get_short_text(header))
        self.pb.progressBar.setValue(0)
        self.pb.progress.setText('')
        self.pb.status.setText('')
        self.pb.is_stop = False
        self.pb.show()

        self.nuke.update_signal.connect(self.update_progress)

        if self.last_run is not None:
            self.nuke.finished.connect(self.last_run)

        self.nuke.start()

    @staticmethod
    def get_short_text(text):

        if len(text) > 50:
            short_name = text[:10] + '...' + text[-30:]
        else:
            short_name = text

        return short_name

    def update_progress(self, pb_value, p_text, info, process_done):

        if self.pb.is_stop:
            self.nuke.terminate()

        if process_done:
            self.pb.close()

        else:
            self.pb.progressBar.setValue(pb_value)
            self.pb.progress.setText(self.get_short_text(p_text))
            self.pb.status.setText(self.get_short_text(info))
