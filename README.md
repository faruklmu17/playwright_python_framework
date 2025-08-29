# Playwright Python Testing Framework

A modular, pytest-based **Playwright (Python)** framework for web UI testing.

This repo is set up so that a new user can:
1. **Sign up once** on the demo page,  
2. **Log in automatically after signup**,  
3. Save credentials to `.env` and the logged-in session to `auth/storage_state.json`, and  
4. **Reuse the logged-in session** on every test run — no login code inside tests.

---

## ✅ What’s Included

- **Page Object Model (POM)** for clean, maintainable tests  
- **Signup+Login bootstrap flow** that persists credentials + session  
- **Global fixtures** via `conftest.py` (one place to manage browser/context/page)  
- **Session auto-recovery**: if the saved session is missing or invalid, the framework auto-runs the bootstrap  
- **Sample tests** to verify setup  
- **HTML/JUnit reports** (via `pytest-html`, JUnit XML)  
- **CI-friendly** configuration (pytest, reports)  

> Tested against **pytest 8+** and **Playwright 1.45+**.

---

## 🧭 First-Time Setup — Step by Step (with explanations)

### 0) Clone the repository
```bash
git clone https://github.com/your-username/playwright_python_framework.git
cd playwright_python_framework
```

---

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```

---

### 2) Install Python deps and Playwright browsers
```bash
pip install -r requirements.txt
playwright install
```

---

### 3) Bootstrap the first user (signup → login → writes `.env` + saves session)
```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```

**What this does:**
- Opens the demo **Sign Up** page: `https://faruk-hasan.com/automation/signup.html`  
- Fills **username**, **email**, **password**, **confirm password**  
- Clicks **Sign Up**  
- Then goes to the **Login** page: `https://faruk-hasan.com/automation/login.html`  
- Logs in with the same credentials (using the placeholders: *Enter your username*, *Enter your password*)  
- Confirms success by asserting the page title:  
  *“Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground”*  
- Writes credentials to **`.env`**  
- Saves the logged-in session to **`auth/storage_state.json`**

---

### 4) Confirm the bootstrap worked
Ensure these now exist:
- `.env` (contains `SIGNUP_NAME`, `SIGNUP_EMAIL`, `SIGNUP_PASSWORD`, `STORAGE_STATE`)  
- `auth/storage_state.json` (a non-empty JSON file with cookies & storage)

---

### 5) Run the sample test (quick health check)
```bash
pytest tests/test_sample.py -vv
```

---

### 6) Run the full test suite
```bash
pytest -vv
```

**How it works now:**  
- If `auth/storage_state.json` is valid → tests start authenticated immediately.  
- If it’s missing/invalid → `conftest.py` auto-runs the bootstrap to create a fresh account + session.  

---

## 🔁 Running the bootstrap only on demand
If you want to explicitly re-bootstrap (fresh account + session):

```bash
python scripts/bootstrap_signup.py --force --random-email --name "New User" --password 'NewStrongPass!23'
```

Or just delete `auth/storage_state.json` and run `pytest` — the auto-bootstrap will kick in.

---

## 🔒 Headless vs. Headed (seeing the browser)

To watch the browser during bootstrap, pass `--headed`:

```bash
python scripts/bootstrap_signup.py --headed --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```

---

## 📊 Test Reports (HTML)

### One-time setup
```bash
pip install pytest-html pytest-metadata
```

### Generate a report
```bash
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

## 🧩 Project Structure

```
playwright_python_framework/
├─ auth/
│  └─ storage_state.json
├─ pages/
│  ├─ signup_page.py
│  └─ login_page.py
├─ scripts/
│  └─ bootstrap_signup.py
├─ tests/
│  ├─ test_sample.py
│  └─ test_login.py
├─ .env.example
├─ conftest.py
├─ pytest.ini
├─ requirements.txt
└─ README.md
```

---

## 🧾 .gitignore

```
.env
auth/storage_state.json
.pytest_cache/
__pycache__/
.venv/
reports/
```

---

## 🔗 Handy Commands

```bash
# First bootstrap (signup → login → save session)
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"

# Force new user & session
python scripts/bootstrap_signup.py --force --random-email --name "New User" --password 'NewStrongPass!23'

# Run tests
pytest -vv

# Run sample test only
pytest tests/test_sample.py -vv

# Generate HTML report
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

**You’re all set!** 🎉  
Now your framework signs up, logs in, saves the session, and auto-recovers if the session goes stale.
