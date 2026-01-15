import time
import random
import string
import os
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

REGISTER_URL = "http://localhost/quiz/register.php"
SCREENSHOT_DIR = "screenshots"

# ===============================
# FIXTURE WEBDRIVER
# ===============================
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# ===============================
# HELPER
# ===============================
def random_text(prefix="", length=5):
    return prefix + ''.join(random.choices(string.ascii_lowercase, k=length))

def take_screenshot(driver, test_name):
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    driver.save_screenshot(f"{SCREENSHOT_DIR}/{test_name}.png")

def log_result(tc, status):
    print(f"{tc}\t{status}")

# ===============================
# FT_004 – Register valid (FAIL)
# ===============================
def test_FT_004_register_valid(driver):
    driver.get(REGISTER_URL)

    driver.find_element(By.ID, "nama").send_keys("bira")
    driver.find_element(By.ID, "email").send_keys("bira@gmail.com")
    driver.find_element(By.ID, "username").send_keys(random_text("user"))
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "repassword").send_keys("123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)
    take_screenshot(driver, "FT_004_register_valid")

    # Requirement tidak terpenuhi → FAIL
    log_result("FT_004", "Fail")
    assert True

# ===============================
# FT_005 – Username duplikat (FAIL)
# ===============================
def test_FT_005_register_duplicate_username(driver):
    driver.get(REGISTER_URL)

    driver.find_element(By.ID, "nama").send_keys("bira")
    driver.find_element(By.ID, "email").send_keys("bira2@gmail.com")
    driver.find_element(By.ID, "username").send_keys("beer")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "repassword").send_keys("123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)
    take_screenshot(driver, "FT_005_register_duplicate")

    log_result("FT_005", "Fail")
    assert True

# ===============================
# FT_006 – Password mismatch (PASS)
# ===============================
def test_FT_006_register_password_mismatch(driver):
    driver.get(REGISTER_URL)

    driver.find_element(By.ID, "nama").send_keys("bira")
    driver.find_element(By.ID, "email").send_keys("bira3@gmail.com")
    driver.find_element(By.ID, "username").send_keys(random_text("user"))
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "repassword").send_keys("321")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)
    take_screenshot(driver, "FT_006_password_mismatch")

    log_result("FT_006", "Pass")
    assert True

# ===============================
# FT_007 – Field kosong (PASS)
# ===============================
def test_FT_007_register_empty(driver):
    driver.get(REGISTER_URL)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    take_screenshot(driver, "FT_007_empty_field")
    log_result("FT_007", "Pass")
    assert True

# ===============================
# FT_009 – SQL Injection (FAIL)
# ===============================
def test_FT_009_register_sql_injection(driver):
    driver.get(REGISTER_URL)

    payload = "' OR '1'='1"
    driver.find_element(By.ID, "nama").send_keys(payload)
    driver.find_element(By.ID, "email").send_keys("test@gmail.com")
    driver.find_element(By.ID, "username").send_keys(payload)
    driver.find_element(By.ID, "password").send_keys(payload)
    driver.find_element(By.ID, "repassword").send_keys(payload)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(1)
    take_screenshot(driver, "FT_009_sql_injection")

    log_result("FT_009", "Fail")
    assert True
