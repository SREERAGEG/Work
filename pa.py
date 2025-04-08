from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    # 1. Navigate to the page
    driver.get("https://benlystacopayprogram.com/patient-authorization?patientInfo=nXcHzVjwhcSNQoUSA4MXCp6MhjNlrmuXqP9.lojf3vG2XZUBBLPpyMUXJt62uEn.9FALJGZy6.QihrefyyYbaa6j.UNerScjM59MmoJCjLyxomJJs9txG.wxhziSquHNJMEscyd5ZoxDYH6L5NOLQdGrAQ.6Sx340eVlDgwvuDylawlvTE5yGc5Vf8VFBsfHbJrmRP1e8bmIA6M.EsVAOzNgapb0WSXwLgNoVL3jo8JQ45qIiRhIbMLx9eMoYFJ.fpRU9NOtuBjmUr9PDatqS.T5J5Ukq9Jvz5LU3sa.H4rS7ZVxEXmZVV.rnTpz.5IYeyJbdkg47nsSsi8m2UzEZRQxOi7wz8qDmAV1I3FjsmoePPD9i1d.hh7D2tbdUUrc.wAgxgYj0.Yx_97FcQhlx1JUwkmJkyAokYvBA8oNIhs6Dnwz8YTNZcAP9Wj0qrrmCUQA9cFrOczwWJ56tozvCXFr2iV40g0h5uO5Q_zRlz837seAyDRLPlB0mxWbp.oaIYFEsrBzrvxmmBF2z3bQtI7JQPnAYFRg25_mzpq2C1JaPSlNbji2_DSMraKgVDI3w04SFUFvbnRkUXGyrwzBh3opkL1BtsXHzqdlMaBLQQPdLbllc4OLJ0urcDhLWKu2ossbNHA3IgjmnhKhjsLLWg8DA.DRdZck3bgAh_58vO03DyOJ_K8xYIgrMisxFI7QDVgbt2I0_PkRpa65oK2FQiyzdAm8OTrDM74TPDgVv5D_hlR5qFS5Ec5RWg2Xq8TV0KVL9fV6ZZl5NQ6wAU7t3RqqhTccMrBjBFWHD1vt4CwzkfXehzaiVaexsOcexGV_Lp6CqKK8_eLzNfII4TmII6av2Q9wHW4PMNBxrfiGFcyNH_P4fcxSoyX2namrALjIaUXT262JOjJX_TCX2gJZRcTx7iDIv55JUdsm.bL3.NZPjJ2w0Q170T1VaaqASaiw2Rbi7XJqaqSxXmPw22lILIC_JxbTRN1y4JCuF7uLV23k46zqghIP8SigNvud_9r8Ua9HD_u.8DbPYf5hkNJv9FmaxLtp6yBwH9jVnHqMTVyQUxNkNw54X9NOJ4AYILu5CVyAnSICNROj42BjfL8b3wZ_Ezzc82FCVJMjsyJq92Fv2n.1TGQbgspFdMALasCs1a07Iz8dqf1fZvNdEuR9vwSbUIckFTjtbHkrP2KbF2NaCyNT83UxoTlwLee97Va0xrVVdQgbuAh0Dut5NHfgIABwvXA4KmhbBdvhnQW61K8uCommLnT63QzFi1SdN.Xg2YV2QJqH2A8E6J6rDFdwwmnxAyh2y_nKwlnPaBhy4B_1hCoMSUI2KyC7ybIEzWLnY4lfW7gepnOZLa0lrQeUrsUnSbC1CHTDrjKBqV.OlS7if3YhNJ306c3fWpxgrY0Z")
    
    # X1. Click on I agree
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


    # X2. Fill First Name
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


    # X3. Fill Last Name
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

    # 2. Click on Im not a robot
    try:
        Captcha = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='recaptcha-checkbox-border']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", Captcha)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", Captcha)
        print("Selected 'Captcha' check box.")
    except Exception as e:
        print("Error selecting Captcha checkbox:", e)

    # 2. Click on Enroll
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
    

    # Take a screenshot of the final state
    time.sleep(10)
    driver.save_screenshot("final_result.png")
    print("\nSaved screenshot of final state to 'final_result.png'")


except Exception as e:
    print("A major error occurred:", e)
finally:
    time.sleep(20)

    driver.quit()
