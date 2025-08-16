import pytest
from playwright.sync_api import Page, expect

@pytest.mark.sample
def test_framework_setup(page: Page):
    url = "https://faruk-hasan.com/automation/signup.html"
    page.goto(url, wait_until="domcontentloaded")

    # Check page title
    expect(page).to_have_title("Sign Up - Automation Practice")

    # Optional sanity check: make sure the form is visible
    form = page.locator("form")
    expect(form).to_be_visible()