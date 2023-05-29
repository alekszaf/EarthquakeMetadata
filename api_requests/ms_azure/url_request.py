"""
This script retrieves the children (files and folders) of a specific folder
in a user's OneDrive using the Microsoft Graph API.
"""

import json
import requests
import api.msa.generate_access_token as generate_access_token


def get_folder_children(user_email, folder_path, access_token, timeout=None):
    """
    Retrieves the children (files and folders) of a specific folder in a user's OneDrive.

    Args:
        user_email (str): The email address of the user whose OneDrive is to be accessed.
        folder_path (str): The path of the folder whose children are to be retrieved.
        access_token (str): The access token used for authentication with the Microsoft Graph API.
        timeout (float, optional): The maximum time allowed for the request to complete, in seconds.

    Returns:
        dict: A dictionary containing the metadata of the folder's children.
    """

    headers = {"Authorization": f"Bearer {access_token}"}

    folder_url = (
        f"https://graph.microsoft.com/v1.0/users/{user_email}/drive/root:/{folder_path}"
    )
    response = requests.get(folder_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    folder_id = response.json()["id"]

    children_url = f"https://graph.microsoft.com/v1.0/users/{user_email} \
                    /drive/items/{folder_id}/children"
    response = requests.get(children_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = json.loads(response.content)

    return data


def main():
    """
    The main function of the script that retrieves and prints the URLs of the files
    in the specified folder.
    """

    user_email = "nsmw4@newcastle.ac.uk"
    folder_path = "/Documents/Qsync/research/EEFIT/new grant/nepal/photos"
    access_token = generate_access_token.token_request()
    data = get_folder_children(user_email, folder_path, access_token)

    file_urls = []
    for file in data["value"]:
        file_name = file["name"]
        file_url = file["webUrl"]
        file_urls.append(file_url)
        print(f"{file_name}: {file_url}")

    print(len(file_urls))


if __name__ == "__main__":
    main()
