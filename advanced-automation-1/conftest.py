import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--window-size=1920,1080")


    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Test sonucunu yakalar
    outcome = yield
    rep = outcome.get_result()
    
    # Sadece test "failed" (kaldı) olduğunda SS almak için (Ödev gereği her zaman da alabilirsin)
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            # Screenshots klasörü yoksa oluşturur
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # Dosya ismine tarih ve test adını ekler
            file_name = f"screenshots/{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(file_name)
            print(f"\n[INFO] Screenshot saved: {file_name}")
