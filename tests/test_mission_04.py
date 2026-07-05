import pytest
from playwright.sync_api import Page, expect

EXPECTED_TITLE = "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground"


@pytest.mark.parametrize(
    "selected_date, expected_text",
    [
        ("2026-07-06", "Monday, July 6, 2026"),
    ]
)
def test_date_picker(page: Page, selected_date, expected_text):

    # Find the page
    page.goto("https://faruk-hasan.com/automation/playwright-selenium-cypress-practice.html")

    # Did the page load?
    expect(page).to_have_title(EXPECTED_TITLE)

    # Find the date-picker
    date_picker = page.locator("#date-picker")
    confirm_button = page.get_by_role("button", name="Confirm Date")
    result = page.locator("#date-result strong")

    # Fill mockup date
    date_picker.fill(selected_date)
    confirm_button.click()

    # Does the date the user set match the output text they get at the bottom?? (NO.)
    expect(date_picker).to_have_value(selected_date)
    expect(result).to_have_text(expected_text)

    
