import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os
from datetime import datetime

#written to test commits
def download_predispatch_csv(base_url, file_prefix, save_dir="."):
    # Step 1: Get HTML directory listing
    print(f"🔍 Searching for files at: {base_url}")
    resp = requests.get(base_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Step 2: Find file that starts with the given prefix
    today = datetime.now().strftime('%Y%m%d')
    file_prefix = file_prefix + str(today)
    zip_links = [a["href"] for a in soup.find_all("a", href=True)
                 if a["href"].startswith(file_prefix) and a["href"].endswith(".zip")]
    
    if not zip_links:
        print(f"❌ No files found with prefix: {file_prefix}")
        return None
    
    zip_name = zip_links[0]
    zip_url = base_url + zip_name
    print(f"📦 Found: {zip_name}")
    
    # Step 3: Download ZIP
    print(f"⬇️ Downloading: {zip_url}")
    r = requests.get(zip_url)
    r.raise_for_status()
    
    # Step 4: Extract ZIP and save CSV
    z = zipfile.ZipFile(io.BytesIO(r.content))
    for csv_file in z.namelist():
        if csv_file.endswith(".csv"):
            print(f"🗃️ Extracting: {csv_file}")
            with z.open(csv_file) as f:
                output_path = os.path.join(save_dir, csv_file)
                with open(output_path, "wb") as out_file:
                    out_file.write(f.read())
            print(f"✅ Saved to: {output_path}")
            return output_path

    print("❌ No CSV file found in the ZIP.")
    return None

if __name__ == "__main__":
    base_url = "https://nemweb.com.au/Reports/CURRENT/PreDispatchIS_Reports/"
    file_prefix = "PUBLIC_PREDISPATCHIS_"

    download_predispatch_csv(base_url, file_prefix)

