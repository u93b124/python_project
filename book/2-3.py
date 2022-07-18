import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

driver.get('https://suumo.jp/ms/chuko/tokyo/city/')
time.sleep(3)

label = driver.find_element_by_xpath("//*[@id='sa01_sc101']")
label.click()

button = driver.find_element_by_link_text('この条件で検索する')
#button = driver.find_element_by_xpath("//*[@id='js-shiborikomiPanel']/div[2]/a")
button.click()

# data = []
# mansions = driver.find_element_by_class_name('property_unit')

# for mansion in mansions:
#   name = mansion.find_element_by_css_selector('dd.dottable-vm').text
#   price = mansion.find_element_by_class_name('dottable-value').text

#   data.append([name, price])
#   print(name,price)


driver.quit()
