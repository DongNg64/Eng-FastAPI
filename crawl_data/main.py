from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from secret import person  
import time

options = webdriver.ChromeOptions() 
options.add_argument("--window-size=1920,1080")
options.add_argument(r"user-data-dir=C:\Users\boot.ai\AppData\Local\Google\Chrome\User Data\Profile 1") #Path to your chrome profile
options.add_argument("--profile-directory=Default")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

driver.get("https://study4.com/")

driver.find_element(By.CSS_SELECTOR, "a[href='/login/']").click()
driver.find_element(By.CSS_SELECTOR, "span[data-href='/oauth/login/google-oauth2/?next=']").click()
email, password = person()
driver.find_element(By.CSS_SELECTOR, "input").send_keys(email)
driver.find_element(By.CSS_SELECTOR, "input").send_keys(Keys.ENTER)
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "input").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "input").send_keys(Keys.ENTER)
time.sleep(5)
