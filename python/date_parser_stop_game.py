import requests
from bs4 import BeautifulSoup as BS

file = open('list.txt', 'r')
list = open('date_list.txt', 'w+')
string = file.readlines()

for k in range(len(string)):
	r = requests.get('https://stopgame.ru/game/'+string[k][0:-1])
	html = BS(r.content, 'html.parser')
	info = string[k][0:-1]+'|Page not found!\n'

	for j in html.select('.article-title'):
		name = j.select('a')

	for i in html.select('.game-specs'):
		value = i.select('.game-spec > .value')
		str = value[2].text
		arr = str.split()
		info = name[0].text+'|'+arr[-2]+'\n'

	print(info)
	list.write(info)
		
input('Press ENTER')
