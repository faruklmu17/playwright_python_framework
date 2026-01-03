# conftest.py
import json
import os
import subprocess
import sys
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
SIGNUP_EMAIL = ENV.get("SIGNUP_EMAIL")  # may be None -> auto-generate
SIGNUP_PASSWORD = ENV.get("SIGNUP_PASSWORD", "StrongPass123")
BOOTSTRAP_CMD = [sys.executable, str(Path("scripts/bootstrap_signup.py"))]  # cross-platform
FORCE_BOOTSTRAP = os.getenv("FORCE_BOOTSTRAP") in {"1", "true", "True"}

HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}

def _valid_storage(path: str) -> bool:
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        cookies_ok = isinstance(data.get("cookies"), list) and len(data.get("cookies", [])) > 0
        origins_ok = isinstance(data.get("origins"), list) and len(data.get("origins", [])) > 0
        return cookies_ok or origins_ok
    except Exception:
        return False

def _bootstrap_if_needed():
    if not FORCE_BOOTSTRAP and _valid_storage(STORAGE):
        return

    Path(STORAGE).parent.mkdir(parents=True, exist_ok=True)
    email = SIGNUP_EMAIL or f"test_{uuid4().hex[:10]}@example.com"

    # IMPORTANT: ensure your bootstrap script accepts --storage
    # If your script uses --out instead, change "--storage" -> "--out"
    cmd = BOOTSTRAP_CMD + [
        "--name", SIGNUP_NAME,
        "--email", email,
        "--password", SIGNUP_PASSWORD,
        "--storage", STORAGE,
    ]

    print(f"[conftest] Bootstrapping auth state: {' '.join(cmd)}")
    
    # Ensure current directory is in PYTHONPATH for the subprocess
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + os.pathsep + env.get("PYTHONPATH", "")

    try:
        subprocess.check_call(cmd, env=env)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"[conftest] Bootstrap failed with exit code {e.returncode}. "
                    f"Cmd: {' '.join(cmd)}")

    if not _valid_storage(STORAGE):
        pytest.fail(f"[conftest] Bootstrap completed but storage is invalid: {STORAGE}")

# --- Playwright lifecycle (without pytest-playwright plugin) ---

@pytest.fixture(scope="session")
def playwright():
    """Start/stop Playwright for the whole session."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    """Launch a single Chromium for the session."""
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()

@pytest.fixture(scope="session", autouse=True)
def ensure_bootstrap():
    """
    Session-wide guard: ensure storage exists before tests run.
    If missing/invalid, bootstrap (signup+login) once.
    """
    _bootstrap_if_needed()

@pytest.fixture
def context(browser):
    """
    Fresh, isolated context per test, but pre-loaded with saved storage.
    This prevents test cross-contamination and supports parallel runs later.
    """
    ctx = browser.new_context(storage_state=STORAGE)
    try:
        yield ctx
    finally:
        ctx.close()

@pytest.fixture
def page(context):
    """Fresh page per test."""
    p = context.new_page()
    try:
        yield p
    finally:
        p.close()
