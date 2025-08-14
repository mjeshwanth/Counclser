"""
Sample script to populate Firebase with test student data
Run this script after setting up Firebase credentials
"""

import firebase_admin
from firebase_admin import credentials, firestore
import json

def setup_firebase():
    try:
        cred = credentials.Certificate('firebase-service-account.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase connection established successfully!")
        return db
    except Exception as e:
        print(f"Firebase connection error: {e}")
        return None

def create_sample_students(db):
    """Create sample student data for testing"""
    
    sample_students = [
        {
            'htno': '21A91A0501',
            'name': 'John Doe',
            'branch': 'CSE',
            'year': '2',
            'semester': '3',
            'subjects': [
                {'subject_code': 'CS201', 'subject_name': 'Data Structures', 'credits': 4, 'grade': 'A'},
                {'subject_code': 'CS202', 'subject_name': 'Computer Organization', 'credits': 3, 'grade': 'B+'},
                {'subject_code': 'CS203', 'subject_name': 'Database Management', 'credits': 4, 'grade': 'A+'},
                {'subject_code': 'MA201', 'subject_name': 'Discrete Mathematics', 'credits': 3, 'grade': 'B'},
                {'subject_code': 'EN201', 'subject_name': 'Technical English', 'credits': 2, 'grade': 'A'},
                {'subject_code': 'CS204', 'subject_name': 'Software Engineering', 'credits': 3, 'grade': 'O'}
            ]
        },
        {
            'htno': '21A91A0502',
            'name': 'Jane Smith',
            'branch': 'CSE',
            'year': '2',
            'semester': '3',
            'subjects': [
                {'subject_code': 'CS201', 'subject_name': 'Data Structures', 'credits': 4, 'grade': 'O'},
                {'subject_code': 'CS202', 'subject_name': 'Computer Organization', 'credits': 3, 'grade': 'A+'},
                {'subject_code': 'CS203', 'subject_name': 'Database Management', 'credits': 4, 'grade': 'A'},
                {'subject_code': 'MA201', 'subject_name': 'Discrete Mathematics', 'credits': 3, 'grade': 'A+'},
                {'subject_code': 'EN201', 'subject_name': 'Technical English', 'credits': 2, 'grade': 'O'},
                {'subject_code': 'CS204', 'subject_name': 'Software Engineering', 'credits': 3, 'grade': 'A'}
            ]
        },
        {
            'htno': '21A91A0503',
            'name': 'Mike Johnson',
            'branch': 'CSE',
            'year': '2',
            'semester': '3',
            'subjects': [
                {'subject_code': 'CS201', 'subject_name': 'Data Structures', 'credits': 4, 'grade': 'B'},
                {'subject_code': 'CS202', 'subject_name': 'Computer Organization', 'credits': 3, 'grade': 'C'},
                {'subject_code': 'CS203', 'subject_name': 'Database Management', 'credits': 4, 'grade': 'F'},
                {'subject_code': 'MA201', 'subject_name': 'Discrete Mathematics', 'credits': 3, 'grade': 'P'},
                {'subject_code': 'EN201', 'subject_name': 'Technical English', 'credits': 2, 'grade': 'B+'},
                {'subject_code': 'CS204', 'subject_name': 'Software Engineering', 'credits': 3, 'grade': 'F'}
            ]
        },
        {
            'htno': '21A91A0504',
            'name': 'Sarah Wilson',
            'branch': 'CSE',
            'year': '2',
            'semester': '3',
            'subjects': [
                {'subject_code': 'CS201', 'subject_name': 'Data Structures', 'credits': 4, 'grade': 'A+'},
                {'subject_code': 'CS202', 'subject_name': 'Computer Organization', 'credits': 3, 'grade': 'A'},
                {'subject_code': 'CS203', 'subject_name': 'Database Management', 'credits': 4, 'grade': 'A+'},
                {'subject_code': 'MA201', 'subject_name': 'Discrete Mathematics', 'credits': 3, 'grade': 'B+'},
                {'subject_code': 'EN201', 'subject_name': 'Technical English', 'credits': 2, 'grade': 'A'},
                {'subject_code': 'CS204', 'subject_name': 'Software Engineering', 'credits': 3, 'grade': 'A+'}
            ]
        },
        {
            'htno': '21A91A0505',
            'name': 'David Brown',
            'branch': 'CSE',
            'year': '2',
            'semester': '3',
            'subjects': [
                {'subject_code': 'CS201', 'subject_name': 'Data Structures', 'credits': 4, 'grade': 'C'},
                {'subject_code': 'CS202', 'subject_name': 'Computer Organization', 'credits': 3, 'grade': 'P'},
                {'subject_code': 'CS203', 'subject_name': 'Database Management', 'credits': 4, 'grade': 'B'},
                {'subject_code': 'MA201', 'subject_name': 'Discrete Mathematics', 'credits': 3, 'grade': 'F'},
                {'subject_code': 'EN201', 'subject_name': 'Technical English', 'credits': 2, 'grade': 'C'},
                {'subject_code': 'CS204', 'subject_name': 'Software Engineering', 'credits': 3, 'grade': 'P'}
            ]
        }
    ]
    
    try:
        for student in sample_students:
            htno = student['htno']
            student_data = {k: v for k, v in student.items() if k != 'htno'}
            db.collection('students').document(htno).set(student_data)
            print(f"Added student: {htno} - {student['name']}")
        
        print(f"\nSuccessfully added {len(sample_students)} sample students to Firebase!")
        
    except Exception as e:
        print(f"Error adding students: {e}")

if __name__ == "__main__":
    print("Setting up sample data for Counselor Application...")
    db = setup_firebase()
    
    if db:
        create_sample_students(db)
        print("\nSample data setup complete!")
        print("You can now run the Flask application with: python app.py")
    else:
        print("Failed to connect to Firebase. Please check your credentials.")
