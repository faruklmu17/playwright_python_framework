import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
def test_logged_in_title(page: Page):
    # Go directly to the main logged-in landing page
    page.goto("https://faruk-hasan.com/automation/login.html")

    # Grab the page title
    title = page.title()
    print(f"\n[TEST] Logged-in page title: {title}")

    # Assert that we are logged in by checking the expected title
    expect(page).to_have_title("Automation Adventure")
