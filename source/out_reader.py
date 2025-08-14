from icecream import ic

class OutReader:

    def __init__(self):
        super().__init__()
        self.out = ''
        self.err = ''
        self.output = []
        self.end = False

    def out_reader(self, prg, splitter=' '):

        while True:
            d = prg.stdout.readline().strip()
            self.out = d
            self.output = d.split(splitter)

            if self.out:
                ic(self.out)
                # print(self.out)

            if self.end:
                break

    def err_reader(self, prg):

        while True:
            d = prg.stderr.readline().strip()
            self.err = d

            if self.err:
                ic(self.err)
                # print(self.err)

            if self.end:
                break
