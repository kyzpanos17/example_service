from app import app
import app.services as sv
import app.models as ml
from flask import jsonify, request, render_template_string
from werkzeug.utils import secure_filename
import markdown2
import os

# ------ API Calls ------ 

# GET: get_projects
# Description:# Home call returns description of the Project
@app.route('/')
def index():
    
    try:
        # Read the contents of the README.md file
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(readme_content)

        # Render the HTML template with the README content
        return render_template_string(html_content)

    except:
        app.logger.error('Error: README.md file was not found.')
        return "Error: File was not found!", 500

# GET: get_projects
# Description: The user can retrieve all the project created in the App
@app.route('/api/get_projects', methods=['GET'])
def get_projects():
    try:
        projects = sv.get_projects()
        resp=[]
        for project in projects:
            resp.append({
                "id":project.id,
                "name":project.name,
                "dataset_path":project.dataset_path,
                "config_path":project.config_path,
                "date":project.date
            })
        return jsonify(resp), 200
    except:
        return jsonify({'message': 'Projects were not retrieved'}), 500

# GET: get_project
# Description: The user can retrieve a project by providing the Project's ID
@app.route('/api/get_project/<string:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = sv.get_project_with_id(project_id)
        if project is None:
            return jsonify({'message': 'Project was not retrieved (Invalid ID)'}), 422
        else:
            return jsonify({
                'id': project.id, 
                'name': project.name, 
                'dataset_path': project.dataset_path, 
                'config_path': project.config_path, 
                'date': project.date}), 200
    except:
        return jsonify({'message': 'Project was not retrieved (Invalid ID)'}), 422

# DELETE: add_project
# Description: The user can add a new project by providing a new Project Name
@app.route('/api/add_project', methods=['POST'])
def add_project():
    try:
        data = request.json
        sv.add_project(data['name'])
        return jsonify({'message': 'Project added successfully'}), 200
    except:
        return jsonify({'message': 'Project was not added'}), 422

# POST: remove_project
# Description: The user can delete a project by providing the Project's ID
@app.route('/api/remove_project/<string:project_id>', methods=['DELETE'])
def remove_project(project_id):
    try:
        ret = sv.remove_project(project_id)

        if ret!=1:
            return jsonify({'message': 'Project was not deleted (Invalid ID)'}), 422
        else:
            return jsonify({'message': 'Project removed successfully'}), 200
    except:
        return jsonify({'message': 'Project was not deleted (Invalid ID)'}), 422

# POST: upload
# Description: The user can upload a file (attach to new project using project name optional)
@app.route('/api/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 422

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'file not uploaded'}), 400

    if file and sv.allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):

        if len(file.read()) > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'message': 'File size exceeds the limit'}), 413

        filename = sv.generate_string(length=10)+"_"+secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Get additional data from form fields
        project_name = request.form.get('project_name')
        if project_name:

            # add new project with attached
            sv.add_project(project_name,os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify({'success': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 415