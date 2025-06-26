from app import app, db
from models.user import User
from models.course import Course
from models.enrollment import Enrollment
from models.discussion import Discussion
import os

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create users
        instructor1 = User(
            name="John Doe",
            email="john.doe@moringa.com",
            track="Software Engineering",
            is_instructor=True
        )
        instructor2 = User(
            name="Jane Smith",
            email="jane.smith@moringa.com",
            track="Data Science",
            is_instructor=True
        )
        student1 = User(
            name="Alice Johnson",
            email="alice.johnson@student.moringa.com",
            track="Software Engineering",
            is_instructor=False
        )
        student2 = User(
            name="Bob Wilson",
            email="bob.wilson@student.moringa.com",
            track="Data Science",
            is_instructor=False
        )
        student3 = User(
            name="Carol Brown",
            email="carol.brown@student.moringa.com",
            track="Software Engineering",
            is_instructor=False
        )

        db.session.add_all([instructor1, instructor2, student1, student2, student3])
        db.session.commit()

        # Create courses
        course1 = Course(
            title="Introduction to Python Programming",
            description="Learn the fundamentals of Python programming language including variables, data types, control structures, functions, and object-oriented programming concepts.",
            instructor_id=instructor1.id
        )
        course2 = Course(
            title="Web Development with React",
            description="Master React.js framework for building modern, interactive web applications. Learn components, state management, and routing.",
            instructor_id=instructor1.id
        )
        course3 = Course(
            title="Data Analysis with Python",
            description="Explore data analysis techniques using Python libraries like Pandas, NumPy, and Matplotlib for data manipulation and visualization.",
            instructor_id=instructor2.id
        )
        course4 = Course(
            title="Machine Learning Fundamentals",
            description="Introduction to machine learning algorithms, model training, and evaluation using scikit-learn and TensorFlow.",
            instructor_id=instructor2.id
        )

        db.session.add_all([course1, course2, course3, course4])
        db.session.commit()

        # Create enrollments
        enrollment1 = Enrollment(user_id=student1.id, course_id=course1.id, progress=75)
        enrollment2 = Enrollment(user_id=student1.id, course_id=course2.id, progress=45)
        enrollment3 = Enrollment(user_id=student2.id, course_id=course1.id, progress=90)
        enrollment4 = Enrollment(user_id=student2.id, course_id=course3.id, progress=30)
        enrollment5 = Enrollment(user_id=student3.id, course_id=course2.id, progress=60)
        enrollment6 = Enrollment(user_id=student3.id, course_id=course4.id, progress=15)

        db.session.add_all([enrollment1, enrollment2, enrollment3, enrollment4, enrollment5, enrollment6])
        db.session.commit()

        # Create discussions
        discussion1 = Discussion(
            content="I'm having trouble understanding list comprehensions in Python. Can someone explain the syntax with examples?",
            user_id=student1.id,
            course_id=course1.id
        )
        discussion2 = Discussion(
            content="List comprehensions are a powerful feature! Here's a simple example: [x*2 for x in range(5)] creates [0,2,4,6,8]. The syntax is [expression for item in iterable].",
            user_id=instructor1.id,
            course_id=course1.id
        )
        discussion3 = Discussion(
            content="What's the best way to handle state in React components? Should I use useState or useReducer?",
            user_id=student2.id,
            course_id=course2.id
        )
        discussion4 = Discussion(
            content="useState is great for simple state, while useReducer is better for complex state logic. For most cases, start with useState and refactor to useReducer if needed.",
            user_id=instructor1.id,
            course_id=course2.id
        )
        discussion5 = Discussion(
            content="Can anyone recommend good resources for learning Pandas? I'm struggling with data manipulation.",
            user_id=student3.id,
            course_id=course3.id
        )
        discussion6 = Discussion(
            content="The official Pandas documentation is excellent! Also check out the '10 minutes to pandas' tutorial. Practice with real datasets from Kaggle.",
            user_id=instructor2.id,
            course_id=course3.id
        )

        db.session.add_all([discussion1, discussion2, discussion3, discussion4, discussion5, discussion6])
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Course.query.count()} courses")
        print(f"Created {Enrollment.query.count()} enrollments")
        print(f"Created {Discussion.query.count()} discussions")

if __name__ == "__main__":
    seed_database()
    app.run(port=5001, debug=True)