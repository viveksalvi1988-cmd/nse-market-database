import requests
import pandas as pd
from datetime import datetime

from src.google_sheet import append_to_sheet

def get_bhavcopy_url():
    today = datetime.now().strftime("%d%m%Y")
    url = f"https://www.nseindia.com/content/historical/EQUITIES/{datetime.now().strftime('%Y')}/{datetime.now().strftime('%b').upper()}/cm{today}bhav.csv.zip"
    return url

def download_bhavcopy():
    url = get_bhavcopy_url()

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)

    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("Bhavcopy not available yet")
        return None

    with open("bhavcopy.zip", "wb") as f:
        f.write(response.content)

    print("Bhavcopy downloaded")

def process_bhavcopy():
    df = pd.read_csv("bhavcopy.zip")

    df = df[['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TOTTRDQTY']]

    df['DATE'] = datetime.now().strftime("%Y-%m-%d")

    return df

def update_bhavcopy():
    download_bhavcopy()

    try:
        df = process_bhavcopy()
        append_to_sheet("Bhavcopy", df)
        print("Bhavcopy updated in Google Sheets")
    except Exception as e:
        print("Error:", e)
