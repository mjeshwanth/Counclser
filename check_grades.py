import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase-service-account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get sample data to understand grading structure
docs = db.collection('student_results').limit(5).stream()
for doc in docs:
    data = doc.to_dict()
    if data and 'subjectGrades' in data:
        print(f"Student: {data.get('student_id', 'Unknown')}")
        print(f"SGPA: {data.get('sgpa', 0)}")
        print(f"Exam Type: {data.get('examType', 'Unknown')}")
        print("Subject Grades:")
        for grade in data['subjectGrades']:
            code = grade.get('code', 'N/A')
            grade_val = grade.get('grade', 'N/A')
            subject = grade.get('subject', 'N/A')
            print(f"  - {code}: {grade_val} ({subject})")
        print('='*50)
        break
