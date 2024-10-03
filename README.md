# Hourly Sales Auto Report

This project automates the retrieval and reporting of hourly sales data from the Revel API. It addresses the challenge faced by the unnamed corporation, where a single report pulling data from all establishments at once is unavailable. By automating the process of extracting, filtering, and formatting sales data, this project streamlines what was previously a manual and time-consuming task.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Improvements](#improvements)

## Introduction

The corporation runs daily sales reports for all of its establishments. Manually downloading and compiling this data into Excel files for analysis was a labor-intensive process. This script automates the process by pulling data directly from the Revel Hourly Sales API endpoint.

The pulled data is stored in a DataFrame and filtered based on specific conditions, such as each establishment's hours of operation and any filters used in running the report. Once filtered, the data is exported to an .xlsx file for report generation.

To maintain formatting, the report is linked to a template .xlsx file using pivot tables, avoiding direct overwriting. The script also ensures that the data connections in the report are updated before saving the final version.

The project runs as a scheduled task on a Windows operating system, executing daily and emailing the completed report to specified recipients.

## Features

- Automates pulling hourly sales data from Revel API for all establishments.
- Filters the data based on hours of operation and user-specified conditions.
- Exports the data to an .xlsx file while preserving pivot table formatting.
- Sends the final report via email to selected recipients.
- Configured to run daily as an .exe through Windows Task Scheduler.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/BLibs/Revel_Hourly_Sales_Auto_Report.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Revel_Hourly_Sales_Auto_Report
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Update the `config.py` file in the project directory and define the following variables:

```python
API_KEY = “Add API key here”
EXCEL_PW = "Excel file password goes here"
PATH = r"C:\PATH TO FILE GOES HERE"

# Email based variables
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'Gmail account address would go here (sender)'
EMAIL_PASSWORD = 'Gmail account password goes here'
RECIPIENT_EMAIL = ['Recipient email address goes here (can be a list of multiple recipients)']
```

## Usage 

The script can either be ran directly as a Python file or compiled into an .exe with Pyinstaller
- Run the script to start the automation process:
    ```sh
    python main.py
    ```
- Compile the .exe which can then be ran in any environment.
    ```sh
    pyinstaller --onefile --clean main.py

## Improvements

1. Consider switching from Windows Task Scheduler to a cloud-based job scheduler for greater flexibility and scalability.
2. Add logging functionality to capture daily report generation details and potential errors.
