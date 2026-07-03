import gspread
import pandas as pd
import os
import json

def get_client():
    creds = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    gc = gspread.service_account_from_dict(creds)
    return gc

def append_to_sheet(sheet_name, df):

    gc = get_client()
    sh = gc.open_by_key(os.environ["GOOGLE_SHEET_ID"])
    worksheet = sh.worksheet(sheet_name)

    data = df.values.tolist()

    worksheet.append_rows(data)
