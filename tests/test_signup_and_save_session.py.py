# tests/test_signup_and_save_session.py
import os
import time
import pytest
from pathlib import Path
from playwright.sync_api import Page, BrowserContext
from pages.signup_page import SignupPage

STORAGE_PATH = os.getenv("STORAGE_STATE", "auth/storage_state.json")

@pytest.mark.sample
def test_signup_and_save_session(page: Page, context: BrowserContext):
    """
    One-time bootstrap:
    - Fill the signup form on the demo page
    - Save storage_state to auth/storage_state.json
    - Future tests will auto-reuse this session via conftest.py
    """
    sp = SignupPage(page)
    sp.goto()

    # Simple generated creds (unique email so repeated runs don't clash)
    epoch = int(time.time())
    full_name = f"Test User {epoch}"
    email = f"playwright_user_{epoch}@example.com"
    password = f"P@ssw0rd{epoch}!"

    sp.sign_up(full_name, email, password)

    # Ensure folder exists, then persist session
    Path("auth").mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_PATH)

    # Sanity: file was created
    assert Path(STORAGE_PATH).exists(), f"Expected storage state at {STORAGE_PATH}"