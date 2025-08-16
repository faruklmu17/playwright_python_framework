# conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright

STORAGE_PATH = os.getenv("STORAGE_STATE", "auth/storage_state.json")
BASE_URL = os.getenv("BASE_URL", "")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def context(browser):
    # Reuse session if it exists
    kwargs = {"base_url": BASE_URL}
    if os.path.exists(STORAGE_PATH):
        kwargs["storage_state"] = STORAGE_PATH
    ctx = browser.new_context(**kwargs)
    yield ctx
    ctx.close()

@pytest.fixture
def page(context):
    p = context.new_page()
    yield p
    p.close()