# %%
#Data Pipeline Main

# Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import uuid

# import 
import input_categories
import select_data
import config


class ofsted_scraper:
    '''
    Extract the data on schools with the rating and last report from ofsted website,
    the data is based on the inputs: pre-nursery/nursery/primary/secondary

    Attributes:
        URL (str): The ofsted URL, which will be modified based on the provided inputs
    '''
    def __init__(self, xpath_category: str, xpath_age:str):
        self.URL="https://reports.ofsted.gov.uk/"
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.xpath_category=xpath_category
        self.xpath_age=xpath_age


    def cookies(self):
    # Open URL page and click accept cookies button
        self.driver.get(self.URL)
        time.sleep(2)
        accept_cookies_button = self.driver.find_element(By.XPATH, config.xpath_cookie)
        accept_cookies_button.click()
        time.sleep(2)

    def select_category(self):
    #Search the URL for entered categories
        self.driver.find_element(By.XPATH, self.xpath_category).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, self.xpath_age).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, config.xpath_submit).click()
        WebDriverWait(self.driver, 10).until(EC.url_changes(self.URL))

    def scraper(self):
        #scraping process will collect <li> tags and loop over them to filter and collect info
        total_pages=self.driver.find_element(By.XPATH, config.xpath_pages).text
        page_number=(int(input(f'There are {total_pages} of your search, enter the number of pages you would like to scrap: ')))
        os.makedirs("/raw_data/ofsted_reports", exist_ok=True)
        with open("/raw_data/ofsted_reports/data.json", "w") as outfile:
            for page in range(page_number):
                li_tags = self.driver.find_elements(By.XPATH, config.xpath_li_tags)
                select_data.select_data(li_tags, outfile)
                self.driver.find_element(By.XPATH, config.xpath_nextpage).click()
                WebDriverWait(self.driver, 15).until(EC.url_changes(self.URL))
                page+=1

if __name__ == "__main__":
    #Request to enter the search fields and update xpaths
    category_age=input_categories.options()
    res=input_categories.setup_xpaths(category_age)
    xpath_category=res[0]
    xpath_age=res[1]
    #initiate the class
    scraper=ofsted_scraper(xpath_category, xpath_age)
    scraper.cookies()
    scraper.select_category()
    scraper.scraper()
















# %%
