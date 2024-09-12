from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import pandas as pd
import time

def repost_all_posts():
    try:
        # Find all repost buttons on the page
        repost_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "social-reshare-button")]')

        # Loop through each repost button
        for repost_button in repost_buttons:
            try:
                print("Clicking on repost button")
                driver.execute_script("arguments[0].click();", repost_button)
                time.sleep(2)  # Wait for the repost options to load

                # Wait for and click the Repost option
                repost_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Repost"]/ancestor::div[@role="button"]'))
                )
                repost_option.click()
                print("Repost option clicked")
                time.sleep(2)

                print("Post successfully reposted")
                time.sleep(5)  # Add delay to mimic human behavior before moving to the next post

            except Exception as e:
                print(f"Error reposting post: {e}")
                continue
    except Exception as e:
        print(f"Error finding repost buttons: {e}")


username = 'burhancamp@yahoo.com'
password = 'B@b9925179281'
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# chrome_executable_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# chromedriver_path = r'D:\chromedriver.exe'
# chrome_options = Options()
# chrome_options.binary_location = chrome_executable_path
# service = Service(executable_path=chromedriver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.maximize_window()
email_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

email_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
time.sleep(5)
input("Please complete the 2FA and press Enter to continue...")
time.sleep(5)
driver.get('https://www.linkedin.com/search/results/content/?keywords=architecture%20design&origin=SWITCH_SEARCH_VERTICAL&searchId=b64ccf5e-dec4-4622-8c54-0f96fa599b82')

time.sleep(5)
wait = WebDriverWait(driver, 10)
start_time = time.time()  
while True:
    time.sleep(3)
    repost_all_posts()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

driver.quit()
