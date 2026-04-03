def run_signup_from_csv(csv_path="users.csv", headed=True):
    import csv
    from pathlib import Path
    from playwright.sync_api import sync_playwright, expect

    URL = "https://faruk-hasan.com/automation/signup.html"
    rows = list(csv.DictReader(Path(csv_path).open(newline="", encoding="utf-8")))

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        context = browser.new_context()

        for u in rows:
            page = context.new_page()
            try:
                page.goto(URL, wait_until="domcontentloaded")
                expect(page).to_have_title("Sign Up - Automation Practice")

                page.locator("#username").fill(u["name"].strip())
                page.locator("#email").fill(u["email"].strip())
                page.locator("#password").fill(u["password"].strip())
                page.locator("#confirmPassword").fill(u["password"].strip())
                page.get_by_role("button", name="Sign Up").click()

                # Let any redirect/JS complete before closing this page
                page.wait_for_load_state("networkidle", timeout=7000)
                print(f"✅ Signed up: {u['name']} ({u['email']})")
            finally:
                page.close()

        browser.close()


if __name__ == "__main__":
    run_signup_from_csv("users.csv", headed=True)
