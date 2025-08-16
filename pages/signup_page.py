# pages/signup_page.py
import re
from playwright.sync_api import Page, expect

class SignupPage:
    URL = "https://faruk-hasan.com/automation/signup.html"

    def __init__(self, page: Page):
        self.page = page
        # Adjust selectors to match your form; these work for the sample page
        self.name = page.get_by_label(re.compile(r"name", re.I))
        self.email = page.get_by_label(re.compile(r"email", re.I))
        self.password = page.get_by_label(re.compile(r"password", re.I))
        self.confirm = page.get_by_label(re.compile(r"confirm", re.I)).or_(page.get_by_label(re.compile(r"confirm password", re.I)))
        self.submit = page.get_by_role("button")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded")

    def sign_up(self, full_name: str, email: str, password: str):
        expect(self.page).to_have_title("Sign Up - Automation Practice")
        self.name.fill(full_name)
        self.email.fill(email)
        self.password.fill(password)
        # If the page has a confirm-password field, fill it; otherwise ignore
        if self.confirm.count() > 0:
            self.confirm.fill(password)
        self.submit.click()
        # If your page shows a success toast/banner, assert it here;
        # for the demo page we just ensure no navigation error occurred.
        expect(self.page).not_to_have_url(re.compile(r"error", re.I))
