# Playwright Python Testing Framework

A modular, pytest-based **Playwright (Python)** framework for web UI testing.

---

## 🚀 Quick Start (2‑Minute Guide)

1. **Clone & enter the project**
   ```bash
   git clone https://github.com/your-username/playwright_python_framework.git
   cd playwright_python_framework
   ```

2. **Create virtualenv & install deps**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # .venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   playwright install
   ```

3. **Bootstrap once (signup → login → save session)**
   ```bash
   python -m scripts.bootstrap_signup --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
   ```

4. **Verify session works (smoke test)**
   ```bash
   pytest tests/test_logged_in_session.py -s
   ```
   > Tip: to **watch it in a real browser**, run headed:
   > ```bash
   > HEADLESS=false pytest -s tests/test_logged_in_session.py
   > ```

5. **Run the full suite**
   ```bash
   pytest -vv
   ```

**If the smoke test fails later:** your saved session likely expired → re-run step 3 (bootstrap) to refresh it.

---

## ✅ What’s Included

- **Page Object Model (POM)** for clean, maintainable tests  
- **Signup + Login bootstrap script** to persist credentials + session  
- **Global fixtures** via `conftest.py` (browser/context/page management)  
- **Session auto‑reuse**: tests start logged in if `auth/storage_state.json` exists  
- **Smoke test** to confirm session reuse  
- **HTML/JUnit reports** (via `pytest-html`, JUnit XML)  
- **CI‑friendly** configuration (pytest, reports)  

> Tested against **pytest 8+** and **Playwright 1.45+**.

---

## 🧭 Full Setup & Usage

### 1) Environment setup
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
playwright install
```

### 2) Bootstrap the first user
Run the bootstrap script (signup → login → save session):
```bash
python -m scripts.bootstrap_signup --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```
This will:
- Open the demo **Sign Up** page (`/signup.html`)  
- Fill username, email, password, confirm password  
- Click **Sign Up**  
- Then go to the **Login** page (`/login.html`)  
- Log in with the same credentials  
- Confirm success by asserting the page title  
- Save credentials to `.env`  
- Save the logged‑in session to `auth/storage_state.json`  

### 3) Verify bootstrap worked
You should see:
- `.env` with your signup credentials and session path  
- `auth/storage_state.json` (non‑empty JSON file containing cookies + localStorage)

### 4) Run a smoke test
```bash
pytest tests/test_logged_in_session.py -s
```
Expected output (or similar):
```
[TEST] Verified logged-in session with title: Playwright, Selenium & Cypress Practice | Interactive Automation Testing Playground
```

### 5) Run all tests
```bash
pytest -vv
```
- If `auth/storage_state.json` is valid → all tests start authenticated.  
- If missing/invalid → your `conftest.py` can auto‑bootstrap (if you enabled that), or just re-run the bootstrap script.

---

## 🔁 Refreshing the Session

If cookies expire or you want a new account:
```bash
python -m scripts.bootstrap_signup --name "New User" --email "new@example.com" --password "AnotherPass123"
```
Or delete `auth/storage_state.json` and run tests again (auto‑bootstrap if enabled).

### When to re‑bootstrap
- Your **login smoke test fails** (e.g., you land on the login page instead of the dashboard), or  
- Tests suddenly can’t find logged‑in elements.  

➡️ The saved session likely expired or was invalidated. **Fix:** rerun the bootstrap script:
```bash
python -m scripts.bootstrap_signup --force --random-email --name "New User" --password "AnotherPass123"
```
Then re-run:
```bash
pytest -m smoke -s
pytest -vv
```

---

## 🔒 Headless vs Headed

By default, runs headless. To see the browser, set `HEADLESS=false`:
```bash
HEADLESS=false pytest -s tests/test_logged_in_session.py
```

You can also run the bootstrap script in headed mode (if it supports a `--headed` flag):
```bash
python -m scripts.bootstrap_signup --headed --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
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

## 🐞 Debugging: "ModuleNotFoundError: No module named 'pages'"

If you see an error like:

```
ModuleNotFoundError: No module named 'pages'
```

…it means Python couldn’t resolve imports when running `scripts/bootstrap_signup.py` directly.

### Fix Options

1. **Run as a module (recommended)**  
   From the project root, use `-m` instead of calling the file directly:
   ```bash
   python -m scripts.bootstrap_signup --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
   ```

2. **Make folders into packages**  
   Add empty `__init__.py` files so Python treats them as packages:
   ```
   pages/__init__.py
   scripts/__init__.py
   ```

3. **Add a safety net inside the script**  
   At the top of `scripts/bootstrap_signup.py`, add:
   ```python
   import os, sys
   sys.path.append(os.path.dirname(os.path.dirname(__file__)))
   ```

This ensures the script can always find `pages/signup_page.py` regardless of how it’s run.

---

## 🔗 Handy Commands

```bash
# Bootstrap (signup → login → save session)
python -m scripts.bootstrap_signup --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"

# Force new user & session
python -m scripts.bootstrap_signup --force --random-email --name "New User" --password 'NewStrongPass!23'

# Run tests
pytest -vv

# Run smoke test only
pytest tests/test_logged_in.py -s

# Generate HTML report
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

🎉 You’re all set — the framework signs up, logs in, saves the session, and reuses it for fast, reliable tests.
