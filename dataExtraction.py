import pandas as pd
from datetime import datetime, timedelta

# Read the file
df = pd.read_csv('Copy_of_Assignment_Timecard.xlsx - Sheet1.csv', delimiter=',')

# Convert the Time and Time Out columns to datetime objects
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Sort the dataframe by Employee Name and Time
df = df.sort_values(by=['Employee Name', 'Time'])

# Create a new column that calculates the difference between the current row's Time and the previous row's Time Out
df['Time Between Shifts'] = df.groupby('Employee Name')['Time'].diff()

# Create a new column that calculates the difference between the current row's Time and the previous row's Time
df['Consecutive Days Worked'] = df.groupby('Employee Name')['Time'].diff().dt.days.ne(1).cumsum()

# Create a new column that calculates the duration of each shift
df['Shift Duration'] = df['Time Out'] - df['Time']

# Find the employees who have worked for 7 consecutive days
consecutive_days = df[df['Consecutive Days Worked'] == 7]['Employee Name'].unique()

# Find the employees who have less than 10 hours of time between shifts but greater than 1 hour
time_between_shifts = df[(df['Time Between Shifts'] > timedelta(hours=1)) & (df['Time Between Shifts'] < timedelta(hours=10))]['Employee Name'].unique()

# Find the employees who have worked for more than 14 hours in a single shift
long_shifts = df[df['Shift Duration'] > timedelta(hours=14)]['Employee Name'].unique()

# Print the results
print(f"Employees who have worked for **7 consecutive days**: {', '.join(consecutive_days)}\n")
print(f"Employees who have **less than 10 hours of time between shifts but greater than 1 hour**: {', '.join(time_between_shifts)}\n")
print(f"Employees who have worked for **more than 14 hours in a single shift**: {', '.join(long_shifts)}\n")
