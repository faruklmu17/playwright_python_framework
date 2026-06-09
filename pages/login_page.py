# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    URL = "https://faruk-hasan.com/automation/login.html"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")
        expect(self.page).to_have_title("Login - Automation Practice")