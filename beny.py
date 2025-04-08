from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    # 1. Navigate to the page
    driver.get("https://benlystacopayprogram.com/patient-intake/confirm?cardModel=IPYmkKtpXAk3I13yyNfcTO6KLF.gx_H9J8Bb9HcwtruTl2jybVe49hvZcE6CGXVJfJ3iUjxkAk_.Z0ft.5M0QuHCc4VKyKnStoYNy_SJ.6gx1ZLHuIXMWFC90pBMm.cEmRall6rAydmVk8pwXt7a_A_AdTusa92fQmqtrKdprBNUX_4Wziag9UzIIq1tSxBM6Eb_XnKU0Ok00TMVg_Zpeq2PjusJIH6Nwkx9Oi3h4zFi1w.Di5leUcRSKF1vVM2n4dKcq3KhV6pJXpDCjo.OU4JZk24G2aXQsK5SnF4rRR4JgkeNeTVjaZl1Nw1VvhfMkHeGnUXtPLDp5CeMZUr5aQ--")
    
    # 2. Scroll to Detailed view
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

    # Take a screenshot of the final state
    time.sleep(10)
    driver.save_screenshot("final_result.png")
    print("\nSaved screenshot of final state to 'final_result.png'")


except Exception as e:
    print("A major error occurred:", e)
finally:
    driver.quit()
