from __future__ import annotations

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


# ──────────────────────────────────────────────────────────────
# JSON helper
# ──────────────────────────────────────────────────────────────
def load_user_data(path: str = "processed_json.json") -> dict:
    """Return dict with user data or empty dict if file missing/bad."""
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object")
            return data
    except Exception as e:
        print(f"[WARN] Could not load {path}: {e}. Falling back to defaults.")
        return {}


# ──────────────────────────────────────────────────────────────
# Dropdown helper for JCF-styled <select>
# ──────────────────────────────────────────────────────────────
def handle_dropdown_selection(
    driver: webdriver.Chrome,
    wait: WebDriverWait,
    dropdown_id: str,
    option_value: str,
):
    """Robustly set <select> value (JCF wrapper) + trigger change."""
    dropdown = wait.until(EC.presence_of_element_located((By.ID, dropdown_id)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)

    # open visible wrapper if present
    try:
        wrapper = driver.find_element(
            By.XPATH,
            f"//select[@id='{dropdown_id}']/following-sibling::span"
            "[contains(@class,'jcf-select')]/span[contains(@class,'jcf-select-text')]",
        )
        driver.execute_script("arguments[0].click();", wrapper)
    except Exception:
        driver.execute_script("arguments[0].click();", dropdown)

    # set value + dispatch change
    driver.execute_script(
        f"document.getElementById('{dropdown_id}').value='{option_value}';"
        "document.getElementById(arguments[0]).dispatchEvent("
        "new Event('change', {bubbles:true}));",
        dropdown_id,
    )

    # click elsewhere to collapse
    try:
        driver.find_element(By.ID, "FirstName").click()
    except Exception:
        pass

    time.sleep(1)


# ──────────────────────────────────────────────────────────────
def automate_patient_enrollment(user: dict):
    # defaults for any missing keys  ──────────────────────────
    defaults = {
        "First_name": "Hari",
        "Last_name": "Sachdeva",
        "DOB": "01/16/2003",       # MM/DD/YYYY
        "Gender": "M",             # M | F | O
        "Address": "PO 98308",
        "City": "Washington",
        "State": "WA",
        "ZIP": "98101",
        "Email": "hariwork78@gmail.com",
        "Contact_number": "2065551234",
        "Phone_type": "MOBILE",    # MOBILE | HOME | WORK
        "CoPay_SignUp": "No",      # Yes | No
    }
    # merge
    data = {**defaults, **user}

    opts = Options()
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--start-maximized")
    opts.add_experimental_option(
        "prefs",
        {"credentials_enable_service": False, "profile.password_manager_enabled": False},
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=opts
    )
    # driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 10)

    # small util for resilient click
    def safe_click(locator: str, by: By = By.XPATH, tries: int = 3):
        for attempt in range(1, tries + 1):
            try:
                el = wait.until(EC.element_to_be_clickable((by, locator)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.5)
                try:
                    el.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", el)
                return True
            except Exception as exc:
                print(f"[{attempt}/{tries}] click failed for {locator}: {exc}")
                time.sleep(1.5)
        print(f"[ERROR] Could not click {locator}")
        return False

    try:
        # ── 1. open page ───────────────────────────────────
        print("Opening enrollment page …")
        driver.get("https://start.leqvio.com/PatientEnrollment")
        time.sleep(3)

        # ── 2. cookies ─────────────────────────────────────
        try:
            cbtn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Accept') or contains(text(),'I agree')]")
                )
            )
            cbtn.click()
            print("Cookies accepted.")
        except TimeoutException:
            pass

        # ── 3. personal info ───────────────────────────────
        wait.until(EC.element_to_be_clickable((By.ID, "FirstName"))).send_keys(
            data["First_name"]
        )
        wait.until(EC.element_to_be_clickable((By.ID, "LastName"))).send_keys(
            data["Last_name"]
        )
        dob_in = wait.until(EC.element_to_be_clickable((By.ID, "DateOfBirth")))
        dob_in.send_keys(data["DOB"])
        dob_in.send_keys(Keys.ENTER)

        # gender selection
        handle_dropdown_selection(driver, wait, "Gender", data["Gender"].upper())
        print(f"Set Gender to {data['Gender'].upper()}")

        # ── 4. address / contact ───────────────────────────
        wait.until(EC.element_to_be_clickable((By.ID, "AddressLine1"))).send_keys(
            data["Address"]
        )
        wait.until(EC.element_to_be_clickable((By.ID, "City"))).send_keys(data["City"])
        wait.until(EC.element_to_be_clickable((By.ID, "Zip"))).send_keys(data["ZIP"])
        handle_dropdown_selection(driver, wait, "State", data["State"])

        wait.until(EC.element_to_be_clickable((By.ID, "Email"))).send_keys(
            data["Email"]
        )
        wait.until(EC.element_to_be_clickable((By.ID, "Phone"))).send_keys(
            data["Contact_number"]
        )
        handle_dropdown_selection(
            driver, wait, "PhoneType", data["Phone_type"].upper()
        )

        # co-pay signup
        handle_dropdown_selection(
            driver, wait, "incCoPaySignUp", data["CoPay_SignUp"].capitalize()
        )

        # consent check boxes ───────────────────────────────
        for cid in ("incAgreePhoneText", "incAgreeReadAuth"):
            chk = wait.until(EC.presence_of_element_located((By.ID, cid)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", chk)
            if not chk.is_selected():
                try:
                    chk.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", chk)

        # ──────────────────────────────────────────────────
        # Patient Authorization modal
        # ──────────────────────────────────────────────────
        auth_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#modal-patient-auth']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", auth_link)
        auth_link.click()

        wait.until(EC.visibility_of_element_located((By.ID, "inc-patient-auth-form")))
        full_name_field = wait.until(
            EC.element_to_be_clickable((By.ID, "incAuthFullName"))
        )
        full_name_field.clear()
        full_name_field.send_keys(
            data.get("AuthFullName") or f"{data['First_name']} {data['Last_name']}"
        )

        # drag custom scrollbar to bottom
        try:
            handle = driver.find_element(
                By.CSS_SELECTOR, "#modal-patient-auth .jcf-scrollbar-handle"
            )
            slider = driver.find_element(
                By.CSS_SELECTOR, "#modal-patient-auth .jcf-scrollbar-slider"
            )
            ActionChains(driver).click_and_hold(handle).move_by_offset(
                0, slider.size["height"]
            ).release().perform()
        except Exception:
            try:
                scrollable = driver.find_element(
                    By.CSS_SELECTOR, "#modal-patient-auth .jcf-scrollable"
                )
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable
                )
            except Exception:
                pass
        time.sleep(0.7)

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//form[@id='inc-patient-auth-form']//button[contains(text(),'SUBMIT')]")
            )
        ).click()
        wait.until(
            EC.invisibility_of_element_located((By.ID, "inc-patient-auth-form"))
        )

        # ── final submit ──────────────────────────────────
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SUBMIT')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        if submit_btn.get_attribute("disabled"):
            raise RuntimeError("Main SUBMIT button is disabled – check required fields.")
        submit_btn.click()

        time.sleep(5)
        print("\n✅  Form completed successfully!")
        driver.save_screenshot("leqvio_final.png")
        print("Screenshot saved: leqvio_final.png")

    except Exception as e:
        print(f"[ERROR] {e}\nCurrent URL: {driver.current_url}")
        try:
            driver.save_screenshot("leqvio_error.png")
            print("Error screenshot saved: leqvio_error.png")
        except Exception:
            pass
    finally:
        time.sleep(60)
        driver.quit()
        print("Browser closed.")


# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    automate_patient_enrollment(load_user_data())
