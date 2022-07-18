from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#url = 'https://suumo.jp/ms/chuko/tokyo/city/'

url = 'http://www.google.com/'

options = Options()
options.headless = True
#driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()

#label = driver.find_element_by_xpath("//*[@id='sa01_sc101']")

print(driver.title)
print(driver.page_source)

# label.click()

# button = brodriverwser.find_element_by_link_text('この条件で検索する')
# button.click()

# data = []
# mansions = browdriverser.find_element_by_class_name('property_unit')

# for mansion in mansions:
#   name = mansion.find_element_by_css_selector('dd.dottable-vm').text
#   price = mansion.find_element_by_class_name('dottable-value').text

#   data.append([name, price])
#   print(name,price)





