from __init__ import db
from datetime import datetime

class Discussion(db.Model):
    __tablename__ = 'discussions'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='discussions')
    course = db.relationship('Course', back_populates='discussions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user_name': self.user.name if self.user else None,
            'course_title': self.course.title if self.course else None
        } 