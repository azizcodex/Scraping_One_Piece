import importlib
import requests
from bs4 import BeautifulSoup
import importlib

Names = []
Links_name = []
Links_url = []
"https://witanime.com/episode/one-piece-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
"https://witanime.com/episode/one-piece-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-2/"

for pn in range(716, 993):
	url2 = f'https://witanime.com/episode/one-piece-%D8%A7%D9%84%D8%AD%D9%84%D9%82%D8%A9-{pn}/'
	pagelink = requests.get(url2)
	content = pagelink.content
	soup = BeautifulSoup(content, 'lxml')
	ename = soup.find('ul', class_="nav nav-tabs")
	name = soup.title.text
	print(name.strip("- WitAnime مترجمة اون لاين"))

	for i in ename.find_all('li'):
		# print(i.find('a').text +": "+i.find('a').attrs['data-ep-url'])
		# print(i.find('a').text)
		# print(i.find('a', string="4shared"))
		Links_url.append(i.find('a').attrs['data-ep-url'])
		Links_name.append(i.text)
		print(i.find('a').attrs['data-ep-url'])

	print("\n")

	# print(Links_url)
# Full_anime = {"Name": Names, "Links": {'Link Name': Links_name, 'Link URL': Links_url}}
# Full_anime = {"Name": Names, "Links": [Links_name, Links_url]}
# Full_anime = {"Name": Names, "Links": {[Links_name, Links_url]}}
# print(Full_anime)
# 	for i in range(len(Links_name)):
# 		full_anime = {Links_name[i]: Links_url[i]}
# 		print(full_anime)
