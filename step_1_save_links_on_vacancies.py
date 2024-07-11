import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Path to the ChromeDriver executable
chrome_driver_path = './chromedriver/chromedriver'  # Assuming chromedriver is in the virtual environment

# Initialize ChromeDriver
chrome_service = Service(chrome_driver_path)
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service)
driver.maximize_window()

# URL to load
url = 'https://www.jobbank.gc.ca/home'
driver.get(url)


# Main code

# Load constants from the file
constants = {}
with open("constants.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split(" = ")
            constants[key] = eval(value)

# Determine constants from the file
SEARCH_TITLE = constants['SEARCH_TITLE']
SEARCH_LOCATION = constants['SEARCH_LOCATION']

# Enter search title
search = driver.find_element(By.ID, "searchString")
search.clear()
search.send_keys(SEARCH_TITLE)
time.sleep(2)

# Enter location title
location = driver.find_element(By.ID, "locationstring")
location.clear()
location.send_keys(SEARCH_LOCATION)
time.sleep(2)

# Press search button
search_btn = driver.find_element(By.ID, "searchButton")
search_btn.click()
time.sleep(2)

# Decrease kilometer range
decrease_km_btn = driver.find_element(By.ID, "decrease-slider")
for i in range(5):
    decrease_km_btn.click()
    time.sleep(1)
time.sleep(10)

# Save amount of vacancies
vacancies_found = driver.find_element(By.CLASS_NAME, "results-summary")
vacancies_found = vacancies_found.find_element(By.CLASS_NAME, "found")
vacancies_found = vacancies_found.text

# Press button "more results" maximum times
try:
    while True:
        more_results_btn = driver.find_element(By.ID, "moreresultbutton")
        more_results_btn.click()
        time.sleep(5)
except Exception:
    pass

# Save link on vacancies to a list
links_list = []
vacancies = driver.find_elements(By.CLASS_NAME, "resultJobItem")
for vacancy in vacancies:
    link = vacancy.get_attribute("href")
    links_list.append(link)

# Get the current date and time in specific format
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")

# Create a folder named "data" if it doesn't exist
folder_name = "data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
file_name = str(f"{formatted_datetime}_{SEARCH_TITLE}_{SEARCH_LOCATION}_vacancies_links.csv")
file_path = os.path.join(folder_name, file_name)

# Save list of vacancies to a .csv file
with open(file_path, mode="w") as file:
    for link in links_list:
        file.write(f"{link},\n")

# Report
print("Report:")
print("Vacancies found:", vacancies_found)
print("Vacancies added:", len(links_list))
print("\n\n\n")

# Close the browser
driver.quit()
