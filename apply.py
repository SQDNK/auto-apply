from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time

def tryBS():
    URL = "https://homeoffice-na-urbn.icims.com/jobs/14391/job?utm_source=hiringcafe_integration&iis=Job+Board&iisn=HiringCafe&mobile=false&width=1249&height=500&bga=true&needsRedirect=false&jan1offset=-420&jun1offset=-360"
    #r = requests.get(URL)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    topLevel = soup.find_all("span")
    #print(topLevel)
    for el in topLevel:
        for iframe in el.find_all("iframe"):
            #WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it(iframe['id']))

            url = iframe.attrs['src']
            page = requests.get(url).content
            soup = BeautifulSoup(page, 'html.parser')

            span = soup.find_all("span")
            print(span)

            #driver.switch_to.frame(iframe['id'])

            #soup needs to be reset
            #leave frame
            driver.switch_to.default_content()

    driver.quit()

def trySel():
    driver = webdriver.Firefox()
    #driver.get(URL)
    #assert "Python" in driver.title

    inputsByTag = driver.find_elements(By.TAG_NAME, "input")
    print(inputsByTag)
    inputsByX = driver.find_elements(By.XPATH, "//input[@type='button']")
    print(inputsByX)

    inputsByText = driver.find_elements(By.XPATH, "//*[contains(text(), 'Apply')]") #must use ' instead of ""
    print(inputsByText)

    #elem = driver.find_element(By.ID, "apply")
    #elem.clear()
    #elem.send_keys("pycon")
    #elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

tryBS()