
from source.reaper import Reaper, file_reaper
from source.ui import localize


class LoadBar(Reaper):

    @file_reaper
    def run(self):

        for i in range(1000):
            self.update_signal.emit(int(i / 10), f'{i}/1000',
                                    f'{localize.saving} - {i}...', False)

        self.update_signal.emit(100, '1000/1000', localize.done, True)
