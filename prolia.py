from selenium import webdriver
# import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random

def print_dialog_snippet(driver):
    """Try to locate the mat-dialog-container and print some of its HTML."""
    try:
        dialog = driver.find_element(By.CSS_SELECTOR, "mat-dialog-container")
        print("=== mat-dialog-container HTML snippet ===")
        print(dialog.get_attribute("innerHTML")[:500])  # print first 500 characters
        print("=== End of snippet ===")
    except Exception as e:
        print("mat-dialog-container not found to print snippet:", e)

# Instantiate the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
driver.set_window_size(2494, 1048)
# driver.maximize_window()
# print("SIZXE",driver.get_window_size())

try:
    ############################################################################
    # Part 1: Login & Enroll New Patient
    ############################################################################

    driver.get("https://copay.amgensupportplus.com/hcp/login")
    wait = WebDriverWait(driver, 10)

    # Accept cookie popup on the login page
    try:
        accept_cookie_button = wait.until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonAccept"))
        )
        accept_cookie_button.click()
        print("Cookie popup accepted on login page.")
    except Exception as e:
        print("Cookie popup not found or already accepted on login page:", e)

    # Fill in login credentials
    username_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[formControlName='username']"))
    )
    username_field.send_keys("anoj@getcopayhelp.com")
    password_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[formControlName='password']"))
    )
    password_field.send_keys("Amgensupport123$")
    
    # Click the Sign In button
    sign_in_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Sign In')]]"))
    )
    sign_in_button.click()
    print("Clicked Sign In button.")

    # Wait for the dashboard to load and click "Enroll New Patient"
    enroll_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Enroll New Patient')]]"))
    )
    enroll_button.click()
    print("Clicked Enroll New Patient button.")

    ############################################################################
    # Part 2: Eligibility Page & Patient Info
    ############################################################################

    # Accept cookie popup on the enrollment page, if present
    try:
        cookie_accept = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonAccept"))
        )
        cookie_accept.click()
        print("Cookie popup accepted on eligibility page.")
    except Exception as e:
        print("Cookie popup not found or already handled on eligibility page:", e)

    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.spinner-container.ng-star-inserted"))
    )
    print("Initial spinner overlay is gone on eligibility page.")

    # Click the eligibility checkbox
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "mat-mdc-checkbox-15"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    time.sleep(1)
    try:
        ActionChains(driver).move_to_element(checkbox).click().perform()
        print("Eligibility checkbox clicked.")
    except Exception as e:
        print("Checkbox click using ActionChains failed; trying JS click.", e)
        driver.execute_script("arguments[0].click();", checkbox)

    # Click the Continue button on the eligibility page
    continue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]/ancestor::button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
    time.sleep(1)
    continue_btn.click()
    print("Eligibility Continue button clicked.")

    ############################################################################
    # Part 3: Patient Info Form
    ############################################################################

    first_name = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[formControlName='firstName']"))
    )
    print("Patient info form loaded.")
    first_name.send_keys("hari")
    last_name = driver.find_element(By.CSS_SELECTOR, "input[formControlName='lastName']")
    last_name.send_keys("sachdeva")
    dob_input = driver.find_element(By.CSS_SELECTOR, "input[formControlName='dob']")
    dob_input.clear()
    dob_input.send_keys("01/16/2003")
    zip_code = driver.find_element(By.CSS_SELECTOR, "input[formControlName='postalCode']")
    zip_code.send_keys(str(random.randint(10000, 99999)))
    email_field = driver.find_element(By.CSS_SELECTOR, "input[formControlName='email']")
    email_field.send_keys("hariwork78@gmail.com")
    
    # Select gender
    gender_select = driver.find_element(By.CSS_SELECTOR, "mat-select[formControlName='gender']")
    gender_select.click()
    male_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Male')]"))
    )
    male_option.click()
    print("Patient info fields filled.")

    continue_button_form = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]/ancestor::button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_button_form)
    time.sleep(1)
    continue_button_form.click()
    print("Patient info Continue button clicked.")

    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.spinner-container.ng-star-inserted"))
    )
    print("Loading overlay after patient info is gone.")

    ############################################################################
    # Part 4: Insurance Section
    ############################################################################

    time.sleep(2)
    try:
        yes_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio']#Yes0ageCheck18"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", yes_radio)
        time.sleep(1)
        yes_radio.click()
        print("Clicked 'Yes' radio button.")
    except Exception as e:
        print("Failed to click 'Yes' radio button:", e)
    
    try:
        commercial_clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mdc-radio"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", commercial_clickable)
        time.sleep(1)
        commercial_clickable.click()
        print("Clicked 'Commercial insurance' radio button (mdc-radio).")
    except Exception as e:
        print("Failed to click 'Commercial insurance' radio button:", e)
    
    try:
        no_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio']#No1governmentInsuranceCheck"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", no_radio)
        time.sleep(1)
        try:
            no_radio.click()
            print("Clicked 'No' for government insurance.")
        except Exception as ex:
            print("Standard click on 'No' failed; trying JS click.", ex)
            driver.execute_script("arguments[0].click();", no_radio)
            print("Clicked 'No' for government insurance via JS click.")
    except Exception as e:
        print("Failed to locate/click 'No' government insurance:", e)
    
      ########################################
    # Part 5: Open and Handle Agreement Dialog
    ########################################
    
    # 1. Click the agreement text to open the dialog
  # 1. Click the agreement text to open the dialog
    try:
        agreement_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'By checking this box, I agree')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", agreement_div)
        time.sleep(1)
        agreement_div.click()
        print("Clicked agreement element to open the dialog.")
    except Exception as e:
        print("Failed to click agreement element:", e)
    
    # 2. Wait for the dialog container to appear
    try:
        dialog_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "mat-dialog-container"))
        )
        print("Dialog container is visible.")
    except Exception as e:
        print("Dialog container not found:", e)
        print("=== Page Source snippet ===")
        print(driver.page_source[:1000])
        print("=== End of snippet ===")
    
    # 3. Find the proper scrollable content element based on the HTML structure
    try:
        # Based on the HTML provided, the correct scrollable element is "mat-dialog-content"
        scrollable_content = dialog_container.find_element(By.CSS_SELECTOR, "mat-dialog-content")
        print("Found scrollable content element:", scrollable_content)
        
        # Get the scroll height
        scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_content)
        print(f"Scroll height: {scroll_height}px")
        
        # Scroll incrementally with pauses to simulate user scrolling
        current_position = 0
        step_size = 150  # px per step
        
        while current_position < scroll_height:
            current_position += step_size
            # Use JavaScript to scroll the element
            driver.execute_script("""
                arguments[0].scrollTop = arguments[1];
                arguments[0].dispatchEvent(new Event('scroll'));
            """, scrollable_content, current_position)
            
            # Add a short delay between scrolls
            time.sleep(0.5)
            
        # Final scroll to ensure we've reached the bottom
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_content)
        print("Successfully scrolled to the bottom of the dialog content.")
        
        # Additional time to ensure any scroll-triggered events are processed
        time.sleep(2)
        
    except Exception as e:
        print("Error finding or scrolling dialog content:", e)
        
        # Fallback approach: try to use the div with class "box" as shown in your HTML
        try:
            box_element = dialog_container.find_element(By.CSS_SELECTOR, "div.box")
            print("Found div.box element, using as fallback.")
            
            # Scroll the box element to the bottom
            driver.execute_script("""
                arguments[0].scrollTop = arguments[0].scrollHeight;
                arguments[0].dispatchEvent(new Event('scroll'));
            """, box_element)
            
            time.sleep(2)
            print("Applied fallback scrolling to div.box element.")
        except Exception as e2:
            print("Fallback scrolling failed:", e2)
            
            # Last resort: try to scroll the entire dialog container
            try:
                driver.execute_script("""
                    var elements = document.querySelectorAll('mat-dialog-container *');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].scrollHeight > elements[i].clientHeight) {
                            elements[i].scrollTop = elements[i].scrollHeight;
                            elements[i].dispatchEvent(new Event('scroll'));
                        }
                    }
                """)
                time.sleep(2)
                print("Applied last-resort scrolling to all potentially scrollable elements.")
            except Exception as e3:
                print("Last-resort scrolling failed:", e3)
    
    # 4. Wait for the Accept button and click it
    try:
        # Using a more precise selector based on your HTML
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#button-accept"))
        )
        print("Accept button is now clickable.")
        
        # Sometimes buttons need a small delay before clicking
        time.sleep(0.5)
        
        # Try multiple click methods to ensure it works
        try:
            accept_button.click()
            print("Clicked Accept button normally.")
        except Exception as e:
            print("Normal click failed, trying JavaScript click:", e)
            driver.execute_script("arguments[0].click();", accept_button)
            print("Clicked Accept button using JavaScript.")
            
    except Exception as e:
        print("Failed to find or click Accept button:", e)
        print_dialog_snippet(driver)
        
        # Handle Patient Authorization checkbox
    try:
        # First, locate the checkbox using the unique ID or class structure
        auth_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "mat-checkbox.mat-mdc-checkbox.mat-accent.ng-untouched"))
        )
        
        # Scroll to the checkbox to ensure it's in view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", auth_checkbox)
        time.sleep(1)
        
        # Click on the checkbox using different approaches
        try:
            # Try regular click first
            auth_checkbox.click()
            print("Clicked on authorization checkbox using standard click.")
        except Exception as e:
            print("Standard click failed on auth checkbox:", e)
            
            try:
                # Try clicking via JavaScript
                driver.execute_script("arguments[0].click();", auth_checkbox)
                print("Clicked on authorization checkbox using JavaScript.")
            except Exception as e2:
                print("JavaScript click failed on auth checkbox:", e2)
                
                try:
                    # Try clicking via ActionChains
                    ActionChains(driver).move_to_element(auth_checkbox).click().perform()
                    print("Clicked on authorization checkbox using ActionChains.")
                except Exception as e3:
                    print("ActionChains click failed on auth checkbox:", e3)
                    
                    # Try finding the inner div that might be more clickable
                    try:
                        inner_checkbox = auth_checkbox.find_element(By.CSS_SELECTOR, "div.mdc-checkbox")
                        driver.execute_script("arguments[0].click();", inner_checkbox)
                        print("Clicked on inner checkbox element using JavaScript.")
                    except Exception as e4:
                        print("Failed to click on inner checkbox element:", e4)
        
        # Verify if checkbox is checked
        time.sleep(1)
        try:
            # Wait for the checkbox to be selected/checked
            WebDriverWait(driver, 5).until(
                lambda d: "mat-mdc-checkbox-checked" in auth_checkbox.get_attribute("class")
            )
            print("Authorization checkbox is now checked.")
        except:
            print("WARNING: Could not verify if authorization checkbox is checked.")
            
    except Exception as e:
        print("Failed to find or interact with authorization checkbox:", e)
    
    # Click on Patient Authorization text to open dialog
    try:
        # Look for the label or text element associated with the checkbox
        auth_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Patient Authorization')]"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", auth_link)
        time.sleep(1)
        auth_link.click()
        print("Clicked on Patient Authorization link to open dialog.")
        
    except Exception as e:
        print("Failed to click on Patient Authorization link:", e)
        
        # Alternative method - try finding the label element
        try:
            label_element = driver.find_element(By.CSS_SELECTOR, "label.mdc-label")
            driver.execute_script("arguments[0].click();", label_element)
            print("Clicked on label element to open dialog.")
        except Exception as e2:
            print("Failed to click on label element:", e2)
    
    # Handle dialog scrolling and accept button
    try:
        # Wait for dialog to appear
        dialog_container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "mat-dialog-container"))
        )
        print("Patient Authorization dialog is visible.")
        
        # Find the scrollable content element
        scrollable_content = dialog_container.find_element(By.CSS_SELECTOR, "mat-dialog-content")
        print("Found scrollable dialog content.")
        
        # Get the scroll height
        scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_content)
        print(f"Dialog scroll height: {scroll_height}px")
        
        # Scroll incrementally with pauses
        current_position = 0
        step_size = 150  # px per step
        
        while current_position < scroll_height:
            current_position += step_size
            # Use JavaScript to scroll the element
            driver.execute_script("""
                arguments[0].scrollTop = arguments[1];
                arguments[0].dispatchEvent(new Event('scroll'));
            """, scrollable_content, current_position)
            
            # Add a short delay between scrolls
            time.sleep(0.5)
            
        # Final scroll to ensure we've reached the bottom
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_content)
        print("Successfully scrolled to the bottom of the Patient Authorization dialog.")
        
        # Wait for any scroll-triggered events
        time.sleep(2)
        
        # Click the Accept button
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#button-accept"))
        )
        print("Found Accept button for Patient Authorization dialog.")
        
        time.sleep(0.5)
        
        # Try multiple click methods to ensure it works
        try:
            accept_button.click()
            print("Clicked Accept button normally.")
        except Exception as e:
            print("Normal click failed, trying JavaScript click:", e)
            driver.execute_script("arguments[0].click();", accept_button)
            print("Clicked Accept button using JavaScript.")
            
    except Exception as e:
        print("Error handling Patient Authorization dialog:", e)
        
        # Fallback approaches
        try:
            # Try to use the div.box element as fallback
            box_element = dialog_container.find_element(By.CSS_SELECTOR, "div.box")
            print("Using div.box element as fallback for scrolling.")
            
            # Scroll the box element to the bottom
            driver.execute_script("""
                arguments[0].scrollTop = arguments[0].scrollHeight;
                arguments[0].dispatchEvent(new Event('scroll'));
            """, box_element)
            
            time.sleep(2)
            
            # Try to find and click the Accept button
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#button-accept, mat-dialog-actions button"))
            )
            driver.execute_script("arguments[0].click();", accept_button)
            print("Clicked Accept button after fallback scrolling.")
            
        except Exception as e2:
            print("Fallback approach for Patient Authorization dialog failed:", e2)
            
            # Last resort: try to find any button that could be the accept button
            try:
                buttons = dialog_container.find_elements(By.CSS_SELECTOR, "button")
                for button in buttons:
                    if "accept" in button.get_attribute("id").lower() or "accept" in button.text.lower():
                        driver.execute_script("arguments[0].click();", button)
                        print("Clicked button that appears to be the Accept button.")
                        break
            except Exception as e3:
                print("Last resort attempt to find Accept button failed:", e3)
                    
    # Handle Health Data Processing Checkbox
    try:
        time.sleep(1)

        checkbox=driver.find_element(By.XPATH,"//input[@name='third-party-disclosure']")
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        time.sleep(1)
        checkbox.click()  # Click to check the box


        try:
            # Wait for dialog to appear
            dialog_container = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "mat-dialog-container"))
            )            
            # Find the scrollable content element
            scrollable_content = dialog_container.find_element(By.CSS_SELECTOR, "mat-dialog-content")

            # Get the scroll height
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_content)
            
            # Scroll incrementally with pauses
            current_position = 0
            step_size = 150  # px per step
            
            while current_position < scroll_height:
                current_position += step_size
                # Use JavaScript to scroll the element
                driver.execute_script("""
                    arguments[0].scrollTop = arguments[1];
                    arguments[0].dispatchEvent(new Event('scroll'));
                """, scrollable_content, current_position)
                
                # Add a short delay between scrolls
                time.sleep(0.5)
                
            # Final scroll to ensure we've reached the bottom
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_content)
            print("Successfully scrolled to the bottom of dialog.")
            
            # Wait for any scroll-triggered events
            time.sleep(2)
        except :
            print("Scroll error")   

        # Click the Accept button
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='Accept']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
        time.sleep(1)
        accept_button.click()
    except Exception as e:
        print(e,"Error at Health Data Processing Checkbox")


    # click Continue button
    time.sleep(1)
    # driver.find_element(By.XPATH,"//button[@class='mdc-button mat-mdc-button mat-primary mat-mdc-button-base ng-star-inserted']//span[@class='mat-mdc-button-touch-target']").click()
    
    # Wait for the enabled "Continue" button and click it
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()=' Continue ']]"))
    )

    # Scroll into view if needed and click
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
    time.sleep(1)
    continue_button.click()


    # Patient Information page
    try:
        try:
            address=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            city=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            state=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            ph_no=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            Insurance_comp_name=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            plan_type=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            group_no=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            member_no=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            effective_date=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            bin=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            pcn=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            not_have_pharmacy_insurance=driver.find_element(By.XPATH,"")
        except Exception as e:
            print(e)

        try:
            continue_btn=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continue']]"))
            )

            # Scroll into view if needed and click
            driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
            time.sleep(1)
            continue_button.click()
        except Exception as e:
            print(e)
            
    except Exception as e:
        print(e,"Error in page Patient Information")


except Exception as e:
    print("An error occurred:", e)

finally:
    input("Press Enter to exit")
    driver.quit()
