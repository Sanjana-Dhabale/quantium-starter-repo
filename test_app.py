import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
from app import app

# Start the Dash server in a background thread
@pytest.fixture(scope="module")
def run_server():
    thread = threading.Thread(target=lambda: app.run(debug=False, port=8050))
    thread.daemon = True
    thread.start()
    import time
    time.sleep(3)  # Wait for server to start

# Setup Chrome browser
@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")       # Run without opening browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

BASE_URL = "http://127.0.0.1:8050"

def test_header_present(browser, run_server):
    """Test 1: Check that the header is present."""
    browser.get(BASE_URL)
    wait = WebDriverWait(browser, 10)
    header = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert header is not None
    assert "Pink Morsel" in header.text
    print("✅ Test 1 Passed: Header is present")

def test_visualisation_present(browser, run_server):
    """Test 2: Check that the line chart is present."""
    browser.get(BASE_URL)
    wait = WebDriverWait(browser, 10)
    chart = wait.until(EC.presence_of_element_located((By.ID, "sales-line-chart")))
    assert chart is not None
    print("✅ Test 2 Passed: Visualisation is present")

def test_region_picker_present(browser, run_server):
    """Test 3: Check that the region picker is present."""
    browser.get(BASE_URL)
    wait = WebDriverWait(browser, 10)
    region_picker = wait.until(EC.presence_of_element_located((By.ID, "region-filter")))
    assert region_picker is not None
    print("✅ Test 3 Passed: Region picker is present")