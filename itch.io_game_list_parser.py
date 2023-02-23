import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup

link = 'https://itch.io/games/downloadable/made-with-godot'

# Set up the webdriver and navigate to the page
driver = webdriver.Chrome()
driver.get(link)

# 36 games on page

iter = 131

# Scroll down the page a few times to load more content
for i in range(iter):
	driver.find_element_by_tag_name('body').send_keys(Keys.END)
	print(str(i) + '/' + str(iter))
	time.sleep(.5)

# Extract the HTML content and parse it with BeautifulSoup
html = driver.page_source
html_soup = soup(html, 'html.parser')

# Find the game titles
game_titles = html_soup.select('.game_title')

for title in game_titles:
	with open('godot.txt', 'a') as result:
		try:
			#print(title.text)
			result.write(title.text + '\n')
		except UnicodeEncodeError: pass

# Close the webdriver
driver.quit()
input('Press ENTER')