# conftest.py
import json
import os
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import load_dotenv, dotenv_values
from playwright.sync_api import sync_playwright

# --- .env / settings ---
load_dotenv()
ENV = dotenv_values(".env")

STORAGE = ENV.get("STORAGE_STATE", "auth/storage_state.json")
SIGNUP_NAME = ENV.get("SIGNUP_NAME", "QA User")
SIGNUP_EMAIL = ENV.get("SIGNUP_EMAIL")  # may be None
SIGNUP_PASSWORD = ENV.get("SIGNUP_PASSWORD", "StrongPass123")
BOOTSTRAP_CMD = ["python", "scripts/bootstrap_signup.py"]

def _valid_storage(path: str) -> bool:
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return bool(data.get("cookies") or data.get("origins"))
    except Exception:
        return False

def _bootstrap_if_needed():
    if _valid_storage(STORAGE):
        return
    Path(STORAGE).parent.mkdir(parents=True, exist_ok=True)
    email = SIGNUP_EMAIL or f"test_{uuid4().hex[:10]}@example.com"
    cmd = BOOTSTRAP_CMD + [
        "--name", SIGNUP_NAME,
        "--email", email,
        "--password", SIGNUP_PASSWORD,
        "--storage", STORAGE,
    ]
    print(f"[conftest] Storage invalid/missing. Bootstrapping: {' '.join(cmd)}")
    subprocess.check_call(cmd)

# --- Playwright lifecycle without pytest-playwright plugin ---

@pytest.fixture(scope="session")
def playwright():
    """Start/stop Playwright for the whole session."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    """Launch a single Chromium for the session."""
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def context(browser):
    """Authenticated browser context; ensures storage_state exists."""
    _bootstrap_if_needed()
    ctx = browser.new_context(storage_state=STORAGE)
    yield ctx
    ctx.close()

@pytest.fixture
def page(context):
    """Fresh page per test."""
    p = context.new_page()
    yield p
    p.close()
