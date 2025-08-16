# Playwright Python Testing Framework

A modular, pytest-based **Playwright (Python)** framework for web UI testing.

This repo is set up so that a new user can:
1) **Sign up once** on the demo page,  
2) Automatically **save credentials to `.env`** and the **session to `auth/storage_state.json`**, and  
3) **Reuse the logged-in session** on every test run — no login code inside tests.

---

## ✅ What’s Included

- **Page Object Model (POM)** for clean, maintainable tests  
- **Signup-first flow** that persists credentials + session  
- **Global fixtures** via `conftest.py` (one place to manage browser/context/page)  
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
**Why?** You need the project files locally.

---

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1
```
**Why?** Keeps your project’s Python packages isolated from system Python.

---

### 2) Install Python deps and Playwright browsers
```bash
pip install -r requirements.txt
playwright install
```
**Why?** Installs pytest, Playwright, and helpers. `playwright install` downloads the browser binaries Playwright drives.

---

### 3) Bootstrap the first user (signup → writes `.env` + saves session)
```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
```
> macOS tip: If your password contains `!` or `$`, wrap it in **single quotes**: `'StrongPass!23'`.

**What this does:**
- Opens the demo **Sign Up** page: `https://faruk-hasan.com/automation/signup.html`
- Fills **username** (`#username`), **email** (`#email`), **password** (`#password`), **confirm password** (`#confirmPassword`)
- Clicks the **Sign Up** button (role: button, name: “Sign Up”)
- Writes your credentials to **`.env`**:
  ```env
  SIGNUP_NAME=Jane Doe
  SIGNUP_EMAIL=jane@example.com
  SIGNUP_PASSWORD=StrongPass123
  STORAGE_STATE=auth/storage_state.json
  ```
- Saves the logged-in session to **`auth/storage_state.json`**

**Why?** From now on, tests start **already authenticated**. No login steps inside tests.

---

### 4) Confirm the bootstrap worked
Ensure these now exist:
- `.env` (contains `SIGNUP_NAME`, `SIGNUP_EMAIL`, `SIGNUP_PASSWORD`, `STORAGE_STATE`)
- `auth/storage_state.json` (a non-empty JSON file)

**Why?** `conftest.py` uses these to build an authenticated Playwright context automatically.

---

### 5) Run the sample test (quick health check)
```bash
pytest tests/test_sample.py -vv
```
**What this does:** Opens the signup page and asserts the title and required form elements exist.

**Success looks like:**
```
collected 1 item
tests/test_sample.py::test_framework_setup PASSED                                   [100%]
```

---

### 6) Run the full test suite
```bash
pytest -vv
```
**Why?** Verifies the project runs end-to-end under pytest.  
If you kept the bootstrap test, see the next section to run it only on demand.

---

## 🔁 Running the one-time signup test only when needed (recommended)

If you keep `tests/test_signup_and_save_session.py`, mark it and skip by default so signup only runs when you ask for it:

**`pytest.ini`**
```ini
[pytest]
markers =
    sample: quick setup verification test
    bootstrap: one-time signup & session save
addopts = -m "not bootstrap"
```

- Daily runs:
  ```bash
  pytest
  ```
  (Bootstrap test is excluded.)
- When you actually need to re-bootstrap:
  ```bash
  pytest -m bootstrap -vv
  ```

---

## 🔒 Headless vs. Headed (seeing the browser)

The browser mode is controlled in `conftest.py` within the `browser` fixture.  
To **watch the browser**, set `headless=False` there:

```python
browser = p.chromium.launch(headless=False)
```

---

## 🔐 Rotating credentials / re-signing up

If login fails or the session is stale, quickly create a new user + session:

```bash
python scripts/bootstrap_signup.py --force --random-email --name "New User" --password 'NewStrongPass!23'
```

**What `--force` does:** deletes old `auth/storage_state.json` and overwrites creds in `.env`.  

---

## 📊 Test Reports (HTML)

### One-time setup
```bash
pip install pytest-html pytest-metadata
```

### Generate a report (one-off)
```bash
pytest -vv --html=reports/html/report.html --self-contained-html
```

Open the report in your browser:
```bash
open reports/html/report.html  # macOS
start reports\html\report.html  # Windows
```

### Always generate reports automatically
Add this to your `pytest.ini`:
```ini
[pytest]
addopts = --html=reports/html/report.html --self-contained-html
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
│  ├─ test_sample.py
│  └─ test_signup_and_save_session.py
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
pytest tests/test_sample.py -vv
pytest -vv
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123"
python scripts/bootstrap_signup.py --force --random-email --name "New User" --password 'NewStrongPass!23'
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

**You’re set!**
