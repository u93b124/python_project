import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

driver.get('https://www.yahoo.co.jp/')

time.sleep(3)

html = driver.page_source
print(html)

driver.save_screenshot("hoge.png")

driver.quit()
