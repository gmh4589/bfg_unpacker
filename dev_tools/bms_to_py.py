import os
import codecs

header = """
import zlib
import struct
import os
from io import BytesIO
from source.reaper import Reaper, file_reaper

class %class_name%(Reaper):

    @file_reaper
    def run(self):
        array = []
        byte_order = 'little'
        code_page = 'utf-8'
        file_size = os.path.getsize(self.file_name)

        with open(self.file_name, 'rb') as f:

"""

class BMSError(Exception):
    pass


class BMSReader:

    def __init__(self, script_path):
        self.script_path = script_path
        print(self.script_path)
        self.out_file = ''
        self.comment = ''
        
        with open(script_path, 'r', errors='ignore') as b:
            self.bms =  b.readlines()

    def worker(self):
        todo_list = ('calldll', 'put', 'putdstring', 'scandir', 'prev', 'putvarchr', 
                     'append', 'namecrc', 'getbits', 'typedef', 'putbits', 'putvarchr', 
                     'namecrc', 'putct', )
        multiline = False
        tabs = 3
        self.out_file = header.replace('%class_name%', 
                               f"_{os.path.basename(self.script_path).split('.')[0].upper()}")

        def add_line(ln):
            self.out_file += f"{'    ' * tabs}{ln}{'\t#' if self.comment.strip() else ''}{self.comment}\n"

        i = -1
        
        while i < len(self.bms):
            i += 1

            try:
                if self.bms[i].strip()[0] == '#':
                    add_line(self.bms[i].strip())
                    continue
            except IndexError:
                pass

            try:
                line, self.comment = self.bms[i].strip().split('#')
            except ValueError:
                line = self.bms[i].strip()
                self.comment = ''
            except IndexError:
                break
            
            line = line.replace('<>', '!=')
            line = line.replace('NotEOF', 'f.tell() < file_size')
            line = line.replace('||', 'or')
            line = line.replace('&&', 'and')
            line = line.replace(r'\\', r'\\\\')
        
            if '/*' in line:
                multiline = True
                continue

            if '*/' in line:
                multiline = False
                continue

            try:
                if line[0] == '<' and line[-1] == '>' or line[:1] == '/' or 'http' in line:
                    add_line(f"# {line}")
                    continue

                if line[-1] == ';':
                    line = line[:-1]

            except IndexError:
                pass

            commands = line.split()

            try:
                c = commands[0].lower()
            except IndexError:
                continue

            if multiline:
                add_line(f"# {line}")
                continue
                
            if len(commands) <= 1:
                add_line(f"# {line}")
                continue

            match c:

                case c if c in ('long', 'word', 'dword', 'byte', 'longlong', 'ulonglong', 'ubyte', 'int',
                                'uint', 'uint8', 'uint16', 'uint32', 'u8', 'u16', 'u32', 'u64', 'char'):
                    add_line(f"{commands[1]} = None")

                case 'idstring':
                    add_line(f"magic = f.read({len(commands[1]) - 1})")
                    magic = commands[1] if commands[1][0] in ('"', "'") else f'"{commands[1]}"'
                    add_line(f"if not self.magic([b{magic}, ], magic, 'Unknown header error'):")
                    add_line(f'    return')

                case 'set':

                    if commands[2] in ('string', 'binary'):
                        
                        if line.count('"') == 1:

                            while True:
                                i += 1
                                s = self.bms[i]
                                add_line(f'"{s}"\\')

                                if r'\"' in s:
                                    continue

                                if '"' in s:
                                    break

                        elif line.count('"') == 2:
                            add_line(f"{commands[1]} = {' '.join(commands[1:])}")

                    else:
                        add_line(f"{commands[1]} = {commands[2]}")

                case 'get':

                    try:
                        k = commands[2].lower()

                        if k == 'extension':
                            add_line(f"{commands[1]} = self.file_name.split('.')[-1]")

                        if k == 'asize':
                            add_line(f"{commands[1]} = file_size")

                        if k == 'basename':
                            add_line(f"{commands[1]} = os.path.basename(self.file_name)")

                        if k == 'filename':
                            add_line(f"{commands[1]} = self.file_name")

                        if k in ('string', 'unicode', 'line'):
                            add_line(f"{commands[1]} = self.get_name(f)")

                        if k == 'char':
                            add_line(f"{commands[1]} = f.read(1).decode()")

                        if k == 'double':
                            add_line(f"{commands[1]} = struct.unpack('<f', f.read(4))[0]")

                        continue

                    except IndexError:
                        add_line(line)

                    def get_type(k):
                        
                        match k:
                            case k if k in ('byte', 'uint8_t'):
                                return 1
                            case k if k in ('short', 'uint16_t'):
                                return 2
                            case k if k in ('threebyte', ):
                                return 3
                            case k if k in ('long', 'uint32_t', 'int'):
                                return 4
                            case k if k in ('longlong', 'uint64_t'):
                                return 8
                            case _:
                                return None
                            
                    l = get_type(commands[2].lower())

                    if l is None:
                        
                        raise BMSError(f'Not supported value type\n'
                                        f'TYPE: {commands[-1]}\n'
                                        f'LINE: {line}\n'
                                        f'FILE: {self.script_path}\n'
                                        f'IN STRING: {i + 1}\n')
                    
                    add_line(f"{commands[1]} = int.frombyte(f.read({l}), order=byte_order)")

                case 'getdstring':
                    add_line(f"{commands[1]} = f.read({commands[2]})")

                case 'strlen':
                    add_line(f"{commands[1]} = len({commands[2]})")

                case 'math':
                    add_line(' '.join(commands[1:]))

                case 'xmath':
                    add_line(f"{commands[1]} = {' '.join(commands[2:]).replace('"', '')}")
                
                case 'putarray':
                    add_line(f"array.append({commands[3]})")

                case 'getarray':
                    add_line(f"{commands[1]} = array[{commands[3]}]")
                
                case 'if':
                    add_line(f"if {' '.join(commands[1:])}:")
                    tabs += 1

                case c if c in ('elif', 'elseif'):
                    tabs -= 1
                    add_line(f"{line}:")
                    tabs += 1
                
                case 'else':
                    tabs -= 1
                    add_line("else:")
                    tabs += 1
                
                case 'do':
                    add_line('while True:')
                    tabs += 1

                case 'while':
                    add_line(f"if {' '.join(commands[1:])}: break")
                    tabs -= 1

                case 'for':

                    try:
                        add_line(f"for {commands[1]} in range({commands[5]}):")
                        tabs += 1
                    except IndexError:
                        continue

                case c if c in ('next', 'endfunction', 'endif', 'end'):
                    tabs -= 1

                case 'getvarchr':
                    add_line(f"{commands[1]} = {commands[2]}[{commands[3]}]")

                case 'string':
                    add_line(f"{commands[1]} = {' '.join(commands[1:])}")

                case 'goto':
                    add_line(f"f.seek({commands[1]})")

                case 'savepos':
                    add_line(f"{commands[1]} = f.tell()")
                
                case 'filexor':
                    add_line(f"{commands[1]} = xor({commands[1]})")

                case 'break':
                    add_line(f"break")
                
                case 'print':
                    add_line(f"print({' '.join(commands[1:])})")
                
                case 'log':
                    add_line(f"f.seek({commands[2]})")
                    add_line(f"__data = f.read({commands[3]})")
                    add_line(f"self.file_save({commands[1]}, __data)")

                case c if c in ('clog', 'slog'):
                    add_line(f"f.seek({commands[2]})")
                    add_line(f"__data = self.smart_deflate(f.read({commands[3]}))")
                    add_line(f"self.file_save({commands[1]}, __data)")

                case 'cleanexit':
                    add_line('return')

                case 'endian':

                    if commands[1].lower() == 'guess':
                        add_line(f"byte_order = 'little' if bytearray({commands[2]})[-1] == 0 else 'big'")
                    else:
                        add_line(f"byte_order = '{commands[1]}'")

                case 'comtype':
                    add_line(f'# TODO: Add "{line}" compression type support!')
                
                case 'startfunction':
                    add_line(f"def {commands[1]}():")
                    tabs += 1

                case 'callfunction':
                    add_line(f"{commands[1]}()")
                
                case 'padding':
                    add_line(f"f.seek({commands[1]}, 1)")

                case 'quickbmsver':
                    add_line(f"# {line}")

                case 'imptype':

                    if commands[1].lower == 'sfilesize':
                        add_line(f'{commands[0]} = os.path.getsize(self.file_name)')
                    
                case 'open':

                    try:

                        if commands[4].lower() == 'exists':
                            add_line(f'if os.path.exists(os.path.dir_name(self.file_name) + "\\" + {commands[2]}):')
                            tabs += 1
                            add_line(f'{commands[1]} = open(os.path.dir_name(self.file_name) + "\\" + {commands[2]}, "rb")')

                    except IndexError:
                        pass
                    
                    if len(commands) == 4:

                        if commands[3] == '0':
                            add_line(f'with open(self.file_name.replace(self.file_name.split(".")[-1], {commands[2]}), "rb") as {commands[1]}:')
                            tabs += 1
                        else:
                            add_line(f'{commands[2]} = {commands[1]}.read({commands[3]})')
                    
                    elif len(commands) == 3:
                        add_line(f'with open(self.file_name.replace(self.file_name.split(".")[-1], {commands[2]}), "rb") as {commands[1]}:')
                        tabs += 1

                case 'include':
                    add_line(f'import {commands[1].replace("\"", "").replace(".", "_")}')

                case 'getct':
                    add_line(f'{commands[1]} = self.get_name(stop_sym=({commands[3]}).to_bytes(1))')
                
                case c if c in ('encryption', 'filecrypt'):
                    add_line(f'# TODO: Add "{line}" encryption type support!')
                
                case 'sortarray':
                    add_line(f'array.sort()')

                case 'findloc':
                    add_line(f'{commands[1]} = len(f.split(b{commands[3]})[0])')
                
                case c if c in ('filerot', 'filerot13'):
                    add_line("from cryptography.fernet import Fernet")
                    add_line("__all_data = f.read()")
                    add_line(f"__felerot = Fernet({commands[1]})")
                    add_line("__enc_data = fernet.decrypt(__all_data)")
                    add_line("f = BytesIO(__enc_data)")

                case 'uint8_t':
                    add_line(f"{commands[1]} = int.frombyte(f.read(1))")

                case 'uint16_t':
                    add_line(f"{commands[1]} = int.frombyte(f.read(2), order=byte_order)")

                case 'uint32_t':
                    add_line(f"{commands[1]} = int.frombyte(f.read(4), order=byte_order)")

                case 'uint64_t':
                    add_line(f"{commands[1]} = int.frombyte(f.read(8), order=byte_order)")

                case 'reverseshort':
                    add_line(f"__temp = {commands[1]}.to_bytes(2, order=byte_order)")
                    add_line(f"{commands[1]} = int.frombyte(BytesIO(__temp).read(), order=byte_order)")

                case 'reverselong':
                    add_line(f"__temp = {commands[1]}.to_bytes(4, order=byte_order)")
                    add_line(f"{commands[1]} = int.frombyte(BytesIO(__temp).read(), order=byte_order)")

                case 'reverselonglong':
                    add_line(f"__temp = {commands[1]}.to_bytes(8, order=byte_order)")
                    add_line(f"{commands[1]} = int.frombyte(BytesIO(__temp).read(), order=byte_order)")
                
                case 'codepage':
                    codec_name = codecs.lookup(f"cp{int(commands[1])}").name
                    add_line(f"codepage = '{codec_name}'")
                                    
                case c if c in todo_list:
                    add_line(f'# TODO: Add "{c}" support!')
                    add_line(f"# TODO: {line}")

                case _:
                    raise BMSError(f'BMS Sintax error!\n'
                                   f'UNKNOWN OPERATOR: {line}\n'
                                   f'FILE: {self.script_path}\n'
                                   f'IN STRING: {i + 1}\n')
                
        tabs = 2
        add_line("\n\n")
        add_line(f"self.update_pb(100, 100, '')")
        
        with open(f'out\\{os.path.basename(self.script_path).replace(".", "_")}.py', 'w') as out:
            out.write(self.out_file)           

for path in os.listdir('scripts\\'):
    bms = BMSReader(f'scripts\\{path}')
    bms.worker()
