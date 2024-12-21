from app import db
from datetime import datetime

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', back_populates='grades', overlaps="student_ref")
    course = db.relationship('Course', back_populates='grades', overlaps="course_ref")

    def __repr__(self):
        return f'<Grade {self.score}% - Student: {self.student_id} Course: {self.course_id}>'

    @property
    def semester(self):
        return self.course.semester if self.course else None