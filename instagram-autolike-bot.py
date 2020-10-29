# Importing selenium

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


import time

# setting up web driver
chrome = webdriver.Chrome('C:/Users\Aqib Ilyas/Downloads/chromedriver_win32/chromedriver.exe')  # Path to chrome driver

chrome.get('https://www.instagram.com/')


def login():
    # logging in
    print("Enter your username")
    username = input()

    print("Enter your password")
    password = input()
    print("Enter username of profile or #tag you want to open")
    name = input()
    username_path = WebDriverWait(chrome, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_path = WebDriverWait(chrome, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username_path.clear()
    password_path.clear()
    username_path.send_keys(username)
    password_path.send_keys(password)
    WebDriverWait(chrome, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    remove_notifications()
    search_user(name)


def remove_notifications():
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


def search_user(name):
    searchbox = WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()
    time.sleep(2)
    searchbox.send_keys(name)
    time.sleep(2)

    searchbox.send_keys(Keys.ENTER)
    time.sleep(1)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)


def scroll_down():
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = chrome.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def open_first_post():
    # Opening first post
    time.sleep(2)
    try:
        chrome.find_element_by_xpath("(//div[@class=\"eLAPa\"]//parent::a)[1]").click()
        return True
    except NoSuchElementException:
        print("This page does not have any posts.")
        return False


def like_all_posts():
    # Open the first picture
    has_post = open_first_post()

    while has_post:
        like_post()
        # Updating value of has_picture
        has_post = next_post()

    # Closing the post popup when all posts have been liked
    try:
        chrome.find_element_by_xpath("//button[@class=\"ckWGn\"]").click()
        print("All posts have been liked")
    except:
        print("Couldn't close the post")


def like_post():
    time.sleep(1)
    like = chrome.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button')

    # you can find the like button using class name too
    time.sleep(2)
    like.click()  # clicking the like button


def next_post():
    # Getting next post
    time.sleep(2)
    next_button = "//a[text()=\"Next\"]"
    try:
        chrome.find_element_by_xpath(next_button).click()
        return True
    except NoSuchElementException:
        print("User has no more posts")
        return False


# Calling functions
login()
scroll_down()
like_all_posts()
