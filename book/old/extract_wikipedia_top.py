from bs4 import BeautifulSoup
import requests

page_data = requests.get('https://ja.wikipedia.org/wiki/Python').text
page = BeautifulSoup(page_data, 'lxml')
for element in page.select("#siteSub"):print(element.txt)
