import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# ?? GOOGLE SHEETS AUTHENTICATION ??
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "client_secret.json"  # Replace with your OAuth file
TOKEN_FILE = "token.json"  # Stores access token

creds = None

# ?? Check if token.json exists (to reuse authentication)
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# ?? If no valid credentials, authenticate user
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())  # Refresh token if expired
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)  # First-time login

    # ?? Save credentials for next time
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

# ?? Authenticate with Google Sheets
client = gspread.authorize(creds)

# Open the Google Spreadsheet (Replace with your actual sheet name)
SHEET_NAME = "2025 GESTIUNE DOSARE"
WORKSHEET_NAME = "Descarcate_platforma"

spreadsheet = client.open(SHEET_NAME)
worksheet = spreadsheet.worksheet(WORKSHEET_NAME)  # ?? Select the specific worksheet

# ?? SELENIUM AUTOMATION ??
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Website login details
url = "****************************"
username = "***********************"
password = "***********************"

try:
    # Open the login page
    driver.get(url)

    # Log in
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(driver, 10).until(EC.url_contains("validate-requests"))
    print("Login successful!")

    # Navigate to the table page
    driver.get("https://avizaredm.anmdm.ro/validate-requests")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

    # Initialize list to store all data
    all_table_data = []
    last_page_data = None  # Store previous page data for comparison

    while True:
        # Extract table data
        try:
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            rows = table.find_elements(By.TAG_NAME, "tr")

            table_data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                table_data.append([col.text for col in cols])

            # Check if the new page has the same data as the last one
            if table_data == last_page_data:
                print("Detected duplicate page data. Exiting loop.")
                break  # Stop if the data is the same as the last page

            all_table_data.extend(table_data)
            last_page_data = table_data  # Update last page data

        except Exception as e:
            print(f"Error extracting table data: {e}")

        # Locate the "Next" button
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//i[@class='bi bi-arrow-right-short']/parent::*"))
            )

            # Check if button is disabled
            is_disabled = next_button.get_attribute("aria-disabled")
            next_button_class = next_button.get_attribute("class")

            if is_disabled == "true" or "disabled" in next_button_class.lower():
                print("Reached last page. Exiting loop.")
                break  # Exit if "Next" is disabled

            # Click the button
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)

        except Exception as e:
            print("No more pages to scrape or Next button not clickable.")
            break  # Exit the loop safely if the button is not found or not clickable

    # ?? SEND DATA TO SPECIFIC GOOGLE SHEETS WORKSHEET ??
    worksheet.batch_clear(["A:Q"])
    if all_table_data:
        worksheet.update(all_table_data,"A2")  # Start from A2# Append all rows to the selected worksheet
        print(f"Data successfully sent to Google Sheet: {SHEET_NAME}, Worksheet: {WORKSHEET_NAME}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
