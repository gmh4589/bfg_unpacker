from icecream import ic

class OutReader:

    def __init__(self, out_print=True, err_print=True):
        super().__init__()
        self.out = ''
        self.err = ''
        self.output = []
        self.end = False
        self.out_print = out_print
        self.err_print = err_print

    def out_reader(self, prg, splitter=' '):

        while True:
            d = prg.stdout.readline().strip()
            self.out = d
            self.output = d.split(splitter)

            if self.out and self.out_print:
                ic(self.out)

            if self.end:
                break

    def err_reader(self, prg):

        while True:
            d = prg.stderr.readline().strip()
            self.err = d

            if self.err and self.err_print:
                ic(self.err)

            if self.end:
                break
