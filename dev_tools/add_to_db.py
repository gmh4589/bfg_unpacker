import sqlalchemy
from sqlalchemy import Table, Column, Integer, String
import requests
from bs4 import BeautifulSoup


def get_release_date(game_name):
    game_name = (game_name.replace(' ', '_')
                 .replace(':', '')
                 .replace("'", '')
                 .replace("-", '')
                 .lower())

    response = requests.get('https://www.playground.ru/' + game_name)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        release_date = soup.select('.release-item')[0].text.replace(' ', '').strip()
        return release_date.split('\n')[0].split('.')[-1]


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

with open('ue4_list.txt', 'r') as ue4:
    table_data = ue4.readlines()

for i, t in enumerate(table_data):
    name, hex_value = t.strip().split(' 0x')
    release_year = get_release_date(name.strip().split(' (')[0])
    print(i, name, release_year)
    ins = game_list.insert().values(game_name=name.strip(),
                                    release_year=release_year,
                                    func_name='_Unreal4',
                                    ext_list='Unreal Engine 4 Archives (*.pak)|Unreal Engine 4 Localization FIles (*.locres; *.txt)|',
                                    script_name=f'0x{hex_value}'
                                    )
    conn.execute(ins)

conn.commit()
conn.close()
