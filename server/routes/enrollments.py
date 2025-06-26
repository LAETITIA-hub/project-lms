from models.enrollment import Enrollment
from models.user import User
from models.course import Course
from __init__ import db
from flask import Blueprint, request, jsonify

enrollments_bp = Blueprint('enrollments', __name__)

@enrollments_bp.route('', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([enrollment.to_dict() for enrollment in enrollments]), 200

@enrollments_bp.route('/<int:id>', methods=['GET'])
def get_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    return jsonify(enrollment.to_dict()), 200

@enrollments_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_enrollments(user_id):
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    return jsonify([enrollment.to_dict() for enrollment in enrollments]), 200

@enrollments_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_enrollments(course_id):
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return jsonify([enrollment.to_dict() for enrollment in enrollments]), 200

@enrollments_bp.route('', methods=['POST'])
def create_enrollment():
    data = request.get_json()
    
    # Validation
    if not data.get('user_id') or not data.get('course_id'):
        return jsonify({'error': 'user_id and course_id are required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if course exists
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Check if enrollment already exists
    existing_enrollment = Enrollment.query.filter_by(
        user_id=data['user_id'], 
        course_id=data['course_id']
    ).first()
    if existing_enrollment:
        return jsonify({'error': 'User is already enrolled in this course'}), 400
    
    # Create enrollment
    new_enrollment = Enrollment(
        user_id=data['user_id'],
        course_id=data['course_id'],
        progress=data.get('progress', 0)
    )
    
    try:
        db.session.add(new_enrollment)
        db.session.commit()
        return jsonify(new_enrollment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/<int:id>', methods=['PATCH'])
def update_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    data = request.get_json()
    
    if 'progress' in data:
        enrollment.progress = data['progress']
    
    try:
        db.session.commit()
        return jsonify(enrollment.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@enrollments_bp.route('/<int:id>', methods=['DELETE'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    
    try:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({'message': 'Enrollment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 