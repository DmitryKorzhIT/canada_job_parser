import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the ChromeDriver executable
chrome_driver_path = './chromedriver/chromedriver'  # Assuming chromedriver is in the virtual environment

# Set up Chrome options to run headless (without opening the browser)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # applicable to windows os only but still, you can include it
chrome_options.add_argument("--window-size=1920x1080")

# Initialize ChromeDriver
chrome_service = Service(chrome_driver_path)
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()

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
VACANCIES_LINKS_FILE_NAME = constants['VACANCIES_LINKS_FILE_NAME']

# Check if the vacancies links file and data folder exist
folder_name = "data"
file_name = VACANCIES_LINKS_FILE_NAME
vacancies_file_path = os.path.join(folder_name, file_name)
if not os.path.exists(folder_name):
    print("Error #1J31: Cannot find the folder data.")
elif not os.path.exists(vacancies_file_path):
    print("Error #1J32: Cannot find the vacancies links file.")

# Save links from file to list
links = []
with open(vacancies_file_path, mode="r") as file:
    for line in file:
        line = line.strip()
        line = line.split(',')
        links.append(line[0])

# Create a name for the file vacancies_data
file_name = VACANCIES_LINKS_FILE_NAME
remove_name = "_vacancies_links.csv"
add_name = "_vacancies_data.csv"
if file_name.endswith(remove_name):
    file_name = file_name[:len(file_name) - len(remove_name)].strip()
    file_name = file_name + add_name
else:
    print("Error #L9Q1: Cannot create a name for a file with vacancies_data")

# Create the file vacancies_data
folder_name = "data"
if not os.path.exists(folder_name):
    print("Error #9Jo2: The folder 'data' does not exist.")
vacancies_data_file_path = os.path.join(folder_name, file_name)
with open(vacancies_data_file_path, "w") as file:
    pass

# Load each url
for link in links:
    driver.get(link)

    # Determine dictionary with vacancies_data
    vacancies_data = {
        "link": "",
        "email": "",
        "title": "",
        "company": "",
        "date": ""
    }

    # Click apply button
    try:
        apply_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "applynowbutton")))
        apply_btn.click()
    except Exception:
        print(f"{datetime.now()}:   Apply button is not found. Exception error #C8X1. Error! ")
        continue

    # Add link to the dictionary
    try:
        vacancy_link = link
        vacancies_data["link"] = vacancy_link
    except Exception:
        print(f"{datetime.now()}:   Link is not added! Exception error #0aIl. Error! ")

    # Add email address to the dictionary
    try:
        time.sleep(1)
        apply_info = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "applynow")))
        hyperlink_elements = apply_info.find_elements(By.TAG_NAME, "a")
        for i in range(len(hyperlink_elements)):
            link = hyperlink_elements[i].get_attribute("href")
            if "mailto:" in link:
                vacancy_email = link[len("mailto:"):]
                vacancies_data["email"] = vacancy_email
            else:
                print(f"{datetime.now()}:   This link doesn't contain an email!")
    except Exception:
        print(f"{datetime.now()}:   Email is not added! Exception error #7Jn2. Error! ")

    # Add title to the dictionary
    try:
        vacancy_title = driver.find_element(By.ID, "wb-cont")
        vacancy_title = vacancy_title.text
        if "\n" in vacancy_title:
            vacancy_title = vacancy_title.split('\n')[0]
        vacancies_data["title"] = str(vacancy_title)
    except Exception:
        print(f"{datetime.now()}:   Title is not added! Exception error #fa71. Error! ")

    # Add company to the dictionary
    try:
        vacancy_company = driver.find_element('xpath', '//span[@property="hiringOrganization"]')
        vacancy_company = vacancy_company.text
        vacancies_data["company"] = str(vacancy_company)
    except Exception:
        print(f"{datetime.now()}:   Company is not added! Exception error #PJoF. Error! ")

    # Add date to the dictionary
    try:
        vacancy_date = driver.find_element(By.CLASS_NAME, "date")
        vacancy_date = vacancy_date.text

        # Make sure that the date element contain date information
        if "Posted on" in vacancy_date:
            vacancy_date = vacancy_date[len("Posted on"):]
            vacancy_date = vacancy_date.strip()

            # Function to parse and convert date strings to ISO 8601 format
            def convert_date_to_iso(date_str):
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
                return date_obj.strftime("%Y-%m-%d")

            # Convert date from one format to another
            vacancy_date = convert_date_to_iso(vacancy_date)

            # Add date to the dictionary
            vacancies_data["date"] = vacancy_date
        else:
            print(f"{datetime.now()}:   Error #L9j2 with the vacancy_date!")
    except Exception:
        print(f"{datetime.now()}:   Date is not added! Exception error #Ga9j. Error! ")

    # Add vacancies_data to the file
    with open(vacancies_data_file_path, 'a') as file:
        print(vacancies_data)
        file.write(f"{vacancies_data['link']}|"
                   f"{vacancies_data['email']}|"
                   f"{vacancies_data['title']}|"
                   f"{vacancies_data['company']}|"
                   f"{vacancies_data['date']}\n")
        print(f"{datetime.now()}:   Email is added successfully!")

# Report

# Total vacancies in the file
with open(vacancies_file_path, "r") as file:
    vacancies_lines = file.readlines()
    vacancies_lines = len(vacancies_lines)

# Total emails in the file
with open(vacancies_data_file_path, "r") as file:
    emails_lines = file.readlines()
    emails_lines = len(emails_lines)

# Print report
print("\n")
print("Report:")
print("Vacancies found:", vacancies_lines)
print("Emails found:", emails_lines)
print("\n")
