import pytest
from playwright.sync_api import Page, expect
import time































# Matches what you set in test_signup_and_save_session
EXPECTED_TITLE = "Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground"

# I guess we'll do something like that.mark stuff for True or false,
# we've only got two choices anyway...
@pytest.mark.parametrize(
    "cheese, pepperoni, expected_result",
    [
        (True, False, "You selected: Cheese"),
        (False, True, "You selected: Pepperoni"),
        (True, True, "You selected: Cheese, Pepperoni"),
    ]
)
def test_pizza_toppings(page: Page, cheese, pepperoni, expected_result):

    page.goto("https://faruk-hasan.com/automation/playwright-selenium-cypress-practice.html")

    # Did the page load?
    expect(page).to_have_title(EXPECTED_TITLE)

    # Are the checkboxes there?
    cheese_checkbox = page.locator("#topping1")
    pepperoni_checkbox = page.locator("#topping2")

    # Unchecked test
    cheese_checkbox.uncheck()
    pepperoni_checkbox.uncheck()

    # Configuration for testing (what a user would do)
    if cheese:
        cheese_checkbox.check()

    if pepperoni:
        pepperoni_checkbox.check()

    # Press the order button
    page.get_by_role("button", name="Confirm Toppings").click()

    # Did the result work/was verified?
    result = page.locator("#checkbox-result")

    expect(result).to_contain_text(expected_result)

    print(f"[TEST] Test Result: {result.text_content()}")