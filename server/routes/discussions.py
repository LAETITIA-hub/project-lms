from models.discussion import Discussion
from models.user import User
from models.course import Course
from __init__ import db
from flask import Blueprint, request, jsonify

discussions_bp = Blueprint('discussions', __name__)

@discussions_bp.route('', methods=['GET'])
def get_discussions():
    discussions = Discussion.query.all()
    return jsonify([discussion.to_dict() for discussion in discussions]), 200

@discussions_bp.route('/<int:id>', methods=['GET'])
def get_discussion(id):
    discussion = Discussion.query.get_or_404(id)
    return jsonify(discussion.to_dict()), 200

@discussions_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_discussions(course_id):
    discussions = Discussion.query.filter_by(course_id=course_id).order_by(Discussion.timestamp.desc()).all()
    return jsonify([discussion.to_dict() for discussion in discussions]), 200

@discussions_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_discussions(user_id):
    discussions = Discussion.query.filter_by(user_id=user_id).order_by(Discussion.timestamp.desc()).all()
    return jsonify([discussion.to_dict() for discussion in discussions]), 200

@discussions_bp.route('', methods=['POST'])
def create_discussion():
    data = request.get_json()
    
    # Validation
    if not data.get('content') or not data.get('user_id') or not data.get('course_id'):
        return jsonify({'error': 'content, user_id, and course_id are required'}), 400
    
    # Content length validation
    if len(data['content']) < 15:
        return jsonify({'error': 'Discussion content must be at least 15 characters long'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if course exists
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Create discussion
    new_discussion = Discussion(
        content=data['content'],
        user_id=data['user_id'],
        course_id=data['course_id']
    )
    
    try:
        db.session.add(new_discussion)
        db.session.commit()
        return jsonify(new_discussion.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<int:id>', methods=['PATCH'])
def update_discussion(id):
    discussion = Discussion.query.get_or_404(id)
    data = request.get_json()
    
    if 'content' in data:
        if len(data['content']) < 15:
            return jsonify({'error': 'Discussion content must be at least 15 characters long'}), 400
        discussion.content = data['content']
    
    try:
        db.session.commit()
        return jsonify(discussion.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@discussions_bp.route('/<int:id>', methods=['DELETE'])
def delete_discussion(id):
    discussion = Discussion.query.get_or_404(id)
    
    try:
        db.session.delete(discussion)
        db.session.commit()
        return jsonify({'message': 'Discussion deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 