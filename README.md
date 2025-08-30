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
- **Signup + Login bootstrap script** to persist credentials + session  
- **Global fixtures** via `conftest.py` (browser/context/page management)  
- **Session auto-reuse**: tests automatically start logged in if `auth/storage_state.json` exists  
- **Sample smoke test** to confirm session reuse  
- **HTML/JUnit reports** (via `pytest-html`, JUnit XML)  
- **CI-friendly** configuration (pytest, reports)  

> Tested against **pytest 8+** and **Playwright 1.45+**.

---

## 🧭 First-Time Setup

### 1. Clone and set up environment
```bash
git clone https://github.com/your-username/playwright_python_framework.git
cd playwright_python_framework

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
playwright install
```

---

### 2. Bootstrap the first user
Run the bootstrap script (signup → login → save session):

```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```

This will:
- Open the demo **Sign Up** page (`/signup.html`)  
- Fill username, email, password, confirm password  
- Click **Sign Up**  
- Then go to the **Login** page (`/login.html`)  
- Log in with the same credentials  
- Confirm success by asserting the page title  
- Save credentials to `.env`  
- Save the logged-in session to `auth/storage_state.json`  

---

### 3. Verify bootstrap worked
After bootstrap, you should see:
- `.env` with your signup credentials and session path  
- `auth/storage_state.json` (non-empty JSON file containing cookies + localStorage)

---

### 4. Run a smoke test
```bash
pytest tests/test_logged_in_session.py -s
```

Expected output:
```
[TEST] Verified logged-in session with title: Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground
```

---

### 5. Run all tests
```bash
pytest -vv
```

- If `auth/storage_state.json` is valid → all tests start authenticated.  
- If missing/invalid → `conftest.py` will auto-run bootstrap.  

---

## 🔁 Refreshing the Session
If cookies expire or you want a new account:

```bash
python scripts/bootstrap_signup.py --name "New User" --email "new@example.com" --password "AnotherPass123"
```

Or just delete `auth/storage_state.json` and rerun pytest — the bootstrap will be triggered again.

---

## 🔒 Headless vs Headed

By default, runs headless. To see the browser, pass `--headed`:

```bash
python scripts/bootstrap_signup.py --headed --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```

---

## 📊 Test Reports

Install extra deps:
```bash
pip install pytest-html pytest-metadata
```

Generate HTML report:
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
│  └─ signup_page.py
├─ scripts/
│  └─ bootstrap_signup.py
├─ tests/
│  ├─ test_logged_in_session.py
│  └─ other_tests.py
├─ .env
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
# Bootstrap (signup → login → save session)
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"

# Force new user & session
python scripts/bootstrap_signup.py --force --random-email --name "New User" --password 'NewStrongPass!23'

# Run tests
pytest -vv

# Run smoke test only
pytest tests/test_logged_in_session.py -s

# Generate HTML report
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

🎉 You’re all set — the framework signs up, logs in, saves the session, and reuses it for fast, reliable tests.
