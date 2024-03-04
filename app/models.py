from flask_sqlalchemy import SQLAlchemy

# Define Database
db = SQLAlchemy()

# Database Classes
class Project(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    dataset_path = db.Column(db.String(255))
    config_path = db.Column(db.String(255))
    date = db.Column(db.String(255))

    def __repr__(self):
        return f"<Project {self.id}>"