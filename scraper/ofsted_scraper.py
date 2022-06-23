# %%
#Data Pipeline Main

# Import libraries/modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.service import Service
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import time
import os
import uuid
import json
import unittest
import boto3
import urllib3
import logging
import sys

#scraper additional modules
import config
import test_module
import aws_keys



class ofsted_scraper:
    '''
    Extract the data on schools from Ofsted website:
        name
        address
        rating
        last report from ofsted website
        snapshot of the school info
    Process it as dataframe (pandas) and store in RDS and S3 on AWS
    Check if scraped piece of data already exists.  
    '''

    def __init__(self, category_age=[]):
        self.URL="https://reports.ofsted.gov.uk/"
        self.category_age=category_age
        
        #connect to RDS
        DATABASE_TYPE = config.DATABASE_TYPE
        DBAPI = config.DBAPI
        ENDPOINT =  config.ENDPOINT
        USER = config.USER
        PASSWORD = config.PASSWORD
        PORT = config.PORT
        DATABASE = config.DATABASE
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect()
    
    def set_up(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        logging.getLogger('WDM').setLevel(logging.NOTSET)
        os.environ['WDM_LOG'] = "false"
        
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        #self.driver = webdriver.Chrome(options=chrome_options) (for local run)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        #self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=chrome_options)        


    def tearDown(self):
        self.driver.quit()

    def get_1st_input(self):
        """Method asks for inputs from the user
        Returns (int): 
            1 or 2
        Raises:
            notify user if input is not correct, repeat the request
        """
        while True:
            self.category=int(input('Please Select: 1 - Education and Training; 2 - Chilcare and Early Education :'))
            if self.category==1 or self.category==2:
                break
            else:
                print("You must choose either 1 or 2")
        
    def get_2nd_input(self):
        """Method asks for inputs from the user
        Returns (int): 
            1 or 2
        Raises:
            notify user if input is not correct, repeat the request
        """
        while True:
            if self.category==1:
                self.age= int(input('Please Select: 1 - Primary, 2 - Secondary: '))
                if self.age==1 or self.age==2:
                    break
                else:
                    print("You must choose either 1 or 2")
            else:
                self.age = int(input("Choose 1: Pre-school/day nursery/out-of-school care, 2: Nursery school/school with nursery: "))
                if self.age==1 or self.age==2:
                    break
                else:
                    print("You must choose either 1 or 2")
        

    def __setup_xpaths(self):
        """private method to assign xpath values according to the provided user inputs
        Attrs:
            category_age(list): list consits of 2 values: 1 or 2, in accordance with the output of the get_inputs method
        Returns:
            list of two values: the assigned xpaths, obtained from the list of xpaths given in config file
        """
               
        if self.category==1:
            self.xpath_category=config.XPATH_ED_TR
            if self.age==1:
                self.xpath_age=config.XPATH_PR
            else: self.xpath_age=config.XPATH_SEC

        else:     
            self.xpath_category=config.XPATH_CH_ED
            if self.age==1:
                self.xpath_age=config.XPATH_PRE_SC
            else: self.xpath_age=config.XPATH_NURS
        


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
            accept_cookies_button = self.driver.find_element(By.XPATH, config.XPATH_COOKIE)
            accept_cookies_button.click()
            time.sleep(2)
        except:
            pass # If there is no cookies button, we won't find it, so we can pass

    
    
    def __select_category(self):
        """Enter the entered categories through provided xpaths and submit obtain search results (new URL)
        Attr:  
            xpath_category (str): class attribute
            xpath_age (str): class attribute
        Returns:
            driver obtains new URL address
        Raises:
            notify the user of the chaged xpaths
        """
        self.__setup_xpaths()     
        try:
            self.driver.find_element(By.XPATH, self.xpath_category).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.xpath_age).click()
            time.sleep(2)
        except:
            print("the categories xpaths has been changed ")
        
        self.driver.find_element(By.XPATH, config.XPATH_SUBMIT).click()
        WebDriverWait(self.driver, 10).until(EC.url_changes(self.URL))

    def __get_screenshot_item(self,item,name):
        """This method is used to click the provided URL of each school, 
        take snapshot of the specific element (i.e. School Info field)
        save it as png file.
        Attr: 
            item (webelement): the webelement used to locate the required <a> link
            name (str): the text that  <a> link has in it, related to the name of the school
            i (str): the number that is used in the name of the file
        Returns: 
            png file: snapshot of each school top section that is being moved to the S3 AWS bucket storage place
        """
        item.find_element(By.PARTIAL_LINK_TEXT, name).click()
        pic_element = self.driver.find_element(By.XPATH, config.XPATH_PIC)
        file_name=str("scraper/raw_data/ofsted_reports/images/"+name+".png")
        s3_name=str(name+".png")
        screenshot_as_bytes = pic_element.screenshot_as_png
        os.makedirs("scraper/raw_data/ofsted_reports/images/", exist_ok=True)
        with open(file_name, 'wb') as f:
            f.write(screenshot_as_bytes)
        s3_client =boto3.client('s3', region_name=aws_keys.AWS_REGION, aws_access_key_id=aws_keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=aws_keys.AWS_SECRET_ACCESS_KEY)
        s3_client.upload_file(file_name, 'ofstedscraper', s3_name)
        os.remove(file_name) 
        time.sleep(3)
        self.driver.back()
        time.sleep(3)

    def __select_data(self, li_tags):
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
        
        df = pd.read_sql_table('ofstedscraper', self.engine)
        df=df[['id', "name", "category", "address", "rating", "last_report"]]

        uuid_list=list(df['id'])

        for i in range(len(li_tags)):
            item = self.driver.find_elements(By.XPATH, config.XPATH_LI_TAGS)[i]
            info=(item.text).split('\n')
            name=info[0]
            id=str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
            if id in uuid_list:
                print('already exists')
                continue
            category=info[1].split(':')[1].strip()
            address=info[2]
            try:
                last_report=info[-2].split(':')[1].strip()
            except IndexError:
                last_report="Null"
        
            if len(info)==6:
                rating=info[-3].split(':')[1].strip()
            elif len(info)==5:
                rating="Null"
            else: continue
            
                     
            #data_json=json.dumps({"id":str(id), "name":name, "category":category, "address":address, "rating":rating, "last_report":last_report}, indent=4)  
            df_new= pd.DataFrame([[id,
                name, 
                category, 
                address, 
                rating, 
                last_report]], columns=['id', "name", "category", "address", "rating", "last_report"]) 
            df=pd.concat([df,df_new],ignore_index=True)
            self.__get_screenshot_item(item,name)
        
        self.aws_upload(df)
        
  
       
    def aws_upload(self,df):
        """Method uses AWS S3 bucket and RDS, and dumps the json file that contains data scraped from the current page,
        removes the file from the directory to minimise the required storage space.
        Args:
            page (int): current webpage number that has been used for data scraping
        """   
        #convert df into json file
        df.to_json('scraper/raw_data/ofsted_reports/data.json', orient='records', lines=True )
        
        #send df back to Aws RDS
        df.to_sql("ofstedscraper", self.engine, if_exists="replace")

        #upload json S3 bucket     
        s3_name=str('full_data.json')
        s3_client =boto3.client('s3')
        s3_client.upload_file('scraper/raw_data/ofsted_reports/data.json', 'ofstedscraper', s3_name)
                   
        #remove json files from the system
        os.remove('scraper/raw_data/ofsted_reports/data.json')
    

    def start_scraping(self):
        """Scraping process will collect <li> tags and loop over them to filter and collect info
        It is also required an input as a total number of pages to scrap
        While running the method will check if the file exist in the specific directory and either create it or open it
        Attr:
            driver: is being used to control the page, is updated with every new page (URL)
        Returns:
            none
        """
        self.__select_category()
        total_pages=self.driver.find_element(By.XPATH, config.XPATH_PAGES).text
        page_number=(int(input(f'There are {total_pages} of your search, enter the number of pages you would like to scrap: ')))
        os.makedirs("scraper/raw_data/ofsted_reports", exist_ok=True)
        for page in range(page_number):
            with open("scraper/raw_data/ofsted_reports/data.json", "w") as outfile:
                li_tags = self.driver.find_elements(By.XPATH, config.XPATH_LI_TAGS)
                self.__select_data(li_tags)
                self.driver.find_element(By.XPATH, config.XPATH_NEXTPAGE).click()
                WebDriverWait(self.driver, 15).until(EC.url_changes(self.URL))
                    
            page+=1



if __name__ == "__main__":
       
    #run test file
    suite = unittest.TestLoader().loadTestsFromModule(test_module)
    unittest.TextTestRunner(verbosity=2).run(suite)

    #initiate the class
    scraper=ofsted_scraper()
    scraper.get_1st_input()
    scraper.get_2nd_input()
    scraper.set_up()
    scraper.cookies()
    scraper.start_scraping()
    scraper.tearDown()

# %%

"""
ideas for dashboard:
% of schools per each rating, including NA
% of schools with last reports over 4 years old (omit NA)
combine rating/old report
geo pandas for location of the rating schools/ outdatted reports

tables: 
provide top 10 / bottom 10 schools based on rating
provide top 10 / bottom 10 schools based on last report


"""
