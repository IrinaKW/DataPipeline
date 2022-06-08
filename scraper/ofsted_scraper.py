# %%
#Data Pipeline Main

# Import libraries/modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import time
import os
import uuid
import json
import unittest
import boto3

#scraper additional modules
import config
import test_module



class ofsted_scraper:
    '''
    Extract the data on schools with the rating and last report from ofsted website,
    the data is based on the inputs: pre-nursery/nursery/primary/secondary

    Attributes:
        xpath_category (str): the link to the category option selected based on the input (pre-school/school) 
        xpath_age (str): the link to the sub_category option selected based on the input (pre-nursery or nursery/ primary or secondary)
    '''
    def __init__(self, category_age=[]):
        self.URL="https://reports.ofsted.gov.uk/"
        self.category_age=category_age
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)


    def get_1st_input(self):
        """Method asks for inputs from the user
        Returns (int): 
            1 or 2
        Raises:
            notify user if input is not correct, repeat the request
        """
        while True:
            self.category=int(input('Please Select: 1 - Education and Training; 2 - Chilcare and Early Education'))
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
                self.age= int(input('Please Select: 1 - Primary, 2 - Secondary'))
                if self.age==1 or self.age==2:
                    break
                else:
                    print("You must choose either 1 or 2")
            else:
                self.age = int(input("Choose 1: Pre-school/day nursery/out-of-school care, 2: Nursery school/school with nursery"))
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
        s3_client =boto3.client('s3')
        s3_client.upload_file(file_name, 'ofstedscraper', s3_name)
        os.remove(file_name) 
        time.sleep(3)
        self.driver.back()
        time.sleep(3)

    def __select_data(self, li_tags, outfile):
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
        data_file=[]
        for i in range(len(li_tags)):

            item = self.driver.find_elements(By.XPATH, config.XPATH_LI_TAGS)[i]
            info=(item.text).split('\n')
            name=info[0]
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
            id = uuid.uuid4()
            
            #data_json=json.dumps({"id":str(id), "name":name, "category":category, "address":address, "rating":rating, "last_report":last_report}, indent=4)  
            data_file.append({"id":str(id), "name":name, "category":category, "address":address, "rating":rating, "last_report":last_report})
        data_json=json.dumps(data_file)
        outfile.write(data_json)
        self.__get_screenshot_item(item,name)
            
       
    def aws_upload(self, page):
        """Method uses AWS S3 bucket and RDS, and dumps the json file that contains data scraped from the current page,
        removes the file from the directory to minimise the required storage space.
        Args:
            page (int): current webpage number that has been used for data scraping
        """   
        #upload to S3 bucket     
        s3_name=str('data'+str(page)+'.json')
        s3_client =boto3.client('s3')
        s3_client.upload_file('scraper/raw_data/ofsted_reports/data.json', 'ofstedscraper', s3_name)
        
        #connect to RDS and upload file
        DATABASE_TYPE = config.DATABASE_TYPE
        DBAPI = config.DBAPI
        ENDPOINT =  config.ENDPOINT
        USER = config.USER
        PASSWORD = config.PASSWORD
        PORT = config.PORT
        DATABASE = config.DATABASE
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect()
        try:
            df = pd.read_sql("ofstedscraper", engine)
            df_new=pd.read_json('data.json')
            frames = [df, df_new]
            df = pd.concat(frames)

        except:
            df=pd.read_json('data.json')

        #send data back to sql
        df.to_sql("ofstedscraper", engine, if_exists="replace")
           
        #remove file from the system
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
                self.__select_data(li_tags, outfile)
                self.driver.find_element(By.XPATH, config.XPATH_NEXTPAGE).click()
                WebDriverWait(self.driver, 15).until(EC.url_changes(self.URL))
                    
            self.aws_upload(page)
            page+=1



if __name__ == "__main__":
       
    #run test file
    suite = unittest.TestLoader().loadTestsFromModule(test_module)
    unittest.TextTestRunner(verbosity=2).run(suite)

    #initiate the class
    scraper=ofsted_scraper()
    scraper.get_1st_input()
    scraper.get_2nd_input()
    scraper.cookies()
    scraper.start_scraping()


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
