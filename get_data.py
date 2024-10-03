from config import API_KEY, ESTABLISHMENT_MAPPING, ESTABLISHMENT_NAME, DAY_OFFSET
from datetime import timedelta, datetime
import pandas as pd
import requests


# Function for pulling the date and transforming with offset to get yesterdays' date
def get_date_from_offset(offset):
    # Get today's date
    today_date = datetime.now().date()

    # Offset the date with the offset argument
    yesterday_date = today_date - timedelta(offset)

    # Changing the format to fit the query param requirements of URL
    return yesterday_date.strftime('%m/%d/%y')


# Creating a dataframe for holding and transforming the data pulled from the API endpoint
def get_data():
    # Empty dataset for holding data
    data = []
    # Establishment URL. Iterates ++ at the end of each loop
    est = 1

    # Getting the date for yesterday based on offset
    date = get_date_from_offset(DAY_OFFSET)

    # Print statement to show that the data is being generated
    print("Pulling data from", date)

    # Running the loop 21 times to get all establishments
    for _ in range(21):

        # We do not want the information from the corporate account (est 2), and there is no establishment 3 in MC?
        # Skips those establishments
        if est != 2 and est != 3:

            # URL that we are going to be calling with the API
            url = f"https://{ESTABLISHMENT_NAME}.revelup.com/reports/hourly_sales/json/"

            querystring = {
                "aggregate_format": "hours",
                "show_unpaid": "1",
                "show_discounts": "1",
                "show_taxes": "1",
                "show_irregular": "1",
                "no-filter": "0",
                "range_from": f"{date} 00:00:00",
                "range_to": f"{date} 23:59:59",
                "establishment": f"{est}"
            }

            headers = {
                "API-AUTHENTICATION": API_KEY
            }

            # Pulling the data with the request library
            response = requests.request("GET", url, headers=headers, params=querystring)

            # Converting the data to JSON
            r = response.json()

            # Set based on the starting time that they are pulling data. 8 = 8:00 AM - 8:59 AM
            hour = 8

            # Looping through the hours in the JSON 16 times to pull all requested hours
            for _ in range(16):
                # Following the JSON structure to pull the sales total from each hour
                sales_value = r["hours"][hour][1]['sales']
                # Doing the same thing for the number of orders per hour
                order_value = r["hours"][hour][1]['n_orders']

                # Appending data to the list
                data.append({'Establishment': est, 'Hour': hour, 'Sales': sales_value, 'Orders': order_value})

                # Increasing the hour by 1 with each pass through this loop
                hour += 1

        # Increasing the establishment variable with each loop. Tells the script to go to the next location
        est += 1

    # Create DataFrame from the list
    df = pd.DataFrame(data)
    # Maps the names to the float values held in the dataframe after API returns the data
    df['Establishment'] = df['Establishment'].map(ESTABLISHMENT_MAPPING).fillna(df['Establishment'])
    df['Hour'] = df['Hour'].apply(transform_hour_format)

    ''' Moving Hour to the front of the columns'''
    # Get a list of all the columns
    cols = list(df.columns)

    # Remove 'Hour' from the list
    cols.remove('Hour')

    # Putting 'Hour' column first
    df = df[['Hour'] + cols]

    return df


# Function for altering the hour format to fit natural language
def transform_hour_format(hour):
    if hour == 11:
        return '11 AM - 12 PM'
    elif hour == 12:
        return '12 PM - 1 PM'
    elif hour == 23:
        return '11 PM - 12 AM'
    elif hour < 13:
        return f'{hour} AM - {hour + 1} AM'
    else:
        hour -= 12
        return f'{hour} PM - {hour + 1} PM'
