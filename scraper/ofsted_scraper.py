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
import json
import unittest

# import 
import input_categories
import config
import tests.test_module


class ofsted_scraper:
    '''
    Extract the data on schools with the rating and last report from ofsted website,
    the data is based on the inputs: pre-nursery/nursery/primary/secondary

    Attributes:
        xpath_category (str): the link to the category option selected based on the input (pre-school/school) 
        xpath_age (str): the link to the sub_category option selected based on the input (pre-nursery or nursery/ primary or secondary)
    '''
    def __init__(self, xpath_category: str, xpath_age:str):
        self.URL="https://reports.ofsted.gov.uk/"
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.xpath_category=xpath_category
        self.xpath_age=xpath_age

    def input_categories(self):
        """Create a method for input values as oppose to input_categories pre-function?

        """
        pass 
        


    def cookies(self):
        """Open URL and identifies the cookies button on the page and click on it.
        Attr:
            URL (str): the global variable, URL to the sebsite (ofsted reports)
            driver (interface); the chrome webdriver used by selenium to control the webpage remotely 

        Raises:
            pass if there is no cookies button but has the URL open

         """
        
        self.driver.get(self.URL)
        time.sleep(2)
        try: 
            accept_cookies_button = self.driver.find_element(By.XPATH, config.xpath_cookie)
            accept_cookies_button.click()
            time.sleep(2)
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    
    def select_category(self):
        """Enter the entered categories through provided xpaths and submit obtain search results (new URL)
        Attr:  
            xpath_category (str): class attribute
            xpath_age (str): class attribute
        Returns:
            driver obtains new URL address
        Raises:
            notify the user of the chaged xpaths
        """
        try:
            self.driver.find_element(By.XPATH, self.xpath_category).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.xpath_age).click()
            time.sleep(2)
        except:
            print("the categories xpaths has been changed ")
        
        self.driver.find_element(By.XPATH, config.xpath_submit).click()
        WebDriverWait(self.driver, 10).until(EC.url_changes(self.URL))


    def select_data(self, li_tags, outfile):
        """Scraps the data from the given page, generates uuid for each item, create the json file with data
        Args:
            li_tags (lst): list of li_tags collected from the page that encapuslates all related data
            outfile (json file): the json file that either empty or has previously collected data
        Returns:
            outfile (json file): updated json file
        Raises:
            IndexError: if the structure of the data is modified or doesn't follow the identify layout, 
            the NA value is entered, or the entry is passed on as irrelevant.
        """

        for item in range(len(li_tags)):
            info=(li_tags[item].text).split('\n')
            name=info[0]
            category=info[1].split(':')[1].strip()
            address=info[2]
            try:
                last_report=info[-2].split(':')[1].strip()
            except IndexError:
                last_report='NA'
        
            if len(info)==6:
                rating=info[-3].split(':')[1].strip()
            elif len(info)==5:
                rating='NA'
            else: continue
            id = uuid.uuid4()
        
            data_json=json.dumps({'id':[str(id)], 'name':[name], 'category':[category], 'address':[address], 'rating':[rating], 'last_report':[last_report]}, indent=4)  
            outfile.write(data_json) 

    def scraper(self):
        """Scraping process will collect <li> tags and loop over them to filter and collect info
        It is also required an input as a total number of pages to scrap
        While running the method will check if the file exist in the specific directory and either create it or open it
        Attr:
            driver: is being used to control the page, is updated with every new page (URL)
        Returns:
            none
        """

        total_pages=self.driver.find_element(By.XPATH, config.xpath_pages).text
        page_number=(int(input(f'There are {total_pages} of your search, enter the number of pages you would like to scrap: ')))
        os.makedirs("raw_data/ofsted_reports", exist_ok=True)
        with open("raw_data/ofsted_reports/data.json", "w") as outfile:
            for page in range(page_number):
                li_tags = self.driver.find_elements(By.XPATH, config.xpath_li_tags)
                self.select_data(li_tags, outfile)
                self.driver.find_element(By.XPATH, config.xpath_nextpage).click()
                WebDriverWait(self.driver, 15).until(EC.url_changes(self.URL))
                page+=1



if __name__ == "__main__":
    #Request to enter the search fields and update xpaths
    
    #run test file
    suite = unittest.TestLoader().loadTestsFromModule(tests.test_module)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    #run input request file
    category_age=input_categories.options()
    res=input_categories.setup_xpaths(category_age)
    xpath_category=res[0]
    xpath_age=res[1]

    #initiate the class with the json file as the result
    scraper=ofsted_scraper(xpath_category, xpath_age)
    scraper.cookies()
    scraper.select_category()
    scraper.scraper()



# %%

"""
ideas for visuals/tabulars:
% of schools per each rating, including NA
% of schools with last reports over 4 years old (omit NA)
combine rating/old report
geo pandas for location of the rating schools/ outdatted reports

tables: 
provide top 10 / bottom 10 schools based on rating
provide top 10 / bottom 10 schools based on last report


"""
