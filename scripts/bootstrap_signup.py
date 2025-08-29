#!/usr/bin/env python3
# scripts/bootstrap_signup.py
# Bootstrap signup → login → assert title → save storage_state.json

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv, set_key, dotenv_values
from playwright.sync_api import sync_playwright, expect

DOTENV_PATH = Path(".env")
DEFAULT_STORAGE_STATE = "auth/storage_state.json"

SIGNUP_URL = "https://faruk-hasan.com/automation/signup.html"
LOGIN_URL  = "https://faruk-hasan.com/automation/login.html"

def ensure_dotenv():
    if not DOTENV_PATH.exists():
        DOTENV_PATH.write_text("STORAGE_STATE=auth/storage_state.json\n")
    load_dotenv(dotenv_path=DOTENV_PATH)

def write_env(name: str, email: str, password: str, storage_path: str):
    set_key(str(DOTENV_PATH), "SIGNUP_NAME", name)
    set_key(str(DOTENV_PATH), "SIGNUP_EMAIL", email)
    set_key(str(DOTENV_PATH), "SIGNUP_PASSWORD", password)
    current = dotenv_values(str(DOTENV_PATH))
    if not current.get("STORAGE_STATE"):
        set_key(str(DOTENV_PATH), "STORAGE_STATE", storage_path)

def do_signup_and_login(name: str, email: str, password: str, storage_path: str, headed: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        ctx = browser.new_context()
        page = ctx.new_page()

        # --- 1) SIGN UP ---
        page.goto(SIGNUP_URL, wait_until="domcontentloaded")
        expect(page).to_have_title("Sign Up - Automation Practice")

        # Fill signup form by id
        page.fill("#username", name)
        page.fill("#email", email)
        page.fill("#password", password)
        page.fill("#confirmPassword", password)
        page.get_by_role("button", name="Sign Up").click()
        page.wait_for_load_state("networkidle")

        # --- 2) LOGIN ---
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        username_field = page.get_by_placeholder("Enter your username")
        password_field = page.get_by_placeholder("Enter your password")

        # Try with the username used at signup first
        username_field.fill(name)
        password_field.fill(password)
        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("networkidle")

        # If still on the login page, retry with email as username
        if page.title() == "Login - Automation Practice":
            username_field.fill(email)
            password_field.fill(password)
            page.get_by_role("button", name="Login").click()
            page.wait_for_load_state("networkidle")

        # --- 3) ASSERT LOGGED IN ---
        expect(page).to_have_title(
            "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground",
            timeout=7000
        )

        # --- 4) SAVE SESSION ---
        Path(os.path.dirname(storage_path) or ".").mkdir(parents=True, exist_ok=True)
        ctx.storage_state(path=storage_path)
        browser.close()

def main():
    parser = argparse.ArgumentParser(description="Bootstrap signup → login and persist credentials/session")
    parser.add_argument("--name", help="Full name for signup")
    parser.add_argument("--email", help="Email (or username) for login")
    parser.add_argument("--password", help="Password for signup/login")
    parser.add_argument("--storage", help="Custom path to storage_state.json (optional)")
    parser.add_argument("--headed", action="store_true", help="Show the browser during bootstrap")
    args = parser.parse_args()

    ensure_dotenv()

    name = args.name or input("Full name: ").strip()
    email = args.email or input("Email (or username): ").strip()
    password = args.password or input("Password: ").strip()

    if not (name and email and password):
        raise SystemExit("Name, email, and password are required.")

    current = dotenv_values(str(DOTENV_PATH))
    storage_path = args.storage or current.get("STORAGE_STATE", DEFAULT_STORAGE_STATE)

    print("[*] Signing up, then logging in…")
    do_signup_and_login(name, email, password, storage_path, headed=args.headed)

    print("[*] Writing credentials to .env")
    write_env(name, email, password, storage_path)

    print(f"[*] Done. Logged-in session saved to {storage_path}. You can now run `pytest`.")

if __name__ == "__main__":
    main()
