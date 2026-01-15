import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL_REGISTER = "http://localhost/quiz/register.php"

@pytest.fixture
def driver():
    if os.getenv("CI") == "true":
        pytest.skip("Skip Selenium test on CI (localhost not available)")

    options = Options()
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def fill_form(driver, username="beer", password="123", repass="123"):
    driver.find_element(By.NAME, "nama").send_keys("bira")
    driver.find_element(By.NAME, "email").send_keys("bira@gmail.com")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "repassword").send_keys(repass)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

# FT_004 – Register valid (FAIL – username sudah ada)
def test_FT_004_register_valid(driver):
    driver.get(URL_REGISTER)
    fill_form(driver)
    time.sleep(1)
    assert "register.php" in driver.current_url.lower()

# FT_005 – Username duplikat (FAIL)
def test_FT_005_register_duplicate_username(driver):
    driver.get(URL_REGISTER)
    fill_form(driver)
    time.sleep(1)
    assert "register.php" in driver.current_url.lower()

# FT_006 – Password tidak cocok (PASS)
def test_FT_006_register_password_mismatch(driver):
    driver.get(URL_REGISTER)
    fill_form(driver, repass="999")
    time.sleep(1)
    assert "register.php" in driver.current_url.lower()

# FT_007 – Field kosong (PASS)
def test_FT_007_register_empty(driver):
    driver.get(URL_REGISTER)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert "register.php" in driver.current_url.lower()

# FT_009 – SQL Injection (FAIL)
def test_FT_009_register_sql_injection(driver):
    driver.get(URL_REGISTER)
    fill_form(driver, username="' OR '1'='1")
    time.sleep(1)
    assert "register.php" in driver.current_url.lower()
