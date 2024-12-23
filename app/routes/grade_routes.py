from flask import Blueprint, request, jsonify
from app import db
from app.models.grade import Grade
from app.models.student import Student
from app.models.course import Course
from app.schemas.grade import GradeSchema
from datetime import datetime

grades_bp = Blueprint('grades', __name__, url_prefix='/api/grades')
grade_schema = GradeSchema()
grades_schema = GradeSchema(many=True)

@grades_bp.route('/', methods=['GET'])
def get_all_grades():
    grades = Grade.query.all()
    return jsonify([{
        'id': grade.id,
        'student_id': grade.student_id,
        'course_id': grade.course_id,
        'score': grade.score,
        'semester': grade.course.semester if grade.course else None,
        'submission_date': grade.submission_date.isoformat() if grade.submission_date else None,
        'comments': grade.comments,
        'student': {
            'id': grade.student.id,
            'student_id': grade.student.student_id,
            'first_name': grade.student.first_name,
            'last_name': grade.student.last_name,
            'email': grade.student.email
        } if grade.student else None,
        'course': {
            'id': grade.course.id,
            'code': grade.course.code,
            'name': grade.course.name,
            'semester': grade.course.semester
        } if grade.course else None
    } for grade in grades])

@grades_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_grades(course_id):
    grades = Grade.query.filter_by(course_id=course_id).all()
    return jsonify([{
        'id': grade.id,
        'student_id': grade.student_id,
        'course_id': grade.course_id,
        'score': grade.score,
        'semester': grade.course.semester if grade.course else None,
        'submission_date': grade.submission_date.isoformat() if grade.submission_date else None,
        'comments': grade.comments,
        'student': {
            'id': grade.student.id,
            'student_id': grade.student.student_id,
            'first_name': grade.student.first_name,
            'last_name': grade.student.last_name,
            'email': grade.student.email
        } if grade.student else None,
        'course': {
            'id': grade.course.id,
            'code': grade.course.code,
            'name': grade.course.name,
            'semester': grade.course.semester
        } if grade.course else None
    } for grade in grades])

@grades_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student_grades(student_id):
    grades = Grade.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': grade.id,
        'student_id': grade.student_id,
        'course_id': grade.course_id,
        'score': grade.score,
        'semester': grade.course.semester if grade.course else None,
        'submission_date': grade.submission_date.isoformat() if grade.submission_date else None,
        'comments': grade.comments,
        'course': {
            'id': grade.course.id,
            'code': grade.course.code,
            'name': grade.course.name
        } if grade.course else None
    } for grade in grades])

@grades_bp.route('/<int:id>', methods=['PUT'])
def update_grade(id):
    grade = Grade.query.get_or_404(id)
    data = request.get_json()

    grade.score = data.get('score', grade.score)
    grade.comments = data.get('comments', grade.comments)
    grade.submission_date = datetime.utcnow()
    grade.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'id': grade.id,
        'student_id': grade.student_id,
        'course_id': grade.course_id,
        'score': grade.score,
        'semester': grade.course.semester if grade.course else None,
        'submission_date': grade.submission_date.isoformat(),
        'comments': grade.comments
    })

@grades_bp.route('/', methods=['POST'])
def create_grade():
    data = request.get_json()
    
    new_grade = Grade(
        student_id=data['student_id'],
        course_id=data['course_id'],
        score=data.get('score'),
        comments=data.get('comments'),
        submission_date=datetime.utcnow() if data.get('score') is not None else None
    )

    db.session.add(new_grade)
    db.session.commit()

    return jsonify({
        'id': new_grade.id,
        'student_id': new_grade.student_id,
        'course_id': new_grade.course_id,
        'score': new_grade.score,
        'semester': new_grade.course.semester if new_grade.course else None,
        'submission_date': new_grade.submission_date.isoformat() if new_grade.submission_date else None,
        'comments': new_grade.comments
    }), 201

@grades_bp.route('/<int:id>', methods=['DELETE'])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    return '', 204