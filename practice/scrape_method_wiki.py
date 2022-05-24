# %%
import requests
from bs4 import BeautifulSoup
URL='https://en.wikipedia.org/wiki/Python_(programming_language)'
page=requests.get(URL)
html=page.text
soup=BeautifulSoup(html, 'html.parser')
a_tag=soup.find_all(name='a', attrs={'class':'mw-redirect', 'title':"Method (programming)" })
print([i.find_parent().text for i in a_tag])


# %%
import requests
from bs4 import BeautifulSoup
URL='https://www.zoopla.co.uk/'
page=requests.get(URL)
html=page.text
soup=BeautifulSoup(html, 'html.parser')
button_tag=soup.find_all(name='button')
print(len(button_tag))
# %%



# %%


#from selenium import webdriver from selenium.webdriver.chrome.options import Options

#chrome_options = Options() chrome_options.add_argument('--headless')

#driver = webdriver.Chrome('/path/to/your_chrome_driver_dir/chromedriver', chrome_options=chrome_options)