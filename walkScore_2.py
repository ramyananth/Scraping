# -*- coding: utf-8 -*-
"""
Created on Thu May  3 10:39:36 2018

@author: ramya.ananth
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import re

BINARY = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none"

def scrapeWalkScore(search_term):
    try:
        url = 'https://www.walkscore.com/score/'+search_term.lower().replace(' ','-')
        #driver = webdriver.Firefox(firefox_binary=BINARY)
        driver = webdriver.Firefox(firefox_binary=BINARY,capabilities=capa)
        wait = WebDriverWait(driver, 120) # Wait for 120 seconds at most
        
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'block-header-badge'))) # Stops loading the page when CAtgories appear
        driver.execute_script("window.stop();")
        res = driver.find_element_by_class_name('block-header-badge')
        oo= re.findall('[0-9]*\.svg',res.get_attribute('outerHTML'))[0].replace('.svg','')
        driver.close()
        return oo
    except:
        driver.close()
        return 'Exception'
    
# File I/O
clet_stores = pd.read_excel('C:\\Users\\ramya.ananth\\Documents\\203 Stores.xlsx',sheetname='Sheet1')
search_terms = clet_stores['Concat'].unique().tolist()
results =[]

for i,search_term in enumerate(search_terms):
    print('Store #'+str(i)+'| Search term: '+search_term)
    x = scrapeWalkScore(search_term)
    results.append(x)
    print('Result: '+ str(x))