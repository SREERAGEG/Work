from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Default values (lowercase keys)
default_data = {
    "firstname": "Hari",
    "lastname": "Sachdeva",
    "email": "hariwork78@gmail.com"
}

# Attempt to load dynamic input data from JSON
try:
    with open('processed_json.json', 'r') as f:
        data = json.load(f)
        print("✅ Loaded JSON data for form inputs.")
except Exception as e:
    print(f"⚠️ Could not load JSON data: {e}. Will use default values.")
    data = {}

def automate_entyvio_form():
    # Setup Chrome driver with options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--headless")  # Uncomment to run headless

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get("https://www.entyvio.com/entyvioconnect-form")
        print("Waiting for page to load...")
        time.sleep(5)
        wait = WebDriverWait(driver, 20)

        handle_popups(driver)
        select_ulcerative_colitis(driver, wait)
        select_no_for_entyvio(driver, wait)
        click_signup_button(driver, wait)
        select_no_for_current_entyvio(driver, wait)
        select_aminosalicylates(driver, wait)
        fill_personal_info(driver, wait)
        check_age_checkbox(driver, wait)
        check_optin_checkbox(driver, wait)
        click_submit_button(driver, wait)

        print("Form submitted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(10)
        driver.quit()

def handle_popups(driver):
    popup_selectors = [
        "//button[contains(text(), 'Accept')]",
        "//button[contains(text(), 'Close')]",
        "//button[contains(text(), 'I agree')]",
        "//button[contains(@class, 'close')]",
        "//div[contains(@class, 'cookie-banner')]//button"
    ]
    for sel in popup_selectors:
        for popup in driver.find_elements(By.XPATH, sel):
            if popup.is_displayed():
                try:
                    popup.click()
                except:
                    driver.execute_script("arguments[0].click();", popup)
                time.sleep(1)

def safe_click(driver, element, wait_time=2):
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        try:
            driver.execute_script("arguments[0].click();", element)
        except:
            try:
                ActionChains(driver).move_to_element(element).click().perform()
            except:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    element
                )
                time.sleep(wait_time)
                driver.execute_script("arguments[0].click();", element)
    time.sleep(wait_time)

def select_ulcerative_colitis(driver, wait):
    selectors = [
        (By.XPATH, "//label[@for='UlcerativeColitis']"),
        (By.ID, "UlcerativeColitis"),
        (By.XPATH, "//input[@id='UlcerativeColitis']"),
        (By.XPATH, "//div[contains(@class, 'radio')]//input[@id='UlcerativeColitis']")
    ]
    for by, sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(2)
            safe_click(driver, el)
            print("✅ Selected Ulcerative Colitis")
            return
        except:
            continue
    driver.execute_script("document.getElementById('UlcerativeColitis').checked = true;")
    time.sleep(2)
    print("✅ Selected Ulcerative Colitis via JS")

def select_no_for_entyvio(driver, wait):
    selectors = [
        (By.XPATH, "//label[@for='TreatmentNo']"),
        (By.ID, "TreatmentNo"),
        (By.XPATH, "//input[@id='TreatmentNo']")
    ]
    for by, sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(2)
            safe_click(driver, el)
            print("✅ Selected 'No' for Entyvio")
            return
        except:
            continue
    driver.execute_script("document.getElementById('TreatmentNo').checked = true;")
    time.sleep(2)
    print("✅ Selected 'No' for Entyvio via JS")

def click_signup_button(driver, wait):
    selectors = [
        (By.XPATH, "//a[contains(text(), 'SIGN UP FOR MORE INFORMATION')]"),
        (By.XPATH, "//a[contains(@class, 'signup') or contains(@class, 'button')]"),
        (By.LINK_TEXT, "SIGN UP FOR MORE INFORMATION")
    ]
    for by, sel in selectors:
        try:
            btn = wait.until(EC.element_to_be_clickable((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(2)
            handle_popups(driver)
            safe_click(driver, btn)
            time.sleep(5)
            print("✅ Clicked sign-up button")
            return
        except:
            continue
    driver.execute_script("""
        var links = document.querySelectorAll('a');
        for (var i = 0; i < links.length; i++) {
            if (links[i].textContent.includes('SIGN UP FOR MORE INFORMATION')) {
                window.location = links[i].href;
                break;
            }
        }
    """)
    time.sleep(5)

def select_no_for_current_entyvio(driver, wait):
    selectors = [
        (By.XPATH, "//label[@for='UseEntyvioNo']"),
        (By.ID, "UseEntyvioNo"),
        (By.XPATH, "//input[@id='UseEntyvioNo']")
    ]
    for by, sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(2)
            safe_click(driver, el)
            print("✅ Selected 'No' for current Entyvio use")
            return
        except:
            continue
    driver.execute_script("document.getElementById('UseEntyvioNo').checked = true;")
    time.sleep(2)
    print("✅ Selected 'No' for current Entyvio via JS")

def select_aminosalicylates(driver, wait):
    selectors = [
        (By.XPATH, "//label[@for='Treatment_Aminosalicylates']"),
        (By.ID, "Treatment_Aminosalicylates"),
        (By.XPATH, "//input[@id='Treatment_Aminosalicylates']")
    ]
    for by, sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(2)
            safe_click(driver, el)
            print("✅ Selected 5-ASAs checkbox")
            return
        except:
            continue
    driver.execute_script("document.getElementById('Treatment_Aminosalicylates').checked = true;")
    time.sleep(2)
    print("✅ Selected 5-ASAs via JS")

def fill_personal_info(driver, wait):
    """Fill in personal information using JSON or defaults"""
    mapping = {
        "FirstName": "firstname",
        "LastName":  "lastname",
        "Email":     "email"
    }
    for field_id, key in mapping.items():
        # Use JSON value if present, else default
        value = data.get(key) or default_data.get(key, "")
        try:
            el = wait.until(EC.presence_of_element_located((By.ID, field_id)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(1)
            el.clear()
            el.send_keys(value)
            print(f"✅ Filled {field_id} with '{value}'")
        except Exception as e:
            print(f"Failed to fill {field_id}: {e}")
            try:
                driver.execute_script(f"document.getElementById('{field_id}').value = '{value}';")
                print(f"✅ Filled {field_id} via JS with '{value}'")
            except:
                pass

def check_age_checkbox(driver, wait):
    selectors = [
        (By.XPATH, "//label[@for='UserIs18']"),
        (By.ID, "UserIs18"),
        (By.XPATH, "//input[@id='UserIs18']")
    ]
    for by, sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(2)
            safe_click(driver, el)
            print("✅ Checked age confirmation box")
            return
        except:
            continue
    driver.execute_script("document.getElementById('UserIs18').checked = true;")
    time.sleep(2)
    print("✅ Checked age box via JS")

def check_optin_checkbox(driver, wait):
    try:
        checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        selectors = [
            (By.XPATH, "//label[@for='OptIn']"),
            (By.ID, "OptIn"),
            (By.NAME, "OptIn"),
            (By.XPATH, "//input[contains(@id, 'opt') or contains(@name, 'opt')]"),
            (By.XPATH, "//label[contains(text(), 'consent') or contains(text(), 'agree')]/preceding-sibling::input[@type='checkbox']")
        ]
        for by, sel in selectors:
            elems = driver.find_elements(by, sel)
            if elems:
                for el in elems:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                    time.sleep(2)
                    if el.tag_name.lower() == 'input':
                        driver.execute_script("arguments[0].checked = true;", el)
                        print("✅ Checked OptIn via JS")
                        return
                    else:
                        safe_click(driver, el)
                        print("✅ Clicked OptIn label")
                        return
        for cb in checkboxes:
            cid = cb.get_attribute('id') or ''
            if any(sub in cid.lower() for sub in ['opt', 'consent', 'agree']):
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cb)
                time.sleep(1)
                driver.execute_script("arguments[0].checked = true;", cb)
                print(f"✅ Checked checkbox ID: {cid}")
                return
    except Exception as e:
        print(f"OptIn selection failed: {e}")
    print("⚠️ Could not conclusively check the OptIn checkbox")

def click_submit_button(driver, wait):
    selectors = [
        (By.ID, "btnSubmit"),
        (By.XPATH, "//button[@id='btnSubmit']"),
        (By.XPATH, "//input[@type='submit']"),
        (By.XPATH, "//button[contains(text(), 'Submit')]"),
        (By.XPATH, "//button[contains(@class, 'submit')]"),
        (By.XPATH, "//input[@value='Submit']")
    ]
    for by, sel in selectors:
        try:
            btn = wait.until(EC.element_to_be_clickable((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(2)
            safe_click(driver, btn)
            print("✅ Clicked submit button")
            return
        except:
            continue
    driver.execute_script("document.querySelector('form').submit();")
    print("✅ Submitted form via JS")

if __name__ == "__main__":
    automate_entyvio_form()
