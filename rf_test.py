
import sqlalchemy
import pandas
from icecream import ic
from source.reapers_factory import ReapersFactory

# ic.disable()

engine = sqlalchemy.create_engine("sqlite:///game_base.db")

with engine.connect() as conn:
    metadata = sqlalchemy.MetaData()
    game_list_table = sqlalchemy.Table('game_list', metadata, autoload_with=engine)
    reapers_table = sqlalchemy.Table('ext_list', metadata, autoload_with=engine)
    mainList = pandas.read_sql_query(sqlalchemy.select(game_list_table), conn)
    reapers_table = pandas.read_sql_query(sqlalchemy.select(reapers_table), conn)

rf = ReapersFactory(reapers_table, "_Other")

# rf.find_reaper(r"I:\tests\[PS3] [God of War - Ascension - 01.12_Online Pass]-BCUS98232.pkg")
# rf.find_reaper(r"I:\tests\idtech\Indi\gamerenderprogs_patch1_pc.resources")
# rf.find_reaper(r"I:\tests\esp\tes2\DF\DFCD\DAGGER\ARENA2\TEXTURE.375")
# rf.find_reaper(r"I:\tests\esp\tesargog\Redguard\ENGLISH.RTX")

with open(r"file_list.txt", 'r') as fl:
    file_list = fl.readlines()

for file in file_list:
    print(file[:-1])
    rf.find_reaper(file[:-1])
