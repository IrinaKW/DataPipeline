# %%
from selenium import webdriver 
driver = webdriver.Chrome()
driver.get("https://www.zoopla.co.uk/")
driver.find_element('//button')

# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = True

driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)

driver.get("https://google.com/")
print(driver.title)
driver.quit()

# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome() 
URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
driver.get(URL)
time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
try:
    driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
    accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="save"]')
    accept_cookies_button.click()

except AttributeError: # If you have the latest version of selenium, the code above won't run because the "switch_to_frame" is deprecated
    driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
    accept_cookies_button = driver.find_element(by=By.XPATH, value=('//*[@id="save"]'))
    accept_cookies_button.click()

except:
    pass # If there is no cookies button, we won't find it, so we can pass

time.sleep(2)
property = driver.find_element(By.XPATH, '//*[@id="listing_61470996"]') 
a_tag = property.find_element(By.TAG_NAME, 'a')
link = a_tag.get_attribute('href')


driver.get(link)
time.sleep(2)
price = driver.find_element(By.XPATH, '//p[@data-testid="price"]').text
print(price)
#<p data-testid="price" class="c-jdOIsX">£1,055,000</p>

address = driver.find_element(By.XPATH, '//address[@data-testid="address-label"]').text
print(address)
#<address data-testid="address-label" class="c-kjEdcl">Embassy Gardens Marke

bedrooms = driver.find_element(By.XPATH, '//div[@class="c-PJLV c-PJLV-ieHhfWi-css"]').text
print(bedrooms)
#<div class="c-PJLV c-PJLV-ieHhfWi-css">2 bed flat for sale</div>

description = driver.find_element(By.XPATH, '//div[@class="css-1sui95d-RichText eid02un0"]/span').text
desription=description.split('\n\n')[2]
print(description)
#<div class="css-1sui95d-RichText eid02un0"><span><strong>The Modern, Embassy 



# %%

result_dict = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}
result_dict['Price'].append(price)
result_dict['Address'].append(address)
result_dict['Bedrooms'].append(bedrooms)
result_dict['Description'].append(description)
result_dict