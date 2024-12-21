from app import db
from datetime import datetime

class CourseSchedule(db.Model):
    __tablename__ = 'course_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    schedule = db.relationship('CourseSchedule', backref='course', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', back_populates='course', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.code} - {self.name}>'