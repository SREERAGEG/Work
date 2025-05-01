import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

def load_user_data(path: str = "processed_json.json") -> dict:
    """
    Load user data from a JSON file, falling back to defaults if unavailable.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load {path}: {e}. Using defaults.")
        return {}

def automate_entyvio_form(user: dict):
    # 0. Setup webdriver
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opts)

    def safe_click(locator, by=By.XPATH, tries=3, scroll=True):
        for attempt in range(1, tries + 1):
            try:
                el = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, locator))
                )
                if scroll:
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", el
                    )
                    time.sleep(0.5)
                try:
                    el.click()
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", el)
                return True
            except Exception as e:
                print(f"[{attempt}/{tries}] click failed for {locator}: {e}")
                time.sleep(1)
        print(f"[ERROR] Could not click {locator}")
        return False

    try:
        # 1. Open the form page
        driver.get("https://www.entyvio.com/entyvioconnect-form")
        time.sleep(2)

        # 2. Accept cookies if present
        try:
            cbtn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Accept') or contains(text(),'I agree')]")
                )
            )
            cbtn.click()
            print("Cookies banner accepted.")
        except TimeoutException:
            pass

        # 3-7: Disease / Treatment
        safe_click("//label[@for='UlcerativeColitis']")
        safe_click("//label[@for='TreatmentYes']")
        safe_click("//label[@for='MaintenanceIV']")
        safe_click("//button[@id='saveBtnTreatmentSurveyConnect']")
        time.sleep(2)

        # 8-15: Service selections
        safe_click("//label[@for='ServiceCopay']")
        safe_click("//label[@for='ServiceNurse']")
        safe_click("//label[@for='ServiceSMS']")
        driver.execute_script("window.scrollBy(0,200)")
        safe_click("//label[@for='HaveCommericialInsurance_Yes']")
        safe_click("//label[@for='NoHeathcareProgram_Yes']")
        safe_click("//label[@for='NotSeekReimbursement_Yes']")
        safe_click("//label[@for='RequireEOB_Yes']")
        safe_click("//div[@id='saveBtnServiceType']")
        time.sleep(2)

        # 16-19: Patient contact info
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "FirstName"))
        )
        driver.find_element(By.ID, "FirstName").send_keys(user.get("First_name", "Hari"))
        driver.find_element(By.ID, "LastName").send_keys(user.get("Last_name", "Sachdeva"))
        driver.find_element(By.ID, "Email").send_keys(user.get("Email", "hariwork78@gmail.com"))
        driver.find_element(By.ID, "Phone").send_keys(user.get("Contact_number", "555-123-4567"))

        # 20: Date of Birth — send with slashes so mask reads correctly
        dob = user.get("DOB", "01/16/2003")  # format MM/DD/YYYY
        dob_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'MM/DD/YYYY')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dob_field)
        dob_field.clear()
        dob_field.send_keys(dob)
        time.sleep(0.5)

        # 21: Gender
        gender_map = {"M": "Gender1", "F": "Gender2", "O": "Gender3"}
        gender_id = gender_map.get(user.get("Gender", "M"), "Gender1")
        safe_click(f"//label[@for='{gender_id}']")

        # 22-25: Address
        driver.find_element(By.ID, "Address1").send_keys(user.get("Address", "Powell Street"))
        driver.find_element(By.ID, "Zip").send_keys(user.get("ZIP", "94102"))
        driver.find_element(By.ID, "City").send_keys(user.get("City", "San Francisco"))
        try:
            Select(driver.find_element(By.ID, "State")).select_by_value(user.get("State", "CA"))
        except Exception:
            state = user.get("State", "CA")
            driver.execute_script(
                "document.getElementById('State').value=arguments[0];"
                "document.getElementById('State').dispatchEvent(new Event('change',{bubbles:true}));",
                state
            )
        safe_click("//button[@id='saveBtnContactInfo']")
        time.sleep(2)

        # 27-33: Prescriber info
        driver.find_element(By.ID, "Prescriber_FirstName").send_keys(user.get("Physician_First_Name", "Anoj"))
        driver.find_element(By.ID, "Prescriber_LastName").send_keys(user.get("Physician_Last_Name", "Vishwanathan"))
        driver.find_element(By.ID, "Prescriber_Phone").send_keys(user.get("Phone_Number", "415-555-7890"))
        driver.find_element(By.ID, "Prescriber_Address1").send_keys(user.get("Prescriber_Address", "Powell"))
        driver.find_element(By.ID, "Prescriber_Zip").send_keys(user.get("Prescriber_ZIP_Code", "94102"))
        driver.find_element(By.ID, "Prescriber_City").send_keys(user.get("Prescriber_City", "San Francisco"))
        time.sleep(30)
        try:
            Select(driver.find_element(By.ID, "Prescriber_State")).select_by_value(user.get("Prescriber_State", "CA"))
        except Exception:
            ps = user.get("Prescriber_State", "CA")
            driver.execute_script(
                "document.getElementById('Prescriber_State').value=arguments[0];"
                "document.getElementById('Prescriber_State').dispatchEvent(new Event('change',{bubbles:true}));",
                ps
            )
        safe_click("//div[@id='saveBtnPrescriberInfo']")
        time.sleep(2)

        # 34-36: Digital signature & submit
        driver.find_element(By.ID, "DigitalSignature_FirstName").send_keys(user.get("First_name", "Hari"))
        driver.find_element(By.ID, "DigitalSignature_LastName").send_keys(user.get("Last_name", "Sachdeva"))
        driver.find_element(By.ID, "DigitalSignatureEnrollment_FirstName").send_keys(user.get("First_name", "Hari"))
        driver.find_element(By.ID, "DigitalSignatureEnrollment_LastName").send_keys(user.get("Last_name", "Sachdeva"))
        safe_click("//button[@id='btnConnectSubmit']")
        time.sleep(3)

        print("Form completed successfully!")
        driver.save_screenshot("final_screenshot_entyvio.png")
        print("Browser will remain open for your review.")
        while True:
            time.sleep(60)

    except Exception as e:
        print(f"[ERROR] {e}\nURL: {driver.current_url}")
        try:
            driver.save_screenshot("error_screenshot.png")
        except:
            pass
    finally:
        # driver.quit()  # Uncomment to auto-close when done
        pass

if __name__ == "__main__":
    data = load_user_data()
    automate_entyvio_form(data)
