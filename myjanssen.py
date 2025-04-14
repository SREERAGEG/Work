from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    # 1. Navigate to the page
    driver.get("https://www.myjanssencarepath.com/user/register?flow=express&product=Remicade")
    
    try:
        patient = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='cart-box cart-bg-light-red']"))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", patient)
    except Exception as e:
        print("Error :", e)

    #Click on accept cookies
    try:
        click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", click)
    except Exception as e:
        print("Error :", e)
    
    #Click on continue
    try:
        click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue']"))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", click)
    except Exception as e:
        print("Error :", e)

    #Click on Commercial or Private Insurance
    try:
        click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//c-ev-button-link[@data-val='commercial']//div[@class='cart-box cart-bg-light-red']"))
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", click)
    except Exception as e:
        print("Error :", e)

    #Click Yes I agree
    try:
        click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='radio-0-25']//span[@class='slds-radio_faux']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", click)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", click)
    except Exception as e:
        print("Error :", e)

    #Click on Continue
    try:
        click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", click)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", click)
    except Exception as e:
        print("Error :", e)

    # Fill patient details
    try: 
        try:    #Click checkbox
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='checkbox-35']//span[@class='slds-checkbox_faux']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", click)
        except Exception as e:
            print("Error :", e)

        try:    # First Name
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-36']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            # driver.execute_script("arguments[0].click();", click)
            click.clear()
            click.send_keys("Sandhya")
        except Exception as e:
            print("Error :", e)

        try:    # Last Name
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-37']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            # driver.execute_script("arguments[0].click();", click)
            click.clear()
            click.send_keys("Vishwanathan")
        except Exception as e:
            print("Error :", e)
        
        try:    # Email
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-43']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            # driver.execute_script("arguments[0].click();", click)
            click.clear()
            click.send_keys("anoj.vishwanathan+remicade@gmail.com")
        except Exception as e:
            print("Error :", e)

        try:    # Sex
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='combobox-button-46']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            driver.execute_script("arguments[0].click();", click)
            time.sleep(1)

            dropdown=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@id='combobox-button-46-1-46']//span[@class='slds-media__body']")) # female
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dropdown)
        except Exception as e:
            print("Error :", e)

        try:    #   DOB
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-49']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            # driver.execute_script("arguments[0].click();", click)
            click.clear()
            click.send_keys("10/31/1960")
        except Exception as e:
            print("Error :", e)

        try:    #   Phone
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-50']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            # driver.execute_script("arguments[0].click();", click)
            click.clear()
            click.send_keys("6193248725")
        except Exception as e:
            print("Error :", e)

        try:    #   Type
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='combobox-button-53']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", click)
            dropdown=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@id='combobox-button-53-1-53']")) # Mobile
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dropdown)
            
        except Exception as e:
            print("Error :", e)

        try:    #   Street address
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-56']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            click.clear()
            click.send_keys("311 N Market St")
            
        except Exception as e:
            print("Error :", e)

        try:    #   City
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-57']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            click.clear()
            click.send_keys("Dallas")
            
        except Exception as e:
            print("Error :", e)

        try:    #   State
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='combobox-button-60']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", click)
            dropdown=WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@id='combobox-button-60-48-60']")) # Texas
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", dropdown)
            
        except Exception as e:
            print("Error :", e)

        try:    #   Zip
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='input-63']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            click.clear()
            click.send_keys("75202")
            
        except Exception as e:
            print("Error :", e)

        try:    #   Checkbox I agree T&C
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//label[@for='checkbox-65']//span[@class='slds-checkbox_faux']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", click)
            
        except Exception as e:
            print("Error :", e)

        try:    #   Click Continue
            click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Continue']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", click)
            
        except Exception as e:
            print("Error :", e)

        
    except Exception as e:
        print("Error on filling patient details")

    # # Take a screenshot of the final state
    # time.sleep(10)
    # driver.save_screenshot("final_result.png")
    # print("\nSaved screenshot of final state to 'final_result.png'")


except Exception as e:
    print("A major error occurred:", e)
finally:
    time.sleep(20)

    driver.quit()
