import requests
from tqdm import tqdm
import os
import pyfiglet


def download_nasa(output_file = 'src/data/nasa_exoplanet_data.csv'):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars&format=csv"

    # Use stream=True to download in chunks
    print(f"Downloading data from {url} to {output_file}")
    
    # if no data directory, create it
    if not os.path.exists('src/data'):
        print("No data directory found, creating it...")
        os.makedirs('src/data')
        print("Data directory created successfully.")

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Get file size if available
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_file, 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=output_file) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive chunks
                        file.write(chunk)
                        pbar.update(len(chunk))
        print(f"Data successfully downloaded to {output_file}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")

if __name__ == "__main__":
    # print ascii art
    print(pyfiglet.figlet_format("HI I'M SPENCER"))
    print(pyfiglet.figlet_format("Exoplanet Data Downloader"))
    # if not in root directory, throw an error
    if os.path.dirname(__file__) != os.path.abspath('src'):
        raise ValueError("This script must be run from the root directory, not src/")
    
    print("Downloading NASA exoplanet data...")

    download_nasa()