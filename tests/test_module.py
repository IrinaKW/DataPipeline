import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import mock
import scraper.input_categories
import scraper.ofsted_scraper
import scraper.config

class Test_URL_CookiesCheck(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def test_main_page(self):
        """
        Method to check if the main URL still return required page
        """
        URL="https://reports.ofsted.gov.uk/"
        driver=self.driver
        driver.get(URL)
        assert "Find an Ofsted inspection report" in driver.title
        
    def test_xpaths_click(self):
        """
        Method to check if the saved xpaths for click options are still valid 
        """
        URL="https://reports.ofsted.gov.uk/"
        driver=self.driver
        driver.get(URL)
        for i in [scraper.config.xpath_cookie, 
            scraper.config.xpath_ed_tr,     
            scraper.config.xpath_ch_ed, 
            scraper.config.xpath_submit, 
            scraper.config.xpath_nextpage]:
            driver.find_element(By.XPATH, i).click()
            new_url=driver.current_url
            response = requests.get(new_url)
            assert response.status_code == 200
   
    #@mock.patch('ofsted_scraper.input_categories.options', return_value=['Education and Training', 'Primary'])
    def test_mock_options(self):
        """
        This method tests whether the function returns required categories selection
        """
        #actual_result=scraper.input_categories.options()
   
        pass




#'Chilcare and Early Education','Pre-school/day nursery/out-of-school care', 'Nursery school/school with nursery', 
#'Education and Training', 'Primary', 'Secondary'



    def test_setup_xpaths(self):
        self.assertEqual(scraper.input_categories.setup_xpaths(['Education and Training','Primary']),['//*[@id="category-1"]','//*[@id="subcatOption-1-1"]'])
        

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

