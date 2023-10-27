
import requests
from bs4 import BeautifulSoup
from table_creator import TableCreator


class Parser(TableCreator):

    def __init__(self):
        super().__init__()
        self.sheet_name = 'STOP_GAME'

    def run(self):
        a = 0

        while True:
            a += 1

            if a > 860:
                break

            url = f'https://stopgame.ru/games/catalog?p={a}'
            response = requests.get(url)
            print(f'{a}/860')

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                links = soup.find_all('a', class_='_card_2lb1u_1')

                for link in links:
                    game_link = f'https://stopgame.ru/{link.get("href")}'
                    page = requests.get(game_link)
                    soup2 = BeautifulSoup(page.text, 'html.parser')
                    title = soup2.select('._title_1jxto_171')
                    game_info = soup2.find('div', '_info-grid_1jxto_194')

                    if game_info:
                        info_items = game_info.find_all('div', class_='_info-grid__title_1jxto_219')
                    else:
                        info_items = []

                    if info_items:

                        info_data = {}

                        for item in info_items:
                            name = item.get_text(strip=True)
                            info_data[name] = item.find_next('div', class_='_info-grid__value_1jxto_220')

                        platforms_info = info_data.get('Платформы')
                        platforms = []

                        if platforms_info:
                            platform_links = platforms_info.find_all('a')

                            for lnk in platform_links:
                                platform_name = lnk.get('title')
                                platforms.append(platform_name)

                        row = self.sheet1.max_row + 1
                        self.sheet1.cell(row, 1, title[0].text.strip())
                        self.sheet1.cell(row, 2, info_data.get('Дата выхода').text)
                        print(title[0].text.strip(), info_data.get('Дата выхода').text, platforms)

                        for platform in platforms:

                            if platform not in self.head:
                                self.head.append(platform)

                            j = self.head.index(platform) + 1
                            self.colorize_cell('X', j, row, color='007500', bold=False)

            else:
                input('Something wrong... Press Enter to continue')

        self.finalize_table('stopgame')


if __name__ == '__main__':
    p = Parser()
    p.run()
