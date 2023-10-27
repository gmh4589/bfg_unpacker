
import time
import os

# 24 feb 2023
# godot = https://itch.io/games/downloadable/made-with-godot = 4,655 results
# renpy = https://itch.io/games/downloadable/made-with-renpy = 2,448 results
# unity = https://itch.io/games/downloadable/made-with-unity = 25,465 results
# gamemaker = https://itch.io/games/downloadable/made-with-gamemaker = 6,157 results

links = ['https://itch.io/games/downloadable/made-with-renpy',
         'https://itch.io/games/downloadable/made-with-godot',
         'https://itch.io/games/downloadable/made-with-unity',
         'https://itch.io/games/downloadable/made-with-gamemaker']


def main():

    for link in links:
        # Set up the webdriver and navigate to the page
        driver = webdriver.Chrome()
        driver.get(link)

        # 36 games on page

        # Extract the HTML content and parse it with BeautifulSoup
        html = driver.page_source
        html_soup = soup(html, 'html.parser')

        # Find the game titles
        gameCount = html_soup.select('.game_count')[1].text.split(' ')[0].replace(',', '')

        count = int(int(gameCount) / 36) + 1

        # Scroll down the page a few times to load more content
        for i in range(count):
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            print(f'{str(i * 36)}/{gameCount}')
            time.sleep(.5)

        # Extract the HTML content and parse it with BeautifulSoup
        html = driver.page_source
        html_soup = soup(html, 'html.parser')

        # Find the game titles
        game_titles = html_soup.select('.game_title')

        name = link.split('-')[-1]
        for title in game_titles:
            with open(f'{name}.txt', 'a') as result:
                try:
                    result.write(title.text + '\n')
                except UnicodeEncodeError:
                    pass

        # Close the webdriver
        driver.quit()

    input('Press ENTER')


try:

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup as soup

    if __name__ == '__main__': main()

except ModuleNotFoundError:

    os.system('pip3 install selenium')
    os.system('pip3 install BeautifulSoup4')

    # TODO: Localized text
    print('Please, rerun this tool')
