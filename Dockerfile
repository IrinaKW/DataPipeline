FROM python:3.9

#version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -\
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'\
    && apt-get -y update\
    && apt-get install -y google-chrome-stable\
    && apt-get --only-upgrade install google-chrome-stable\
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip\
    && apt-get install -yqq unzip\
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

   
    
COPY . .

RUN pip install -r requirements.txt
 
CMD ["python", "scraper/ofsted_scraper.py"]