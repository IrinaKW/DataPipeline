# Data Pipeline

This is the web scraper project that employs the scraper on the Ofsted website for primary and secondary public schools
The idea is to collect all the information for quick update on last reports and rating of various schools.

The project uses Python, Selenium, Chromedrive, AWS S3, AWS RDS
 to perform the above

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)



## General Information
- The project came as an idea of combining data mining/ pipeline and education, finidng the way to improve of the current website. 
- It is essential for the schools to be checked once in 4 years. 
- The project not only showed that the system is behind but also demonstrated how far behand and what schools are in need to be observed.


## Technologies Used
- Python 3.9.7
- Chromedriver 101.0.4951.41 
- Chrome 101.0.4951.67
- AWS S3
- AWS RDS



## Features
List the ready features here:
- ability to accept cookies
- selection of required options
- tabular data file as json created one per page, uploaded to AWS S3 bucket and to Postgres RDS
- screenshot images, 10 per page, uploaded to AWS S3
- all files are deleted from the local system to minimise storage issues


## Screenshots
section _in progress_
The scraper does image scraping from each school name, address, unique ID registered with Ofsted

School's snapshot that is being collected
![Example of one of the school's snapshot](.scraper/img/school_screenshot.png)

Dataframe sample
![Example of the pd dataframe created](.scraper/img/df.png)



## Setup
The required libraries are:
- selenium / webdriver
- time
- os
- uuid
- json
- psycopg2
- pandas
- unittest
- boto3
- sqlalchemy


Required additional modules:
- import config: xpath constants, input RDS credentials
- test_module (test_module.py). Module checks: 
    - if buildin link and xpaths are active and valid
    - if inputs provide required variable assignments


## Usage
1. The code gives an option for the user to enter required categories (partial code below)
```
def options():
    category_choice=input('Please Select: 1 - Education and Training; 2 - Chilcare and Early Education')
    if category_choice == "1":
        category_choice== "Education and Training"
        age = input('Please Select: 1 - Primary, 2 - Secondary')
        if age == "1":
            return [category_choice, "Primary"]
        
        elif age == "2":
            return [category_choice, "Secondary"]
        
        else:
            print("You must choose between 1 or 2")
            return options()
```

2. Intro into of the scraper class:
```
class ofsted_scraper (partial code below):
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
```
3. selenium drive is used to control the link(s) and take snapshots of the linked school
```
def __get_screenshot_item(self,item,name):
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
```
4. information is uploaded to AWS
```
        #upload to S3 bucket     
        s3_name=str('data'+str(page)+'.json')
        s3_client =boto3.client('s3')
        s3_client.upload_file('scraper/raw_data/ofsted_reports/data.json', 'ofstedscraper', s3_name)

```
## Project Status
Project is: _in progress_ 


## Room for Improvement
Room for improvement:
- The project will benefit from the selection of the driver as an option for various web browsers: Firefox, Safari, etc.
- The option for the user to have a choice of either print the data on screen or store the file remotely as at present

To do:
- The visualisation/ dashboard of the data as per the user request.


## Acknowledgements
- This project was inspired by AiCore program and my background in education.



## Contact
Created by [@IrinaKW](irina.k.white@gmail.com) - feel free to contact me!

