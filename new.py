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

comments_df = pd.read_excel('Linked_comment.xlsx')
comments = comments_df['Comments'].tolist()

def get_random_comment():
    return random.choice(comments)

def comment_on_all_posts():
    try:
        time.sleep(5)
        comment_buttons = driver.find_elements(By.XPATH, '//button[@aria-label="Comment"]')
        for comment_button in comment_buttons:
            try:
                comment_button.click()
                time.sleep(5)
                comment_container = comment_button.find_element(By.XPATH, '../../..')
                comment_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-placeholder="Add a comment…"]'))
                )
                print("4")
                time.sleep(5)
                comment_text = get_random_comment()
                comment_box.send_keys(comment_text)
                time.sleep(10)

                post_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "comments-comment-box__submit-button")]'))
                )
                driver.execute_script("arguments[0].click();", post_button) 
                print("6")
                time.sleep(15)

                print(f"Commented on post with comment: {comment_text}")
            except Exception as e:
                print("7")
                print(f"Error commenting on post: {e}")
    except Exception as e:
        print(f"Error finding comment buttons: {e}")

username = 'burhancamp@yahoo.com'
password = 'B@b9925179281'

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.maximize_window()
email_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

email_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
time.sleep(5)
driver.get('https://www.linkedin.com/search/results/content/?keywords=architecture%20design&origin=SWITCH_SEARCH_VERTICAL&searchId=b64ccf5e-dec4-4622-8c54-0f96fa599b82')

time.sleep(5)
wait = WebDriverWait(driver, 10)
start_time = time.time()  
while True:
    time.sleep(3)
    comment_on_all_posts()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

driver.quit()
