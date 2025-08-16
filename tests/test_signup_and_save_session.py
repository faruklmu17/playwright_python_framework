# tests/test_signup_and_save_session.py
import os
import time
from pathlib import Path
import pytest
from playwright.sync_api import Page, BrowserContext
from pages.signup_page import SignupPage

STORAGE_PATH = os.getenv("STORAGE_STATE", "auth/storage_state.json")

@pytest.mark.sample
def test_signup_and_save_session(page: Page, context: BrowserContext):
    sp = SignupPage(page)
    sp.goto()

    epoch = int(time.time())
    full_name = f"Test User {epoch}"
    email = f"playwright_user_{epoch}@example.com"
    password = f"P@ssw0rd{epoch}!"

    sp.sign_up(full_name, email, password)
    Path("auth").mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_PATH)

    assert Path(STORAGE_PATH).exists(), f"Expected storage state at {STORAGE_PATH}"
