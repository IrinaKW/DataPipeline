# Data Pipeline

This is the web scraper project that employs the scraper on the Ofsted website for primary and secondary public schools
The idea is to collect all the information for quick update on last reports and rating of various schools.

The project uses Python, Selenium, Chromedrive to perform the above

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


## Features
List the ready features here:
- ability to accept cookies
- selection of required options
- data file as an output


## Screenshots
section _in progress_


## Setup
The required libraries are:
- from selenium import webdriver
- from selenium.webdriver.common.by import By
- from selenium.webdriver.chrome.options import Options
- from selenium.webdriver.support.ui import WebDriverWait
- from selenium.webdriver.support import expected_conditions as EC
- import time
- import pandas as pd

## Usage
The code gives an option for the user to enter: Primary or Secondary:
```
#Now depends on the type of school chosen the final choice is made
if choice=='Primary':
    choice_field=driver.find_element(By.XPATH, '//*[@id="subcatOption-1-1"]')
    choice_field.click()
else: 
    choice_field=driver.find_element(By.XPATH, '//*[@id="subcatOption-1-2"]')
    choice_field.click()
time.sleep(2)
```
For demostration purposes only 5 pages are being selected for data scraping, however with better storage facility one can modify to select all.
```
#Three, we can loop over next whatever pages, for space/time only 5 pages is set:
page_number=driver.find_element(By.XPATH, '//span[@class="pagination__numbers"]').text
print(f'There are {page_number} pages to go through\n ')

for page in range(5):
    driver.find_element(By.XPATH, '//a[@class="pagination__next"]').click()
    WebDriverWait(driver, 15).until(EC.url_changes(URL))
    li_tags = driver.find_elements(By.XPATH, '//ul[@class="results-list list-unstyled"]/li') 
    school_data= select_data.select_data(li_tags, choice,school_data)

```

## Project Status
Project is: _in progress_ 


## Room for Improvement
Room for improvement:
- The project will benefit from the addion of drivers for various web browsers: Firefox, Safari, etc.

To do:
- The visualisation of the data, etc.


## Acknowledgements
- This project was inspired by AiCore program and my background in education.



## Contact
Created by [@IrinaKW](irina.k.white@gmail.com) - feel free to contact me!

