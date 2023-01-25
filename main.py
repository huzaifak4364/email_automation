from googleapiclient.discovery import build
import pandas as pd
import time
from send_email import send_email
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials
import json


spreadsheet_id = '1422gMeYwrhGoMXasvQ8_FDoxiTAblM5yivfJyYO3w7M'

range_name = 'Sheet1!A1:Z1000'

creds = Credentials.from_service_account_file(
        'email-374509-4f72425b93d2.json', scopes=["https://www.googleapis.com/auth/spreadsheets"])

service = build('sheets', 'v4', credentials=creds)

result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()

df = pd.DataFrame(result.get('values', []))

initial_rows = df.shape[0]

while True:

    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
    df = pd.DataFrame(result.get('values', []))

    current_rows = df.shape[0]
    if current_rows > initial_rows:

        send_email(df.iloc[-1])  #
        initial_rows = current_rows

    time.sleep(3)