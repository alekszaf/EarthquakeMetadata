# Import necessary modules
import os
import sys
import requests
from panoptes_client import Panoptes, Project, SubjectSet, Subject
from package.apis.loaders.google_cloud_platform.gcp_request import process_files

# Connect to the Zooniverse Panoptes API
Panoptes.connect(username="carrowmw", password="2VcqEhRjFKN73Tp")

# Get the current working directory
root = os.getcwd()
print(root)

# Append the path of the 'package' folder to the system path
sys.path.append(os.path.join(root, "\package"))

# Check if a project with the specified display name already exists
projects = list(
    Project.where(display_name="Learning from Earthquakes (Image Labelling)")
)
if len(projects) > 0:
    # If yes, use the existing project
    learning_from_earthquakes = projects[0]
else:
    # Otherwise, create a new project
    learning_from_earthquakes = Project()
    learning_from_earthquakes.display_name = (
        "Learning from Earthquakes (Image Labelling)"
    )
    learning_from_earthquakes.description = (
        "A project for labelling earthquakes so we can learn from them"
    )
    learning_from_earthquakes.primary_language = "en"
    learning_from_earthquakes.private = True
    learning_from_earthquakes.save()

# Check if a subject set with the specified name already exists
subject_sets = list(SubjectSet.where(display_name="Earthquake images subject set"))

if len(subject_sets) > 0:
    # If yes, use the existing subject set
    subject_set = subject_sets[0]
else:
    # Otherwise, create a new subject set
    subject_set = SubjectSet()
    subject_set.links.project = learning_from_earthquakes
    subject_set.display_name = "Earthquake images subject set"
    subject_set.save()

# Reload the project to update it with the newly saved subject set
learning_from_earthquakes.reload()

# Print the linked subject sets of the project
print(learning_from_earthquakes.links.subject_sets)

# Fetch the data from Google Cloud Platform (GCP) and store it in a DataFrame
df = process_files(bucket_name="photos_for_zooniverse")

# Convert the DataFrame to dictionary format suitable for Panoptes subjects
subject_metadata = df.to_dict(orient="records")

# Fetch the list of subjects for the project
subjects = list(Subject.where(project_id=learning_from_earthquakes.id))

# Create a list containing filenames of already uploaded subjects
uploaded_files = [subject.metadata["#filename"] for subject in subjects]

new_subjects = []

# Loop through the metadata to create new subjects
for i, record in enumerate(subject_metadata):
    url = record["File URL"]
    metadata = record["File Name"]
    print(f"Processing: {i+1}/{len(subject_metadata)}")

    # Skip already uploaded files
    if metadata in uploaded_files:
        print(f"File {metadata} already uploaded. Skipping.")
        continue

    # Download the image file locally
    response = requests.get(url)
    local_filename = metadata + ".jpg"
    with open(local_filename, "wb") as f:
        f.write(response.content)

    # Create a new subject
    subject = Subject()
    subject.links.project = learning_from_earthquakes
    subject.add_location(local_filename)

    # Add 'File Name' and 'File URL' to metadata
    subject.metadata.update(
        {"#filename": metadata, "File Name": metadata, "File URL": url}
    )

    subject.save()

    # Delete the local file after upload
    os.remove(local_filename)

    new_subjects.append(subject)

# Add new subjects to the subject set
if len(new_subjects) > 0:
    subject_set.add(new_subjects)
    print("New subjects added to the subject set.")
    print("Processing completed.")
else:
    print("No new subjects added")
