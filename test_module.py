import unittest
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import unittest.mock as mock
import input_categories

class Test_URL_CookiesCheck(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def test_main_page(self):
        URL="https://reports.ofsted.gov.uk/"
        driver=self.driver
        driver.get(URL)
        assert "Find an Ofsted inspection report" in driver.title
        
    def test_xpaths_click(self):
        URL="https://reports.ofsted.gov.uk/"
        driver=self.driver
        driver.get(URL)
        for i in [config.xpath_cookie, config.xpath_ed_tr, config.xpath_ch_ed, config.xpath_submit, config.xpath_nextpage]:
            driver.find_element(By.XPATH, i).click()
            new_url=driver.current_url
            response = requests.get(new_url)
            assert response.status_code == 200
   
    def test_options(self):
        #with mock.patch(['1','2'], return_value='1'):
        #    assert input_categories.options()=='Education and Training'
        pass
    
    def test_setup_xpaths(self):
        pass

    def tearDown(self):
        self.driver.close()
if __name__ == "__main__":
    unittest.main()

