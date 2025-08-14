"""
Test script to fetch data for specific student IDs and understand the structure better
"""

import firebase_admin
from firebase_admin import credentials, firestore

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

def search_student_by_id(db, student_id):
    """Search for a student by ID in the collection"""
    try:
        # Try to find documents containing the student ID
        students_ref = db.collection('student_results')
        
        # Method 1: Direct document ID search
        possible_doc_ids = [
            f"{student_id}_Unknown_Semester_1_regular",
            f"{student_id}_Unknown_Semester_1_supply",
            student_id
        ]
        
        for doc_id in possible_doc_ids:
            doc = students_ref.document(doc_id).get()
            if doc.exists:
                print(f"Found student with document ID: {doc_id}")
                return doc.to_dict()
        
        # Method 2: Query by student_id field
        query = students_ref.where('student_id', '==', student_id).limit(1)
        docs = query.stream()
        
        for doc in docs:
            print(f"Found student via query with document ID: {doc.id}")
            return doc.to_dict()
        
        print(f"No student found with ID: {student_id}")
        return None
        
    except Exception as e:
        print(f"Error searching for student: {e}")
        return None

def get_sample_student_ids(db, limit=10):
    """Get some sample student IDs from the collection"""
    try:
        students_ref = db.collection('student_results')
        docs = students_ref.limit(limit).stream()
        
        student_ids = []
        for doc in docs:
            data = doc.to_dict()
            student_id = data.get('student_id')
            if student_id:
                student_ids.append(student_id)
        
        return student_ids
    except Exception as e:
        print(f"Error getting sample student IDs: {e}")
        return []

if __name__ == "__main__":
    db = setup_firebase()
    
    if db:
        print("\nGetting sample student IDs...")
        sample_ids = get_sample_student_ids(db, 20)
        print(f"Sample student IDs: {sample_ids[:10]}")
        
        # Test searching for a few students
        test_students = ['17B81A0106', '18B81A0322', '19B81A0284']
        
        for student_id in test_students:
            print(f"\n{'='*50}")
            print(f"Searching for student: {student_id}")
            print(f"{'='*50}")
            
            student_data = search_student_by_id(db, student_id)
            if student_data:
                print(f"Student ID: {student_data.get('student_id')}")
                print(f"SGPA: {student_data.get('sgpa')}")
                print(f"Semester: {student_data.get('semester')}")
                print(f"Number of subjects: {len(student_data.get('subjectGrades', []))}")
                
                # Show subject details
                subjects = student_data.get('subjectGrades', [])
                if subjects:
                    print("\nSubjects:")
                    for i, subject in enumerate(subjects[:3], 1):  # Show first 3 subjects
                        print(f"  {i}. {subject.get('code')} - {subject.get('subject')} - Grade: {subject.get('grade')}")
                    if len(subjects) > 3:
                        print(f"  ... and {len(subjects) - 3} more subjects")
    else:
        print("Failed to connect to Firebase")
