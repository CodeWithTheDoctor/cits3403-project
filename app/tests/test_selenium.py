import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from app.models import User
from app import db


def test_selenium(app_ctx):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000/auth/register")
    driver.maximize_window()

    # Test register user with existing user
    driver.find_element(By.ID, "username").send_keys("test_user")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "password2").send_keys("password")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "submit").click()

    user_span = driver.find_elements(By.TAG_NAME, "span")[1].text

    assert user_span == "[Please use a different username]"

    sleep(1)

    # Test user can login
    driver.get("http://127.0.0.1:5000/auth/login")
    driver.find_element(By.ID, "username").send_keys("david")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "submit").click()

    result = driver.find_element(By.ID, "startButton").text

    assert result == "Start"

    driver.get("http://127.0.0.1:5000/auth/logout")

    login = driver.find_elements(By.TAG_NAME, "h1")

    assert login[1].text == "Sign In"

    sleep(1)
    driver.close()
