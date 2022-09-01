#import chromedriver_binary  # Adds chromedriver binary to path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException        
<<<<<<< HEAD
from selenium.webdriver.chrome.options import Options



driver = webdriver.Chrome('/usr/bin/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

import os
import json
import time
=======

driver = webdriver.Chrome('C:/codebase/webdriver/chromedriver.exe')


import os
import json

>>>>>>> 64839f0768b66d38aa0aa3ca0fec77fc9ab5c82e

driver.get("http://10.0.0.16:82/")
elem = driver.find_element(By.XPATH, "HTML/BODY")

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

chk = check_exists_by_xpath("HTML/BODY")

assert "No results found." not in driver.page_source

<<<<<<< HEAD
filename ="testresults.png"
delay=3
zoom=100

driver.execute_script(f"document.body.style.zoom='{zoom}%'")
time.sleep(delay)
driver.save_screenshot(filename)
os.system("/usr/bin/imgur/imgur.sh testresults.png")

=======
>>>>>>> 64839f0768b66d38aa0aa3ca0fec77fc9ab5c82e
if chk == True :
    print("The test was successful!")

else: 
    print("The test failed")


driver.quit()
