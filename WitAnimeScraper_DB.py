from selenium.webdriver import Chrome
import time
import importlib
import pymongo
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

#  Get the Webpage content 
dp = '/Users/aziz/PycharmProjects/scrapingAnime/chromedriver-1' # driver path
driver = Chrome(dp)
url = f"https://witanime.com/anime-type/tv/"
page = (requests.get(url))
content = page.content
soup = BeautifulSoup(content, 'lxml')
# find all the animes' name
all_names = soup.find_all("div", class_="anime-card-title")

#remove any special characters 
clean = []
for name in all_names:
	clean.append(re.sub(f"!", "", name.find('a').text))

special_char = "@_!#$%^&*()<>?/\|}{~:;.[]-,♭'"

out_list = [''.join(x for x in string if not x in special_char) for string in clean]

dd = []
newname = []

# function to find how many episodes in each anime
def get_lenght(anime_name):
	Anime_Name = anime_name.replace(" ", '-')
	url2 = f"https://witanime.com/episode/{Anime_Name}-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
	driver.get(url2)
	ep = driver.find_element_by_xpath('//*[@id="mCSB_1_container"]')
	links = ep.find_elements_by_tag_name("li")
	li_length = []
	for i in links:
		li_length.append(i.text)
	last_ep = len(li_length)
	return last_ep


client = pymongo.MongoClient()
mydb = client['WitAnime']

broken = []
for i in out_list:
	Links_url = []
	Links_name = []
	op_mbd = mydb[i]
	# print(i)
	try:
		end = get_lenght(i)
		for pn in range(1, end + 1):
			ani_name = i.replace(" ", "-")
			dname = []
			dlink = []

			url3 = f'https://witanime.com/episode/{ani_name}-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-{pn}/'
			pagelink = requests.get(url3)
			content = pagelink.content
			soup = BeautifulSoup(content, 'lxml')
			ename = soup.find('ul', class_="nav nav-tabs")
			name = soup.title.text

			for k in ename.find_all('li'):
				dname.append(k.find('a').text)
				dlink.append(k.find('a').attrs['data-ep-url'])
				dd.append(name.strip("- WitAnime مترجمة اون لاين"))

			op_mbd.insert_one(
				{'Episode': pn, 'Stream': {'Stream Name': dname, 'Stream Link': dlink}})
	except:
		print("Error: " + i)
		broken.append(i)
		pass

len(broken)
print(broken)
driver.quit()
