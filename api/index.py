import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify

app = Flask(__name__)

# Function to generate a random password (8 characters, at least 3 types of characters)
def generate_random_password():
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice(string.punctuation)
    
    remaining_chars = random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation,
        k=4
    )
    
    password = [lowercase, uppercase, digit, special] + remaining_chars
    random.shuffle(password)
    return ''.join(password)

# Function to generate a random Gmail address
def generate_random_gmail():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@gmail.com"

# Function to run the Selenium script and get the value
def retrieve_value():
    # Set up Chrome options
    options = Options()
    options.add_experimental_option("detach", True)

    # Initialize WebDriver
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

        # Locate the "Sign up" link and click it
        sign_up_link = driver.find_element(By.CSS_SELECTOR, 'a[href*="/u/signup/identifier"]')
        sign_up_link.click()

        # Wait for the email input field to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )

        # Locate the email input field using the 'id' attribute
        email_field = driver.find_element(By.ID, "email")

        # Generate a random Gmail address
        random_gmail = generate_random_gmail()

        # Enter the generated email into the input field
        email_field.send_keys(random_gmail)

        # Wait for the "Continue" button to be clickable
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # Click the "Continue" button
        continue_button.click()

        # Wait for the password input field to appear after clicking "Continue"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        # Generate a random password that meets the requirements
        random_password = generate_random_password()

        # Locate the password input field
        password_field = driver.find_element(By.ID, "password")

        # Wait for the password field to be clickable before entering the password
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )

        # Click on the password field to ensure it's focused
        password_field.click()

        # Enter the generated password into the password field
        password_field.send_keys(random_password)

        # Wait for the final "Continue" button to be clickable and click it
        final_continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        final_continue_button.click()

        # Wait for the next button (chakra-button) to be clickable and click it
        final_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.chakra-button.css-1a1nl3a'))
        )
        final_button.click()

        # Wait for the input field with the value to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.css-ggff38 input.chakra-input"))
        )

        # Locate the input field and get its value
        input_field = driver.find_element(By.CSS_SELECTOR, "td.css-ggff38 input.chakra-input")
        input_value = input_field.get_attribute("value")

        return input_value

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        driver.quit()

# Define the Flask route to trigger the Selenium function and return the result
@app.route('/get_value', methods=['GET'])
def get_value():
    value = retrieve_value()
    return jsonify({"retrieved_value": value})

if __name__ == '__main__':
    app.run(debug=True)
