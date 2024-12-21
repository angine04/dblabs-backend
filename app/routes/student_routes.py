from flask import Blueprint, request, jsonify
from app import db
from app.models.student import Student
from app.schemas.student import StudentSchema
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Create the blueprint
student_bp = Blueprint('students', __name__, url_prefix='/api/students')
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

def format_student(student):
    return {
        'id': student.id,
        'studentId': student.student_id,
        'firstName': student.first_name,
        'lastName': student.last_name,
        'email': student.email,
        'dateOfBirth': student.date_of_birth.isoformat() if student.date_of_birth else None,
        'enrollmentDate': student.enrollment_date.isoformat() if student.enrollment_date else None,
        'program': student.program,
        'status': student.status,
        'contactNumber': student.contact_number,
        'createdAt': student.created_at.isoformat() if student.created_at else None,
        'updatedAt': student.updated_at.isoformat() if student.updated_at else None
    }

@student_bp.route('/', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        student = Student(**student_schema.load(data))
        db.session.add(student)
        db.session.commit()
        return jsonify(format_student(student)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Student ID or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@student_bp.route('/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([format_student(student) for student in students])

@student_bp.route('/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(format_student(student))

@student_bp.route('/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = Student.query.get_or_404(id)
        data = request.get_json()
        for key, value in student_schema.load(data).items():
            setattr(student, key, value)
        student.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(format_student(student))
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Student ID or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@student_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

@student_bp.route('/search', methods=['GET'])
def search_students():
    query = {}
    
    if 'student_id' in request.args:
        query['student_id'] = request.args['student_id']
    if 'email' in request.args:
        query['email'] = request.args['email']
    if 'program' in request.args:
        query['program'] = request.args['program']
    if 'status' in request.args:
        query['status'] = request.args['status']
    
    students = Student.query.filter_by(**query).all()
    return jsonify([format_student(student) for student in students])