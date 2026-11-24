import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8091")
ROLL_NUMBER = "FA23-BSE-090"


@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-data-dir=/tmp/chrome-profile")
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    yield drv
    drv.quit()


def test_page_title_has_roll_number(driver):
    driver.get(BASE_URL)
    assert driver.title == "CI/CD Assignment 3 - " + ROLL_NUMBER


def test_main_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading")
    assert heading.text == "Cloud Computing CI/CD Assignment"


def test_name_and_roll_number_shown(driver):
    driver.get(BASE_URL)
    assert driver.find_element(By.ID, "student").text == "Name: Sufian Siddique"
    assert driver.find_element(By.ID, "roll").text == "Roll number: " + ROLL_NUMBER


def test_button_shows_message(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Pipeline")
    )
    assert driver.find_element(By.ID, "message").text == "Pipeline deployment successful!"


def test_text_box_input_is_displayed(driver):
    driver.get(BASE_URL)
    box = driver.find_element(By.ID, "text-input")
    box.send_keys("Hello from Selenium")
    driver.find_element(By.ID, "submit-btn").click()
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "output"), "You entered")
    )
    assert driver.find_element(By.ID, "output").text == "You entered: Hello from Selenium"
    driver.save_screenshot("screenshot.png")
