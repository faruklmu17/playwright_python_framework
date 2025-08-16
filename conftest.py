# conftest.py
import os
from pathlib import Path
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load .env (SIGNUP_EMAIL, SIGNUP_PASSWORD, STORAGE_STATE, BASE_URL, etc.)
load_dotenv()

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
    # Require a pre-generated storage state (user bootstrapped)
    if not Path(STORAGE_PATH).exists():
        raise RuntimeError(
            f"Missing storage state at {STORAGE_PATH}. "
            "Run `python scripts/bootstrap_signup.py --name 'Your Name' --email you@example.com --password 'YourPass'` first."
        )
    ctx = browser.new_context(base_url=BASE_URL, storage_state=STORAGE_PATH)
    yield ctx
    ctx.close()

@pytest.fixture
def page(context):
    pg = context.new_page()
    yield pg
    pg.close()
