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

# Create a name for the file emails
file_name = VACANCIES_LINKS_FILE_NAME
remove_name = "_vacancies_links.csv"
add_name = "_emails.csv"
if file_name.endswith(remove_name):
    file_name = file_name[:len(file_name) - len(remove_name)].strip()
    file_name = file_name + add_name
else:
    print("Error #L9Q1: Cannot create a name for a file with emails")

# Create the file emails
folder_name = "data"
if not os.path.exists(folder_name):
    print("Error #9Jo2: The folder 'data' does not exist.")
emails_file_path = os.path.join(folder_name, file_name)
with open(emails_file_path, "w") as file:
    pass

# Load each url
for link in links:
    driver.get(link)
    time.sleep(5)

    # Click apply button
    try:
        apply_btn = driver.find_element(By.ID, "applynowbutton")
        apply_btn.click()
        time.sleep(6)
    except Exception:
        time.sleep(4)
        try:
            apply_btn = driver.find_element(By.ID, "applynowbutton")
            apply_btn.click()
            time.sleep(6)
        except Exception:
            print(f"{datetime.now()}:   Apply button is not found. Exception error #C8X1. Error! ")

    # Extract email address
    try:
        apply_info = driver.find_element(By.ID, "applynow")
        hyperlink_elements = apply_info.find_elements(By.TAG_NAME, "a")
        for i in range(len(hyperlink_elements)):
            link = hyperlink_elements[i].get_attribute("href")
            if "mailto:" in link:
                email = link[len("mailto:"):]

                # Add email address to the file
                with open(emails_file_path, 'a') as file:
                    file.write(f"{email},\n")
                    print(f"{datetime.now()}:   Email is added successfully!")
            else:
                print(f"{datetime.now()}:   This link doesn't contain an email!")
    except Exception:
        print(f"{datetime.now()}:   Email is not added! Exception error #7Jn2. Error! ")

# Report

# Total vacancies in the file
with open(vacancies_file_path, "r") as file:
    vacancies_lines = file.readlines()
    vacancies_lines = len(vacancies_lines)

# Total emails in the file
with open(emails_file_path, "r") as file:
    emails_lines = file.readlines()
    emails_lines = len(emails_lines)

# Print report
print("\n")
print("Report:")
print("Vacancies found:", vacancies_lines)
print("Emails found:", emails_lines)
print("\n")
