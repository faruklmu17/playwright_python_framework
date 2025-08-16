# pages/signup_page.py
import re
from playwright.sync_api import Page, expect

class SignupPage:
    URL = "https://faruk-hasan.com/automation/signup.html"

    def __init__(self, page: Page):
        self.page = page
        self.name = page.get_by_label(re.compile(r"name", re.I))
        self.email = page.get_by_label(re.compile(r"email", re.I))
        self.password = page.get_by_label(re.compile(r"password", re.I))
        self.confirm = page.get_by_label(re.compile(r"confirm", re.I))  # may not exist
        self.submit = page.get_by_role("button")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")
        expect(self.page).to_have_title("Sign Up - Automation Practice")

    def sign_up(self, full_name: str, email: str, password: str):
        self.name.fill(full_name)
        self.email.fill(email)
        self.password.fill(password)
        if self.confirm.count() > 0:
            self.confirm.fill(password)
        self.submit.click()
        expect(self.page).not_to_have_url(re.compile(r"error", re.I))
