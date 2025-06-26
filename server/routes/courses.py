from models.course import Course
from models.user import User
from __init__ import db
from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@courses_bp.route('/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict()), 200

@courses_bp.route('', methods=['POST'])
def create_course():
    data = request.get_json()
    
    # Validation
    if not data.get('title') or not data.get('description') or not data.get('instructor_id'):
        return jsonify({'error': 'Title, description, and instructor_id are required'}), 400
    
    # Check if instructor exists
    instructor = User.query.get(data['instructor_id'])
    if not instructor:
        return jsonify({'error': 'Instructor not found'}), 404
    
    if not instructor.is_instructor:
        return jsonify({'error': 'User must be an instructor to create courses'}), 400
    
    # Title length validation
    if len(data['title']) < 5:
        return jsonify({'error': 'Title must be at least 5 characters long'}), 400
    
    # Description length validation
    if len(data['description']) < 20:
        return jsonify({'error': 'Description must be at least 20 characters long'}), 400
    
    # Create course
    new_course = Course(
        title=data['title'],
        description=data['description'],
        instructor_id=data['instructor_id']
    )
    
    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:id>', methods=['PATCH'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        if len(data['title']) < 5:
            return jsonify({'error': 'Title must be at least 5 characters long'}), 400
        course.title = data['title']
    
    if 'description' in data:
        if len(data['description']) < 20:
            return jsonify({'error': 'Description must be at least 20 characters long'}), 400
        course.description = data['description']
    
    if 'instructor_id' in data:
        instructor = User.query.get(data['instructor_id'])
        if not instructor:
            return jsonify({'error': 'Instructor not found'}), 404
        if not instructor.is_instructor:
            return jsonify({'error': 'User must be an instructor'}), 400
        course.instructor_id = data['instructor_id']
    
    try:
        db.session.commit()
        return jsonify(course.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'message': 'Course deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 