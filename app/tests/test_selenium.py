import pytest
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def test_lambdatest_todo_app():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # chrome_driver = webdriver.Chrome(
    #     "/home/timothy/code/cits3403/cits3403-project/webdrivers"
    # )

    driver.get("https://flask_te")
    driver.maximize_window()

    driver.find_element_by_name("li1").click()
    driver.find_element_by_name("li2").click()

    title = "Sample page - lambdatest.com"
    assert title == driver.title

    sample_text = "Happy Testing at LambdaTest"
    email_text_field = driver.find_element_by_id("sampletodotext")
    email_text_field.send_keys(sample_text)
    sleep(5)

    driver.find_element_by_id("addbutton").click()
    sleep(5)

    output_str = driver.find_element_by_name("li6").text
    sys.stderr.write(output_str)

    sleep(2)
    driver.close()
