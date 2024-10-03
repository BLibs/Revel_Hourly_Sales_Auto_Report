from config import *
from email_file import send_report_email
from file_handling import handle_file
from get_data import get_data, get_date_from_offset
import pandas as pd
import time


''' This project is designed to pull data from the Revel Hourly Sales API endpoint. This project is necessary
    because there is no single report that can pull this data for all establishments at once. The unnamed 
    corporation in this example runs these reports daily for all establishments. They would then take the data
    from those reports and put them in an Excel file for analysis. This turned into a time consuming process.
    
    Pulling the data from the API endpoint, a dataframe is used to store everything. The data is then filtered 
    based on a few conditions, including the hours of operation for the establishments and the filters that they 
    include when running the numbers. Filtered data is then output to an .xlsx file to generate a report.
    
    The report is generated from a linked .xlsx file using pivot tables for formatting. Overwriting the file directly
    would have removed formatting, so data linkage was the best option. 
    
    The report is handled to ensure that the data connection is updating and that the file is saving, which is all
    done through controlling the operating system (Windows in this case).
    
    Once completed, the report is emailed to the requested recipients. This runs as an .exe file linked to a 
    scheduled task on the operating system daily.  '''


# Main application logic
def main():
    # Getting the data. Returns a filtered dataframe
    df = get_data()

    # Export to Excel file
    output_path = 'data_files/output.xlsx'
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, index=False)

    # Handle the file (OS operations to update report file with output.xlsx data)
    handle_file(PATH)
    time.sleep(5)

    # Email the file
    send_report_email(PATH, f"{ABR_EST_NAME} Hourly Sales File " + get_date_from_offset(DAY_OFFSET))


if __name__ == "__main__":
    main()
