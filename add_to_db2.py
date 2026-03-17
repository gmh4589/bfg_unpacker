import base64

from source.codecs.dds_tools import DDSCreator

import sqlalchemy
from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from source.reapers import ext_list

engine = sqlalchemy.create_engine('sqlite:///game_base.db')
Base = declarative_base()

class Codecs(Base):
    __tablename__ = 'dds_codecs'
    index = Column(Integer, primary_key=True)
    codec_name = Column(String)
    codec = Column(String)
    codec_data = Column(String)
    depth = Column(Integer)
    keys = Column(Integer)
    pixel_format = Column(Integer)
    rgb = Column(String)

class Ext(Base):
    __tablename__ = 'ext_list'
    index = Column(Integer, primary_key=True)
    ext = Column(String)
    file_name = Column(String)
    magic1 = Column(Integer)
    magic2 = Column(Integer)
    magic3 = Column(Integer)
    class_path = Column(String)
    script = Column(String)
    file_type = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# dds_creator = DDSCreator()
# codecs = dds_creator.codec_list()

# for codec in codecs:
#     dds_creator.__getattribute__(codec)()
    
#     ins = Codecs(
#         codec_name = codec,
#         codec = base64.b64encode(dds_creator.codec),
#         codec_data = base64.b64encode(dds_creator.codec_data),
#         depth = int.from_bytes(dds_creator.depth),
#         keys = int.from_bytes(dds_creator.keys),
#         pixel_format = int.from_bytes(dds_creator.pixel_format),
#         rgb = base64.b64encode(dds_creator.rgb)
#     )
#     session.add(ins)
#     session.commit()

# ext_list = ext_list.after_dot['_VGMToolbox'].replace('All supported files(*.', '').replace(')', '').replace('|', '').split('; *.')

ext_list = open(r"C:\Users\User\Desktop\ext_list.txt", 'r').readlines()

for ext in ext_list:
    print(ext[:-1])

    ins = Ext(
        ext = ext[:-1],
        file_name = '*',
        magic1 = -1,
        magic2 = -1,
        magic3 = -1,
        class_path = 'other_prg.OtherProg',
        script = r'data\vgmstream\vgmstream-cli.exe -o "%out_path\%file_name%.wav" "%full_file_name%"',
        file_type = 'Audio File'
    )
    session.add(ins)
    session.commit()

session.close()