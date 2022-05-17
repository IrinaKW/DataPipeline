# %%
#Data Pipeline Main

# Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# import methods
import one_or_two
import select_data

#Request information: data on Primary or Secondary Maintained schools
choice=one_or_two.one_or_two()

# Open URL page and click accept cookies button
driver = webdriver.Chrome() 
options = Options()
options.headless = True
URL="https://reports.ofsted.gov.uk/"
driver.get(URL)
time.sleep(2)
accept_cookies_button = driver.find_element(By.XPATH, '//button[@class="btn cookie-banner__close"]')
accept_cookies_button.click()
time.sleep(2)

#Search the URL for required schools:
#select Education and Training categor
category_radio=driver.find_element(By.XPATH, '//*[@id="category-1"]')
category_radio.click()
time.sleep(2)

#Now depends on the type of school chosen the final choice is made
if choice=='Primary':
    choice_field=driver.find_element(By.XPATH, '//*[@id="subcatOption-1-1"]')
    choice_field.click()
else: 
    choice_field=driver.find_element(By.XPATH, '//*[@id="subcatOption-1-2"]')
    choice_field.click()
time.sleep(2)

#Time to submit the selectd options and give system up to 10 seconds waiting time in case the responce is slow
driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[1]/form/button').click()
WebDriverWait(driver, 10).until(EC.url_changes(URL))

#Time for scrapping
#First identify all tags with the information
# Second use pre-defined method that select and add info to the data frame
li_tags = driver.find_elements(By.XPATH, '//ul[@class="results-list list-unstyled"]/li') 
school_data={'name':[], 'address':[], 'rating':[], 'last_report':[]}
school_data=pd.DataFrame(school_data)
school_data= select_data.select_data(li_tags, choice, school_data)

#Three, we can loop over next whatever pages, for space/time only 5 pages is set:
page_number=driver.find_element(By.XPATH, '//span[@class="pagination__numbers"]').text
print(f'There are {page_number} pages to go through\n ')

for page in range(5):
    driver.find_element(By.XPATH, '//a[@class="pagination__next"]').click()
    WebDriverWait(driver, 15).until(EC.url_changes(URL))
    li_tags = driver.find_elements(By.XPATH, '//ul[@class="results-list list-unstyled"]/li') 
    school_data= select_data.select_data(li_tags, choice,school_data)

#The required data is collected
school_data






# %%
