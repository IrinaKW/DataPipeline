#%%
import unittest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import ofsted_scraper
import config
import sys


class Test_Scraper(unittest.TestCase):
    def setUp(self):
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.test_scraper=ofsted_scraper.ofsted_scraper()
        try: 
            accept_cookies_button = self.driver.find_element(By.XPATH, config.XPATH_COOKIE)
            accept_cookies_button.click()
            time.sleep(3)
        except:
            pass

    
    def test_main_page(self):
        """
        Test if the main URL returns required page
        """
        URL="https://reports.ofsted.gov.uk/"
        self.driver.get(URL)
        time.sleep(2)
        assert "Find an Ofsted inspection report" in self.driver.title
        
    def test_xpaths_click(self):
        """
        Test if the saved xpaths for click options are still valid 
        """
        URL="https://reports.ofsted.gov.uk/"
        driver=self.driver
        driver.get(URL)
        for i in [config.XPATH_COOKIE, 
            config.XPATH_ED_TR,     
            config.XPATH_CH_ED, 
            config.XPATH_SUBMIT, 
            config.XPATH_NEXTPAGE]:
            driver.find_element(By.XPATH, i).click()
            time.sleep(2)
            new_url=driver.current_url
            
            with requests.Session() as s:
                   response = s.get(new_url)
            assert response.status_code == 200
            
    
    @patch('builtins.input', return_value=1)
    def test_get_1st_input1(self, mock_input):
        """Test when input is 1st category"""
        self.test_scraper.get_1st_input()
        self.assertTrue(self.test_scraper.category == 1)

    @patch('builtins.input', return_value=2)
    def test_get_1st_input2(self, mock_input):
        """Test when input is 2nd category"""
        self.test_scraper.get_1st_input()
        self.assertTrue(self.test_scraper.category == 2)

    #@patch('builtins.input', return_value=3)
    #def test_get_1st_inputNo(self, mock_input):
     #   """Test when input is wrong, not 1 or 2"""
      #  with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
       #     self.test_scraper.get_1st_input()
        #    self.assertEqual(mock_stdout.getvalue(), "You must choose either 1 or 2\n")
    


    @patch('builtins.input', return_value=1)
    def test_get_2nd_input1(self, mock_input):
        """Test when input is 1st category"""
        self.test_scraper.category=1
        self.test_scraper.get_2nd_input()
        self.assertTrue(self.test_scraper.age == 1)

    @patch('builtins.input', return_value=2)
    def test_get_2nd_input2(self, mock_input):
        """Test when input is 2nd category"""
        self.test_scraper.category=1
        self.test_scraper.get_2nd_input()
        self.assertTrue(self.test_scraper.age == 2)

    
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Scraper)
    unittest.TextTestRunner(verbosity=2).run(suite)



# %%
