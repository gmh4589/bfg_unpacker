import base64

from source.codecs.dds_tools import DDSCreator

import sqlalchemy
from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
dds_creator = DDSCreator()
codecs = dds_creator.codec_list()

for codec in codecs:
    dds_creator.__getattribute__(codec)()
    
    ins = Codecs(
        codec_name = codec,
        codec = base64.b64encode(dds_creator.codec),
        codec_data = base64.b64encode(dds_creator.codec_data),
        depth = int.from_bytes(dds_creator.depth),
        keys = int.from_bytes(dds_creator.keys),
        pixel_format = int.from_bytes(dds_creator.pixel_format),
        rgb = base64.b64encode(dds_creator.rgb)
    )
    session.add(ins)
    session.commit()

session.close()