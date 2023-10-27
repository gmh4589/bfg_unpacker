import requests
from selenium import webdriver
from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from time import sleep
from table_creator import TableCreator

options = Options()
options.add_argument("--headless")


class Parser(TableCreator):

    def __init__(self):
        super().__init__()
        self.sheet_name = 'IGROMANIA'

    def run(self):
        a = 0

        while True:
            a += 1

            if a > 10:
                break

            while True:
                try:
                    driver = webdriver.Chrome(options=options)
                    url = f'https://www.igromania.ru/games/?page={a}'
                    driver.get(url)
                    sleep(randint(1, 5))
                    response = requests.get(url)
                    break
                except requests.exceptions.ConnectionError:
                    print('Они думают, что мы их ддосим)))\nПоспим минуту-две...')
                    sleep(randint(50, 100))

            if response.status_code == 200:
                # soup = BeautifulSoup(response.text, 'html.parser')

                names = BeautifulSoup(driver.page_source, 'html.parser').select('.GameCard_title__V4i1j')
                dates = BeautifulSoup(driver.page_source, 'html.parser').select('.GameCard_date__ZEatM')
                platforms = BeautifulSoup(driver.page_source,
                                          'html.parser').find_all('div', class_='GameCard_platforms__UGGQ1')

                driver.close()
                driver.quit()

                for i, d in enumerate(names):

                    try:
                        platforms_list = [a.get_text() for a in platforms[i].find_all('a')]
                    except IndexError:
                        platforms_list = []

                    row = self.sheet1.max_row + 1
                    name = d.text
                    date = dates[i].text.replace("Вышла: ", "")
                    self.sheet1.cell(row, 1, name)
                    self.sheet1.cell(row, 2, date)

                    for pl in platforms_list:

                        if pl not in self.head:
                            self.head.append(pl)

                        j = self.head.index(pl) + 1
                        self.colorize_cell('X', j, row, color='007500', bold=False)

                    print(f'{names[i].text}\t{dates[i].text}\tПлатформы: {platforms_list}')
            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
                break

        self.finalize_table('igromania')


if __name__ == '__main__':
    p = Parser()
    p.run()
