import os
from icecream import ic

from source.qprocess import QProcessList
from source.ui import localize
from source.ui.file_type_selector import TypeSelector
from source.setting import setting
from source.reapers_factory import ReapersFactory


class QuickOpen(QProcessList):

    def __init__(self):
        super().__init__()
        self.script_name = ''
        self.setting = setting

    @staticmethod
    def sorry(msg=localize.not_find_unpacker):  # 😢
        print(msg)
        return None

    def find_reaper(self, func_name=None, script_name=None, maximum=100):
        factory = ReapersFactory(self.reapers_table, func_name, script_name)
        ic(func_name, script_name)
        
        if self.file_list:
            fn = self.file_list.pop(0)
            subfolder = bool(int(self.setting['Main']['subfolders']))
            fp = f'{self.out_dir}\\{os.path.basename(fn).replace(".", "_")}' if subfolder else self.out_dir

            if len(self.file_list) == 0:
                self.last_run = None
            
            if func_name is None:
                reaper_result = factory.find_reaper(fn, fp) 
            else: 
                reaper_result = factory.get_class(func_name)

                try:
                    reaper_result.script_name = script_name
                    ic(type(reaper_result), reaper_result.__dict__)
                    
                    self.q_connect(nuke=reaper_result, fn=fn,
                                header=f'{localize.unpacking}: {fn}...',
                                maximum=maximum,
                                out_dir=self.setting['Main']['out_path'],
                                subfolder=bool(int(self.setting['Main']['subfolders'])))
                    return
                
                except (AttributeError, IndexError):
                    # TODO: Translate text below
                    msg = f"Can't get function {func_name} or script {script_name}. Maybe error in database...\n We will try to detect file type automatly..."
                    ic(msg)
                    print(msg)
                    reaper_result = factory.find_reaper(fn, fp)

            ic(reaper_result)

            if reaper_result:

                if len(reaper_result) > 1:
                    reaper_result = sorted(reaper_result, key=lambda k: k.name.lower())
                    tp = TypeSelector(reaper_result)
                    tp.exec()
                    
                    if tp.returned_data is not None:
                        reaper_result = [reaper_result[tp.returned_data], ]
                    else:
                        self.sorry()
                        return

                ic(reaper_result)

                proc_list = reaper_result[0]
                print(f"{localize.file_type} {proc_list.name}")

                function = proc_list.class_path
                function.script_name = proc_list.script_path
                mx = proc_list.progress_max.item()

                self.q_connect(function, fn,
                                header=f'{localize.unpacking}: {fn}...',
                                maximum=mx,
                                out_dir=self.setting['Main']['out_path'],
                                subfolder=bool(int(self.setting['Main']['subfolders'])))

            else:
                self.sorry()
