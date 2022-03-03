import requests
import os.path
import re
from bs4 import BeautifulSoup as soup
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys

link = 'https://itch.io/games/made-with-godot'

for k in range(10):
	r = requests.get(link)
	html = soup(r.content, 'html.parser')

	list = html.select('.grid_outer')

for i in list:
	game_name = i.select('.game_title')
	
for j in game_name:
	print(j.text)
		
input('Press ENTER')
