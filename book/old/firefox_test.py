from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

#url = 'https://nikkei225jp.com/data/karauri.php'
url = 'http://www.google.com'

driver.get(url)
sleep(5)
html = driver.page_source.encode('utf-8')

q = driver.find_element_by_name("q")
q.send_keys('月間IO')
q.submit()

driver.close()

#df_list = pd.read_html(html, header=0)
#print(df_list[3].head())
