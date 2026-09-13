import time
import random
import string
import subprocess
import threading
import tkinter as tk
from tkinter import font as tkfont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

TOTAL_RUNS = 5

EMAILS = [
    "higher-used1y@icloud.com",
    "rivals-hider3g@icloud.com",
    "squarer_charges_4g@icloud.com",
]

BG       = "#0f1117"
PANEL    = "#1a1d27"
BORDER   = "#2a2d3a"
ACCENT   = "#4f8ef7"
ACCENT2  = "#7c5cbf"
TEXT     = "#e2e8f0"
MUTED    = "#8892a4"
SUCCESS  = "#34d399"
COPY_BTN = "#1e293b"
COPY_HOV = "#2d3f5a"
RED      = "#f87171"


# ── helpers ───────────────────────────────────────────────────────────────────

def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    try:
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.communicate(text.encode('utf-8'))
    except Exception:
        pass

def generate_username():
    return f"SCgenerator{random.randint(100000000, 999999999)}"

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def random_email():
    return random.choice(EMAILS)

def random_country():
    countries = [
        "United States","United Kingdom","Afghanistan","Albania","Algeria",
        "American Samoa","Andorra","Angola","Anguilla","Antarctica",
        "Antigua and Barbuda","Argentina","Armenia","Aruba","Australia",
        "Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados",
        "Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia",
        "Bosnia and Herzegovina","Botswana","Brazil","Brunei","Bulgaria",
        "Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde",
        "Cayman Islands","Central African Republic","Chad","Chile","China",
        "Colombia","Comoros","Congo","Cook Islands","Costa Rica","Croatia",
        "Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica",
        "Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea",
        "Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon",
        "Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland",
        "Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti",
        "Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq",
        "Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan",
        "Kenya","Kiribati","Kuwait","Kyrgyzstan","Latvia","Lebanon","Lesotho",
        "Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Madagascar",
        "Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands",
        "Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia",
        "Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru",
        "Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria",
        "Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea",
        "Paraguay","Peru","Philippines","Poland","Portugal","Qatar",
        "Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia",
        "Saint Vincent and the Grenadines","Samoa","San Marino","Saudi Arabia",
        "Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia",
        "Slovenia","Solomon Islands","Somalia","South Africa","South Sudan",
        "Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland",
        "Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tonga",
        "Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu",
        "Uganda","Ukraine","United Arab Emirates","Uruguay","Uzbekistan",
        "Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe",
    ]
    return random.choice(countries)

def random_birth():
    return random.randint(1, 12), random.randint(1904, 2000)

def make_driver():
    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=opts)
    d.execute_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    return d


# ── GUI ───────────────────────────────────────────────────────────────────────

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Scratch Account Generator")
        self.root.configure(bg=BG)
        self.root.geometry("780x680")
        self.root.resizable(True, True)

        self.mono    = tkfont.Font(family="Menlo", size=11)
        self.mono_sm = tkfont.Font(family="Menlo", size=10)
        self.bold    = tkfont.Font(family="Menlo", size=12, weight="bold")
        self.title_f = tkfont.Font(family="Menlo", size=15, weight="bold")

        self._build_header()
        self._build_scroll_area()
        self._build_footer()

        self.session = 0   # incremented each time Start is pressed

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG, pady=14)
        hdr.pack(fill="x", padx=20)
        tk.Label(hdr, text="◈ Scratch Generator", font=self.title_f,
                 bg=BG, fg=ACCENT).pack(side="left")
        self.start_btn = tk.Button(
            hdr, text="▶  Start", font=self.mono,
            bg=ACCENT, fg="#ffffff", relief="flat",
            padx=16, pady=6, cursor="hand2",
            command=self._start
        )
        self.start_btn.pack(side="right")
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

    def _build_scroll_area(self):
        wrapper = tk.Frame(self.root, bg=BG)
        wrapper.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrapper, bg=BG, bd=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview)
        sb.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=sb.set)

        self.scroll_frame = tk.Frame(self.canvas, bg=BG)
        self._cwin = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self._cwin, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

    def _build_footer(self):
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        foot = tk.Frame(self.root, bg=BG, pady=8)
        foot.pack(fill="x", padx=20)
        self.status_lbl = tk.Label(foot, text="Idle — press Start to begin",
                                   font=self.mono_sm, bg=BG, fg=MUTED)
        self.status_lbl.pack(side="left")

    # ── session divider ───────────────────────────────────────────────────────

    def _insert_session_divider(self, session_num):
        wrap = tk.Frame(self.scroll_frame, bg=BG)
        wrap.pack(fill="x", padx=16, pady=(18, 4))
        tk.Frame(wrap, bg=BORDER, height=1).pack(side="left", fill="x", expand=True)
        tk.Label(wrap, text=f"  Session {session_num}  ",
                 font=self.mono_sm, bg=BG, fg=MUTED).pack(side="left")
        tk.Frame(wrap, bg=BORDER, height=1).pack(side="left", fill="x", expand=True)

    # ── per-account panel (created once per run, on the main thread) ──────────

    def _create_panel(self, run):
        """Build the card shell and return an info dict. Called via root.after."""
        outer = tk.Frame(self.scroll_frame, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="x", padx=16, pady=(12, 0))

        # purple header bar
        hbar = tk.Frame(outer, bg=ACCENT2)
        hbar.pack(fill="x")
        tk.Label(hbar, text=f"  Account {run} / {TOTAL_RUNS}",
                 font=self.bold, bg=ACCENT2, fg="#ffffff", pady=6).pack(side="left")
        status_dot = tk.Label(hbar, text="● Running",
                              font=self.mono_sm, bg=ACCENT2, fg="#fcd34d", padx=10)
        status_dot.pack(side="right")

        body = tk.Frame(outer, bg=PANEL, padx=16, pady=12)
        body.pack(fill="x")

        # log box
        log = tk.Text(body, font=self.mono_sm, bg="#0d1018", fg=TEXT,
                      relief="flat", height=5, state="disabled",
                      insertbackground=TEXT, wrap="word",
                      highlightbackground=BORDER, highlightthickness=1)
        log.pack(fill="x")

        return {"outer": outer, "body": body, "status_dot": status_dot, "log": log}

    def _append_credentials(self, info, username, password, email):
        """Add credential rows + divider into body. Called via root.after."""
        body = info["body"]

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(10, 6))

        def make_row(label, value, copyable):
            row = tk.Frame(body, bg=PANEL)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label:<10}", font=self.mono_sm,
                     bg=PANEL, fg=MUTED, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=self.mono,
                     bg=PANEL, fg=TEXT, anchor="w").pack(side="left", padx=(4, 8))
            if copyable:
                btn = tk.Button(
                    row, text="Copy", font=self.mono_sm,
                    bg=COPY_BTN, fg=ACCENT, relief="flat",
                    padx=8, pady=2, cursor="hand2",
                    command=lambda v=value: self._flash_copy(btn, v)
                )
                btn.pack(side="left")
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COPY_HOV))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COPY_BTN))

        make_row("Username", username, copyable=True)
        make_row("Password", password, copyable=True)
        make_row("Email",    email,    copyable=False)

    def _append_captcha_gate(self, info, event):
        """Add the captcha confirm row. Called via root.after."""
        body = info["body"]
        gate = tk.Frame(body, bg=PANEL)
        gate.pack(fill="x", pady=(8, 0))

        lbl = tk.Label(gate,
                       text="⚠  Solve captcha in browser, then press Confirm",
                       font=self.mono_sm, bg=PANEL, fg="#fcd34d")
        lbl.pack(side="left")

        def confirm():
            event.set()
            btn.config(state="disabled", text="✓ Confirmed", fg=SUCCESS, bg=COPY_BTN)
            lbl.config(text="Captcha confirmed.", fg=MUTED)

        btn = tk.Button(gate, text="Confirm →", font=self.mono_sm,
                        bg=ACCENT, fg="#ffffff", relief="flat",
                        padx=10, pady=3, cursor="hand2",
                        command=confirm)
        btn.pack(side="right")

    # ── small UI helpers ──────────────────────────────────────────────────────

    def _flash_copy(self, btn, value):
        copy_to_clipboard(self.root, value)
        btn.config(text="✓ Copied", fg=SUCCESS)
        self.root.after(1200, lambda: btn.config(text="Copy", fg=ACCENT))

    def _log(self, info, msg):
        w = info["log"]
        w.config(state="normal")
        w.insert("end", msg + "\n")
        w.config(state="disabled")
        w.see("end")
        self.root.after(50, lambda: self.canvas.yview_moveto(1.0))

    def _set_status(self, info, text, color):
        info["status_dot"].config(text=f"● {text}", fg=color)

    def _ui_status(self, msg):
        self.status_lbl.config(text=msg)

    # ── selenium ──────────────────────────────────────────────────────────────

    def _signup(self, driver, info):
        wait = WebDriverWait(driver, 5)

        self._log(info, "→ Opening scratch.mit.edu ...")
        driver.get("https://scratch.mit.edu/")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Join Scratch"))).click()

        username = generate_username()
        password = generate_password()
        email    = random_email()

        self._log(info, f"→ Username: {username}")
        self._log(info, f"→ Password: {password}")
        self._log(info, f"→ Email:    {email}")

        # step 1 — credentials
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        pw_confirm = wait.until(EC.presence_of_element_located((By.NAME, "passwordConfirm")))
        pw_confirm.send_keys(password)

        clicked = False
        for sel in ["button[type='submit']", "button.modal-flush-bottom-button",
                    ".join-flow-next-button", "button.button"]:
            try:
                b = driver.find_element(By.CSS_SELECTOR, sel)
                if b.is_displayed() and b.is_enabled():
                    b.click(); clicked = True; break
            except Exception:
                pass
        if not clicked:
            pw_confirm.send_keys(Keys.ENTER)

        # step 2 — country
        self._log(info, "→ Selecting country ...")
        Select(wait.until(EC.element_to_be_clickable((By.ID, "country")))).select_by_visible_text(random_country())
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-flush-bottom-button"))).click()

        # step 3 — birth
        self._log(info, "→ Setting birth date ...")
        month, year = random_birth()
        Select(wait.until(EC.element_to_be_clickable((By.ID, "birth_month")))).select_by_value(str(month))
        Select(wait.until(EC.element_to_be_clickable((By.ID, "birth_year")))).select_by_value(str(year))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-flush-bottom-button"))).click()

        # step 4 — gender
        self._log(info, "→ Selecting gender ...")
        wait.until(EC.element_to_be_clickable((By.ID, "GenderRadioOptionPreferNot"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-flush-bottom-button"))).click()

        # step 5 — email + TOS
        self._log(info, "→ Entering email + TOS ...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))).send_keys(email)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "tos"))).click()
        except Exception:
            pass
        for b in driver.find_elements(By.TAG_NAME, "button"):
            if b.is_displayed() and b.is_enabled():
                try: b.click(); break
                except Exception: pass

        time.sleep(1)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.modal-flush-bottom-button[type='submit']")
            )).click()
            time.sleep(3)
        except Exception:
            pass

        self._log(info, "⚡ Signup flow complete.")
        return username, password, email

    # ── run loop ──────────────────────────────────────────────────────────────

    def _start(self):
        self.session += 1
        self.start_btn.config(state="disabled", text="Running...")
        self._insert_session_divider(self.session)
        threading.Thread(target=self._run_all, daemon=True).start()

    def _run_all(self):
        for run in range(1, TOTAL_RUNS + 1):
            self.root.after(0, lambda: self._ui_status(f"Run {run}/{TOTAL_RUNS} — starting ..."))

            # create panel on main thread, wait for it
            ready = threading.Event()
            panel_holder = [None]

            def make_panel(r=run, h=panel_holder, e=ready):
                h[0] = self._create_panel(r)
                e.set()

            self.root.after(0, make_panel)
            ready.wait()
            info = panel_holder[0]

            driver = make_driver()
            try:
                username, password, email = self._signup(driver, info)

                # add credential rows on main thread
                self.root.after(0, lambda u=username, p=password, em=email:
                                self._append_credentials(info, u, p, em))

                # captcha gate
                event = threading.Event()
                self.root.after(0, lambda e=event: self._append_captcha_gate(info, e))
                self.root.after(0, lambda: self._set_status(info, "Waiting for captcha", "#fcd34d"))
                self.root.after(0, lambda: self._ui_status(f"Run {run}/{TOTAL_RUNS} — waiting for captcha"))
                event.wait()

                self._log(info, "✓ Account confirmed created.")
                self.root.after(0, lambda: self._set_status(info, "Done", SUCCESS))
                self.root.after(0, lambda: self._ui_status(f"Run {run}/{TOTAL_RUNS} — complete"))

            except Exception as e:
                self._log(info, f"✗ Error: {e}")
                self.root.after(0, lambda: self._set_status(info, "Error", RED))
            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

        self.root.after(0, lambda: self._ui_status("All runs complete."))
        self.root.after(0, lambda: self.start_btn.config(state="normal", text="▶  Start Again"))


# ── entry ─────────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
