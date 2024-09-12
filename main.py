import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def is_internet_connected(url='http://www.google.com/', timeout=5):
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def wait_for_internet():
    while not is_internet_connected():
        print("No internet connection. Retrying in 10 seconds...")
        time.sleep(10)
    print("Internet connected.")

def scroll_page(driver):
    driver.execute_script("window.scrollBy(0, 100);")

def main():
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login')
    driver.maximize_window()
    email = driver.find_element(By.ID, 'username')
    email.send_keys('burhancamp@yahoo.com')

    password = driver.find_element(By.ID, 'password')
    password.send_keys('B@b9925179281')
    driver.find_element(By.XPATH, '//*[@type="submit"]').click()
    time.sleep(5)
    start_time = time.time()

    try:
        while True:
            wait_for_internet()
            scroll_page(driver)
            print("Scrolled down 100px.")
            time.sleep(3)

            # Every 2 min , sleep for 1 minutes
            if time.time() - start_time >= 120:  # 3600 seconds = 1 hour
                print("Sleeping for 1 minutes...")
                time.sleep(60)
                start_time = time.time()

    except KeyboardInterrupt:
        print("Script interrupted by user.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()