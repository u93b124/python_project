from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

url = 'https://www.google.com'

CHROME_BIN = '/usr/bin/chromium-browser'
CHROME_DRIVER = '/usr/bin/chromedriver'


# 実行オプション
options = Options()
options.binary_location = CHROME_BIN
options.add_argument('--headless')
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

display = Display(visible=0, size=(800, 800))  
display.start()


#browser = webdriver.Firefox()
browser = webdriver.Chrome(CHROME_DRIVER, options=options)

browser.get(url)

q = browser.find_element_by_name("q")
q.send_keys('月刊IO')

q.submit()


