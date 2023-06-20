"""
This script sends an API request to the Earthquake photos bucket on the Google Cloud platform.
"""

import os
from google.cloud import storage
from google.oauth2.service_account import Credentials
import pandas as pd

# define the bucket name and service account key file path
BUCKET_NAME = "test_photos_earthquake_research"
KEY_FILE = "service_account_key.json"
PATH = "./package/apis/loaders/google_cloud_platform/"
KEY_FILE_PATH = os.path.join(PATH, KEY_FILE)


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
    """
    Retrieves the file URLs and file names from a specified Google Cloud bucket,
    and stores them in a Pandas DataFrame.

    The function uses predefined constants to define the Google Cloud bucket name,
    the path of the service account key, and the relevant file path.

    Returns:
        df (pandas.DataFrame): A DataFrame containing file URLs and file names
        from the specified bucket. The DataFrame has two columns - 'File URL' and
        'File Name'.
    """

    # get the file URLs and file names
    file_urls, file_names = get_bucket_file_info(BUCKET_NAME, KEY_FILE_PATH)

    # create a Pandas DataFrame
    file_info_df = pd.DataFrame({"File URL": file_urls, "File Name": file_names})

    return file_info_df


# this section only runs if the script is being run directly
if __name__ == "__main__":
    df = process_files()

    # save the dataframe to a csv file
    OUTPUT_FILE = "output.csv"
    df.to_csv(os.path.join(PATH, OUTPUT_FILE), index=False)
