import sys
# import argparse
import struct
import operator
import os
import errno
from collections import deque

from source.reaper import Reaper, file_reaper

# Source take from here: https://gitlab.com/rgss/rgsstool/-/blob/master/rgsstool.py?ref_type=heads

# parser = argparse.ArgumentParser(description="""View and extract data from RGSS Archives""")
# parser.add_argument('archive', metavar='RGSS FILE', nargs='?', help="""RGSS archive (default to STDIN if no file)""")
# parser.add_argument('files', metavar='FILE', nargs='*', help="""FILEs to add to archive (in create mode)""")
# parser.add_argument('-l', '--list', dest='mode_list', action='store_true', help="""LIST files in archive (default mode)""")
# parser.add_argument('-x', '--extract', dest='mode_extract', action='store_true', help="""EXTRACT files from archive""")
# parser.add_argument('-c', '--create', dest='mode_create', action='store_true', help="""CREATE archive from files""")
# parser.add_argument('-d', '--dir', dest='outdir', default=None, help="""Interact with archive at root of DIR instead of current directory (e.g. extract to DIR or add from DIR)""", metavar='DIR')
# parser.add_argument('-k', '--key', dest='key', default=None, help="""Encrypt/Decrypt with KEY (in hexidecimal notation, default "deadcafe", implies RPG Maker XP Archive format)""", metavar='KEY')
# parser.add_argument('-1', '--rgssadv1', dest='v1', action='store_true', help="""Create RPG Maker XP Archive without explicitly setting a key (default if using a key)""")
# parser.add_argument('-2', '--rgssadv2', dest='v2', action='store_true', help="""Create RPG Maker VX Archive even if setting a key""")
# parser.add_argument('-3', '--rgssadv3', dest='v3', action='store_true', help="""Create RPG Maker VX Ace Archive even if setting a key (default if no key)""")

def eprint(s):
	sys.stderr.write(s + '\n')
	
def dump_hex_array(bytes):
	return ' '.join('{:02X}'.format(b) for b in bytes)

def add_to_array(a, pos, val, valDefault):
	
	if (pos < len(a)):
		a[pos] = val
		return
	
	for i in range(len(a), pos):
		a.append(valDefault) # Inflate with default value
		
	a.append(val)

def to_uint32(val):
	return (val & 0xFFFFFFFF) # Only deal with last 32 bits

def read_uint(source, size=4):
	s = source.read(size) if hasattr(source, 'read') else source
	val, = struct.unpack('<I', (s[0:4] if len(s) >= 4 else (s + struct.pack(b'x' * (4 - len(s)))))) # Pad to 4 bytes
	return val

def list_to_array(l, valDefault):
	a = []
	
	for i, v in l:
		add_to_array(a, i, v, valDefault)
		
	return a

class KeyTracker(object):
	
	def __init__(self, key_start):
		self.key = key_start
		
	def encrypt_int(self, i):
		return struct.pack('<I', to_uint32(operator.xor(i, self.key)))
	
	def encrypt_bytes(self, a_bytes):
		return self.decrypt_bytes(a_bytes)
	
	def decrypt_int(self, fIn):
		return operator.xor(read_uint(fIn), self.key)
	
	def decrypt_bytes(self, a_bytes):
		bytes_key = struct.pack('<I', self.key)
		return (operator.xor(b, bytes_key[pos % 4]) for (pos, b) in enumerate(a_bytes))

class RGSSArchive(object):
	version = 0
	encoding = 'utf-8'
	
	def get_keytracker(self, key_start):
		pass

	def files(self, fIn, match, action):
		files = []
		t = self.get_keytracker(self.get_key(fIn))
		
		while True:
			pos = fIn.tell()
			fp = self.get_file(fIn, t)
			
			if fp is None:
				break
			
			f, name = fp
			
			try:
				f.name = name.decode(self.encoding)
			except UnicodeDecodeError:
				eprint('Key: 0x{:08X}, Offset: 0x{:08X}'.format(t.key, pos))
				eprint('File: {}'.format(f))
				eprint(dump_hex_array(name[:99]) + (' ...' if (len(name) > 99) else ''))
				raise
			
			if match(f):
				action(f)
				files.append(f)
				
		return files
	
	def write_files(self, fOut, files_and_paths, t, offset_start):
		pass

	def get_file(self, fIn, tracker):
		pass

	def print(self, fIn, f):
		print(f.name)
		self.pass_next(fIn, f)
		
	def pass_next(self, fIn, f):
		pass
	
	def extract_list(self, fIn, files, outdir):
		pass
	
	def extract_inline(self, fIn, f, outdir):
		pass
	
	def extract_file(self, fIn, f, outdir):
		print('Extracting {} ...'.format(f.name, f.offset, fIn.tell()))
		path = os.path.join(*f.name.split('\\')) # Handle back slashes
		
		if outdir is not None:
			path = (outdir + os.sep + path)
			
		d, name = os.path.split(path)
		
		try:
			os.makedirs(d)
		except OSError as ex:
			
			if (ex.errno != errno.EEXIST) or (not os.path.isdir(d)): # Allow for existence of directory
				raise
			
		with open(path, 'wb') as fExtract:
			self.decrypt_data(fIn, fExtract, f.size, f.key)

	def decrypt_data(self, fIn, fOut, size, k):
		
		def decrypt(bytes):
			nonlocal k
			bytes_k = struct.pack('<I', to_uint32(k))
			bytes_dec = []
			
			for (pos, b) in enumerate(bytes):
				bytes_dec.append(operator.xor(b, bytes_k[pos % 4]))
				
				if ((pos % 4) == 3):
					k = to_uint32((k * 7) + 3)
					bytes_k = struct.pack('<I', k)
					
			return bytearray(bytes_dec)
		
		count_bytes = 0
		
		while count_bytes < size:
			remaining = size - count_bytes
			data = fIn.read(4096 if remaining > 4096 else remaining)
			
			if data == b'':
				raise Exception('Reached end of file attempting decryption: {} ({} of {})'.format(fIn.name, count_bytes, size))
			
			data_decrypt = decrypt(data)
			count_bytes = count_bytes + len(data)
			fOut.write(data_decrypt)

	def metadata_bin(self, f, key):
		pass

class RGSSADV1(RGSSArchive, Reaper):
	version = 1
	key = 0xDEADCAFE
	encoding = 'cp1252' # Can you believe that people used this once upon a time? Me neither.
	
	def __init__(self, key):
		
		if key is not None:
			self.key = key
			
	def get_key(self, fIn):
		return self.key
	
	def get_keytracker(self, key_start):
		
		class KeyTracker_V1(KeyTracker): # Track a rotating key
			
			def __init__(self, key_start):
				self.key = key_start
				
			def rotate_key(self, v):
				self.key = to_uint32((7 * self.key) + 3)
				return v
			
			def encrypt_int(self, i):
				return self.rotate_key(struct.pack('<I', to_uint32(operator.xor(i, self.key))))
			
			def decrypt_int(self, fIn):
				return self.rotate_key(operator.xor(read_uint(fIn), self.key))
			
			def decrypt_bytes(self, a_bytes):
				
				for b in a_bytes:
					yield self.rotate_key(operator.xor(b, (self.key & 0xFF))) # Only compare against lowest byte
					
		return KeyTracker_V1(self.key if (key_start is None) else key_start)

	def write_files(self, fOut, files_and_paths, t, offset_start):
		current_file = 0
		all_files = len(files_and_paths)
		
		for (f, p) in files_and_paths:
			fOut.write(self.metadata_bin(f, t))
			self.update_pb(all_files, current_file, p)
			current_file += 1
			
			with open(p, 'rb') as fIn:
				self.decrypt_data(fIn, fOut, f.size, t.key)

	def get_file(self, fIn, tracker):
		key_start = tracker.key
		length_data = fIn.read(4)
		length = tracker.decrypt_int(length_data)
		
		if length_data == b'':
			return None # We've finished
		
		name_enc = fIn.read(length)
		name = bytearray(tracker.decrypt_bytes(name_enc))
		size = tracker.decrypt_int(fIn)
		offset = fIn.tell()
		
		return (ArchiveFile(offset, size, '', tracker.key), name)

	def pass_next(self, fIn, f):
		fIn.seek(f.offset + f.size)
		
	def extract_inline(self, fIn, f, outdir):
		self.extract_file(fIn, f, outdir)

	def metadata_bin(self, f, t):
		a_name = f.name.encode(self.encoding)
		key_start = t.key
		
		return (
			t.encrypt_int(len(a_name)) +
			bytearray(t.encrypt_bytes(a_name)) +
			t.encrypt_int(f.size)
		)

#class RGSSADV2(RGSSADV1): # RPG Maker VX and RPG Maker XP have the same format
class RGSSADV3(RGSSArchive, Reaper):
	version = 3
	
	def get_keytracker(self, key_start):
		return KeyTracker(57 if (key_start is None) else key_start)
		# "57" as default because (57 - 3) is divisible by 9 (see header key calculation below in "write_files")

	def write_files(self, fOut, files_and_paths, t, offset_start):
		
		if ((t.key % 9) != 3):
			raise Exception('Provided key does not match encoding parameters. Dividing the key by 9 must yield a remainder of 3 (key % 9 == 3), but key of 0x{:08X} yields remainder of {}'.format(t.key, (t.key % 9)))
		data_header = struct.pack('<I', int((t.key - 3) / 9))
		fOut.write(data_header)
		pos = offset_start + len(data_header)

		for (f, p) in files_and_paths: # Calculate the start of the file data portion
			a = self.metadata_bin(f, t)
			pos = pos + len(a)
			
		marker_end = t.encrypt_int(0) # Do we need to add padding to align the files?
		pos = pos + len(marker_end)
		
		for (f, p) in files_and_paths:
			f.offset = pos
			f.key = 42 # Set the key to anything
			fOut.write(self.metadata_bin(f, t))
			pos = pos + f.size
			
		fOut.write(marker_end)
		
		current_file = 0
		all_files = len(files_and_paths)
		
		for (f, p) in files_and_paths:
			self.update_pb(current_file, all_files, p)
			current_file += 1
			
			with open(p, 'rb') as fIn:
				self.decrypt_data(fIn, fOut, f.size, f.key)

	def get_key(self, fIn):
		return ((read_uint(fIn) * 9) + 3) # Poor man's encryption
	
	def get_file(self, fIn, tracker):
		offset_data = fIn.read(4)
		offset = tracker.decrypt_int(offset_data)
		
		if offset == 0 or offset_data == b'':
			return None # We've finished
		
		size = tracker.decrypt_int(fIn)
		key_file = tracker.decrypt_int(fIn)
		length = tracker.decrypt_int(fIn)
		name_enc = fIn.read(length)
		name = bytearray(tracker.decrypt_bytes(name_enc))
		return (ArchiveFile(offset, size, '', key_file), name)
	
	def extract_list(self, fIn, files, outdir):
		
		for (i, f) in enumerate(sorted(files, key = (lambda f: f.offset))):
			
			if f.offset > fIn.tell():
				print('Skip {} bytes to jump to file data at offset 0x{:08X} for File {}'.format((f.offset - fIn.tell()), f.offset, i))
				
			fIn.seek(f.offset)
			self.extract_file(fIn, f, outdir)
			
	def metadata_bin(self, f, t):
		a_name = f.name.encode(self.encoding)
		a = (
			t.encrypt_int(f.offset) +
			t.encrypt_int(f.size) +
			t.encrypt_int(f.key) +
			t.encrypt_int(len(a_name))
		)
		return a + bytearray(t.encrypt_bytes(a_name))

class ArchiveFile(object):
	
	def __init__(self, offset, size, name, key):
		self.offset = offset
		self.size = size
		self.name = name
		self.key = key
		
	def __str__(self):
		return 'Offset: 0x{:08X}, Size: {}, Key: 0x{:08X}, Length (of name): {}'.format(self.offset, self.size, self.key, ('N/A' if self.name is None else len(self.name)))

def rgss_read(fIn, mode_extract, outdir, key_decrypt): # Binary Input
	
	if not fIn.seekable():
		
		class UnseekableWrapper(object):
			
			def __init__(self, fRead):
				self.pos = 0
				self.fRead = fRead
				
			def read(self, length):
				data = self.fRead.read(length)
				self.pos = self.pos + len(data)
				return data
			
			def tell(self):
				return self.pos
			
			def seek(self, pos): # Replace default seek method
				assert pos >= self.pos
				count = (pos - self.pos)
				
				while (count > 0):
					a = self.read(count if (count < 4096) else 4096)
					
					if a == b'':
						raise Exception('Reached end of file (0x{:08X}) trying to seek to posision: 0x{:08X}'.format(self.tell(), pos))
					
					count = (count - len(a))
					
			def fileno(self):
				return self.fRead.fileno()
			
		fIn = UnseekableWrapper(fIn)

	header = fIn.read(7).decode('utf-8')
	
	if header != 'RGSSAD\0':
		raise Exception('File does not conform to RPG Maker Archive file type')
	
	version = read_uint(fIn, 1)
	rgss = RGSSADV1(key_decrypt) if (version == 1) else RGSSADV3()

	def action_inline(a, f_extract, d):
		
		if f_extract:
			return (lambda f: a.extract_inline(fIn, f, d))
		
		return (lambda f: a.print(fIn, f))
	
	try:
		files = rgss.files(fIn, (lambda f: True), action_inline(rgss, mode_extract, outdir))
		
		if mode_extract:
			rgss.extract_list(fIn, files, outdir)
			size = os.fstat(fIn.fileno()).st_size
			
			if fIn.tell() < size:
				print('Ended read {} bytes before end'.format(size - fIn.tell()))
				
	except KeyboardInterrupt:
		sys.exit(1)
	except BrokenPipeError: # Allow killing of pipe to cause early exit (without error)
		return

def rgss_write(fOut, dir_root, file_names, key, version):
	# Compile list from outdir/files
	rgss = RGSSADV3() if (version == 3) else RGSSADV1(key)
	t = rgss.get_keytracker(key)

	if dir_root:
		
		if not os.path.exists(dir_root):
			eprint('Non-existent root path: {}'.format(dir_root))
			return
		elif (not os.path.isdir(dir_root)):
			eprint('Root path is not a directory: {}'.format(dir_root))
			return
		
		dir_root = os.path.normpath(dir_root) + '/'
		
		if dir_root == './':
			dir_root = None

	to_process = deque((os.path.normpath(p) for p in file_names) if (len(file_names) > 0) 
		else ([dir_root] if dir_root else os.listdir(os.getcwd())))
	files_and_paths = deque([])
	
	while len(to_process) > 0:
		p = to_process.popleft()
		
		# TODO: Add filtering
		if os.path.isdir(p):
			
			for f in os.listdir(p):
				to_process.append(os.path.join(p, f))
				
		else:
			p_part = p
			
			if dir_root:
				
				if not p.startswith(dir_root):
					eprint('Path mismatch with root directory: {} (path: {})'.format(dir_root, p))
					return
				
				p_part = p[len(dir_root):]
				
			name = (p_part if os.sep == '\\' else p_part.replace(os.sep, '\\'))
			f = ArchiveFile(0, os.path.getsize(p), name, 0)
			files_and_paths.append((f, p))

	fOut.write('RGSSAD'.encode('utf-8'))
	fOut.write(bytearray([0, rgss.version]))
	pos = 8 # We just wrote 8 bytes
	rgss.write_files(fOut, list(files_and_paths), t, pos)

# if __name__ == '__main__':
# 	args = parser.parse_args()
# 	outdir = None if args.outdir == '' else args.outdir
# 	key = (None if args.key is None else int(args.key, 16))
# 	if args.mode_create:
# 		with (sys.stdout.detach() if args.archive is None else open(args.archive, 'wb')) as fOut:
# 			rgss_write(fOut, outdir, args.files
# 				, key
# 				, (3 if args.v3 else 2 if args.v2 else 1 if args.v1 else (3 if key is None else 1)))
# 	else:
# 		with (sys.stdin.detach() if args.archive is None else open(args.archive, 'rb')) as fIn:
# 			if outdir is None:
# 				outdir = next(iter(args.files), None) # Try first item in files collection
# 			rgss_read(fIn, args.mode_extract, outdir, key)


class RGSS(Reaper):

    @file_reaper
    def run(self):
		
        with open(self.file_name, 'rb') as file:
            rgss_read(file, True, self.output_folder, None)
		
        self.update_pb(100, 100, 'Done')
		