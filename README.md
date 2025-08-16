# Playwright Python Testing Framework

A modular, pytest-based Playwright framework for testing React applications (or any web apps) in Python.  
This framework includes support for:

* **Page Object Model** (POM) for clean, maintainable test code
* **Data-driven testing** via JSON fixtures
* **Visual regression** with baseline snapshots and automatic diffs
* **Screenshots & videos** on failures for easier debugging
* **Environment configuration** using `.env` files
* **Authenticated session reuse** using Playwright's `storageState`
* **HTML & JUnit reporting** via `pytest-html` and JUnit XML
* **Optional Allure reporting** for advanced dashboards
* **CLI & CI integration** with GitHub Actions and GitHub Pages

---
x
## 🚀 Getting Started

Follow these steps to set up and verify that the framework is working correctly on your machine.

### ✅ Prerequisites

- Python 3.8 or later installed
- Git installed
- Google Chrome or Chromium installed
- Node.js (optional, for Git hooks with Husky)

---

### 🪜 Step-by-Step Setup

#### 1. **Clone the Repository**
This copies the framework into your machine.

```bash
git clone https://github.com/your-username/playwright_python_framework.git
cd playwright_python_framework
```

#### 2. **Create a Virtual Environment**
Keeps your project dependencies isolated from your system Python.

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\activate  # Windows
```

#### 3. **Install Dependencies**
Installs all required Python libraries and Playwright browsers.

```bash
pip install -r requirements.txt
playwright install
```

#### 4. **Bootstrap Signup**
Before running any tests, you must create a test account.  
This script will **sign up on the demo app** and save your credentials into a `.env` file automatically.

```bash
python scripts/bootstrap_signup.py --name "Test User" --email testuser@example.com --password "MyPass123!"
```

What happens here:
- Navigates to the signup page.
- Fills in your provided name, email, and password.
- Submits the form.
- Saves your credentials in `.env` so tests can use them.

#### 5. **Run the Sample Test**
Run the included test to confirm everything is set up correctly.

```bash
pytest tests/test_sample.py -vv
```

Expected result:
- Test should **pass** ✅ if the framework is installed and configured properly.

#### 6. **View Reports**
After running tests, open the HTML report:

```bash
open reports/html/report.html   # macOS
start reports\html\report.html  # Windows
```

---

## 🔐 Environment Variables

The `.env` file is created automatically during signup, but you can also edit it manually.

```env
BASE_URL=https://faruk-hasan.com/automation/signup.html
LOGIN_EMAIL=testuser@example.com
LOGIN_PASSWORD=MyPass123!
```

These values are used by tests to log in without signing up each time.

---

## 🧪 Writing Your Own Tests

- Add new tests inside the `tests/` folder.
- Use the `page` fixture provided by Playwright to interact with the browser.
- Example:

```python
def test_example(page):
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

---

## 🤖 Common Commands

| Action                    | Command                                |
|---------------------------|----------------------------------------|
| Run all tests             | `pytest`                               |
| Run one test file         | `pytest tests/test_sample.py`          |
| Run with detailed output  | `pytest -vv`                           |
| View HTML report          | Open `reports/html/report.html`        |

---

## 🎉 You’re Ready!

Now you can:
- Run tests to validate your setup
- Extend the framework with new pages and tests
- Use `.env` to manage login credentials automatically

This project is **beginner-friendly** — just follow the steps above, and you’ll be up and running with a professional-grade Playwright testing framework.
