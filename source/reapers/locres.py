import os
from source.reaper import Reaper, file_reaper


class Locres2TXT(Reaper):

    @file_reaper
    def run(self):
        pass


class TXT2Locres(Reaper):

    @file_reaper
    def run(self):
        pass

