# import libraries 
import pandas as pd
import time, urllib.request
from urllib.request import urlopen
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#chromedriver in the same folder
chrome_path = "chromedriver.exe"

#customize options
custom_options = webdriver.ChromeOptions()

# translate the site into english 
prefs = {
    "translate_whitelists": {"ru": "en"},
    "translate": {"enabled":"true"}
}
custom_options.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome(chrome_path, options=custom_options)
    time.sleep(6)
# the actual link for the site 
    driver.get("https://wiki.mipt.tech/index.php/")


#our file will contain the following fields 
field_names = 
