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
The scraper does image scraping from each school name, address, unique ID registered with Ofsted
![Example of one of the school's snapshop](./images/school_screenshot.png)


## Setup
The required libraries are:
- selenium / webdriver
- time
- os
- uuid
- json

The reqduired files, with list of constants and methods:
- import input_categories: convert input information into related xpaths
- import config: xpath constants

The scraper runs the test_module (test_module.py)
Module checks: 
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

2. Introducation of the scraper class:
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

## Project Status
Project is: _in progress_ 


## Room for Improvement
Room for improvement:
- The project will benefit from the selection of the driver as an option for various web browsers: Firefox, Safari, etc.
- The option for the user to have a choice of either print the data on screen or write all in file as at present

To do:
- The visualisation of the data as per the user request.


## Acknowledgements
- This project was inspired by AiCore program and my background in education.



## Contact
Created by [@IrinaKW](irina.k.white@gmail.com) - feel free to contact me!

