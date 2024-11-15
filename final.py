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
import pyperclip

class LinkedInAutomation:
    def __init__(self, username, password, keyword, comments_file, output_file='tracking_output.xlsx', cookie_file='linkedin_cookies.pkl'):
        self.username = username
        self.password = password
        self.keyword = keyword
        self.search_url = f'https://www.linkedin.com/search/results/content/?keywords={keyword.replace(" ", "%20")}&origin=SWITCH_SEARCH_VERTICAL'
        self.comments = self.load_comments(comments_file)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.start_time = time.time()
        self.output_file = output_file
        self.actions_log = []
        self.existing_log = self.load_existing_log()
        self.cookie_file = cookie_file  # Add cookie_file here
        self.running_time = 1000
        self.sleeping_time = 60

    def load_existing_log(self):
        # Load the tracking output file if it exists, else return an empty DataFrame
        if os.path.exists(self.output_file):
            return pd.read_excel(self.output_file)
        else:
            return pd.DataFrame(columns=['Action', 'Post URL', 'User', 'Comment', 'Timestamp'])
    
    def post_already_processed(self, post_url, action):
        # Check if the post URL and action already exist in the log
        return not self.existing_log[(self.existing_log['Post URL'] == post_url) & (self.existing_log['Action'] == action)].empty
    
    # def save_cookies(self):
    #     with open(self.cookie_file, 'wb') as file:
    #         pickle.dump(self.driver.get_cookies(), file)
    #     print("Cookies saved.")
    
    def save_cookies(self): 
        cookies = self.driver.get_cookies()
        with open("linkedin_cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
        print("Cookies saved successfully.")
    
    def load_cookies(self):
        if os.path.exists("linkedin_cookies.pkl"):
            with open("linkedin_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print("Cookies loaded successfully.")
            return True
        return False

    # def load_cookies(self):
    #     if os.path.exists(self.cookie_file):
    #         with open(self.cookie_file, 'rb') as file:
    #             cookies = pickle.load(file)
    #             for cookie in cookies:
    #                 self.driver.add_cookie(cookie)
    #         print("Cookies loaded.")
    #         return True
    #     return False

    def initialize_output_file(self):
        # Create the tracking output file
        df = pd.DataFrame(columns=['Action', 'Post URL', 'User', 'Comment', 'Timestamp'])
        df.to_excel(self.output_file, index=False)
    
    def log_action(self, action, post_url, user, comment=""):
        # Log the actions taken by the bot (like, comment, repost)
        self.actions_log.append({
            'Action': action,
            'Post URL': post_url,
            'User': user,
            'Comment': comment,
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
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
        # comments_df = pd.read_excel(file_path)
        comments_df = pd.read_csv(file_path, delimiter='\t')
        return comments_df['Comments'].tolist()
    
    def get_random_comment(self):
        return random.choice(self.comments)
    
    # def login(self):
    #     # Check if cookies exist and try to load them
    #     self.driver.get('https://www.linkedin.com')
    #     self.driver.maximize_window()
    #     if self.load_cookies():
    #         # Refresh after loading cookies to see if session is valid
    #         self.driver.refresh()
    #         time.sleep(3)
    #         # Verify if the session is valid by checking if it redirects to the LinkedIn feed or profile
    #         if "feed" in self.driver.current_url:
    #             print("Logged in using cookies.")
    #             return

    #     # If no cookies or session invalid, perform login
    #     self.driver.get('https://www.linkedin.com/login')
    #     self.driver.maximize_window()
    #     email_field = self.driver.find_element(By.ID, 'username')
    #     password_field = self.driver.find_element(By.ID, 'password')

    #     email_field.send_keys(self.username)
    #     password_field.send_keys(self.password)
    #     password_field.send_keys(Keys.RETURN)

    #     try:
    #         # Wait up to 40 seconds for the 2FA code entry (if applicable)
    #         WebDriverWait(self.driver, 40).until(
    #             EC.url_contains("feed")  # Adjust if the post-login URL might vary
    #         )
    #         print("Logged in successfully.")
    #     except:
    #         print("2FA code entry timeout. Exiting.")
    #         self.driver.quit()
    #         return


    #     time.sleep(5)
    #     # input("Please complete the 2FA and press Enter to continue...")

    #     # Save cookies after logging in successfully
    #     self.save_cookies()

    def login(self):
        # Load LinkedIn main page
        self.driver.get('https://www.linkedin.com')
        self.driver.maximize_window()

        # Check if cookies exist and try to load them
        if self.load_cookies():
            # Refresh to see if the session is still valid
            self.driver.refresh()
            time.sleep(3)
            
            # Verify if the session is valid
            if "feed" in self.driver.current_url or "profile" in self.driver.current_url:
                print("Logged in using cookies.")
                return
            else:
                print("Cookies loaded but session is invalid. Proceeding to manual login.")
        else:
            print("No valid cookies found. Logging in manually.")

        # If cookies do not exist or session is invalid, perform manual login
        self.driver.get('https://www.linkedin.com/login')
        email_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')

        # Enter username and password
        email_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

        # Wait for 2FA code entry or timeout after 40 seconds
        try:
            # Wait for up to 40 seconds for LinkedIn to redirect to feed/profile (after 2FA entry)
            WebDriverWait(self.driver, 40).until(
                EC.url_contains("feed")  # Adjust if LinkedIn redirects to a different URL upon successful login
            )
            print("Logged in successfully.")
            # Save cookies after successful login
            self.save_cookies()
        except:
            print("2FA code entry timeout. Exiting.")
            self.driver.quit()

    def navigate_to_search(self):
        self.driver.get(self.search_url)
        time.sleep(5)

    def click_like_buttons(self):
        try:
            all_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@aria-label, "Like")]')
            print(f"Total buttons found: {len(all_buttons)}")
            time.sleep(5)
            
            like_buttons = [
                button for button in all_buttons
                if button.is_displayed() and button.is_enabled()
            ]
            print(f"Visible and interactable buttons: {len(like_buttons)}")

            for button in like_buttons:
                # post_url = self.driver.current_url  # Fetch post URL
                try:
                    if time.time() - self.start_time >= self.running_time:
                        print(f"Sleeping for {self.sleeping_time} sec...")
                        time.sleep(self.sleeping_time)
                        self.start_time = time.time()

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(5)
                    
                    self.driver.execute_script("arguments[0].click();", button)
                    # button.click()
                    print("Post liked.")
                    time.sleep(5)
                    # post_url = self.driver.current_url
                    # print(f"Liked post: {post_url}")
                    # self.log_action('Like', post_url, "N/A")
                    # if "Liked" not in button.get_attribute("aria-label"):
                    #     # Click only if it's not already liked
                    #     self.driver.execute_script("arguments[0].click();", button)
                    #     print("Post liked.")
                    #     time.sleep(5)  # Delay between actions
                    # else:
                    #     print("Post already liked. Skipping.")

                except Exception as e:
                    print(f"Error clicking Like button: {e}")
                    continue

        except Exception as e:
            print(f"Error finding Like buttons: {e}")

    def repost_all_posts(self):
        try:
            repost_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@class, "social-reshare-button")]')
            time.sleep(5)

            for repost_button in repost_buttons:
                try:
                    print("Clicking on repost button")
                    self.driver.execute_script("arguments[0].click();", repost_button)
                    time.sleep(3)

                    repost_option = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[text()="Repost"]/ancestor::div[@role="button"]'))
                    )
                    if time.time() - self.start_time >= self.running_time:
                        print(f"Sleeping for {self.sleeping_time} sec...")
                        time.sleep(self.sleeping_time)
                        self.start_time = time.time()

                    repost_option.click()
                    post_url = self.driver.current_url
                    print("Repost option clicked")
                    time.sleep(2)
                    print("Post successfully reposted")
                    self.log_action('Repost', post_url, "N/A")
                    time.sleep(2)

                except Exception as e:
                    print(f"Error reposting post: {e}")
                    continue

        except Exception as e:
            print(f"Error finding repost buttons: {e}")
    
    def comment_on_all_posts(self):
        try:
            comment_buttons = self.driver.find_elements(By.XPATH, '//button[@aria-label="Comment"]')
            time.sleep(5)
            for comment_button in comment_buttons:
                try:
                    if time.time() - self.start_time >= self.running_time:
                        print(f"Sleeping for {self.sleeping_time} sec...")
                        time.sleep(self.sleeping_time)
                        self.start_time = time.time()

                    comment_button.click()
                    time.sleep(3)

                    comment_box = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@data-placeholder="Add a comment…"]'))
                    )
                    time.sleep(5)
                    comment_text = self.get_random_comment()
                    time.sleep(5)
                    comment_box.send_keys(comment_text)
                    time.sleep(3)

                    post_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "comments-comment-box__submit-button")]'))
                    )
                    time.sleep(3)
                    self.driver.execute_script("arguments[0].click();", post_button)
                    post_url = self.driver.current_url
                    print(f"Commented on post with comment: {comment_text}")
                    self.log_action('Comment', post_url, "N/A", comment_text)
                    time.sleep(5)

                except Exception as e:
                    print(f"Error commenting on post: {e}")
                    continue

        except Exception as e:
            print(f"Error finding comment buttons: {e}")

    def click_dot_buttons(self):
        copied_links = set()  # To store unique links and prevent duplicates
        last_processed_index = 0  # Keep track of the last processed post index
        try:
            with open("copied_links.txt", "r") as file:
                copied_links = set(file.read().splitlines())
        except FileNotFoundError:
            print("No previously saved links found. Starting fresh.")

        while True:
            # Find all the "three dots" buttons on the page
            dot_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@class, "feed-shared-control-menu__trigger")]')

            # Process only the new posts loaded after scrolling
            for index in range(last_processed_index, len(dot_buttons)):
                dot_button = dot_buttons[index]
                try:
                    # Scroll to the dot button and click it using JavaScript
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", dot_button)
                    time.sleep(3)
                    self.driver.execute_script("arguments[0].click();", dot_button)
                    time.sleep(3)  # Small delay to ensure dropdown loads

                    # Locate the "Copy link to post" option and click it
                    copy_link_option = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//h5[normalize-space()='Copy link to post']"))
                    )
                    self.driver.execute_script("arguments[0].click();", copy_link_option)
                    time.sleep(3)

                    # Get the copied link from the clipboard
                    copied_link = pyperclip.paste()

                    # Save the link if it hasn't been saved before
                    if copied_link not in copied_links:
                        copied_links.add(copied_link)
                        with open("copied_links.txt", "a") as file:
                            file.write(copied_link + "\n")
                        print("Link copied and saved:", copied_link)

                        self.driver.execute_script(f"window.open('{copied_link}', '_blank');")
                        time.sleep(5)

                        # Switch to the new tab
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        print(f"Opened new tab for: {copied_link}")
                        time.sleep(5)
                        self.click_like_buttons()    
                        # self.repost_all_posts()
                        # self.comment_on_all_posts()
                        time.sleep(10)

                        # Close the new tab
                        self.driver.close()
                        print(f"Closed tab for: {copied_link}")

                        # Switch back to the original tab
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    else:
                        print("Duplicate link skipped:", copied_link)

                    
                    if time.time() - self.start_time >= self.running_time:
                        print(f"Sleeping for {self.sleeping_time} sec...")
                        time.sleep(self.sleeping_time)
                        self.start_time = time.time()
                    

                except Exception as e:
                    print(f"Error clicking dot button or copying link: {e}")
                    continue

            # Update the last processed index to the current count of dot buttons
            last_processed_index = len(dot_buttons)

            # Scroll down to load more posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new posts to load

            # Check if new posts are loaded by comparing the count of dot buttons
            new_dot_buttons = self.driver.find_elements(By.XPATH, '//button[contains(@class, "feed-shared-control-menu__trigger")]')
            if len(new_dot_buttons) <= last_processed_index:
                print("No more new posts found. Stopping.")
                break
        
    def start_automation(self):
        self.wait_for_internet()
        self.login()
        self.navigate_to_search()
    
        while True:
            time.sleep(3)
            self.click_dot_buttons()
            # self.repost_all_posts()
            # self.comment_on_all_posts()
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            self.save_log_to_file()

    def quit(self):
        self.save_log_to_file()
        self.driver.quit()

username = 'burhancamp@yahoo.com'
password = 'Fatema@5252'
# search_url = 'https://www.linkedin.com/search/results/content/?keywords=cricket%20design&origin=SWITCH_SEARCH_VERTICAL' # 'https://www.linkedin.com/feed/'
keyword = "cricket" 
comments_file = 'Linked_comment.txt'
linkedin = LinkedInAutomation(username, password, keyword, comments_file)
linkedin.start_automation()
linkedin.quit()
