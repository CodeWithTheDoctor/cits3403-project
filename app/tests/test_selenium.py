import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


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

    assert "test" in driver
    print(driver)
    title = "Akari"
    assert title in driver.title

    sleep(5)

    driver.find_element(By.ID, "addbutton").click()
    sleep(5)

    sleep(2)
    driver.close()
