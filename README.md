# Scratch Account Generator

A fully automated, GUI-driven tool for bulk-creating Scratch accounts with randomized credentials. Built in Python using Selenium for browser automation and Tkinter for the interface. No terminal interaction required after launch.

---

## Features

- **Automated account creation** — Fills out the entire Scratch registration flow automatically: username, password, country, birth date, gender, email, and Terms of Service acceptance.
- **Randomized usernames** — Every account gets a unique username in the format `SCgenerator` followed by a random 9-digit number (e.g. `SCgenerator382719054`).
- **Randomized passwords** — 12-character alphanumeric passwords generated fresh each run.
- **Random email assignment** — Each account is assigned a randomly chosen email from a built-in pool of iCloud addresses.
- **Random country & birth date** — Country is selected at random from a full global list. Birth year is randomised between 1904 and 2000.
- **Anti-detection** — ChromeDriver launches with `AutomationControlled` disabled and `navigator.webdriver` spoofed to reduce bot fingerprinting.
- **Dark GUI** — Clean dark-theme Tkinter window. All logs and account data display inline — no terminal needed.
- **Per-account cards** — Each of the 5 runs gets its own card in the UI showing live step-by-step logs, credentials, and status.
- **One-click copy** — Username and password each have their own `Copy` button with a flash confirmation. Email is displayed but intentionally not copyable.
- **Clipboard support** — Copies to both the system clipboard (cross-platform) and `pbcopy` on macOS.
- **Captcha gate** — After the signup flow completes, a `Confirm →` button appears in the card. You solve any captcha or verification in the browser, then press Confirm to continue. No terminal input ever required.
- **Session dividers** — Each batch of 5 accounts is visually separated by a `── Session N ──` divider so repeated runs stay organised.
- **Scrollable log area** — All cards stack vertically in a scrollable canvas that auto-scrolls to the latest activity.
- **Sequential runs** — Accounts are created one at a time. The next run only starts after the previous captcha is confirmed, keeping the browser load minimal.
- **Runs: 5 per session** — Configurable via the `TOTAL_RUNS` constant at the top of the script.

---

## Dependencies

Install all dependencies with:

```
pip install selenium pynput
```

| Package      | Purpose                              |
|--------------|--------------------------------------|
| `selenium`   | Browser automation (Chrome)          |
| `tkinter`    | GUI — ships with Python, no install  |
| `pynput`     | Keyboard listener (legacy, retained) |
| `subprocess` | macOS `pbcopy` clipboard integration |
| `threading`  | Keeps UI responsive during selenium  |

You also need **ChromeDriver** installed and on your PATH, matching your installed version of Google Chrome.

---

## Email Verification

All accounts are registered under email addresses linked to **Buck's iCloud**. This means:

- Scratch will send verification emails to those addresses.
- **You cannot verify the accounts yourself** — the inboxes are not yours.
- If you need the accounts **email-verified**, contact Buck directly:

  📧 **buckmangrum@gmail.com**

### Alternative — transfer the email yourself

If you'd prefer to handle it independently, you can change the linked email on each account after creation:

1. Log into the Scratch account
2. Go to **Account Settings** (top-right menu)
3. Click the **Email** tab
4. Enter your own email address and save
5. Verify from your own inbox

This fully transfers ownership of the account's email and lets you verify independently without needing to contact Buck.
