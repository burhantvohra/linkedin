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
import pickle
import os

class LinkedInAutomation:
    def __init__(self, username, password, search_url, comments_file, output_file='tracking_output.xlsx', cookie_file='linkedin_cookies.pkl'):
        self.username = username
        self.password = password
        self.search_url = search_url
        self.comments = self.load_comments(comments_file)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.start_time = time.time()
        self.output_file = output_file
        self.actions_log = []
        self.cookie_file = cookie_file  # Add cookie_file here

        self.existing_log = self.load_existing_log()
        # if not os.path.exists(self.output_file):
        #     self.initialize_output_file()

    def load_existing_log(self):
        # Load the tracking output file if it exists, else return an empty DataFrame
        if os.path.exists(self.output_file):
            return pd.read_excel(self.output_file)
        else:
            return pd.DataFrame(columns=['Action', 'Post URL', 'User', 'Comment', 'Timestamp'])
    
    def post_already_processed(self, post_url, action):
        # Check if the post URL and action already exist in the log
        return not self.existing_log[(self.existing_log['Post URL'] == post_url) & (self.existing_log['Action'] == action)].empty
    
    def log_action(self, action, post_url, user, comment=""):
        # Log the actions taken by the bot (like, comment, repost)
        self.actions_log.append({
            'Action': action,
            'Post URL': post_url,
            'User': user,
            'Comment': comment,
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })

    def save_cookies(self):
        with open(self.cookie_file, 'wb') as file:
            pickle.dump(self.driver.get_cookies(), file)
        print("Cookies saved.")

    def load_cookies(self):
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print("Cookies loaded.")
            return True
        return False
    
    def initialize_output_file(self):
        # Create the tracking output file
        df = pd.DataFrame(columns=['Action', 'Post URL', 'User', 'Comment', 'Timestamp'])
        df.to_excel(self.output_file, index=False)
    
    def save_log_to_file(self):
        # Save the log to the Excel file
        df = pd.DataFrame(self.actions_log)
        if os.path.exists(self.output_file):
            existing_df = pd.read_excel(self.output_file)
            df = pd.concat([existing_df, df], ignore_index=True)
        df.to_excel(self.output_file, index=False)

    def is_internet_connected(self, url='http://www.google.com/', timeout=5):
        try:
            requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    def wait_for_internet(self):
        while not self.is_internet_connected():
            print("No internet connection. Retrying in 10 seconds...")
            time.sleep(10)
        print("Internet connected.")

    def load_comments(self, file_path):
        comments_df = pd.read_excel(file_path)
        return comments_df['Comments'].tolist()

    def get_random_comment(self):
        return random.choice(self.comments)

    def login(self):
        # Check if cookies exist and try to load them
        self.driver.get('https://www.linkedin.com')
        if self.load_cookies():
            # Refresh after loading cookies to see if session is valid
            self.driver.refresh()
            time.sleep(3)
            # Verify if the session is valid by checking if it redirects to the LinkedIn feed or profile
            if "feed" in self.driver.current_url:
                print("Logged in using cookies.")
                return

        # If no cookies or session invalid, perform login
        self.driver.get('https://www.linkedin.com/login')
        self.driver.maximize_window()
        email_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')

        email_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)
        input("Please complete the 2FA and press Enter to continue...")

        # Save cookies after logging in successfully
        self.save_cookies()

    # def login(self):
    #     self.driver.get('https://www.linkedin.com/login')
    #     self.driver.maximize_window()
    #     email_field = self.driver.find_element(By.ID, 'username')
    #     password_field = self.driver.find_element(By.ID, 'password')

    #     email_field.send_keys(self.username)
    #     password_field.send_keys(self.password)
    #     password_field.send_keys(Keys.RETURN)

    #     time.sleep(10)
    #     # input("Please complete the 2FA and press Enter to continue...")

    def navigate_to_search(self):
        self.driver.get(self.search_url)
        time.sleep(5)

    def repost_all_posts(self):
        try:
            repost_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@class, "social-reshare-button")]')

            for repost_button in repost_buttons:
                try:
                    print("Clicking on repost button")
                    self.driver.execute_script("arguments[0].click();", repost_button)
                    time.sleep(10)

                    repost_option = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[text()="Repost"]/ancestor::div[@role="button"]'))
                    )
                    if time.time() - self.start_time >= 120:
                        print("Sleeping for 1 minute...")
                        time.sleep(60)
                        self.start_time = time.time()

                    time.sleep(5)
                    repost_option.click()
                    post_url = self.driver.current_url
                    print("Repost option clicked")
                    time.sleep(2)
                    print("Post successfully reposted")
                    self.log_action('Repost', post_url, "N/A")
                    time.sleep(5)

                except Exception as e:
                    print(f"Error reposting post: {e}")
                    continue

        except Exception as e:
            print(f"Error finding repost buttons: {e}")

    def comment_on_all_posts(self):
        try:
            time.sleep(5)
            comment_buttons = self.driver.find_elements(By.XPATH, '//button[@aria-label="Comment"]')
            time.sleep(5)
            for comment_button in comment_buttons:
                try:
                    if time.time() - self.start_time >= 120:
                        print("Sleeping for 1 minute...")
                        time.sleep(60)
                        self.start_time = time.time()

                    comment_button.click()
                    time.sleep(5)

                    comment_box = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@data-placeholder="Add a comment…"]'))
                    )
                    time.sleep(5)
                    comment_text = self.get_random_comment()
                    comment_box.send_keys(comment_text)
                    time.sleep(10)

                    post_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "comments-comment-box__submit-button")]'))
                    )
                    time.sleep(5)
                    self.driver.execute_script("arguments[0].click();", post_button)
                    post_url = self.driver.current_url
                    print(f"Commented on post with comment: {comment_text}")
                    self.log_action('Comment', post_url, "N/A", comment_text)
                    time.sleep(15)

                except Exception as e:
                    print(f"Error commenting on post: {e}")
                    continue

        except Exception as e:
            print(f"Error finding comment buttons: {e}")

    def click_like_buttons(self):
        try:
            like_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Like")]')
            time.sleep(5)

            for button in like_buttons:
                post_url = self.driver.current_url  # Fetch post URL

                # Check if this post has already been liked
                if self.post_already_processed(post_url, 'Like'):
                    print(f"Post already liked: {post_url}. Skipping...")
                    continue
                try:
                    if time.time() - self.start_time >= 120:
                        print("Sleeping for 1 minute...")
                        time.sleep(60)
                        self.start_time = time.time()

                    button.click()
                    time.sleep(5)
                    post_url = self.driver.current_url
                    print(f"Liked post: {post_url}")
                    self.log_action('Like', post_url, "N/A")
                    time.sleep(5)

                except Exception as e:
                    print(f"Error clicking Like button: {e}")
                    continue

        except Exception as e:
            print(f"Error finding Like buttons: {e}")

    def start_automation(self):
        self.wait_for_internet()
        self.login()
        self.navigate_to_search()

        while True:
            time.sleep(3)
            self.click_like_buttons()
            # self.repost_all_posts()
            # self.comment_on_all_posts()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            self.save_log_to_file()

    def quit(self):
        self.save_log_to_file()
        self.driver.quit()


username = 'burhancamp@yahoo.com'
password = 'Taher@1234'
search_url = 'https://www.linkedin.com/search/results/content/?keywords=architecture%20design&origin=SWITCH_SEARCH_VERTICAL'
comments_file = 'Linked_comment.xlsx'

linkedin = LinkedInAutomation(username, password, search_url, comments_file)
linkedin.start_automation()
linkedin.quit()
