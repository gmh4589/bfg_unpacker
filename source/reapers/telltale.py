
from subprocess import Popen, PIPE

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.db_connect import DatabaseConnect
from icecream import ic


class TellTale(Reaper):

    def __init__(self):
        super().__init__()
        self.script_name = ''

    def run(self):

        if not self.script_name:
            db = DatabaseConnect()
            table = db.get_table('game_list', filter=True, column_name='func_name', value='_TellTale')
            # self.script_name = None
            self.get_index(table)

    def get_index(self, tbl):
        game_names = tbl['game_name'].tolist()
        script_names = tbl['script_name'].tolist()
        
        def get_user_choice(selected_game):
            
            if selected_game in game_names:
                index = game_names.index(selected_game)
                self.script_name = script_names[index]
                self.continue_run()
            else:
                self.update_signal.emit(100, '', localize.error, True)

        self.user_choice_signal.emit('Select a game', game_names, get_user_choice)

    @file_reaper
    def continue_run(self):
        ic(self.script_name)

        if self.script_name is not None:

            script = f'data\\tools\\ttarchext.exe -o {self.script_name} "{self.file_name}" "{self.output_folder}"'
            ic(script)

            try:
                prg = Popen(script, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8', errors='ignore', shell=False)

            except Exception as error:
                self.update_signal.emit(100, '', localize.done, True)
                print(error)
                return
            
            self.pipe_reader(prg)