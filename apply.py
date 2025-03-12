from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import requests
from bs4 import BeautifulSoup
import time
import os 
import re
            
def findIFrame(soup):
    # if iframe nested in span, can only access it from span? 
    spans = soup.find_all("span")
    
    # DEBUG
    print(spans)
    for span in spans:
        print(span.find_all("iframe"))
    #
    
    for span in spans:
        for iframe in span.find_all("iframe"):
            # try first frame?
            return iframe
    return None

def switchToFrame(iframe, driver):
    #WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it(iframe['id']))
    url = iframe.attrs['src']
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    driver.switch_to.frame(driver.find_element(By.ID, iframe['id']))
    
    return soup

def findEle(soup, tag, str):
    # TODO: list other searches 
    eleStr = soup.find(tag, string=re.compile(str, re.IGNORECASE))
    eleAttr = soup.find(tag, type=str)
    return eleStr or eleAttr or None

#TODO: method signature 
def click(driver, soupEle):
    for key in soupEle.attrs:
        if key == "class":
            driver.execute_script("arguments[0].click();", driver.find_element(By.CLASS_NAME, soupEle['class'][0]))
            return
        if key == "id":
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, soupEle['id']))
            return 
            
def sendKeys(driver, soupEle, content):
    for key in soupEle.attrs:
        if key == "class":
            driver.find_element(By.CLASS_NAME, soupEle['class'][0]).send_keys(content)
            return
        if key == "id":
            driver.find_element(By.ID, soupEle['id']).send_keys(content)
            return 
        
def setSoup(driver, wait, uniqueEle):
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, uniqueEle)))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def stringExists(str, el):
    #TODO: 1) you can either list out the values of the dict OR get key, value pair 
    if str in el.attrs.values():
        return True
    return False

def fillForm(driver, inputs):
    #TODO: some checks may not be unique 
    #TODO: respond to errors sent by website
    for el in inputs:
        if el['type'] == "file" and stringExists("resume", el):
            upload_resume = os.path.abspath("Desktop/Holly_Liu_Resume.pdf")
            el.send_keys(upload_resume)
            
        if stringExists("email", el):
            sendKeys(driver, el, "hsliu.021@gmail.com")
            
        if stringExists("password", el) or stringExists("verify", el):
            sendKeys(driver, el, "!Ducked012345")
            
        if stringExists("checkbox", el):
            click(driver, el)
            
def workday():
    URL = "https://uasys.wd5.myworkdayjobs.com/en-US/uasys/login?redirect=%2Fen-US%2Fuasys%2Fjob%2FFayetteville%2FTechnology-Solutions-Specialist_R0068543%2Fapply%2FautofillWithResume"
    
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(URL)
    soup = setSoup(driver, wait, "form")
        
    soupEle = findEle(soup, "button", "create")    
    if soupEle:
        click(driver, soupEle)
    else:
        print("Did not find element")
        
    soup = setSoup(driver, wait, "form") #TODO: this might check for old form
    
    # TODO: 1) check for specific elements to fill out, known beforehand b/c workday follows same format OR
    # 2) check for all inputs
    fillForm(driver, soup.find_all("input"))
    soupEle = findEle(soup, "*", "create")
    if soupEle:
        click(driver, soupEle)
    else:
        print("Did not find element")

def tryBS():
    oldURL = "https://homeoffice-na-urbn.icims.com/jobs/14391/job?utm_source=hiringcafe_integration&iis=Job+Board&iisn=HiringCafe&mobile=false&width=1249&height=500&bga=true&needsRedirect=false&jan1offset=-420&jun1offset=-360"
    #r = requests.get(URL)
    URL = "https://uasys.wd5.myworkdayjobs.com/en-US/uasys/login?redirect=%2Fen-US%2Fuasys%2Fjob%2FFayetteville%2FTechnology-Solutions-Specialist_R0068543%2Fapply%2FautofillWithResume"

    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')
    
    wait = WebDriverWait(driver, 10)

    iframe = findIFrame(soup)
    if iframe: 
        soup = switchToFrame(iframe, driver)
    
    #TODO: not all elements have "button" in class attribute, or even a class attribute 
    apply_window = driver.current_window_handle
    for el in soup.select('*[class*="Button"]'): #also check for href
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, el['class'][0]))).click() #clean up
        break
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("should have entered consent page")
            
    iframe = findIFrame(soup)
    if iframe: 
        soup = switchToFrame(iframe, driver)
        
    #inputs = driver.find_elements(By.XPATH, "//form")
    
    # so, we could just assume there is one form per page
    # TODO: checking if "email" is in el.attrs.items() does something weird 
    inputs = soup.form.find_all("input") 
    for el in inputs:
        if el['type'] == "email":
            driver.find_element(By.ID, el['id']).send_keys("hsliu.021@gmail.com")
        elif el['type'] == "checkbox":
            # click on the input or the label OR both?? 
            check = driver.find_element(By.ID, el['id'])
            driver.execute_script("arguments[0].click();", check)
        elif el['type'] == "submit":
            # assume necessary inputs have already run 
            wait.until(EC.element_to_be_clickable((By.ID, el['id'])))
            driver.execute_script("arguments[0].click();", driver.find_element(By.ID, el['id']))
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "*[type='file' i]")))
            
            break 
        
    print("should have entered candidate profile page")
            
    # TODO: re-format for modularity
    
    # this might be a new iframe
    iframe = findIFrame(soup)
    if iframe:
        print("hello")
        soup = switchToFrame(iframe, driver)
        
    #print(driver.page_source)
        
    # specific wait after submitting a form 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "*[type='file' i]")))
        
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    inputs = soup.form.find_all("input") 
    print(inputs)
    fillForm(inputs)
    
    '''  
    wait.until(EC.number_of_windows_to_be(2))
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != apply_window:
            driver.switch_to.window(window_handle)
            break
    '''

    #soup needs to be reset
    #leave frame
    #driver.switch_to.default_content()

    #driver.quit()

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

if __name__ == "__main__":
    workday()