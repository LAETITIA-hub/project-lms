from __init__ import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    track = db.Column(db.String(50), nullable=False)
    is_instructor = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', back_populates='user', cascade='all, delete-orphan')
    discussions = db.relationship('Discussion', back_populates='user', cascade='all, delete-orphan')
    courses_taught = db.relationship('Course', back_populates='instructor', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'track': self.track,
            'is_instructor': self.is_instructor,
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 