from app.models import db, Project
from datetime import datetime
import random
import string
import json

# -------- Tools -------- 

# Function: generate_string
# Description: Generats a random id string
def generate_string(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function: allowed_file
# Description: checks if the filename has the correct extension
def allowed_file(filename, extention):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extention


# ------ Functions ------ 

# Function: create_configuration_file
# Description: create a json configuration file for a project
def create_configuration_file(data):

    config_path=data['Dataset_Filepath'][:-4]+'.json'

    # Write data to the JSON file
    with open(config_path, 'w') as json_file:
        json.dump(data, json_file)

    return config_path

# Function: add_project
# Description: Adds a new project to database
def add_project(name, dataset_filepath=''):

    # get timestamp in string format
    now=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # Data to be written to the JSON file
    data = {
        "Project_Name": name,
        "Creation_Date": now,
        "Dataset_Filepath": dataset_filepath,
        "Results":{}
    }

    # create project's configuration file
    config_filepath=create_configuration_file(data)

    # add new project to db
    project = Project(id=generate_string(),name=name,dataset_path=dataset_filepath, config_path=config_filepath, date=now)
    db.session.add(project)
    db.session.commit()

# Function: remove_project
# Description: Removes a project from database using the ID
def remove_project(project_id):
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return 1
    else:
        return 0

# Function: get_projects
# Description: Returns all the projects inside the Database
def get_projects():
    return Project.query.all()

# Function: get_project_with_id
# Description: Returns a project using the ID
def get_project_with_id(project_id):
    return Project.query.get(project_id)

