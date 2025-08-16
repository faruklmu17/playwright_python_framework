# tests/test_signup_and_save_session.py
import os
from pathlib import Path
import time
import pytest
from playwright.sync_api import Page, BrowserContext
from pages.signup_page import SignupPage

STORAGE_PATH = os.getenv("STORAGE_STATE", "auth/storage_state.json")

@pytest.mark.bootstrap
def test_signup_and_save_session(page: Page, context: BrowserContext):
    # If storage already exists, don't run the bootstrap again
    if Path(STORAGE_PATH).exists():
        pytest.skip(f"Storage state already exists at {STORAGE_PATH}; bootstrap not needed.")

    sp = SignupPage(page)
    sp.goto()

    epoch = int(time.time())
    username = f"TestUser{epoch}"
    email = f"playwright_user_{epoch}@example.com"
    password = f"P@ssw0rd{epoch}!"

    sp.sign_up(username, email, password)

    Path("auth").mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_PATH)
    assert Path(STORAGE_PATH).exists(), f"Expected storage state at {STORAGE_PATH}"
