from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions() 
options.add_argument("--start-maximized")
options.add_argument('--no-sandbox')
options.add_argument("user-data-dir=C:\\Users\\boot.ai\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 1')
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options)

driver.get("https://study4.com/")

# login
# driver.find_element(By.CSS_SELECTOR, "a[href='/login/']").click()
# driver.find_element(By.CSS_SELECTOR, "span[data-href='/oauth/login/google-oauth2/?next=']").click()
# driver.find_element(By.CLASS_NAME, "d2laFc").click()

driver.find_element(By.CSS_SELECTOR, "a[href='/tests/']").click()
driver.find_element(By.CSS_SELECTOR, "a[href='/tests/toeic/']").click()
driver.find_element(By.CSS_SELECTOR, "a[href='/tests/4590/ets-23-toeic-test-1/']").click()
driver.find_element(By.CSS_SELECTOR, "a[href='/tests/4590/ets-23-toeic-test-1/results/8860453/']").click()
driver.find_element(By.CSS_SELECTOR, "a[href='/tests/4590/ets-23-toeic-test-1/results/8860453/details/']").click()
                                        href="/tests/4590/ets-23-toeic-test-1/results/8860453/details/"
# driver.find_element(By.CLASS_NAME, "btn btn-sm btn-sky").click()

