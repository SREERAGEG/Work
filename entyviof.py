from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
import json


def automate_entyvio_form(processed_json):
    # Set up the webdriver with options to maximize window
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start with browser maximized
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the base URL
        print("Navigating to the website...")
        driver.get("https://www.entyvio.com/entyvioconnect-form")
        
        # Wait for page to load
        time.sleep(3)
        
        # Accept cookies if necessary (depends on the website)
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]"))
            )
            cookie_button.click()
            print("Accepted cookies.")
        except TimeoutException:
            print("No cookie consent prompt found or already accepted.")
        
        # Helper function to click elements with retry and JavaScript fallback
        def safe_click(element_locator, locator_type=By.XPATH, max_attempts=3, scroll_first=True):
            attempts = 0
            while attempts < max_attempts:
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((locator_type, element_locator))
                    )
                    
                    if scroll_first:
                        # Scroll element into view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(1)
                    
                    try:
                        element.click()
                        return True
                    except ElementClickInterceptedException:
                        # Try using JavaScript to click
                        print(f"Using JavaScript to click element: {element_locator}")
                        driver.execute_script("arguments[0].click();", element)
                        return True
                        
                except Exception as e:
                    print(f"Attempt {attempts+1} failed for {element_locator}: {e}")
                    attempts += 1
                    time.sleep(2)
            
            print(f"Failed to click element after {max_attempts} attempts: {element_locator}")
            return False
        
        # Step 1: Click the "Ulcerative Colitis" label
        print("Selecting 'Ulcerative Colitis'...")
        safe_click("//label[@for='UlcerativeColitis']")
        time.sleep(2)
        
        # Step 2: Click "Yes" for "Are you currently taking or about to start taking ENTYVIO?"
        print("Selecting 'Yes' for currently taking ENTYVIO...")
        safe_click("//label[@for='TreatmentYes']")
        time.sleep(2)
        
        # Step 3: Click "IV Infusions" for "Which ENTYVIO maintenance option were you prescribed?"
        print("Selecting 'IV Infusions' for maintenance option...")
        safe_click("//label[@for='MaintenanceIV']")
        time.sleep(2)
        
        # Step 4: Click the "Save & Continue" button on first page
        print("Clicking 'Save & Continue' on first page...")
        safe_click("//button[@id='saveBtnTreatmentSurveyConnect']")
        time.sleep(4)  # Longer wait for page transition
        
        # Step 5: Click the "Co-Pay & Insurance Help" checkbox
        print("Selecting 'Co-Pay & Insurance Help' option...")
        safe_click("//label[@for='ServiceCopay']")
        time.sleep(2)
        
        # Step 6: Click the "Connect with a Nurse Educator" checkbox
        print("Selecting 'Connect with a Nurse Educator' option...")
        safe_click("//label[@for='ServiceNurse']")
        time.sleep(2)
        
        # Step 7: Click the "Text Message Treatment Reminders" checkbox
        print("Selecting 'Text Message Treatment Reminders' option...")
        safe_click("//label[@for='ServiceSMS']")
        time.sleep(2)
        
        # Explicitly scroll down to ensure next elements are visible
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        # Step 8: Click "Yes" for "Do you have commercial insurance?"
        print("Selecting 'Yes' for commercial insurance...")
        safe_click("//label[@for='HaveCommericialInsurance_Yes']", scroll_first=True)
        time.sleep(2)
        
        # Step 9: Click "Yes" for healthcare program question
        print("Selecting 'Yes' for healthcare program...")
        safe_click("//label[@for='NoHeathcareProgram_Yes']", scroll_first=True)
        time.sleep(2)
        
        # Step 10: Click "Yes" for seek reimbursement question
        print("Selecting 'Yes' for not seeking reimbursement...")
        safe_click("//label[@for='NotSeekReimbursement_Yes']", scroll_first=True)
        time.sleep(2)
        
        # Step 11: Click "Yes" for EOB requirement
        print("Selecting 'Yes' for EOB requirement...")
        safe_click("//label[@for='RequireEOB_Yes']", scroll_first=True)
        time.sleep(2)
        
        # Step 12: Click the final "Save & Continue" button
        print("Clicking the final 'Save & Continue' button...")
        safe_click("//div[@id='saveBtnServiceType']", scroll_first=True)
        time.sleep(4)  # Longer wait for page transition
        
        # Wait for the personal information page to load
        print("Waiting for personal information page to load...")
        
        # Step 13: Fill in First Name
        print("Filling in First Name...")
        first_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "FirstName"))
        )
        first_name_field.clear()
        first_name_field.send_keys(processed_json["First_name"] if processed_json["First_name"] else "Hari")
        time.sleep(2)
        
        # Step 14: Fill in Last Name
        print("Filling in Last Name...")
        last_name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "LastName"))
        )
        last_name_field.clear()
        last_name_field.send_keys(processed_json["Last_name"] if processed_json["Last_name"] else "Sachdeva")
        
        # Step 15: Fill in Email
        print("Filling in Email...")
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        email_field.clear()
        email_field.send_keys(processed_json["Email"] if processed_json["Email"] else "hariwork78@gmail.com")
        
        # Step 16: Fill in Phone Number (random US number)
        print("Filling in Phone Number...")
        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Phone"))
        )
        phone_field.clear()
        phone_field.send_keys(processed_json["Contact_number"] if processed_json["Contact_number"] else "555-123-4567")  # Random US format phone number
        
        # Step 17: Fill in Birth Date - Enhanced approach
        print("Filling in Birth Date using enhanced methods...")
        
        # Find all possible date fields
        date_field_selectors = [
            "//input[@id='BirthDate']",
            "//input[@id='date_of_birth']",
            "//input[contains(@class, 'masked')]",
            "//input[contains(@placeholder, 'MM/DD/YYYY')]",
            "//input[contains(@name, 'Birth')]",
            "//input[contains(@name, 'birth')]"
        ]
        
        date_filled = False
        
        for selector in date_field_selectors:
            if date_filled:
                break
                
            try:
                date_field = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                print(f"Found date field using selector: {selector}")
                
                # Scroll to make sure it's visible
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_field)
                time.sleep(1)
                
                # Try various methods to set the date
                methods = [
                    {"name": "Direct input", "func": lambda: date_field.send_keys("01162003")},
                    {"name": "Formatted input with tab", "func": lambda: [date_field.send_keys("01/16/2003"), date_field.send_keys(Keys.TAB)]},
                    {"name": "Digit by digit", "func": lambda: [date_field.send_keys(d) and time.sleep(0.1) for d in "01162003"]},
                    {"name": "JavaScript with events", "func": lambda: driver.execute_script("""
                        arguments[0].value = '01/16/2003';
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
                    """, date_field)}
                ]
                
                for method in methods:
                    if date_filled:
                        break
                    
                    try:
                        date_field.clear()
                        method["func"]()
                        time.sleep(1)
                        
                        value = date_field.get_attribute("value")
                        if "01" in value and "16" in value and "2003" in value:
                            print(f"Successfully filled date with {method['name']}: {value}")
                            date_filled = True
                            break
                    except Exception as e:
                        print(f"{method['name']} failed: {e}")
                    
            except Exception as e:
                print(f"Selector {selector} failed: {e}")
                
        if not date_filled:
            print("WARNING: Could not fill date field with any method!")
        
        # Step 18: Select "Male" for gender
        print("Selecting 'Male' for gender...")
        safe_click("//label[@for='Gender1']", scroll_first=True)
        time.sleep(1)
        
        # Step 19: Fill in Address Line 1 with Powell Street
        print("Filling in Address Line 1...")
        address_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Address1"))
        )
        address_field.clear()
        address_field.send_keys(processed_json["Address"] if processed_json["Address"] else "Powell Street")
        time.sleep(1)
        
        # Step 20: Fill in ZIP Code (valid San Francisco zipcode)
        print("Filling in ZIP Code...")
        zip_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Zip"))
        )
        zip_field.clear()
        zip_field.send_keys(processed_json["ZIP"] if processed_json["ZIP"] else "94102")  # Valid San Francisco zipcode
        time.sleep(1)
        
        # Step 21: Fill in City as San Francisco
        print("Filling in City...")
        city_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "City"))
        )
        city_field.clear()
        city_field.send_keys(processed_json["City"] if processed_json["City"] else "San Francisco")
        time.sleep(1)
        
        # Step 22: Select CA from State dropdown
        print("Selecting state CA...")
        try:
            # Try using the select dropdown
            state_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "State"))
            )
            # Scroll to dropdown
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_dropdown)
            time.sleep(1)
            
            # Use Select class to select by value
            Select(state_dropdown).select_by_value(processed_json["State"] if processed_json["State"] else "CA")
            time.sleep(1)
            
            print(f"Selected {processed_json["State"]}/CA from dropdown")
        except Exception as e:
            print(f"Standard dropdown selection failed: {e}")
            
            # Fallback method using JavaScript
            try:
                driver.execute_script("document.getElementById('State').value = 'CA';")
                driver.execute_script("""
                    var element = document.getElementById('State');
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """)
                print("Selected CA using JavaScript")
            except Exception as e:
                print(f"JavaScript state selection failed: {e}")
        
        # Step 23: Click the "Save & Continue" button after filling contact info
        print("Clicking 'Save & Continue' button after contact info...")
        safe_click("//button[@id='saveBtnContactInfo']", scroll_first=True)
        time.sleep(4)  # Longer wait for page transition
        
        # Wait for prescriber information page to load
        print("Waiting for prescriber information page to load...")
        time.sleep(2)
        
        # Step 24: Fill in Prescriber's First Name
        print("Filling in Prescriber's First Name...")
        prescriber_first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_FirstName"))
        )
        prescriber_first_name.clear()
        # prescriber_first_name.send_keys(processed_json[""] if processed_json[""] else "Anoj")
        prescriber_first_name.send_keys("Anoj")
        time.sleep(1)
        
        # Step 25: Fill in Prescriber's Last Name
        print("Filling in Prescriber's Last Name...")
        prescriber_last_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_LastName"))
        )
        prescriber_last_name.clear()
        # prescriber_last_name.send_keys(processed_json[""] if processed_json[""] else "Vishwanathan")
        prescriber_last_name.send_keys("Vishwanathan")
        time.sleep(1)
        
        # Step 26: Fill in Prescriber's Phone Number
        print("Filling in Prescriber's Phone Number...")
        prescriber_phone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_Phone"))
        )
        prescriber_phone.clear()
        # prescriber_phone.send_keys(processed_json[""] if processed_json[""] else "415-555-7890")  # Valid US format number
        prescriber_phone.send_keys("415-555-7890")  # Valid US format number
        time.sleep(1)
        
        # Step 27: Fill in Prescriber's Address Line 1
        print("Filling in Prescriber's Address...")
        prescriber_address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_Address1"))
        )
        prescriber_address.clear()
        # prescriber_address.send_keys(processed_json[""] if processed_json[""] else "Powell")
        prescriber_address.send_keys("Powell")
        time.sleep(1)
        
        # Step 28: Fill in Prescriber's ZIP Code
        print("Filling in Prescriber's ZIP Code...")
        prescriber_zip = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_Zip"))
        )
        prescriber_zip.clear()
        # prescriber_zip.send_keys(processed_json[""] if processed_json[""] else "94102")  # Valid San Francisco zipcode
        prescriber_zip.send_keys("94102")  # Valid San Francisco zipcode
        time.sleep(1)
        
        # Step 29: Fill in Prescriber's City
        print("Filling in Prescriber's City...")
        prescriber_city = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Prescriber_City"))
        )
        prescriber_city.clear()
        # prescriber_city.send_keys(processed_json[""] if processed_json[""] else "San Francisco")
        prescriber_city.send_keys("San Francisco")
        time.sleep(1)
        
        # Step 30: Select CA from Prescriber's State dropdown
        print("Selecting Prescriber's state CA...")
        try:
            # Try using the select dropdown
            prescriber_state_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "Prescriber_State"))
            )
            # Scroll to dropdown
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", prescriber_state_dropdown)
            time.sleep(1)
            
            # Use Select class to select by value
            Select(prescriber_state_dropdown).select_by_value("CA")
            time.sleep(1)
            
            print("Selected CA from prescriber state dropdown")
        except Exception as e:
            print(f"Prescriber state dropdown selection failed: {e}")
            
            # Fallback method using JavaScript
            try:
                driver.execute_script("document.getElementById('Prescriber_State').value = 'CA';")
                driver.execute_script("""
                    var element = document.getElementById('Prescriber_State');
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """)
                print("Selected CA for prescriber state using JavaScript")
            except Exception as e:
                print(f"JavaScript prescriber state selection failed: {e}")
        
        # Step 31: Click the "Save & Continue" button after filling prescriber info
        print("Clicking 'Save & Continue' button after prescriber info...")
        safe_click("//div[@id='saveBtnPrescriberInfo']", scroll_first=True)
        time.sleep(4)  # Longer wait for page transition
        
        # Wait for digital signature page to load
        print("Waiting for digital signature page to load...")
        time.sleep(2)
        
        # Step 32: Fill in Digital Signature First Name
        print("Filling in Digital Signature First Name...")
        dig_sig_first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DigitalSignature_FirstName"))
        )
        dig_sig_first_name.clear()
        dig_sig_first_name.send_keys(processed_json["First_name"] if processed_json["First_name"] else "Hari")
        time.sleep(1)
        
        # Step 33: Fill in Digital Signature Last Name
        print("Filling in Digital Signature Last Name...")
        dig_sig_last_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DigitalSignature_LastName"))
        )
        dig_sig_last_name.clear()
        dig_sig_last_name.send_keys(processed_json["Last_name"] if processed_json["Last_name"] else "Sachdeva")
        time.sleep(1)
        
        # Step 34: Fill in Digital Signature Enrollment First Name
        print("Filling in Digital Signature Enrollment First Name...")
        dig_sig_enroll_first_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DigitalSignatureEnrollment_FirstName"))
        )
        dig_sig_enroll_first_name.clear()
        dig_sig_enroll_first_name.send_keys(processed_json["First_name"] if processed_json["First_name"] else "Hari")
        time.sleep(1)
        
        # Step 35: Fill in Digital Signature Enrollment Last Name
        print("Filling in Digital Signature Enrollment Last Name...")
        dig_sig_enroll_last_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DigitalSignatureEnrollment_LastName"))
        )
        dig_sig_enroll_last_name.clear()
        dig_sig_enroll_last_name.send_keys(processed_json["Last_name"] if processed_json["Last_name"] else "Sachdeva")
        time.sleep(1)
        
        # Step 36: Click the "Continue" button
        print("Clicking the 'Continue' button...")
        safe_click("//button[@id='btnConnectSubmit']", scroll_first=True)
        time.sleep(4)  # Longer wait for page transition
        
        # Wait to see the result
        print("Form completed successfully!")
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Current URL: {driver.current_url}")
        
        # Take screenshot on error
        try:
            driver.save_screenshot("error_screenshot.png")
            print("Screenshot saved as error_screenshot.png")
        except:
            print("Failed to save screenshot")
    
    finally:
        try:
            driver.save_screenshot("final_screenshot_entyvio.png")
            print("Screenshot saved as final_screenshot_entyvio.png")
        except:
            print("Failed to save screenshot")

        # Close the browser
        driver.quit()
        print("Browser closed.")

def get_processed_json():
    try:
        with open("./processed_json.json","r") as file:
        # Sample json format : {"First_name": "Aevy", "Last_name": "Jackson", "Address": "A803", "City": "Dover", "State": "Delaware", "ZIP": "19901", "Contact_number": "+1 6193248725", "Email": "anoj.viswanathan@gmail.com", "Medical_Insurance_Name": "Aetna", "Primary_Insurance_Member_ID": "5676532q"}
            return json.load(file)
    except:
        print("Load json file failed")

if __name__ == "__main__":
    automate_entyvio_form(get_processed_json())