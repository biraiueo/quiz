import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL_LOGIN = "http://localhost/quiz/login.php"

# ==============================
# SETUP DRIVER
# ==============================
@pytest.fixture
def driver():
    # Jika jalan di GitHub Actions → SKIP
    if os.getenv("CI") == "true":
        pytest.skip("Skip Selenium test on CI (localhost not available)")

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# ==============================
# FT_001 – Login valid (PASS)
# ==============================
def test_FT_001_login_valid(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.NAME, "username").send_keys("beer")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    assert "index.php" in driver.current_url.lower()

# ==============================
# FT_002 – Login invalid (PASS)
# ==============================
def test_FT_002_login_invalid(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.NAME, "username").send_keys("salah")
    driver.find_element(By.NAME, "password").send_keys("salah")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    assert "login.php" in driver.current_url.lower()

# ==============================
# FT_003 – Field kosong (PASS)
# ==============================
def test_FT_003_login_empty(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    assert "login.php" in driver.current_url.lower()

# ==============================
# FT_008 – SQL Injection (PASS)
# ==============================
def test_FT_008_login_sql_injection(driver):
    driver.get(URL_LOGIN)
    driver.find_element(By.NAME, "username").send_keys("' OR '1'='1")
    driver.find_element(By.NAME, "password").send_keys("' OR '1'='1")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    assert "login.php" in driver.current_url.lower()
