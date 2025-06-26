from __init__ import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    instructor = db.relationship('User', back_populates='courses_taught')
    enrollments = db.relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    discussions = db.relationship('Discussion', back_populates='course', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructor_id': self.instructor_id,
            'instructor_name': self.instructor.name if self.instructor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'enrollment_count': len(self.enrollments),
            'discussion_count': len(self.discussions)
        } 