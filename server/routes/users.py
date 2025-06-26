from flask import Blueprint, request, jsonify
from models.user import User
from __init__ import db
from email_validator import validate_email, EmailNotValidError

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200

@users_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validation
    if not data.get('name') or not data.get('email') or not data.get('track'):
        return jsonify({'error': 'Name, email, and track are required'}), 400
    
    # Email validation
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    new_user = User(
        name=data['name'],
        email=data['email'],
        track=data['track'],
        is_instructor=data.get('is_instructor', False)
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        # Email validation
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists for another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != id:
            return jsonify({'error': 'Email already registered'}), 400
        
        user.email = data['email']
    if 'track' in data:
        user.track = data['track']
    if 'is_instructor' in data:
        user.is_instructor = data['is_instructor']
    
    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 