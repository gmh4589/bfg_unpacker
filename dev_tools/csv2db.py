import sqlalchemy
from sqlalchemy import Table, Column, Integer, String


engine = sqlalchemy.create_engine('sqlite:///game_base.db')
conn = engine.connect()
metadata = sqlalchemy.MetaData()

game_list = Table('game_list', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('game_name', String),
                  Column('release_year', String),
                  Column('func_name', String),
                  Column('ext_list', String),
                  Column('script_name', String),
                  extend_existing=True)

with open('re_engine.csv', 'r') as ue4:
    table_data = ue4.readlines()

for i, t in enumerate(table_data):
    name, release_year, list_name = t.strip().split('\t')

    ins = game_list.insert().values(game_name=name.strip(),
                                    release_year=release_year,
                                    func_name='_REEngine',
                                    ext_list='RE Engine Files (*.pak; *.tex)|',
                                    script_name=list_name
                                    )
    conn.execute(ins)

conn.commit()
conn.close()
