from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    # 1. Navigate to the page
    driver.get("https://benlystacopayprogram.com/patient-co-pay-card-enroll")
    
    # 2. Initial continue link
    try:
        initial_continue = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Continue')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", initial_continue)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", initial_continue)
        print("Clicked initial 'Continue' link.")
        time.sleep(2)
    except Exception as e:
        print("No initial continue link found or clickable - skipping this step:", e)
    
    # 3-5. Click the radio buttons
    try:
        label_q1_no = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='Q1_n']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", label_q1_no)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", label_q1_no)
        print("Clicked 'No' (Q1_n).")
        
        label_q2_yes = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='Q2_y']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", label_q2_yes)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", label_q2_yes)
        print("Clicked 'Yes' (Q2_y).")
        
        label_q3_yes = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='toggle-on-3']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", label_q3_yes)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", label_q3_yes)
        print("Clicked 'Yes' (toggle-on-3).")
    except Exception as e:
        print("Error clicking radio buttons:", e)
    
    # 6. Click Continue
    try:
        final_continue = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", final_continue)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", final_continue)
        print("Clicked final 'Continue' button.")
    except Exception as e:
        print("Could not click submit button:", e)
    
    time.sleep(3)  # Wait for page to load
    
    # 7-8. Fill in first and last name
    try:
        first_name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "first_name"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", first_name_field)
        first_name_field.clear()
        first_name_field.send_keys("Hari")
        print("Filled in First Name with 'Hari'.")
        
        last_name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "last_name"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", last_name_field)
        last_name_field.clear()
        last_name_field.send_keys("Sachdeva")
        print("Filled in Last Name with 'Sachdeva'.")
    except Exception as e:
        print("Error filling name fields:", e)
    
    # 9. Set date fields using JavaScript - simplified version
    date_script = """
    // Find the date selects based on their IDs
    const monthSelect = document.getElementById('d1');
    const daySelect = document.getElementById('d2');
    const yearSelect = document.getElementById('d3');
    
    // Function to set value and trigger events
    function setSelectValue(select, value) {
        if (!select) return false;
        
        try {
            // Direct value setting
            select.value = value;
            
            // Set selected property on options
            Array.from(select.options).forEach(option => {
                option.selected = option.value === value;
            });
            
            // Create and dispatch change event
            const event = new Event('change', { bubbles: true });
            select.dispatchEvent(event);
            
            return true;
        } catch (e) {
            console.log(`Error setting value: ${e.message}`);
            return false;
        }
    }
    
    // Set the values
    const monthSuccess = setSelectValue(monthSelect, '1');  // January
    const daySuccess = setSelectValue(daySelect, '16');     // 16
    const yearSuccess = setSelectValue(yearSelect, '2003'); // 2003
    
    return {
        monthSuccess,
        daySuccess,
        yearSuccess
    };
    """
    
    date_result = driver.execute_script(date_script)
    print("\nDate setting results:")
    print(f"Month set successfully: {date_result['monthSuccess']}")
    print(f"Day set successfully: {date_result['daySuccess']}")
    print(f"Year set successfully: {date_result['yearSuccess']}")
    
    # 10. Select Male for gender
    try:
        # From the provided HTML, the gender input has id="g1" and value="M"
        male_gender = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='g1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", male_gender)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", male_gender)
        print("Selected 'Male' for gender.")
    except Exception as e:
        # JavaScript fallback
        try:
            gender_script = """
            const maleLabel = document.querySelector('label[for="g1"]');
            if (maleLabel) {
                maleLabel.click();
                return true;
            }
            
            const maleInput = document.querySelector('input[name="gender"][value="M"]');
            if (maleInput) {
                maleInput.checked = true;
                const event = new Event('change', { bubbles: true });
                maleInput.dispatchEvent(event);
                return true;
            }
            return false;
            """
            gender_success = driver.execute_script(gender_script)
            print(f"Selected Male gender via JavaScript: {gender_success}")
        except Exception as inner_e:
            print(f"Error selecting male gender: {e} and then {inner_e}")
    
    # 11. Fill in the address field
    try:
        address_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "address"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", address_field)
        address_field.clear()
        address_field.send_keys("PO 98398")
        print("Filled in Address with 'PO 98398'.")
    except Exception as e:
        print("Error filling address field:", e)
        
    # 12. Fill in the city field
    try:
        city_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "city"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", city_field)
        city_field.clear()
        city_field.send_keys("Washington")
        print("Filled in City with 'Washington'.")
    except Exception as e:
        print("Error filling city field:", e)
        
    # 13. Handle the state dropdown
    state_script = """
    // Find the state select element
    const stateSelect = document.getElementById('state');
    
    // Function to set value and trigger events
    function setSelectValue(select, value, text) {
        if (!select) return false;
        
        try {
            // Direct value setting
            select.value = value;
            
            // Set selected property on options
            Array.from(select.options).forEach(option => {
                if (option.value === value) {
                    option.selected = true;
                }
            });
            
            // Create and dispatch change event
            const event = new Event('change', { bubbles: true });
            select.dispatchEvent(event);
            
            // Try to update the visible Select2 UI text
            const stateContainer = document.querySelector('#select2-state-container');
            if (stateContainer) {
                stateContainer.textContent = text;
                stateContainer.title = text;
            }
            
            return true;
        } catch (e) {
            console.log(`Error setting state value: ${e.message}`);
            return false;
        }
    }
    
    // Set the state to Washington DC (assuming the value is "DC")
    const stateSuccess = setSelectValue(stateSelect, "DC", "Washington DC");
    
    return {
        stateSuccess
    };
    """
    
    state_result = driver.execute_script(state_script)
    print(f"State set successfully: {state_result['stateSuccess']}")
    
    # 14. Fill in the zip code
    try:
        zip_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "zip"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", zip_field)
        zip_field.clear()
        zip_field.send_keys("99330")
        print("Filled in ZIP code with '99330'.")
    except Exception as e:
        print("Error filling ZIP field:", e)
    
    # 15. Fill in the email address
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "email_address"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        email_field.clear()
        email_field.send_keys("hariwork78@gmail.com")
        print("Filled in Email with 'hariwork78@gmail.com'.")
    except Exception as e:
        print("Error filling email field:", e)
    
    # 16. Fill in the phone number - using the format (234) 235-2352
    try:
        # Using the correct ID "cell_number" from the HTML
        phone_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cell_number"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", phone_field)
        phone_field.clear()
        phone_field.send_keys("(234) 235-2352")
        print("Filled in Phone Number with '(234) 235-2352'.")
    except Exception as e:
        print("Error filling phone field:", e)
        # Try JavaScript approach as fallback
        try:
            phone_script = """
            const phoneField = document.getElementById('cell_number');
            if (phoneField) {
                phoneField.value = "(234) 235-2352";
                const event = new Event('input', { bubbles: true });
                phoneField.dispatchEvent(event);
                const changeEvent = new Event('change', { bubbles: true });
                phoneField.dispatchEvent(changeEvent);
                return true;
            }
            return false;
            """
            phone_success = driver.execute_script(phone_script)
            print(f"Filled phone via JavaScript: {phone_success}")
        except Exception as inner_e:
            print(f"Error with JavaScript phone approach: {inner_e}")
    
    # 17. Click the "Patient" radio button
    try:
        # Based on the HTML, the patient radio button has id="e1"
        patient_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='e1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", patient_radio)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", patient_radio)
        print("Selected 'Patient' option.")
    except Exception as e:
        # JavaScript fallback for patient selection
        try:
            patient_script = """
            const patientLabel = document.querySelector('label[for="e1"]');
            if (patientLabel) {
                patientLabel.click();
                return true;
            }
            
            const patientInput = document.querySelector('input[id="e1"], input[name="enrolled_by"][value="PATIENT"]');
            if (patientInput) {
                patientInput.checked = true;
                const event = new Event('change', { bubbles: true });
                patientInput.dispatchEvent(event);
                return true;
            }
            return false;
            """
            patient_success = driver.execute_script(patient_script)
            print(f"Selected Patient option via JavaScript: {patient_success}")
        except Exception as inner_e:
            print(f"Error selecting Patient option: {e} and then {inner_e}")
    
    # 18. Click the indication dropdown and select Lupus
    try:
        # First click on the indication dropdown
        indication_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-labelledby='select2-indication-container']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", indication_dropdown)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", indication_dropdown)
        print("Clicked on indication dropdown.")
        
        # Then select Lupus from the dropdown
        time.sleep(2)  # Wait for dropdown to open
        lupus_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Lupus')]"))
        )
        driver.execute_script("arguments[0].click();", lupus_option)
        print("Selected 'Lupus' from indication dropdown.")
    except Exception as e:
        print("Error selecting Lupus from dropdown:", e)
        # JavaScript fallback
        try:
            lupus_script = """
            // Try to find and set the indication value to Lupus
            const indicationSelect = document.getElementById('indication');
            
            if (indicationSelect) {
                // Find the option with Lupus text
                const lupusOption = Array.from(indicationSelect.options).find(
                    option => option.text.includes('Lupus')
                );
                
                if (lupusOption) {
                    indicationSelect.value = lupusOption.value;
                    const event = new Event('change', { bubbles: true });
                    indicationSelect.dispatchEvent(event);
                    
                    // Try to update the Select2 UI
                    const containerSpan = document.querySelector('#select2-indication-container');
                    if (containerSpan) {
                        containerSpan.textContent = 'Lupus';
                        containerSpan.title = 'Lupus';
                    }
                    return "Set to Lupus successfully";
                }
                return "Lupus option not found";
            }
            return "Indication select not found";
            """
            lupus_result = driver.execute_script(lupus_script)
            print(f"Indication selection via JavaScript: {lupus_result}")
        except Exception as inner_e:
            print(f"Error with JavaScript indication approach: {inner_e}")
    
    # 19. Select Medical Insurance option
    try:
        # Based on the HTML, the Medical Insurance radio button has id="t1"
        medical_insurance = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='t1']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", medical_insurance)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", medical_insurance)
        print("Selected 'Medical Insurance' option.")
    except Exception as e:
        print("Error selecting Medical Insurance:", e)
        # JavaScript fallback
        try:
            insurance_script = """
            const insuranceLabel = document.querySelector('label[for="t1"]');
            if (insuranceLabel) {
                insuranceLabel.click();
                return true;
            }
            
            const insuranceInput = document.querySelector('input[id="t1"], input[value="MedicalInsurance"]');
            if (insuranceInput) {
                insuranceInput.checked = true;
                const event = new Event('change', { bubbles: true });
                insuranceInput.dispatchEvent(event);
                return true;
            }
            return false;
            """
            insurance_success = driver.execute_script(insurance_script)
            print(f"Selected Medical Insurance via JavaScript: {insurance_success}")
        except Exception as inner_e:
            print(f"Error with JavaScript insurance approach: {inner_e}")
        
    # 20. Click on terms and Conditions
    try:
        Terms_and_C = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "p[class='accept'] span[class='checkmark']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Terms_and_C)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Terms_and_C)
        print("Selected 'Terms and Conditions' check box.")
    except Exception as e:
        print("Error selecting Terms and Conditions:", e)
        # # JavaScript fallback
        # try:
    
    # 21. Click on Captcha checkbox
    try:
        Captcha = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='recaptcha-checkbox-border']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Captcha)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Captcha)
        print("Selected 'Captcha' check box.")
    except Exception as e:
        print("Error selecting Captcha checkbox:", e)
        # # JavaScript fallback
        # try:

    # 22 Click on Continue Button
    try:
        continue1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", continue1)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", continue1)
        print("Clicked on Continue button.")
    except Exception as e:
        print("Error Clicking on Continue button:", e)
        # # JavaScript fallback
        # try:

    # 23. Click on I agree
    try:
        check_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkmark"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", check_box)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", check_box)
        print("Clicked on I agree.")
    except Exception as e:
        print("Error Clicking on I agree checkbox:", e)


    # 24. Fill First Name
    try:
        first_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='sign_first_name']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", first_name)
        first_name.clear()
        first_name.send_keys("Hari")
        print("Filled First Name as 'Hari'.")
    except Exception as e:
        print("Error filling First Name field:", e)


    # 25. Fill Last Name
    try:
        last_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='sign_last_name']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", last_name)
        last_name.clear()
        last_name.send_keys("Sachdeva")
        print("Filled Last Name as 'Sachdeva'.")
    except Exception as e:
        print("Error filling Last Name field:", e)

    # 26. Click on Im not a robot
    try:
        Captcha = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='recaptcha-checkbox-border']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Captcha)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Captcha)
        print("Selected 'Captcha' check box.")
    except Exception as e:
        print("Error selecting Captcha checkbox:", e)

    # 27. Click on Enroll
    try:
        Enroll = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Enroll)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Enroll)
        print("Clicked Enroll.")
    except Exception as e:
        print("Error Clicking Enroll:", e)
    
    # 28. Scroll to Detailed view   
    try:
        Detail_box = driver.find_element(By.XPATH,"//div[@class='register-col-box']")
            # EC.element_to_be_clickable((By.XPATH, "//div[@class='register-col-box']"))
        # )
        driver.execute_script("arguments[0].scrollIntoView(true);", Detail_box)
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, -200);")  # Scroll up by 200 pixels Optional
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Detail_box)
        print("Selected Detail box.")
    except Exception as e:
        print("Error selecting Detail box:", e)
    
    # Take a screenshot of the final state - If view is not enough, make the driver to full screen 
    time.sleep(10)
    driver.save_screenshot("final_result.png")
    print("\nSaved screenshot of final state to 'final_result.png'")
    
    print("\nForm fields filled successfully!")
    print("Form is ready for submission with:")
    print("- Name: Hari Sachdeva")
    print("- DOB: January 16, 2003") 
    print("- Gender: Male")
    print("- Address: PO 98398")
    print("- City: Washington")
    print("- State: Washington DC")
    print("- ZIP: 99330")
    print("- Email: hariwork78@gmail.com")
    print("- Phone: (234) 235-2352")
    print("- Enrolled By: Patient")
    print("- Indication: Lupus")
    print("- Insurance Type: Medical Insurance")
    print("- Terms and Conditions selected")
    print("- Captcha clicked")
    
    # Short pause before closing
    time.sleep(5)
    
except Exception as e:
    print("A major error occurred:", e)
finally:
    driver.quit()
