"""Shared pytest configuration and fixtures."""
import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk import create_app


@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture(scope="function")
def client(app):
    """Provide Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def app_context(app):
    """Provide application context."""
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def chrome_driver():
    """Provide Selenium WebDriver for Chrome."""
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def selenium_client(chrome_driver):
    """Provide Selenium client for e2e tests."""
    return chrome_driver


# Markers for different test types
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "security: mark test as security test"
    )
    config.addinivalue_line(
        "markers", "accessibility: mark test as accessibility test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as edge case test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
