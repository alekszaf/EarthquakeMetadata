# Import necessary modules
import json
from panoptes_client import (
    Panoptes,
    Classification,
    Project,
    Subject,
)  # Import Panoptes API client
from datetime import datetime  # For working with datetime objects
from dateutil.parser import parse  # For parsing date strings into datetime objects

# Authenticate to connect to the Zooniverse Panoptes API
Panoptes.connect(username="carrowmw", password="2VcqEhRjFKN73Tp")

# Find and fetch the project by its slug
project = Project.find(slug="carrowmw/learning-from-earthquakes-image-labelling")

# Get all classifications for this project
# Classification.where returns a generator
classifications_export_generator = Classification.where(project_id=project.id)

# Convert the generator to a list for easier manipulation
# NOTE: REMOVE THIS LINE BEFORE UPLOADING
classifications_export = list(classifications_export_generator)

# Define the date after which classifications are considered correct
CUTOFF_DATE_STR = "2023-07-19T20:00:59.041Z"
cutoff_date = parse(CUTOFF_DATE_STR)

# Define the USER_ID to exclude from the list of classifications
USER_ID = "2607531"

# Initialize an empty list to hold classifications that meet certain criteria
filtered_classifications = []

# Loop through all classifications and filter them based on the date and user_id
for classification in classifications_export:
    classification_date = parse(classification.created_at)

    if (
        classification_date >= cutoff_date
        and classification.raw["links"]["user"] != USER_ID
    ):
        filtered_classifications.append(classification)

# Initialize an empty list to hold dictionaries for JSON serialization
json_filtered_classifications = []

# Loop through all classifications and convert them to dictionaries
for classification in filtered_classifications:
    # Fetch the subject to access its metadata
    subject_id = classification.raw["links"]["subjects"][0]
    subject = Subject.find(subject_id)

    json_classification = {
        "ID": classification.id,
        "Annotations": classification.annotations,
        "Subject": classification.raw["links"]["subjects"],
        "Metadata": {
            "File Name": subject.metadata.get("File Name", ""),
            "File URL": subject.metadata.get("File URL", ""),
        },
        "Source": "zooniverse",
    }

    json_filtered_classifications.append(json_classification)

# Save the filtered_classifications as a JSON file
with open("filtered_classifications.json", "w", encoding="utf8") as f:
    json.dump(json_filtered_classifications, f, indent=4)


#############################################################

# Print out details of each filtered classification
for classification in filtered_classifications:
    # Fetch the subject to access its metadata
    subject_id = classification.raw["links"]["subjects"][0]
    subject = Subject.find(subject_id)

    print(f"ID: {classification.id}")
    print(f"Annotations: {classification.annotations}")
    print(f"Subject: {classification.raw['links']['subjects']}")
    print(f"File Name: {subject.metadata.get('File Name', '')}")
    print(f"File URL: {subject.metadata.get('File URL', '')}")
    print("-------------------")

# Print the full list of filtered classifications
print(filtered_classifications)

# TODO: Create a dictionary that relates the answer value from each task to the answer given in zooniverse
