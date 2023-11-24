from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
# element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/tests/4590/ets-23-toeic-test-1/results/8860453/details/']")))
# ActionChains(driver).move_to_element(element).click()
driver.execute_script("document.querySelector(`.lg-container > .row > .col-md-9 > .contentblock > h4 > a`).click()")

# part 1
# scroll to end
driver.execute_script("Array.from(document.querySelectorAll('.context-image')).forEach((item,index) => { setTimeout(() => {  item.scrollIntoView()   }, 400 * index)})")
time.sleep(5)
# get image
images = driver.execute_script("return Array.from(document.querySelectorAll('.lazyel.entered.loaded')).map(item => item.src)")
# click 'Hiện transcript'
driver.execute_script(f"return Array.from(document.querySelectorAll('.tab-content .test-questions-wrapper > .context-wrapper > .context-content.context-transcript.text-highlightable > p > a')).slice(0, {len(images)}).forEach(item=>item.click())")
time.sleep(5)
# get questions
driver.execute_script("return Array.from(document.querySelectorAll('.tab-content .test-questions-wrapper > .context-wrapper > .context-content.context-transcript.text-highlightable > .collapse.show')).map(item => item.innerText)")
# get answers
driver.execute_script("return Array.from(document.querySelectorAll('.tab-content .test-questions-wrapper > .question-wrapper > .question-content.text-highlightable > .mt-2.text-success')).map(item => item.innerText).filter(item => !item.includes('\\n'))")

# click next button
driver.find_element(By.XPATH, "").click()