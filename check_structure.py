import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase-service-account.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get a sample of documents to understand structure
docs = db.collection('student_results').limit(20).stream()
regular_found = False
supply_found = False

for doc in docs:
    doc_id = doc.id
    print(f'Document ID: {doc_id}')
    
    if 'regular' in doc_id and not regular_found:
        data = doc.to_dict()
        print(f'REGULAR Sample keys: {list(data.keys()) if data else "No data"}')
        print(f'REGULAR Sample: {data}')
        regular_found = True
        print('='*50)
    
    elif 'supply' in doc_id and not supply_found:
        data = doc.to_dict()
        print(f'SUPPLY Sample keys: {list(data.keys()) if data else "No data"}')
        print(f'SUPPLY Sample: {data}')
        supply_found = True
        print('='*50)
    
    if regular_found and supply_found:
        break
    
    print('---')
