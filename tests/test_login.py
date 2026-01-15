from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytest
import time
import os

URL = "http://localhost/quiz/login.php"
SUCCESS_PAGE = "index.php"
SCREENSHOT_DIR = "screenshots"


def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


@pytest.fixture
def driver():
    driver = setup_driver()
    yield driver
    driver.quit()


def take_screenshot(driver, test_name, status):
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

    filename = f"{SCREENSHOT_DIR}/{test_name}_{status}.png"
    driver.save_screenshot(filename)


# ==========================================
# FT_001 – Login Valid (PASS)
# ==========================================
def test_FT_001_login_valid(driver, request):
    driver.get(URL)

    driver.find_element(By.NAME, "username").send_keys("beer")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(2)

    if SUCCESS_PAGE in driver.current_url.lower():
        take_screenshot(driver, request.node.name, "PASS")
        assert True
    else:
        take_screenshot(driver, request.node.name, "FAIL")
        assert False


# ==========================================
# FT_002 – Login Tidak Valid (PASS)
# ==========================================
def test_FT_002_login_invalid(driver, request):
    driver.get(URL)

    driver.find_element(By.NAME, "username").send_keys("salah")
    driver.find_element(By.NAME, "password").send_keys("salah")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)

    # PASS jika TIDAK masuk ke index.php
    if SUCCESS_PAGE not in driver.current_url.lower():
        take_screenshot(driver, request.node.name, "PASS")
        assert True
    else:
        take_screenshot(driver, request.node.name, "FAIL")
        assert False


# ==========================================
# FT_003 – Login Kolom Kosong (PASS)
# ==========================================
def test_FT_003_login_empty(driver, request):
    driver.get(URL)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    if SUCCESS_PAGE not in driver.current_url.lower():
        take_screenshot(driver, request.node.name, "PASS")
        assert True
    else:
        take_screenshot(driver, request.node.name, "FAIL")
        assert False


# ==========================================
# FT_008 – SQL Injection Login (PASS)
# ==========================================
def test_FT_008_login_sql_injection(driver, request):
    driver.get(URL)

    driver.find_element(By.NAME, "username").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)

    if SUCCESS_PAGE not in driver.current_url.lower():
        take_screenshot(driver, request.node.name, "PASS")
        assert True
    else:
        take_screenshot(driver, request.node.name, "FAIL")
        assert False
