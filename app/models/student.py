from app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    enrollment_date = db.Column(db.Date)
    program = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    grades = db.relationship('Grade', back_populates='student', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Student {self.student_id} - {self.first_name} {self.last_name}>'