# pages/signup_page.py
from playwright.sync_api import Page, expect

class SignupPage:
    URL = "https://faruk-hasan.com/automation/signup.html"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.confirm_password = page.locator("#confirmPassword")
        self.signup_button = page.get_by_role("button", name="Sign Up")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")
        expect(self.page).to_have_title("Sign Up - Automation Practice")

    def sign_up(self, username: str, email: str, password: str):
        self.username.fill(username)
        self.email.fill(email)
        self.password.fill(password)
        self.confirm_password.fill(password)
        self.signup_button.click()
