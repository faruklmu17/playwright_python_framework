#!/usr/bin/env python3
# scripts/bootstrap_signup.py
# Bootstrap signup:
#   - Accepts --name, --email, --password (CLI) or prompts interactively
#   - Visits demo signup page and creates the account
#   - Writes/updates .env with SIGNUP_* values
#   - Saves Playwright storage state to auth/storage_state.json

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv, set_key, dotenv_values
from playwright.sync_api import sync_playwright, expect

DOTENV_PATH = Path(".env")
DEFAULT_STORAGE_STATE = "auth/storage_state.json"

# Demo signup page; for real apps, read BASE_URL from .env and go to `${BASE_URL}/signup`
SIGNUP_URL = "https://faruk-hasan.com/automation/signup.html"

def ensure_dotenv():
    if not DOTENV_PATH.exists():
        DOTENV_PATH.write_text("STORAGE_STATE=auth/storage_state.json\n")
    load_dotenv(dotenv_path=DOTENV_PATH)

def write_env(name: str, email: str, password: str):
    set_key(str(DOTENV_PATH), "SIGNUP_NAME", name)
    set_key(str(DOTENV_PATH), "SIGNUP_EMAIL", email)
    set_key(str(DOTENV_PATH), "SIGNUP_PASSWORD", password)
    current = dotenv_values(str(DOTENV_PATH))
    if not current.get("STORAGE_STATE"):
        set_key(str(DOTENV_PATH), "STORAGE_STATE", DEFAULT_STORAGE_STATE)

def do_signup(name: str, email: str, password: str, storage_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()

        page.goto(SIGNUP_URL, wait_until="domcontentloaded")
        expect(page).to_have_title("Sign Up - Automation Practice")

        # Fill the form by ID
        page.fill("#username", name)
        page.fill("#email", email)
        page.fill("#password", password)
        page.fill("#confirmPassword", password)

        # Click Sign Up button by role+name
        page.get_by_role("button", name="Sign Up").click()

        # Save session
        Path(os.path.dirname(storage_path) or ".").mkdir(parents=True, exist_ok=True)
        ctx.storage_state(path=storage_path)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Bootstrap signup and persist credentials/session")
    parser.add_argument("--name", help="Full name for signup")
    parser.add_argument("--email", help="Email for signup/login")
    parser.add_argument("--password", help="Password for signup/login")
    parser.add_argument("--storage", help="Custom path to storage_state.json (optional)")
    args = parser.parse_args()

    ensure_dotenv()

    name = args.name or input("Full name: ").strip()
    email = args.email or input("Email: ").strip()
    password = args.password or input("Password: ").strip()

    if not (name and email and password):
        raise SystemExit("Name, email, and password are required.")

    current = dotenv_values(str(DOTENV_PATH))
    storage_path = args.storage or current.get("STORAGE_STATE", DEFAULT_STORAGE_STATE)

    print("[*] Signing up on demo page…")
    do_signup(name, email, password, storage_path)

    print("[*] Writing credentials to .env")
    write_env(name, email, password)

    print(f"[*] Done. Session saved to {storage_path}. You can now run `pytest`.")

if __name__ == "__main__":
    main()
