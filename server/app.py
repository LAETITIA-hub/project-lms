from __init__ import create_app, db
from models.user import User
from models.course import Course
from models.enrollment import Enrollment
from models.discussion import Discussion

app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=True) 