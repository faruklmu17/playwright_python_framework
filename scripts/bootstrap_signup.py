# tests/test_signup_and_save_session.py
import os
import time
from pathlib import Path
import pytest
from playwright.sync_api import Page, BrowserContext, expect
from pages.signup_page import SignupPage

STORAGE_PATH = os.getenv("STORAGE_STATE", "auth/storage_state.json")
FORCE_BOOTSTRAP = os.getenv("FORCE_BOOTSTRAP") in {"1", "true", "True"}

# Your hosted pages + expected post-login title
LOGIN_URL = os.getenv("LOGIN_URL", "https://faruk-hasan.com/automation/login.html")
EXPECTED_TITLE = os.getenv(
    "EXPECTED_TITLE",
    "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground"
)

@pytest.mark.bootstrap
def test_signup_and_save_session(page: Page, context: BrowserContext):
    """
    1) Sign up (hosted signup page from SignupPage)
    2) Login (same context)
    3) Verify success by title
    4) Save storage_state.json
    """
    if Path(STORAGE_PATH).exists() and not FORCE_BOOTSTRAP:
        pytest.skip(f"Storage state already exists at {STORAGE_PATH}; bootstrap not needed.")

    # --- Sign Up ---
    sp = SignupPage(page)
    sp.goto()

    epoch = int(time.time())
    username = f"TestUser{epoch}"
    email = f"playwright_user_{epoch}@example.com"
    password = f"P@ssw0rd{epoch}!"

    sp.sign_up(username, email, password)

    # --- Login in the SAME CONTEXT ---
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.get_by_placeholder("Enter your username").fill(username)
    page.get_by_placeholder("Enter your password").fill(password)
    page.get_by_role("button", name="Login").click()

    # --- Verify we're authenticated ---
    # Adjust this if your app shows a specific logged-in element (e.g., Logout button)
    expect(page).to_have_title(EXPECTED_TITLE)

    # --- Save session for reuse ---
    Path(STORAGE_PATH).parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=STORAGE_PATH)
    assert Path(STORAGE_PATH).exists(), f"Expected storage state at {STORAGE_PATH}"
