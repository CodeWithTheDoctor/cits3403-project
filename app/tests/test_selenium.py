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


def test_lambdatest_todo_app(app_ctx):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://127.0.0.1:5000/auth/register")
    driver.maximize_window()

    # Test register user
    driver.find_element(By.ID, "username").send_keys("john")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "password2").send_keys("password")
    driver.find_element(By.ID, "email").send_keys("john@example.com")
    driver.find_element(By.ID, "submit").click()

    sleep(1)
    # assert "test" in driver

    sleep(1)
    driver.get("http://127.0.0.1:5000/auth/login")
    driver.find_element(By.ID, "username").send_keys("david")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "submit").click()

    User.query.filter_by(username="john").first().delete()
    db.session.commit()

    sleep(1)
    driver.close()
