import csv
import datetime
import random

# Set the start date for the time series
start_date = datetime.date(2020, 1, 1)

# Create a list of dates for the time series
dates = [start_date + datetime.timedelta(days=i) for i in range(365 * 3)]

# Create a list of values for the time series
values = [random.randint(1, 100) for _ in range(len(dates))]

# Save the time series to a CSV file
with open('time_series_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'target'])
    for i in range(len(dates)):
        writer.writerow([dates[i], values[i]])