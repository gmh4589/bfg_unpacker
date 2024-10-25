
import acefile
from source.reaper import Reaper, file_reaper


class UnAce(Reaper):

    @file_reaper
    def run(self):

        with acefile.open(self.file_name) as ace_file:
            file_count = 0

            for _ in ace_file:
                file_count += 1

            for i, file in enumerate(ace_file):
                ace_file.extract(file, path=self.output_folder)
                self.update_pb(file_count, i + 1, file.filename)
