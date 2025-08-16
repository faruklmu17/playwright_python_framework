# Playwright Python Testing Framework

A modular, pytest-based Playwright framework for testing React applications (or any web apps) in Python.  

It includes:
* **Page Object Model** (POM) for clean, maintainable test code  
* **Data-driven testing** via JSON fixtures  
* **Visual regression** with baseline snapshots and diffs  
* **Screenshots & videos** on failures  
* **Environment configuration** using `.env` files  
* **Authenticated session reuse** using Playwright's `storageState`  
* **HTML & JUnit reporting** (`pytest-html`, JUnit XML)  
* **Optional Allure reporting** for advanced dashboards  
* **CI integration** with GitHub Actions & Pages  

---

## ✅ Prerequisites
- Python 3.8 or later  
- Git installed  
- Node.js installed (optional, only for Husky Git hooks)  
- Google Chrome (for visual debugging)  

---

## 🪜 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/playwright_python_framework.git
cd playwright_python_framework
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
playwright install
```

---

## 🔐 First-Time Bootstrap (Signup → `.env` → Session)

Before running any tests, you must **sign up once**.  
This creates a user, saves the credentials in `.env`, and saves the session in `auth/storage_state.json`.

```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email jane@example.com --password "StrongPass!23"
```

👉 This will:
- Open the signup page (`https://faruk-hasan.com/automation/signup.html`)  
- Fill in the signup form with your details  
- Save your credentials to `.env`:
  ```env
  SIGNUP_NAME=Jane Doe
  SIGNUP_EMAIL=jane@example.com
  SIGNUP_PASSWORD=StrongPass!23
  STORAGE_STATE=auth/storage_state.json
  ```
- Save your logged-in session to `auth/storage_state.json`  

### Resetting
If you need to sign up again or rotate credentials:  
```bash
rm -f auth/storage_state.json
python scripts/bootstrap_signup.py --name "New User" --email new@example.com --password "NewPass123!"
```

---

## 🧪 Verify the Setup

Run the included **sample test** to make sure everything works:
```bash
pytest tests/test_sample.py -vv --headed
```

Expected result:
```
collected 1 item
tests/test_sample.py .      [100%]
```

---

## ▶️ Running Tests

Run the entire suite:
```bash
pytest -vv
```

Run a single test file:
```bash
pytest tests/test_signup.py
```

Run only tests with the `sample` marker:
```bash
pytest -m sample --headed
```

---

## 📊 Viewing Reports

HTML report:
```bash
pytest --html=reports/html/report.html --self-contained-html
```

Open the report:
```bash
open reports/html/report.html   # macOS
start reports\html\report.html  # Windows
```

JUnit XML (for CI):
```bash
pytest --junitxml=reports/junit/report.xml
```

---

## 🧩 Git Hooks with Husky (Optional)

You can enforce quality checks before committing using [Husky](https://github.com/typicode/husky).

1. Install Husky:
   ```bash
   npm install husky --save-dev
   npx husky install
   ```

2. Add a pre-commit hook:
   ```bash
   npx husky add .husky/pre-commit "pytest && black --check . && flake8"
   git add .husky/pre-commit
   ```

Now every commit will automatically run your tests and linters.

---

## 🚀 Project Structure

```
playwright_python_framework/
│
├── auth/                     # Saved Playwright session (storage_state.json)
├── pages/                    # Page Object Models
│   └── signup_page.py
├── scripts/                  # Utility scripts
│   └── bootstrap_signup.py
├── tests/                    # Test cases
│   ├── test_sample.py
│   └── test_signup_and_save_session.py
├── .env.example              # Template for environment variables
├── conftest.py               # Global fixtures (loads session, page, etc.)
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🤖 Common Commands

| Action                       | Command                                               |
|------------------------------|-------------------------------------------------------|
| Run all tests                | `pytest -vv`                                          |
| Run sample setup test        | `pytest -m sample --headed`                           |
| Run bootstrap signup         | `python scripts/bootstrap_signup.py --name ...`       |
| Reset session                | `rm -f auth/storage_state.json && python scripts/bootstrap_signup.py` |
| View HTML report             | `open reports/html/report.html` (Mac) / `start ...` (Win) |

---

> 🔰 This project is beginner-friendly. After the one-time signup, you can run tests without ever worrying about logging in again.
