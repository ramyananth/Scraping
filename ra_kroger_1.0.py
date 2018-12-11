# -*- coding: utf-8 -*-
"""
Created on Mon May 28 06:00:22 2018

@author: ramya.ananth
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
import urllib
import pandas as pd
import numpy as np
import os
import re

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
os.getcwd()
os.chdir("C:\\Users\\ramya.ananth\\Desktop\\kroger.com")
BINARY = FirefoxBinary('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')

df=pd.read_csv('us_zipcodes_sample.txt',sep=',',encoding='latin-1',thousands=',')
df['Zipcode'].astype(str)
type(df['Zipcode'])
df['Zipcode'] = df['Zipcode'].apply(lambda x: '{0:0>5}'.format(x))

driver = webdriver.Firefox(firefox_binary=BINARY,executable_path='C:/Users/ramya.ananth/Downloads/geckodriver-v0.20.1-win64/geckodriver.exe')
driver.get("https://www.kroger.com/stores/search")

elem = driver.find_element_by_class_name('Input-input SearchBox-inputBox')

EXCEPTION_COUNT = 0

def getMiles(string):
    foo = re.findall('([0-9]*(\.)?[0-9]*)',string)
    return [x for x in foo if x!= ('','')][1][0]

def checkKroger(zipcode):
    try:
        elem.clear()
        elem.send_keys(zipcode)
        elem.send_keys(Keys.RETURN)
        sleep(4)
        
        first_store_name = 'Color StoreResult-vanityNameLink Link'
        first_store_dist = 'StoreResult-distance'
        second_store_name = 'Color StoreResult-vanityNameLink Link'
        second_store_dist = 'StoreResult-distance'
        
        first_store_name1 = driver.find_element_by_class_name(first_store_name).get_attribute('innerHTML')
        first_store_dist1 = getMiles(driver.find_element_by_class_name(first_store_dist).get_attribute('innerHTML'))
        second_store_name1 = driver.find_element_by_class_name(second_store_name).get_attribute('innerHTML')
        second_store_dist1 = getMiles(driver.find_element_by_class_name(second_store_dist).get_attribute('innerHTML'))
        
        return pd.DataFrame({'Zipcode':zipcode,'Store1':first_store_name1,'Store1_dist':first_store_dist1,
                          'Store2':second_store_name1,'Store2_dist':second_store_dist1},index=[0])
    except:
        return 'Exception'

result_df = pd.DataFrame()   
m=0 


for everyZip in df['Zipcode'].tolist():
    if(m>100):
        result_df.to_csv('zip_file.csv', sep='\t', encoding='utf-8')
        driver.quit()
        driver = webdriver.Firefox(firefox_binary=BINARY,executable_path='C:/Users/ramya.ananth/Downloads/geckodriver-v0.20.1-win64/geckodriver.exe')
        driver.get("https://www.kroger.com/stores/search")
        sleep(15)
        m=0
    m=m+1
    x = checkKroger(everyZip)
    if(isinstance(x,str)):
        EXCEPTION_COUNT+=1
        if(EXCEPTION_COUNT>=5):
            print('Delay of 10 minutes.')
            sleep(60)
            #sleep(60*10)
            EXCEPTION_COUNT = 0
    else:
        result_df = result_df.append(x)
    
#####RUN at the LAST 
#result_df.to_csv('zip_file2.1.csv', sep='\t', encoding='utf-8')
