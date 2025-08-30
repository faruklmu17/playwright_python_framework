import pytest
from playwright.sync_api import Page, expect
import time

# Matches what you set in test_signup_and_save_session
EXPECTED_TITLE = "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground"

@pytest.mark.smoke
def test_logged_in_session(page: Page):
    # Navigate directly to a page that requires you to be logged in
    page.goto("https://faruk-hasan.com/automation/playwright-selenium-cypress-practice.html")

    # Assert that the session from storage_state.json is applied
    expect(page).to_have_title(EXPECTED_TITLE)

    # (Optional) Check for a logged-in UI element, e.g. Logout button
    # expect(page.get_by_role("button", name="Logout")).to_be_visible()

    print(f"\n[TEST] Verified logged-in session with title: {page.title()}")
    time.sleep(5)
