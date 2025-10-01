import threading
import pytest
import time
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from werkzeug.serving import make_server

from app.app import create_app


@pytest.fixture(scope="session")
def test_app():
    """Create app instance for testing with test database"""
    app = create_app({
        'TESTING': True,
        'DATABASE': 'test.db',
        'SECRET_KEY': 'test-secret-key',
        'DEBUG': False,
        # 'SERVER_NAME': 'localhost:5000'
    })
    return app



@pytest.fixture(scope="session")
def selenium_server(test_app):
    """Custom live server that doesn't interact with pytest-flask"""
    # Find an available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
    
    def run_app():
        test_app.run(host='localhost', port=port, debug=False, use_reloader=False, threaded=True)
    
    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(2)
    
    server_url = f'http://localhost:{port}'
    print(f"Selenium server running at: {server_url}")
    
    return server_url  # Return just the URL string


@pytest.fixture
def driver(selenium_server):
    """Setup Selenium WebDriver with headless option for CI"""
    chrome_options = Options()
    chrome_options.add_argument("--headless") #Run in background for CI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    #Use the live_server URL
    driver.get(selenium_server)

    yield driver
    driver.quit()

@pytest.fixture
def client(test_app):
    """Regular test client for non-Selenium tests"""
    return test_app.test_client()