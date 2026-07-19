
from subprocess import Popen, PIPE
from tkinter.filedialog import askopenfilename
from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui import localize


class Q_BMS(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.add = '-K'
        self.file_count = None
        self.out_folder_count = 0
        self.error = None

    def get_file_count(self, proc):
        self.start_reader(proc)

        while True:
            e = self.out_reader.err

            if "file" in e and "found" in e:
                self.file_count = int(e.split(' ')[1])
                self.out_reader.end = True
                break

            if 'error' in e.lower():
                self.out_reader.end = True
                self.error = e
                break

    def execute(self, proc):
        self.start_reader(proc)
        prev_files = 0
        prev_name = ''

        while True:
            current_file = self.folderSize(self.output_folder, self.out_folder_count)[1]

            if current_file >= self.file_count:
                break

            file_name = self.out_reader.out.split(' ')[-1]

            if prev_files != current_file and prev_name != file_name:
                self.update_pb(self.file_count, current_file, file_name)
                prev_files = current_file
                prev_name = file_name
                print(self.out_reader.out)

        self.out_reader.end = True

    @file_reaper
    def run(self):
        ic(self.script_name)

        if not self.script_name:
            self.script_name = askopenfilename(filetypes=[("BMS Scripts files", "*.bms *.txt *.wcx"), (localize.all_files, "*.*")],)

        if not self.script_name:
            # TODO: Translate text below!
            print('You must select a file...')
            self.update_signal.emit(100, '', 'You must select a file...', True)
            return

        self.file_name = self.file_name.replace("/", "\\")
        self.script_name = self.script_name if ':' in self.script_name else f"{self.path_to_root}\\{self.script_name}"
        script_test = (f'"{self.path_to_root}\\data\\QuickBMS\\quickbms.exe" {self.add} -l -Y '
                  f'"{self.script_name}" '
                  f'"{self.file_name}" "{self.output_folder}"').replace('/', '\\')
        script = script_test.replace(' -l ', ' ')
        ic(script)

        bms_test = Popen(script_test, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        self.get_file_count(bms_test)

        if self.error is None:
            self.out_folder_count = self.folderSize(self.output_folder)[1]
            bms = Popen(script, stdout=PIPE, stderr=PIPE, encoding='utf-8')
            self.execute(bms)
        else:
            print(self.error)

        self.update_signal.emit(100, '', localize.done, True)
