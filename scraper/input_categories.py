#Function to question the required input from the user:
import config

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

    elif category_choice == "2":
        category_choice == "Chilcare and Early Education"
        age = input("Choose 1: Pre-school/day nursery/out-of-school care, 2: Nursery school/school with nursery")
        if age == "1":
            return [category_choice, "Pre-school/day nursery/out-of-school care"]
        
        elif age == "2":                
            return [category_choice, "Nursery school/school with nursery"]
        
        else:
            print("You must choose between 1 or 2")
            return options()
    
    else: 
        print("You must choose between 1 or 2")
        return options()

def setup_xpaths(category_age):
    if category_age[0]=='Education and Training':
        xpath_category=config.xpath_ed_tr
        if category_age[1]=='Primary':
            xpath_age=config.xpath_pr
        else: xpath_age=config.xpath_sec

    else:     
        xpath_category=config.xpath_ch_ed
        if category_age[1]=='Pre-school/day nursery/out-of-school care':
            xpath_age=config.xpath_pre_sc
        else: xpath_age=config.xpath_nurs
    
    return [xpath_category, xpath_age]