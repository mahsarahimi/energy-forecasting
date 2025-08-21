import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
import re

def download_predispatch_30min(base_url, prefix_datetime, save_dir="."):
    """
    Download and extract a 30-min PreDispatchIS file from AEMO.

    Parameters
    ----------
    base_url : str
        URL of the AEMO PreDispatchIS_Reports directory.
    prefix_datetime : str
        Datetime part to match, e.g., '202508121400'.
    save_dir : str
        Local folder where CSV will be saved.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Step 1: Fetch directory listing
    print(f"🔍 Fetching file list from: {base_url}")
    resp = requests.get(base_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    
    # Step 2: Regex to match desired filename pattern
    pattern = re.compile(rf"^PUBLIC_PREDISPATCHIS_{prefix_datetime}_.+\.zip$")
    matches = [a['href'] for a in soup.find_all("a", href=True) if pattern.match(os.path.basename(a['href']))]
    

    if not matches:
        print(f"❌ No files found for datetime: {prefix_datetime}")
        return None

    # We'll take the first match
    filename = os.path.basename(matches[0])
    file_url = base_url + filename
    print(f"📦 Found: {filename}")

    # Step 3: Download the ZIP
    print(f"⬇️ Downloading from: {file_url}")
    r = requests.get(file_url)
    r.raise_for_status()

    # Step 4: Extract CSV from ZIP
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for name in z.namelist():
            if name.lower().endswith(".csv"):
                output_path = os.path.join(save_dir, name)
                with z.open(name) as f_in, open(output_path, "wb") as f_out:
                    f_out.write(f_in.read())
                print(f"✅ Extracted: {output_path}")
                return output_path

    print("❌ No CSV found inside the ZIP.")
    return None


# Example usage:
if __name__ == "__main__":
    BASE_URL = "https://nemweb.com.au/Reports/CURRENT/PredispatchIS_Reports/"
    DATETIME_PREFIX = "202508121400"  # <-- change this as needed
    SAVE_DIR = "./data/raw/"

    download_predispatch_30min(BASE_URL, DATETIME_PREFIX, SAVE_DIR)
