import os
import subprocess
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Function to install Google Chrome
def install_google_chrome():
    try:
        # Download Google Chrome
        if not os.path.exists("google-chrome-stable_current_amd64.deb"):
            subprocess.run(
                ["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"],
                check=True
            )
        # Install Google Chrome
        subprocess.run(
            ["sudo", "apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"],
            check=True
        )
        print("Google Chrome installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during Chrome installation: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure 'wget' and 'apt' are available.")
        return False

# Function to check if Google Chrome is installed
def is_chrome_installed():
    try:
        subprocess.run(
            ["google-chrome-stable", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False

# Function to retrieve the value using Selenium
def retrieve_value():
    # Ensure Chrome is installed
    if not is_chrome_installed() and not install_google_chrome():
        raise Exception("Google Chrome installation failed.")

    # Set up Chrome options for headless execution
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Disable sandbox for cloud environments
    options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage in cloud

    # Initialize the WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Open the target URL
        driver.get("https://app.tavily.com/")  # Replace with the correct URL

        # Wait for the "Sign up" link to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/u/signup/identifier"]'))
        )

        # Locate and click the "Sign up" link
        sign_up_link = driver.find_element(By.CSS_SELECTOR, 'a[href*="/u/signup/identifier"]')
        sign_up_link.click()

        # Wait for the email input field to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Locate the email input field
        email_field = driver.find_element(By.ID, "email")

        # Input a random Gmail address
        email_field.send_keys("test_email@gmail.com")  # Replace with your email generation logic

        # Wait for and click the "Continue" button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        continue_button.click()

        # Wait for the password input field to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        # Input a random password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("random_password123!")  # Replace with your password generation logic

        # Wait for and click the final "Continue" button
        final_continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        final_continue_button.click()

        # Wait for the input field with the value to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.css-ggff38 input.chakra-input"))
        )

        # Retrieve the value from the input field
        input_field = driver.find_element(By.CSS_SELECTOR, "td.css-ggff38 input.chakra-input")
        input_value = input_field.get_attribute("value")

        return input_value
    finally:
        # Close the driver after usage
        driver.quit()

# Flask route to call retrieve_value and return the result
@app.route("/get_value", methods=["GET"])
def get_value():
    try:
        value = retrieve_value()
        return jsonify({"retrieved_value": value}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
