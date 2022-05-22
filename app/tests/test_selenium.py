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

    sleep(2)
    # assert "test" in driver

    sleep(5)
    driver.get("http://127.0.0.1:5000/auth/login")
    assert (
        "Please log in" in driver.find_element(By.CLASS_NAME, "alert alert-danger").text
    )
    driver.find_element(By.ID, "username").send_keys("david")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "submit").click()

    User.query.filter_by(username="john").first().delete()
    db.session.commit()

    sleep(2)
    driver.close()
