# %%
from curses import use_default_colors
from socket import timeout
import unittest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import io
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
    
    def tearDown(self):
        self.driver.close()


    @patch('builtins.input', return_value=1)
    def test_get_1st_input1(self, mock_input):
        """Test when input is 1st category"""
        self.test_scraper.get_1st_input()
        self.assertTrue(self.test_scraper.category == 1)
    
    @patch('builtins.input')
    def test_get1st_inputNo(self, mock_choice):
        for response in [1, 2, 3]:
            with self.subTest(response=response):
                mock_choice.return_value = response
                if mock_choice.return_value==3:
                    self.test_scraper.get_1st_input()
                    export_option = self.test_scraper.category
                    capturedOutput = io.StringIO()
                    sys.stdout = capturedOutput
                    self.test_scraper.get_1st_input()
                    output = capturedOutput.getvalue()
                    sys.stdout = sys.__stdout__ 
                    self.assertEqual(output,'You must choose either 1 or 2')
                    
                else:
                    self.test_scraper.get_1st_input()
                    export_option = self.test_scraper.category
                    self.assertEqual(export_option, response)
                mock_choice.reset_mock()   






if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Scraper)
    unittest.TextTestRunner(verbosity=2).run(suite)



# %%
import pandas as pd
from sqlalchemy import create_engine
import config

DATABASE_TYPE = config.DATABASE_TYPE
DBAPI = config.DBAPI
ENDPOINT =  config.ENDPOINT
USER = config.USER
PASSWORD = config.PASSWORD
PORT = config.PORT
DATABASE = config.DATABASE
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
engine.connect()

#%%

df = pd.read_sql_table('ofstedscraper', engine)
df=df[['id', "name", "category", "address", "rating", "last_report"]]
df.head(31)

#%%
df_new=pd.read_json('raw_data/ofsted_reports/data.json')
df_new.head(10)

#%%
frames = [df, df_new]
df = pd.concat(frames, axis=0, join='inner', ignore_index=True)
df.head(20)


# %%
import pandas as pd
empty_df=pd.DataFrame(columns=('id', "name", "category", "address", "rating", "last_report"))
empty_df.head()
empty_df.to_sql("ofstedscraper", engine, if_exists="replace")
      
# %%
