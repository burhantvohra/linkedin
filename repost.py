from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import pandas as pd
from datetime import datetime

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.maximize_window()
time.sleep(3)

email = driver.find_element(By.ID, 'username')
email.send_keys('burhancamp@yahoo.com')

password = driver.find_element(By.ID, 'password')
password.send_keys('B@b9925179281')

driver.find_element(By.XPATH, '//*[@type="submit"]').click()


driver.get('https://www.linkedin.com/search/results/all/?keywords=wire%20mesh&origin=AUTO_COMPLETE&searchId=d41270eb-125c-44ed-a4b6-98fb82076ea4&sid=w%3BH&spellCorrectionEnabled=false')
driver.execute_script("window.scrollBy(0,500)", "")

time.sleep(5)
wait = WebDriverWait(driver, 10)

def repost_post():
    try:
        print("Locating repost button")
        repost_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "social-reshare-button")]'))
        )
        repost_button.click()
        print("Repost button clicked")
        time.sleep(2)

        print("Waiting for repost option")
        repost_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Repost"]/ancestor::div[@role="button"]'))
        )
        repost_option.click()
        print("Repost option clicked")
        time.sleep(2)

        print("Reposted post")
    except Exception as e:
        print(f"Error reposting post: {e}")

repost_post()
driver.quit()