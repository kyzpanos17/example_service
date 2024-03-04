# Service Example

## Description

This is an example python Flask service project. It has an SQLITE database with only one table called projects. 
Each project contains an

   - ID string(32): A random-generated unique ID.
   - name string(255): The name of the project.
   - dataset_path string(255): The path to the project's dataset.
   - config_path string(255): The path to the project's configuration file.
   - date = string(255): The create date of the project in string format (%d/%m/%Y, %H:%M:%S)

The example python Flask service contains an API that the user can interqact with the app.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [API](#api)
- [License](#license)

## Installation

### Using Python Virtual Environments:

   1. Clone this repository
   2. Navigate to your Flask app directory
   3. Create a Python Virtual Environment: `python3 -m venv example_service_env`
   4. Activate the Virtual Environment:
      - On macOS/Linux: `source example_service_env/bin/activate`
      - On Windows: `example_service_env\Scripts\activate`
   5. Install Requirements:
      Install the requirements from requirements.txt: `pip install -r requirements.txt`

### Using Conda Environments:

   1. conda create --name example_service python=3.10
   2. conda activate example_service
   3. Navigate to your Flask app directory
   4. pip install -r requirements.txt

## Usage

Run your Flask app using: `python app.py`

or 

Set the environment variable to point to the entry point of the Flask application: 

   - On macOS/Linux: `export FLASK_APP=app.py`
   - On Windows: `set FLASK_APP=app.py`

and then run the Flask app: `flask run`

## Deployment 

On the app.py file: 

   1. Uncomment line: `from waitress import serve` to import the wsgi server called waitress
   2. Uncomment line: `serve(app, host="0.0.0.0", port=5000)` to serve the app using waitress
   3. Comment line: app.run(debug=False, host='0.0.0.0', port=5000)

On the app/__init__.py file:
   
   Change line: 

   `app.config.from_object('config.development')` 

   to 

   `app.config.from_object('production.py')`

This line will use the production instance of the database.

### Containerization:
Use Docker to create a 'production' app container:

   1. Navigate to your Flask app directory
   2. Build the container: `docker build -t example_app .`
   3. Deploy container: `docker run --name example_app -d -p 5000:5000 example_app`


## API
Navigate to `/apidocs` to interact with the API using the flasgger interface. The APP uses swagger API protocol

Example API routes:

   - `POST /api/add_project`: Add a new project.
   - `GET /api/get_project/<project_id>`: Get project details by ID.
   - `GET /api/get_projects`: Get all projects.
   - `DELETE /api/remove_project/<project_id>`: Remove a project.
   - `POST /api/upload/`: Upload a dataset in csv format. Optionally, specify the project name to create a new project with that dataset.

## License

This project is licensed under the MIT License - see the LICENSE file for details.