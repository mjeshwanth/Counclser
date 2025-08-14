"""
Script to fetch all data from student_results collection in Firebase
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

def fetch_all_students(db):
    """Fetch all student data from student_results collection"""
    
    try:
        # Get all documents from student_results collection
        students_ref = db.collection('student_results')
        docs = students_ref.stream()
        
        all_students = []
        
        for doc in docs:
            student_data = doc.to_dict()
            student_data['document_id'] = doc.id
            all_students.append(student_data)
            
        print(f"\nFound {len(all_students)} students in the database")
        print("="*50)
        
        for i, student in enumerate(all_students, 1):
            print(f"\nStudent {i}:")
            print(f"Document ID: {student['document_id']}")
            
            # Print all fields in the document
            for key, value in student.items():
                if key != 'document_id':
                    if isinstance(value, list):
                        print(f"{key}: {len(value)} items")
                        if len(value) > 0:
                            print(f"  Sample item: {value[0]}")
                    else:
                        print(f"{key}: {value}")
            print("-" * 30)
        
        return all_students
        
    except Exception as e:
        print(f"Error fetching students: {e}")
        return []

def analyze_structure(students):
    """Analyze the data structure to understand format"""
    
    if not students:
        print("No students found to analyze")
        return
    
    print("\n" + "="*50)
    print("DATA STRUCTURE ANALYSIS")
    print("="*50)
    
    # Get common fields
    all_fields = set()
    for student in students:
        all_fields.update(student.keys())
    
    print(f"Common fields found: {list(all_fields)}")
    
    # Sample detailed analysis of first student
    if students:
        print(f"\nDetailed analysis of first student:")
        sample_student = students[0]
        
        for key, value in sample_student.items():
            print(f"\nField: {key}")
            print(f"Type: {type(value)}")
            print(f"Value: {value}")
            
            if isinstance(value, list) and len(value) > 0:
                print(f"List item type: {type(value[0])}")
                print(f"Sample list item: {value[0]}")

if __name__ == "__main__":
    print("Fetching all data from student_results collection...")
    db = setup_firebase()
    
    if db:
        students = fetch_all_students(db)
        analyze_structure(students)
        
        # Save to JSON file for reference
        with open('fetched_students.json', 'w') as f:
            json.dump(students, f, indent=2, default=str)
        print(f"\nData saved to 'fetched_students.json' for reference")
    else:
        print("Failed to connect to Firebase. Please check your credentials.")
