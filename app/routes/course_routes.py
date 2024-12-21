from flask import Blueprint, request, jsonify
from app import db
from app.models.course import Course, CourseSchedule
from app.schemas.course import CourseSchema
from datetime import datetime

# Create the blueprint
course_bp = Blueprint('courses', __name__, url_prefix='/api/courses')
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M:%S').time()
    except ValueError:
        return datetime.strptime(time_str, '%H:%M').time()

@course_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify(courses_schema.dump(courses))

@course_bp.route('/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course_schema.dump(course))

@course_bp.route('/', methods=['POST'])
def create_course():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Print received data for debugging
        print("Received data:", data)
        
        # Create course instance
        try:
            course = Course(
                code=data.get('code'),
                name=data.get('name'),
                description=data.get('description'),
                credits=data.get('credits'),
                instructor=data.get('instructor'),
                semester=data.get('semester'),
                capacity=data.get('capacity'),
                status=data.get('status', 'active')
            )
        except Exception as e:
            print("Error creating course:", str(e))
            return jsonify({'error': 'Invalid course data', 'details': str(e)}), 400
        
        # Add schedules
        schedule_data = data.get('schedule', [])
        for schedule in schedule_data:
            try:
                course_schedule = CourseSchedule(
                    day=schedule['day'],
                    start_time=parse_time(schedule['start_time']),
                    end_time=parse_time(schedule['end_time'])
                )
                course.schedule.append(course_schedule)
            except Exception as e:
                print("Error creating schedule:", str(e))
                return jsonify({'error': 'Invalid schedule data', 'details': str(e)}), 400
        
        db.session.add(course)
        db.session.commit()
        
        return jsonify(course_schema.dump(course)), 201
        
    except Exception as e:
        db.session.rollback()
        print("Error in create_course:", str(e))
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@course_bp.route('/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    
    # Update basic course info
    for key, value in data.items():
        if key != 'schedule' and hasattr(course, key):
            setattr(course, key, value)
    
    # Update schedule if provided
    if 'schedule' in data:
        # Remove existing schedules
        course.schedule.clear()
        
        # Add new schedules
        for schedule in data['schedule']:
            course_schedule = CourseSchedule(
                day=schedule['day'],
                start_time=parse_time(schedule['start_time']),
                end_time=parse_time(schedule['end_time'])
            )
            course.schedule.append(course_schedule)
    
    db.session.commit()
    return jsonify(course_schema.dump(course))

@course_bp.route('/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204

@course_bp.route('/<int:id>/schedule', methods=['GET'])
def get_course_schedule(id):
    course = Course.query.get_or_404(id)
    return jsonify(CourseSchema(only=('schedule',)).dump(course))

@course_bp.route('/<int:id>/status', methods=['PATCH'])
def update_course_status(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    
    if 'status' in data:
        course.status = data['status']
        db.session.commit()
        return jsonify({'status': course.status})
    
    return jsonify({'error': 'Status not provided'}), 400

# ... rest of your route handlers ... 