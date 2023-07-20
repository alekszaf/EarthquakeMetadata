from panoptes_client import Panoptes, Classification, Project
from datetime import datetime
from dateutil.parser import parse

Panoptes.connect(username='carrowmw', password='2VcqEhRjFKN73Tp')

project = Project.find(slug='carrowmw/learning-from-earthquakes-image-labelling')

classifications_export_generator = Classification.where(project_id=project.id)
classifications_export = list(classifications_export_generator)  # convert generator to list - REMOVE LINE BEFORE UPLOADING

for classification in classifications_export:
    print(classification.raw)
    print(classification.href)
    print(classification.links.subjects[0])
    print("-------------------")

for classification in classifications_export:
    print(f"ID: {classification.id}")
    print(f"Annotations: {classification.annotations}")
    print(f"Created at: {classification.created_at}")
    print(f"Updated at: {classification.updated_at}")
    print(f"Live project: {classification.metadata['live_project']}")
    print(f"Already seen: {classification.metadata['subject_selection_state']['already_seen']}")
    print(f"User has finished workflow: {classification.metadata['subject_selection_state']['user_has_finished_workflow']}")
    print(f"User {classification.links.user[0]}")
    print("-------------------")


# The date of the first correct classification
cutoff_date_str = '2023-07-19T20:00:59.041Z'
cutoff_date = parse(cutoff_date_str)

# Your user_id
user_id = '2607538'

filtered_classifications = []

for classification in classifications_export:
    classification_date = parse(classification.created_at)

    if classification_date >= cutoff_date and classification.links['user'] != user_id:
        filtered_classifications.append(classification)

for classification in filtered_classifications:
    print(f"ID: {filtered_classifications.id}")
    print(f"Annotations: {filtered_classifications.annotations}")
    print(f"Created at: {filtered_classifications.created_at}")
    print(f"Updated at: {filtered_classifications.updated_at}")
    print(f"Live project: {filtered_classifications.metadata['live_project']}")
    print(f"Already seen: {filtered_classifications.metadata['subject_selection_state']['already_seen']}")
    print(f"User has finished workflow: {filtered_classifications.metadata['subject_selection_state']['user_has_finished_workflow']}")
    print("-------------------")