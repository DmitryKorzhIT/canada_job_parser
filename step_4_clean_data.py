import pandas as pd
import re
from datetime import datetime, timedelta

# Define the function to check for valid email
def is_valid_email(email):
    if isinstance(email, str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
    return False

# Define the function to check for recent dates
def is_recent_date(date, weeks=4):
    return datetime.now() - date <= timedelta(weeks=weeks)

# Define keywords list
keywords = ['kitchen', 'kitchen helper', 'cook', 'cook helper']
data_path = 'data/20240725205928__Calgary_vacancies_data(part_1).csv'
cleaned_suffix = '_cook'
cleaned_name = data_path.replace('.csv', '') + cleaned_suffix + '.csv'

# Load the .csv file into a DataFrame
df = pd.read_csv(data_path, sep='|', header=None, names=['link', 'email', 'title', 'company', 'date'])

# Debugging: Check the first few rows and column names
print("DataFrame loaded with columns:", df.columns)
print(df.head())

# Remove rows with missing or incorrect email data
df = df[df['email'].apply(is_valid_email)]

# Convert the 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Debugging: Check for any NaT values in 'date' column after conversion
print("Rows with invalid date format:")
print(df[df['date'].isna()])

# Remove rows where the date is older than 4 weeks
df = df[df['date'].apply(is_recent_date)]

# Sort the DataFrame by date from newest to oldest
df = df.sort_values(by='date', ascending=False)

# Extract rows where the 'title' matches any keyword in the list
keyword_df = df[df['title'].apply(lambda x: any(keyword in x for keyword in keywords))]

# Save the extracted DataFrame with keywords to another .csv file
keyword_df.to_csv(cleaned_name, index=False)

print(f"Data cleaning and extraction complete. File saved as '{cleaned_name}'.")
