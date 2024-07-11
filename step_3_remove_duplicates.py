import pandas as pd
import os


# Load constants from the file
constants = {}
with open("constants.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split(" = ")
            constants[key] = eval(value)

# Check if the vacancies links file and data folder exist
folder_name = "data"
EMAILS_FILE_NAME = constants['EMAILS_FILE_NAME']
emails_file_path = os.path.join(folder_name, EMAILS_FILE_NAME)
if not os.path.exists(folder_name):
    print("Error #7Jl1: Cannot find the folder data.")
elif not os.path.exists(emails_file_path):
    print("Error #7Jl2: Cannot find the emails file.")

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(emails_file_path, header=None, names=['Email'])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Save the cleaned DataFrame back to a CSV file
file_name = EMAILS_FILE_NAME
remove_name = "emails.csv"
add_name = "emails_clean.csv"
if EMAILS_FILE_NAME.endswith(remove_name):
    file_name = file_name[:len(file_name) - len(remove_name)].strip()
    file_name = file_name + add_name
    file_path = os.path.join(folder_name, file_name)
    df.to_csv(file_path, index=False, header=False)
else:
    print("Error #7JL5: Cannot create a name for a file with clean emails")
