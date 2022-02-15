from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
#set chromodriver.exe path
install_chrome = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=install_chrome)
driver.implicitly_wait(0.5)
#launch URL
driver.get("https://accounts.google.com/")
#identify element
m = driver.find_element_by_link_text("Help")
m.click()
#obtain parent window handle
p= driver.window_handles[0]
#obtain browser tab window
c = driver.window_handles[1]
#switch to tab browser
driver.switch_to.window(c)
print("Page title :")
print(driver.title)
#close browser tab window
driver.close()
#switch to parent window
driver.switch_to.window(p)
print("Current page title:")
print(driver.title)
#close browser parent window
time.sleep(10)
driver.quit()