import os
import requests
from panoptes_client import Panoptes, Project, SubjectSet, Subject
from loaders.google_cloud_platform.gcp_request import process_files

Panoptes.connect(username="carrowmw", password="2VcqEhRjFKN73Tp")

# check if a project with the desired name already exists
projects = list(
    Project.where(display_name="Learning from Earthquakes (Image Labelling)")
)
if len(projects) > 0:
    learning_from_earthquakes = projects[0]  # use the existing project
else:
    # create a new project with a unique name
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

# check if a subject set with the desired name already exists in the project
subject_sets = list(SubjectSet.where(display_name="Earthquake images subject set"))

if len(subject_sets) > 0:
    # use the existing subject set
    subject_set = subject_sets[0]
else:
    # create a new subject set with a unique name
    subject_set = SubjectSet()
    subject_set.links.project = learning_from_earthquakes
    subject_set.display_name = "Earthquake images subject set"
    subject_set.save()

# reload the project after saving the subject set
learning_from_earthquakes.reload()


# print the subject sets
print(learning_from_earthquakes.links.subject_sets)

# get dataframe from GCP
df = process_files()

# convert dataframe to the dictionary format needed for panoptes subjects
subject_metadata = df.to_dict(orient="records")

learning_from_earthquakes = Project.find(
    slug="learning-from-earthquakes-image-labelling"
)  # slug is a url-friendly version of the project name

# Fetch list of all subjects in the project
subjects = list(Subject.where(project_id=learning_from_earthquakes.id))

# Extract '#filename' metadata from each subject and store in a list
uploaded_files = [subject.metadata["#filename"] for subject in subjects]

new_subjects = []

for i, record in enumerate(subject_metadata):
    # record is a dictionary representing one row of data
    url = record["File URL"]
    metadata = record["File Name"]
    print(f"Processing: {i+1}/{len(subject_metadata)}")

    # check if a subject with the file name already exists
    if metadata in uploaded_files:
        print(f"File {metadata} already uploaded. Skipping.")
        continue

    # download the image file to a local temporary file
    response = requests.get(url)
    local_filename = metadata + ".jpg"
    with open(local_filename, "wb") as f:
        f.write(response.content)

    # create and save the subject
    subject = Subject()
    subject.links.project = learning_from_earthquakes
    subject.add_location(local_filename)
    subject.metadata.update(
        {"#filename": metadata}
    )  # store filename in subject metadata
    subject.save()

    # remove the local temporary file after upload
    os.remove(local_filename)

    new_subjects.append(subject)

print("Processing completed.")

# add the new subjects to the subject set
subject_set.add(new_subjects)

print("New subjects added to the subject set")
