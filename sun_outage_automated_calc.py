import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
satellite_name_mapping = {
"ASTRA 1L":"ASTRA 1L",
"SES-6":"SES-6",
"ASTRA 4A":"ASTRA 4A (SIRIUS 4)",
"Eutelsat Hot Bird 13C (13 E)":"EUTELSAT HOT BIRD 13C",
"Nilesat 201 (7 W)":"NILESAT 201",
"Eutelsat Hot Bird 13E (13 E)":"EUTELSAT HOT BIRD 13E",
"Eutelsat Hot Bird 13B (13 E)":"EUTELSAT HOT BIRD 13B",
"AMC-11":"AMC-11 (GE-11)",
"Measat 3A (91.5 E)":"MEASAT-3A",
"Badr 4 (26 E)":"BADR-4",
"Eutelsat 9B (9 E)":"EUTELSAT 9B",
"ASTRA 3C":"ASTRA 3B",
"Eutelsat 7 West A (7.3 W)":"EUTELSAT 7 WEST A",
"Eutelsat 8 West B (8 W)":"EUTELSAT 8 WEST B",
"AsiaSat 7 (105.5 E)":"ASIASAT 7",
"ABS 2 (75 E)":"ABS-2",
"SES-9":"SES-9",
"ASTRA 2F":"ASTRA 2F",
"SES-5":"SES-5",
"NSS-12":"NSS-12",
"ASTRA 1KR":"ASTRA 1KR",
"ASTRA 1N":"ASTRA 1N",
"ASTRA 1M":"ASTRA 1M",
"Intelsat 20 (68.5 E)":"INTELSAT 20 (IS-20)",
"ASTRA 2G":"ASTRA 2G",
"ASTRA 3B":"ASTRA 3B",
"SES-4":"SES-4",
"ASTRA 2E":"ASTRA 2e",
"Arabsat 5C (20 E)":"ArabSat-5c",
"Thor 6 (0.8 W)":"THOR 6",
"Express AM6 (53 E)":"EXPRESS-AM6",
"Apstar 7 (76.5 E)":"APSTAR 7",
"AsiaSat 5 (100.5 E)":"ASIASAT 5",
"Badr 8 (26 E)":"BADR-7 (ARABSAT-6B)",
"Arabsat 5A (30.5 E)":"ArabSat-5a",
"BelinterSat-1 (51.5 E)": "BELINTERSAT-1",
"Amos 3 (4.0 W)":"AMOS-3",
"Amos 7 (3.9 W)":"ASIASAT 8",
"Eutelsat 7B (7 E)":"EUTELSAT 7B",
"AlYah1":"YAHSAT 1A",
"Hellas Sat 3 (39 E)":"HELLAS-SAT 3",
"Nilesat 102 (7 W)":"NILESAT 102",
"Es'hail 2 (25.8 E)":"EUTELSAT 25B",
"AzerSpace-1":"AZERSPACE 1",
"Thaicom 5 (78.5 E)":"THAICOM 5",
"YahSat1A":"YAHSAT 1A",
"XTAR-EUR (29 E)":"XTAR-EUR",
"SES-11":"SES-11",
"Intelsat 21 (58 W)":"INTELSAT 21 (IS-21)",
"SES-18":"SES-3",
"Intelsat 34 (55.5 W)":"INTELSAT 34 (IS-34)",
"Galaxy 32 (91 W)":"GALAXY 17 (G-17)",
"Galaxy 19 (97 W)":"GALAXY 19 (G-19)",
"Galaxy 13 (127 W)":"GALAXY 13 (HORIZONS-1)",
"Galaxy 16 (99 W)":"GALAXY 16 (G-16)",
"SES-14":"NSS-806",
"SES-19 (135 W)":"AMC-7 (GE-7)",
"SES-15":"CIEL-2",
"SES-21 (131W)":"AMC-11 (GE-11)",
"Telstar 12 VANTAGE (15 W)":"TELSTAR 12V",
"Eutelsat 3B (3.1 E)":"EUTELSAT 3B",
"Eutelsat 10B (10 E)":"EUTELSAT 10A",
"Measat 3A (91.4 E)":"MEASAT-3A",
"Turksat 3A (42 E)":"TURKSAT 3A",
"SES-3":"SES-3",
"AsiaSat 9 (122 E)":"ASIASAT 9"

}
# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

url = "https://gi.globaltt.com/Tools/ToolsSolarOutage.aspx"
driver.get(url)

try:
    # Function to get the dropdown
    def get_dropdown():
        return Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div[2]/select"))
        ))

    # Function to get location button
    def get_location():
        return WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/a[3]/span"))
        )

    # Function to select a country
    def select_country(country_name):
        country_dropdown = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/select"))
        ))
        country_dropdown.select_by_visible_text(country_name)

    # Function to enter a city name
    def enter_city(city_name):
        city_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[2]/div[2]/input"))
        )
        city_input.clear()
        city_input.send_keys(city_name)

    # Function to select a frequency band
    def select_band(band_name):
        band_dropdown = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[4]/div[2]/select"))
        ))
        band_dropdown.select_by_visible_text(band_name)

    # Function to click the calculate button
    def click_calculate():
        calculate_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div/div[1]/div/div/div/div[3]/div[3]/div/div/a"))
        )
        calculate_btn.click()
        print("Clicked 'Calculate' button!")

    # Function to extract table data
    def extract_table(xpath):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        table = driver.find_element(By.XPATH, xpath)
        rows = table.find_elements(By.TAG_NAME, "tr")

        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            data.append([cell.text for cell in cells])

        return data

    # Function to select the closest matching satellite name
    def select_closest_match(partial_text):
        max_retries = 3  # Retry mechanism for handling stale elements

        # Use mapping to get the closest match for satellite name
        mapped_name = satellite_name_mapping.get(partial_text, partial_text)  # Default to input if no mapping found

        for attempt in range(max_retries):
            try:
                dropdown = get_dropdown()  # Re-fetch dropdown each time
                options = dropdown.options  # Get updated options list
                
                for option in options:
                    option_text = option.text.strip()
                    if mapped_name.lower() in option_text.lower():  # Case-insensitive contains check
                        dropdown.select_by_visible_text(option_text)
                        print(f"Selected closest match: {option_text}")
                        return  # Success
                
                raise ValueError(f"No matching option found for '{mapped_name}' in the dropdown.")

            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    print(f"StaleElementReferenceException! Retrying... ({attempt + 1}/{max_retries})")
                    time.sleep(1)  # Wait before retrying
                else:
                    print("Failed to select a satellite due to stale element issues.")
                    raise  # Raise exception after max retries

    # Load data from Excel
    satellites = {}
    file_path = "export_insight.xlsx"
    df = pd.read_excel(file_path, usecols=[2, 8, 9, 10, 19, 20, 21, 22])  # Indexing starts at 0
    df = df.values.tolist()

    for line in df:
        satellite_name = line[4]

        if "EHA" in str(line[0]):
            country = "Israel"
            city = "Netiv HaLamed He"

            if isinstance(line[7], (int, float)):
                if line[7] < 100:
                    line[7] *= 1000
                elif line[7] > 100000:
                    line[7] /= 1000

                band = "C Band" if line[7] < 10000 else "Ku Band"

                if satellite_name not in satellites:
                    satellites[satellite_name] = set()
                
                satellites[satellite_name].add((country, city, band))  # Store as a tuple in a set
                satellites = {key: value for key, value in satellites.items() if pd.notna(key)}


    # Convert sets back to lists for further processing
    for satellite in satellites:
        satellites[satellite] = [{"country": loc[0], "city": loc[1], "band": loc[2]} for loc in satellites[satellite]]

    # Print extracted satellite data (now without duplicates)
    for satellite_name, locations in satellites.items():
        print(f"{satellite_name}: {locations}")
    all_data = []

    # Process each satellite
    for satellite, locations in satellites.items():
        try:
            select_closest_match(satellite)  # Now uses the improved function with retries
        except ValueError as e:
            print(e)
            continue  # Skip this satellite if no match is found

        print(f"Selected Satellite: {satellite}")
        time.sleep(2)

        location = get_location()
        location.click()
        print("Selected Location Mode!")
        time.sleep(2)

        for loc in locations:
            select_country(loc["country"])
            time.sleep(2)
            enter_city(loc["city"])
            time.sleep(2)
            select_band(loc["band"])
            time.sleep(2)
            print(f"Entered: {loc['country']} - {loc['city']} - {loc['band']}")

            click_calculate()
            time.sleep(5)

            # Extract data from both tables
            spring_data = extract_table("/html/body/form/div[3]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/table")
            autumn_data = extract_table("/html/body/form/div[3]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/table")

            # Store the results
            for row in spring_data:
                all_data.append([satellite, loc["country"], loc["city"], "Spring"] + row + [loc["band"]])

            for row in autumn_data:
                all_data.append([satellite, loc["country"], loc["city"], "Autumn"] + row + [loc["band"]])

finally:
    driver.quit()

# Define headers for Excel
headers = ["Satellite", "Country", "City", "Season", "Start", "End", "Duration", "Min. antenna diameter", "Band"]

# Save results to an Excel file
df = pd.DataFrame(all_data, columns=headers)
df.to_excel("solar_outage_results.xlsx", index=False)
print("Results saved to solar_outage_results.xlsx")
