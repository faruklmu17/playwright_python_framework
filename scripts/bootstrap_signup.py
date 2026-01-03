# scripts/bootstrap_signup.py
import argparse
import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from pages.signup_page import SignupPage

# Load defaults from env if available (matching your original logic)
LOGIN_URL = os.getenv("LOGIN_URL", "https://faruk-hasan.com/automation/login.html")
EXPECTED_TITLE = os.getenv(
    "EXPECTED_TITLE",
    "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground"
)

def main():
    parser = argparse.ArgumentParser(description="Bootstrap auth state via signup + login")
    parser.add_argument("--name", required=True, help="User display name")
    parser.add_argument("--email", required=True, help="User email")
    parser.add_argument("--password", required=True, help="User password")
    parser.add_argument("--storage", required=True, help="Path to save storage state")
    
    args = parser.parse_args()
    
    print(f"[bootstrap] Starting bootstrap for {args.email}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1. Sign Up
            signup_page = SignupPage(page)
            signup_page.goto()
            # We use the 'name' argument as the username for both signup and login
            signup_page.sign_up(args.name, args.email, args.password)

            # 2. Login (Some apps require manual login after signup)
            print(f"[bootstrap] Logging in at {LOGIN_URL}...")
            page.goto(LOGIN_URL, wait_until="domcontentloaded")
            
            # Use placeholders as in your original script
            page.get_by_placeholder("Enter your username").fill(args.name)
            page.get_by_placeholder("Enter your password").fill(args.password)
            page.get_by_role("button", name="Login").click()

            # 3. Verify we're authenticated
            expect(page).to_have_title(EXPECTED_TITLE)
            
            # 4. Save storage state
            storage_path = Path(args.storage)
            storage_path.parent.mkdir(parents=True, exist_ok=True)
            context.storage_state(path=str(storage_path))
            
            print(f"[bootstrap] Successfully saved storage state to {args.storage}")
            
        except Exception as e:
            print(f"[bootstrap] Error during bootstrap: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
