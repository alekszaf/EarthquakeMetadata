"""
This script sends an API request to the Earthquake photos bucket on the Google Cloud platform.
"""

from google.cloud import storage
from google.oauth2.service_account import Credentials
import pandas as pd
import os


def get_bucket_file_info(bucket_name, key_file_path):
    """
    Retrieve the file URLs and file names from the specified bucket.

    Args:
        bucket_name (str): Name of the bucket.
        key_file_path (str): Path to the service account key file.

    Returns:
        tuple: A tuple containing lists of file URLs and file names.
    """
    credentials = Credentials.from_service_account_file(key_file_path)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    urls = []
    names = []
    for blob in blobs:
        urls.append(blob.public_url)
        names.append(blob.name)

    return urls, names


def process_files():
    # Define the bucket name and service account key file path
    BUCKET_NAME = "test_photos_earthquake_research"
    KEY_FILE = "service_account_key.json"
    PATH = "./package/api_requests/google_cloud_platform/"
    KEY_FILE_PATH = os.path.join(PATH, KEY_FILE)

    # Get the file URLs and file names
    file_urls, file_names = get_bucket_file_info(BUCKET_NAME, KEY_FILE_PATH)

    # Create a Pandas DataFrame
    df = pd.DataFrame({"File URL": file_urls, "File Name": file_names})

    # Print the DataFrame
    print(df)

    # Save the dataframe to a csv file
    OUTPUT_FILE = "output.csv"
    df.to_csv(os.path.join(PATH, OUTPUT_FILE), index=False)


if __name__ == "__main__":
    process_files()