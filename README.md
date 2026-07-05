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

   # Activate virtual environment

   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\Activate.ps1
   ```

   If you see this error on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
   ```

   Run:

   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   Then press:

   ```powershell
   Y
   ```

   After that, activate the virtual environment again:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   Continue with installation:

   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Bootstrap once (signup → login → save session)**
   ```bash
   python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123" --storage "auth/storage_state.json"
   ```
   or try this
   ```bash
   python -m scripts.bootstrap_signup --name "Jane Doe" --email "test@example.com" --password "StrongPass123" --storage "auth/storage_state.json"


4. **Verify session works (smoke test)**
   ```bash
   pytest tests/test_logged_in_session.py -s
   ```

   > Tip: to **watch it in a real browser**, run headed.

   ### macOS / Linux / Git Bash / WSL
   ```bash
   HEADLESS=false pytest -s tests/test_logged_in_session.py
   ```

   ### Windows PowerShell
   ```powershell
   $env:HEADLESS="false"
   pytest -s tests/test_logged_in_session.py
   ```

   ### Windows Command Prompt (cmd)
   ```cmd
   set HEADLESS=false && pytest -s tests/test_logged_in_session.py
   ```

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
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123" --storage "auth/storage_state.json"
```bash
python -m scripts.bootstrap_signup --name "Jane Doe" --email "test@example.com" --password "StrongPass123" --storage "auth/storage_state.json"
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
python scripts/bootstrap_signup.py --name "New User" --email "new@example.com" --password "AnotherPass123" --storage "auth/storage_state.json"
```
Or delete `auth/storage_state.json` and run tests again — the framework now auto-bootstraps if the file is missing!

### When to re‑bootstrap
- Your **login smoke test fails** (e.g., you land on the login page instead of the dashboard), or  
- Tests suddenly can’t find logged‑in elements.  

➡️ The saved session likely expired or was invalidated. **Fix:** rerun the bootstrap script:
```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123" --storage "auth/storage_state.json"
```
Then re-run:
```bash
pytest tests/test_logged_in.py -s
pytest -vv
```

---

## � Login‑Only Flow (No Signup)

If your application does not have a Sign Up page or you prefer to use a pre-existing account:

1.  **Modify the Bootstrap Script**: Open `scripts/bootstrap_signup.py`.
2.  **Remove Signup Logic**: Comment out or delete the `SignupPage` interaction:
    ```python
    # signup_page = SignupPage(page)
    # signup_page.goto()
    # signup_page.sign_up(args.name, args.email, args.password)
    ```
3.  **Ensure Login Logic is Active**: The script already includes a login step that uses the credentials provided via CLI.
4.  **Run as Usual**: The rest of the framework (session saving and auto-loading in tests) will work identically.

This ensures you can still benefit from the "log in once, test many times" architecture even without an automated signup.

---

## �🔒 Headless vs Headed

By default, runs headless. To see the browser, set `HEADLESS=false`:
```bash
HEADLESS=false pytest -s tests/test_logged_in_session.py
```

You can also run the bootstrap script directly if you need to refresh credentials manually. The framework handles the `PYTHONPATH` automatically, so you can run it from the project root:
```bash
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123" --storage "auth/storage_state.json"
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

## 🐞 Cross-Platform Path Handling

The framework is fully cross-platform (Windows/macOS/Linux). It automatically handles the `PYTHONPATH` when running bootstrap scripts as subprocesses from `conftest.py`.

If you are running scripts manually and encounter `ModuleNotFoundError: No module named 'pages'`, ensure you are in the project root and use:

```bash
# Recommended way to run any script manually
set PYTHONPATH=.
python scripts/bootstrap_signup.py [args]
```

*(Note: On macOS/Linux use `export PYTHONPATH=.`)*

---

## 🔗 Handy Commands

```bash
# Bootstrap (signup → login → save session)
python scripts/bootstrap_signup.py --name "Jane Doe" --email "jane@example.com" --password "StrongPass123" --storage "auth/storage_state.json"

# Run tests
pytest -vv

# Run smoke test only
pytest tests/test_logged_in.py -s

# Generate HTML report
pytest -vv --html=reports/html/report.html --self-contained-html
```

---

🎉 You’re all set — the framework signs up, logs in, saves the session, and reuses it for fast, reliable tests.

Watson Testing here :)