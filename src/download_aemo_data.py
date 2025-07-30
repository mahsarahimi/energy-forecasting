import os
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime

BASE_URL = "https://nemweb.com.au/Reports/Current/Demand30/"

def download_latest_demand_data(save_dir="data/raw"):
    os.makedirs(save_dir, exist_ok=True)
    today = datetime.now().strftime('%Y%m%d')
    filename = f"PUBLIC_DISPATCHLOAD_{today}000000.zip"
    url = BASE_URL + filename
    print(f"Fetching: {url}")

    r = requests.get(url)
    if r.status_code == 200:
        with ZipFile(BytesIO(r.content)) as zip_file:
            zip_file.extractall(save_dir)
            print(f"Extracted to {save_dir}")
    else:
        print("Data not available yet or invalid URL.")

if __name__ == "__main__":
    download_latest_demand_data()
