from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



driver = webdriver.Firefox()
urlString = "https://homeoffice-na-urbn.icims.com/jobs/14391/job?utm_source=hiringcafe_integration&iis=Job+Board&iisn=HiringCafe&mobile=false&width=1249&height=500&bga=true&needsRedirect=false&jan1offset=-420&jun1offset=-360"
driver.get(urlString)
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
#driver.close()