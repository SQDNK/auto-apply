from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("https://austincc.wd1.myworkdayjobs.com/external/job/Highland-Business-Center/E3-Alliance-Software-Developer_R-7172")
#assert "Python" in driver.title

elem = driver.find_element(By.ID, "apply")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
#driver.close()