# General Stuff
import os
import gc
import pandas as pd
import numpy as np
import time

# Scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests import get
from requests.exceptions import RequestException

# Parsing
import re
from bs4 import BeautifulSoup

# Global variables
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROMEDRIVER_PATH = '../../chromedriver'

def extract_html(driver_path, driver_options,
                 url, 
                 sleep_time=1):
    with webdriver.Chrome(executable_path=driver_path,
                         options=driver_options) as driver:
        # Retrieve
        driver.get(url)
        
        # Sleeper
        time.sleep(sleep_time)
        
        # Extract html
        html = driver.page_source
    
    return(html)

def parse_firm_index(html):
    # Create BS
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extrac highlevel info
    firmContent = soup.find('div', {'ng-show': 'firm.details.name'})
    wantItems = ['Revisionsstelle/n:', 'UID:']
    contentDelimiters = re.compile(r'>(.*?)<')
    
    #
    for item in firmContent.find_all('tr'):
        
        for nameItem in item.find_all('td', {'class': 'ng-binding'}):
            iterTerm = re.findall(contentDelimiters, str(nameItem))[0]

            if iterTerm in wantItems:
                for webItem in item.find_all('span', {'class': 'ng-binding'}):
                    webIter = re.findall(contentDelimiters, str(webItem))[0]
                    print(iterTerm, webIter)
    
    for item in firmContent.find_all('strong'):
        firmName = re.findall(contentDelimiters, str(item))[0]
        print(firmName)
    
    for item in firmContent.find_all('span',
                                     {'ng-repeat': "translation in firm.translation"}):
        otherNames = re.findall(contentDelimiters, str(item))[0]
        print(otherNames)
    

# Define options (ie. headlessness)
#class TopLevelGrazer():
    #self.chrome_options = Options()
    #self.CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    
    #chrome_options.add_arguemtn("--headless")
    #chrome_options.binary_location()