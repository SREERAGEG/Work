from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
import json


# Create a function to handle dropdown selections
def handle_dropdown_selection(driver, wait, dropdown_id, option_value, option_text):
    """
    Function to handle the custom dropdown selections
    
    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        dropdown_id: ID of the dropdown element
        option_value: Value attribute of the option to select
        option_text: Visible text of the option to select
    """
    # Find the dropdown element
    dropdown = wait.until(EC.presence_of_element_located((By.ID, dropdown_id)))
    
    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
    time.sleep(1)
    
    # First try clicking on the custom jcf wrapper to open the dropdown
    try:
        # Find the custom jcf-select-text span element that's visible to users
        jcf_select_element = driver.find_element(
            By.XPATH, f"//select[@id='{dropdown_id}']/following-sibling::span[contains(@class, 'jcf-select')]/span[contains(@class, 'jcf-select-text')]"
        )
        driver.execute_script("arguments[0].click();", jcf_select_element)
        print(f"Clicked on {dropdown_id} dropdown wrapper")
        time.sleep(1)
    except Exception as e:
        print(f"Could not click on jcf wrapper: {e}")
        # Try clicking directly on the select element as fallback
        try:
            driver.execute_script("arguments[0].click();", dropdown)
            print(f"Clicked on {dropdown_id} dropdown directly")
            time.sleep(1)
        except Exception as e2:
            print(f"Could not click dropdown directly: {e2}")
    
    # Now select the option using JavaScript to set the value directly
    try:
        driver.execute_script(f"document.getElementById('{dropdown_id}').value = '{option_value}';")
        # Trigger change event to ensure UI updates
        driver.execute_script(f"var event = new Event('change'); document.getElementById('{dropdown_id}').dispatchEvent(event);")
        print(f"Set {dropdown_id} value to '{option_value}' via JavaScript")
        
        # Also try to click the option directly if it's visible
        try:
            # Click on the specific option if it's visible in the dropdown
            option_element = driver.find_element(
                By.XPATH, f"//select[@id='{dropdown_id}']/option[@value='{option_value}']"
            )
            driver.execute_script("arguments[0].selected = true;", option_element)
            print(f"Selected {option_text} option directly")
        except Exception as e:
            print(f"Could not select option directly: {e}")
            # Try to find and click any element with the option text
            try:
                text_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{option_text}')]")
                if text_elements:
                    for elem in text_elements:
                        try:
                            elem.click()
                            print(f"Clicked element with text {option_text}")
                            break
                        except:
                            continue
            except Exception as e2:
                print(f"Could not find text elements: {e2}")
    except Exception as e:
        print(f"Failed to set {dropdown_id} value: {e}")
    
    # Click elsewhere to close the dropdown
    try:
        first_name_field = driver.find_element(By.ID, "FirstName")
        first_name_field.click()
        print(f"Clicked elsewhere to close {dropdown_id} dropdown")
    except:
        pass
    
    # Verify the selection
    try:
        # Check the selected value
        selected_value = driver.execute_script(f"return document.getElementById('{dropdown_id}').value;")
        print(f"Current {dropdown_id} value: {selected_value}")
        
        # Check displayed text
        try:
            selected_text = driver.find_element(
                By.XPATH, f"//select[@id='{dropdown_id}']/following-sibling::span[contains(@class, 'jcf-select')]/span[contains(@class, 'jcf-select-text')]"
            ).text
            print(f"Displayed {dropdown_id} text: {selected_text}")
        except:
            print(f"Could not get displayed text for {dropdown_id}")
    except Exception as e:
        print(f"Could not verify {dropdown_id} selection: {e}")
    
    # Give the page a moment to update
    time.sleep(1)


def automate_patient_enrollment(processed_json):
    # Set up Chrome options
    chrome_options = Options()
    # Add window size to ensure elements are visible
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    # Disable the "Save password?" prompt
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    # Uncomment the line below if you want to run in headless mode (no browser UI)
    # chrome_options.add_argument("--headless=new")
    
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Set an implicit wait to give elements time to appear
    driver.implicitly_wait(10)
    # Set page load timeout
    driver.set_page_load_timeout(30)
    
    try:
        # Navigate to the enrollment page
        driver.get("https://start.leqvio.com/PatientEnrollment")
        print("Navigated to the enrollment page")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Fill in First Name
        first_name_field = wait.until(EC.element_to_be_clickable((By.ID, "FirstName")))
        first_name_field.clear()
        first_name_field.send_keys(processed_json["First_name"] if processed_json["First_name"] else "hari")
        print("Filled in First Name")
        
        # Fill in Last Name
        last_name_field = wait.until(EC.element_to_be_clickable((By.ID, "LastName")))
        last_name_field.clear()
        last_name_field.send_keys(processed_json["Last_name"] if processed_json["Last_name"] else "sachdeva")
        print("Filled in Last Name")
        
        # Fill in Date of Birth
        dob_field = wait.until(EC.element_to_be_clickable((By.ID, "DateOfBirth")))
        dob_field.clear()
        # dob_field.send_keys(processed_json[""] if processed_json[""] else "01/16/2003")
        dob_field.send_keys("01/16/2003")
        print("Filled in Date of Birth")
        
        # Press ENTER to exit the date field
        dob_field.send_keys(Keys.ENTER)
        print("Pressed ENTER to exit the date field")
        
        # Add a short wait to allow any field validation to complete
        time.sleep(2)
        
        # Make sure the page is scrolled to the Gender dropdown
        gender_dropdown = wait.until(EC.presence_of_element_located((By.ID, "Gender")))
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_dropdown)
        time.sleep(1)  # Give the page time to scroll
        
        # First, click on the dropdown to open it (we'll try multiple approaches)
        try:
            # Try clicking on the jcf-select-text span which is the visible part of the dropdown
            jcf_select = driver.find_element(By.XPATH, "//span[contains(@class, 'jcf-select-text')]")
            driver.execute_script("arguments[0].click();", jcf_select)
            print("Clicked on jcf-select-text span")
        except Exception as e:
            print(f"Failed to click jcf-select-text: {e}")
            try:
                # Try clicking the actual select element
                driver.execute_script("arguments[0].click();", gender_dropdown)
                print("Clicked on Gender dropdown using JavaScript")
            except Exception as e2:
                print(f"Failed to click with JavaScript: {e2}")
        
        # Wait for dropdown to open
        time.sleep(2)
        
        # Now directly select the option with value="M" using JavaScript
        # This bypasses the custom dropdown UI and sets the value directly
        try:
            driver.execute_script("document.getElementById('Gender').value = 'M';")
            # Trigger change event to ensure the UI updates
            driver.execute_script("var event = new Event('change'); document.getElementById('Gender').dispatchEvent(event);")
            print("Set Gender value to 'M' and triggered change event")
            
            # Additionally, try to click the actual Male option if it's visible
            try:
                male_option = driver.find_element(By.XPATH, "//option[@value='M']")
                driver.execute_script("arguments[0].selected = true;", male_option)
                print("Set Male option to selected=true")
            except Exception as opt_err:
                print(f"Could not directly select option: {opt_err}")
        except Exception as e:
            print(f"Failed to set Gender value: {e}")
            # As a last resort, try clicking any element with 'Male' text
            try:
                male_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Male')]")
                if male_elements:
                    for elem in male_elements:
                        try:
                            elem.click()
                            print(f"Clicked element with text Male: {elem.tag_name}")
                            break
                        except:
                            continue
            except Exception as click_err:
                print(f"Failed to click Male elements: {click_err}")
        
        # After selection attempt, click elsewhere to close the dropdown
        try:
            # Click on a safe element outside the dropdown
            first_name_field = driver.find_element(By.ID, "FirstName")
            first_name_field.click()
            print("Clicked elsewhere to close dropdown")
        except:
            pass
        
        # Fill in Address Line 1 - use the same scroll and click approach
        address_field = wait.until(EC.presence_of_element_located((By.ID, "AddressLine1")))
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", address_field)
        time.sleep(1)  # Give the page time to scroll
        
        # Try multiple approaches to interact with the field
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "AddressLine1")))
            address_field.clear()
            address_field.send_keys(processed_json["Address"] if processed_json["Address"] else "PO 98308")
            print("Filled in Address Line 1")
        except Exception as e:
            print(f"Standard approach for Address failed: {e}")
            try:
                # Try JavaScript to set the value
                driver.execute_script("arguments[0].value = 'PO 98308';", address_field)
                print("Filled in Address Line 1 using JavaScript")
            except Exception as js_error:
                print(f"JavaScript approach for Address failed: {js_error}")
        
        # Fill in City - use the same approach
        city_field = wait.until(EC.presence_of_element_located((By.ID, "City")))
        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_field)
        time.sleep(1)  # Give the page time to scroll
        
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "City")))
            city_field.clear()
            city_field.send_keys(processed_json["City"] if processed_json["City"] else "Washington")
            print("Filled in City")
        except Exception as e:
            print(f"Standard approach for City failed: {e}")
            try:
                # Try JavaScript to set the value
                driver.execute_script("arguments[0].value = 'Washington';", city_field)
                print("Filled in City using JavaScript")
            except Exception as js_error:
                print(f"JavaScript approach for City failed: {js_error}")
        
        # Handle State dropdown selection
        handle_dropdown_selection(driver, wait, "State", "WA", "Washington")
        
        # Fill in ZIP Code
        zip_field = wait.until(EC.element_to_be_clickable((By.ID, "Zip")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", zip_field)
        time.sleep(1)
        zip_field.clear()
        zip_field.send_keys(processed_json["ZIP"] if processed_json["ZIP"] else "98101")  # Valid Washington ZIP code
        print("Filled in ZIP Code")
        
        # Fill in Email
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "Email")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", email_field)
        time.sleep(1)
        email_field.clear()
        email_field.send_keys(processed_json["Email"] if processed_json["Email"] else "hariwork78@gmail.com")
        print("Filled in Email Address")
        
        # Fill in Phone
        phone_field = wait.until(EC.element_to_be_clickable((By.ID, "Phone")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", phone_field)
        time.sleep(1)
        phone_field.clear()
        phone_field.send_keys(processed_json["Contact_number"].split()[-1] if processed_json["Contact_number"] else "2065551234")  # Valid US phone number format
        print("Filled in Phone Number")
        
        # Handle PhoneType dropdown selection
        handle_dropdown_selection(driver, wait, "PhoneType", "MOBILE", "Mobile")
        
        # Handle co-pay signup dropdown - select "Yes"
        handle_dropdown_selection(driver, wait, "incCoPaySignUp", "Yes", "Yes")

        try:
            checkbox = driver.find_element(By.ID, "incCoPaySignUpYes")
            # Scroll to the button
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(2)
            checkbox.click()
        except Exception as e:
            print(e,"Error at incCoPaySignUpYes")

        # Check the "incAgreePhoneText" checkbox
        try:
            # Scroll to the checkbox to ensure it's visible
            agree_phone_checkbox = wait.until(EC.presence_of_element_located((By.ID, "incAgreePhoneText")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", agree_phone_checkbox)
            time.sleep(1)
            
            # Check if already selected, if not, click it
            if not agree_phone_checkbox.is_selected():
                # Try direct click first
                try:
                    agree_phone_checkbox.click()
                    print("Clicked incAgreePhoneText checkbox")
                except Exception as e:
                    print(f"Standard click on incAgreePhoneText failed: {e}")
                    # Try JavaScript click as fallback
                    try:
                        driver.execute_script("arguments[0].click();", agree_phone_checkbox)
                        print("Clicked incAgreePhoneText checkbox with JavaScript")
                    except Exception as js_e:
                        print(f"JavaScript click on incAgreePhoneText failed: {js_e}")
                        # Try clicking the label as another fallback
                        try:
                            phone_label = driver.find_element(By.XPATH, "//label[@for='incAgreePhoneText']")
                            driver.execute_script("arguments[0].click();", phone_label)
                            print("Clicked incAgreePhoneText label with JavaScript")
                        except Exception as label_e:
                            print(f"Label click for incAgreePhoneText failed: {label_e}")
            else:
                print("incAgreePhoneText checkbox is already selected")
        except Exception as e:
            print(f"Error interacting with incAgreePhoneText checkbox: {e}")
        
        # Check the "incAgreeReadAuth" checkbox
        try:
            # Scroll to the checkbox to ensure it's visible
            agree_auth_checkbox = wait.until(EC.presence_of_element_located((By.ID, "incAgreeReadAuth")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", agree_auth_checkbox)
            time.sleep(1)
            
            # Check if already selected, if not, click it
            if not agree_auth_checkbox.is_selected():
                # Try direct click first
                try:
                    agree_auth_checkbox.click()
                    print("Clicked incAgreeReadAuth checkbox")
                except Exception as e:
                    print(f"Standard click on incAgreeReadAuth failed: {e}")
                    # Try JavaScript click as fallback
                    try:
                        driver.execute_script("arguments[0].click();", agree_auth_checkbox)
                        print("Clicked incAgreeReadAuth checkbox with JavaScript")
                    except Exception as js_e:
                        print(f"JavaScript click on incAgreeReadAuth failed: {js_e}")
                        # Try clicking the label as another fallback
                        try:
                            auth_label = driver.find_element(By.XPATH, "//label[@for='incAgreeReadAuth']")
                            driver.execute_script("arguments[0].click();", auth_label)
                            print("Clicked incAgreeReadAuth label with JavaScript")
                        except Exception as label_e:
                            print(f"Label click for incAgreeReadAuth failed: {label_e}")
            else:
                print("incAgreeReadAuth checkbox is already selected")
            time.sleep(2)
            try:
                # click the patient authorization 
                click_element = driver.find_element(By.XPATH, "//a[normalize-space()='Patient Authorization']")
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", click_element)
                time.sleep(2)
                click_element.click()

                # Wait for the scrollable div inside the modal
                scrollable_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-body-copy.jcf-scrollable"))
                )

                # Scroll the div to the bottom using JavaScript
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

                time.sleep(2)

                name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='incAuthFullName']"))
                )
                name_input.clear()
                full_name=processed_json["First_name"]+ (f" {processed_json["Last_name"]}" if len(processed_json["Last_name"]) else "")
                name_input.send_keys(full_name)
                time.sleep(1)
                submit_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-primary col align-self-center']")))
                submit_btn.click()

            except Exception as e:
                # click close btn
                close_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='modal-patient-auth']//div[@class='modal-close-btn']")))
                close_btn.click()
                time.sleep(1)
                print(e,"Error at - click the patient authorization link")

        except Exception as e:
            print(f"Error interacting with incAgreeReadAuth checkbox: {e}")
            
        # Wait a moment for any UI updates after checkbox selections
        time.sleep(2)
        
        # Click the Submit button
        try:
            # Find the submit button - there are multiple ways it might be located
            submit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'SUBMIT')]")
            if submit_buttons:
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_buttons[0])
                time.sleep(1)
                
                # Check if the button is disabled
                is_disabled = submit_buttons[0].get_attribute("disabled")
                if is_disabled:
                    print("Submit button is disabled. Form may have validation errors.")
                else:
                    # Try clicking the button
                    try:
                        submit_buttons[0].click()
                        print("Clicked Submit button")
                    except Exception as click_e:
                        print(f"Standard click on Submit button failed: {click_e}")
                        try:
                            driver.execute_script("arguments[0].click();", submit_buttons[0])
                            print("Clicked Submit button with JavaScript")
                        except Exception as js_e:
                            print(f"JavaScript click on Submit button failed: {js_e}")
            else:
                # Try to find the button by class
                submit_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-primary')]")
                if submit_buttons:
                    driver.execute_script("arguments[0].click();", submit_buttons[0])
                    print("Clicked primary button with JavaScript")
                else:
                    print("Could not find Submit button")
        except Exception as e:
            print(f"Error interacting with Submit button: {e}")
            
        # Wait for form submission to complete
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        try:
            driver.save_screenshot("final_screenshot_levyvio.png")
            print("Screenshot saved as final_screenshot_levyvio.png")
        except:
            print("Failed to save screenshot")

        # Close the browser
        time.sleep(40)
        driver.quit()
        print("Browser closed")


def get_processed_json():
    try:
        with open("./processed_json.json","r") as file:
        # Sample json format : {"First_name": "Aevy", "Last_name": "Jackson", "Address": "A803", "City": "Dover", "State": "Delaware", "ZIP": "19901", "Contact_number": "+1 6193248725", "Email": "anoj.viswanathan@gmail.com", "Medical_Insurance_Name": "Aetna", "Primary_Insurance_Member_ID": "5676532q"}
            return json.load(file)
    except:
        print("Load json file failed")

if __name__ == "__main__":
    automate_patient_enrollment(get_processed_json())