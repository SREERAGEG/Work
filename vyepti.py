# vyepti_form_automation.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import json
import os


# ─────────────────────────── utilities ─────────────────────────── #
def get_processed_json(path: str = "./processed_json.json") -> dict:
    """
    Loads user-specific data from a JSON file.
    Falls back to an empty dict if the file is missing / malformed.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        print(f"[WARN] Could not load {path}: {exc}")
        return {}


def val(data: dict, key: str, default: str = "") -> str:
    """
    Shorthand to fetch `data[key]` with a sensible default.
    """
    return data.get(key, default)


# ─────────────────────────── main worker ─────────────────────────── #
def automate_vyepti_form(data: dict) -> None:
    download_dir = os.path.abspath("my_downloads")  # or any full path like "/home/user/downloads"

    # Chrome options — disable save-password / address bubbles
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.password_manager_enabled":   False,
        "credentials_enable_service":         False,
        "autofill.profile_enabled":           False,
        "autofill.credit_card_enabled":       False,
        "download.default_directory": download_dir,              # Set custom download folder
        "download.prompt_for_download": False,                   # Don't prompt for download
        "directory_upgrade": True,                               # Allow folder creation
        # "safebrowsing.enabled": True 
    }
    options.add_experimental_option("prefs", prefs)

    driver  = webdriver.Chrome(options=options)
    wait    = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    # ---------- tiny helpers ---------- #
    def js_click(el):
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            el,
        )

    def click_input(input_id):
        el = wait.until(EC.presence_of_element_located((By.ID, input_id)))
        js_click(el)

    # ---------- page 1 ---------- #
    driver.maximize_window()
    driver.get("https://portal.trialcard.com/lundbeck/vyepti/")

    # close cookie banner
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cookie-close"))).click()
    except:
        pass

    # 1) “Healthcare Professional”
    js_click(
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(normalize-space(.),'Healthcare') and "
                    "contains(normalize-space(.),'Professional')]/ancestor::button",
                )
            )
        )
    )

    # 2) State
    time.sleep(5)
    slot = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.v-input__slot[role='combobox']")))
    js_click(slot)
    inp = slot.find_element(By.TAG_NAME, "input")
    inp.send_keys(val(data, "State", "New York"), Keys.ARROW_DOWN, Keys.ENTER)

    # 3) Enrollment-site type
    slot2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='input-61']")))
    js_click(slot2)
    # inp2 = slot2.find_element(By.TAG_NAME, "input")
    slot2.send_keys(val(data, "Site_Type", "Specialty Pharmacy"), Keys.ARROW_DOWN, Keys.ENTER)
    # time.sleep(10)

    # 4) Fax, Phone, Site Name
    page1_fields = [
        ("input-72",  val(data, "Facility_Phone", "(407) 792-6588")),
        ("input-80",  val(data, "Facility_Fax",  "(612) 357-3628")),
        ("input-87",  val(data, "Facility_Name", "Sake Infusion")),
    ]
    for field_id, field_val in page1_fields:
        e = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
        e.clear()
        e.send_keys(field_val)

    # 5) Radio buttons (kept static)
    for rid in ["input-97", "input-108", "input-121", "input-132", "input-143"]:
        click_input(rid)

    # 6) Attestation
    att = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='input-149'] .attestation")))
    js_click(att)

    # 7) Next
    js_click(
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'nextBack') and .//span[normalize-space()='Next']]")
            )
        )
    )
    print("✔️ Page 1 done")

    # ---------- page 2 (patient info) ---------- #
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
    driver.find_element(By.NAME, "firstName").send_keys(val(data, "First_name", "Hari"))
    driver.find_element(By.NAME, "lastName").send_keys(val(data, "Last_name", "Sachdeva"))
    driver.find_element(By.NAME, "dateOfBirth").send_keys(val(data, "DOB", "01/16/2003"))

    # phone
    js_click(
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='phoneRadioOption'][value='2']")  # “Cell”
            )
        )
    )
    driver.find_element(By.NAME, "phone").send_keys(val(data, "Phone", "6189462323"))

    # address
    driver.find_element(By.NAME, "addressOne").send_keys(val(data, "Address", "101 Georgetown"))
    driver.find_element(By.NAME, "zip").send_keys(val(data, "ZIP", "10003"))
    driver.find_element(By.NAME, "city").send_keys(val(data, "City", "New York"))

    # state
    st_inp = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.v-input__slot[role='combobox'] input[name='state']"))
    )
    js_click(st_inp)
    st_inp.send_keys(val(data, "State", "New York"), Keys.ARROW_DOWN, Keys.ENTER)

    # gender
    g_inp = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.v-input__slot[role='combobox'] input[name='gender']"))
    )
    js_click(g_inp)
    g_inp.send_keys(val(data, "Gender", "Male"), Keys.ARROW_DOWN, Keys.ENTER)

    # Next
    js_click(
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'nextBack') and .//span[normalize-space()='Next']]")
            )
        )
    )
    print("✔️ Page 2 done")
    actions.send_keys(Keys.ESCAPE).perform()

    # ---------- page 3 (physician) ---------- #
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.ID, "input-430")))
    driver.find_element(By.ID, "input-430").send_keys(val(data, "Physician_First", "Laura"))
    driver.find_element(By.NAME, "lastName").send_keys(val(data, "Physician_Last", "Mccopin"))
    driver.find_element(By.NAME, "addressOne").send_keys(val(data, "Physician_Address", "607 missouri"))
    driver.find_element(By.NAME, "zip").send_keys(val(data, "Physician_Zip", "77001"))

    # # office & fax
    office_num = val(data, "Office_Phone", "(464) 578-2145")
    driver.find_element(By.NAME, "office").send_keys(office_num)
    fax_num    = val(data, "Fax", "(619) 324-8725")
    driver.find_element(By.NAME, "fax").send_keys(fax_num)
    time.sleep(10)
    # text_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']")))
    # if len(text_inputs) >= 5:
    #     text_inputs[4].send_keys(office_num)
    # if len(text_inputs) >= 6:
    #     text_inputs[5].send_keys(fax_num)

    time.sleep(1)
    js_click(
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'nextBack') and .//span[normalize-space()='Next']]")
            )
        )
    )
    print("✔️ Page 3 done")
    # time.sleep(600)

    # ---------- page 4 (insurance) ---------- #
    time.sleep(5)
    wait.until(EC.visibility_of_element_located((By.NAME, "primaryInsuranceFirstName")))
    # state
    st_ins = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.v-input__slot[role='combobox'] input[name='primaryInsuranceState']")
        )
    )
    js_click(st_ins)
    st_ins.send_keys(val(data, "Insurance_State", "New York"), Keys.ARROW_DOWN, Keys.ENTER)
    time.sleep(2)

    # carrier
    ins_carrier = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.v-input__slot[role='combobox'] input[name='primaryInsuranceCarrier']")
        )
    )
    js_click(ins_carrier)
    time.sleep(0.8)
    ins_carrier.send_keys(val(data, "Insurance_Carrier", "AETNA"), Keys.ARROW_DOWN, Keys.ENTER)

    # names / IDs
    driver.find_element(By.NAME, "primaryInsuranceFirstName").send_keys(
        val(data, "Insurance_First", "John")
    )
    driver.find_element(By.NAME, "primaryInsuranceLastName").send_keys(
        val(data, "Insurance_Last", "Wilson")
    )
    driver.find_element(By.NAME, "primaryInsurancePolicyNumber").send_keys(
        val(data, "Insurance_Policy", "1234567890")
    )
    driver.find_element(By.NAME, "primaryInsuranceGroupNumber").send_keys(
        val(data, "Insurance_Group", "123456")
    )
    # time.sleep(600)

    # # checkboxes
    # if data.get("Secondary_Insurance", True):
    #     js_click(
    #         wait.until(
    #             EC.element_to_be_clickable(
    #                 (
    #                     By.XPATH,
    #                     "//label[contains(text(),'Patient has secondary Medical insurance')]",
    #                 )
    #             )
    #         )
    #     )
    if data.get("No_Prescription_Drug", True):
        js_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='medical_drug_insurance']"))))

    # signature
    driver.find_element(By.ID, "patientSignName").send_keys(val(data, "Patient_Sign", "John Wilson"))

    time.sleep(1)
    # Enroll
    js_click(
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Enroll']")
            )
        )
    )
    print("✔️ Form submitted — success!")
    try:
        time.sleep(20)
        # Download copay info
        js_click(wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='v-btn__content']"))))
        time.sleep(15)
        driver.save_screenshot("vyepti_final.png")
        print("Screenshot saved: vyepti_final.png")
    except:
        print("Error occured in download")

    # keep open for manual confirmation
    input("Press ENTER to close browser…")
    driver.quit()


# ─────────────────────────── run ─────────────────────────── #
if __name__ == "__main__":
    user_data = get_processed_json()
    automate_vyepti_form(user_data)
