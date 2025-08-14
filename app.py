from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import statistics

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize Firebase Admin SDK
try:
    # Initialize Firebase with service account key
    cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase connection established successfully!")
except Exception as e:
    print(f"Firebase connection error: {e}")
    db = None

def is_htno_in_range(student_id, from_htno, to_htno):
    """Check if a student ID falls within the specified HTNO range"""
    try:
        # Handle different HTNO formats
        # Extract year and numeric parts for comparison
        
        # Get year from student ID (first 2 digits)
        if len(student_id) < 2:
            return False
            
        student_year = student_id[:2]
        from_year = from_htno[:2]
        to_year = to_htno[:2]
        
        # If years don't match the range, exclude
        if student_year < from_year or student_year > to_year:
            return False
        
        # If years match, do more detailed comparison
        if student_year == from_year == to_year:
            # Same year, compare the full IDs lexicographically
            return from_htno <= student_id <= to_htno
        elif student_year == from_year:
            # Student is in the starting year, must be >= from_htno
            return student_id >= from_htno
        elif student_year == to_year:
            # Student is in the ending year, must be <= to_htno
            return student_id <= to_htno
        else:
            # Student is in a year between from and to
            return True
            
    except Exception:
        # If any error in comparison, include the student for safety
        return True

def calculate_sgpa(subjects):
    """Calculate SGPA from subjects with grades - using JNTUK grade system"""
    grade_points = {
        'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6,
        'E': 5, 'F': 0, 'ABSENT': 0, 'COMPLE': 0
    }
    
    total_credits = 0
    total_points = 0
    
    for subject in subjects:
        credits = subject.get('credits', 0)
        grade = subject.get('grade', 'F')
        points = grade_points.get(grade, 0)
        
        total_credits += credits
        total_points += (credits * points)
    
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

def get_failed_subjects(subjects):
    """Get list of failed subjects"""
    failed_subjects = []
    for subject in subjects:
        grade = subject.get('grade', 'F')
        if grade in ['F', 'ABSENT']:
            failed_subjects.append({
                'subject_code': subject.get('code', ''),
                'subject_name': subject.get('subject', ''),
                'grade': grade
            })
    return failed_subjects

def merge_regular_supply_results(student_data_list):
    """
    Merge regular and supply exam results for the same student.
    Supply grades take priority over failed regular grades.
    Returns merged student data with duplicates removed.
    """
    merged_students = {}
    
    for student_data in student_data_list:
        student_id = student_data.get('student_id', '')
        exam_type = student_data.get('examType', 'regular')
        
        if student_id not in merged_students:
            merged_students[student_id] = {
                'student_id': student_id,
                'sgpa': student_data.get('sgpa', 0.0),
                'subjectGrades': {},
                'examType': exam_type,
                'semester': student_data.get('semester', ''),
                'year': student_data.get('year', ''),
                'format': student_data.get('format', ''),
                'university': student_data.get('university', '')
            }
        
        # Process subject grades
        for grade_info in student_data.get('subjectGrades', []):
            subject_code = grade_info.get('code', '')
            grade = grade_info.get('grade', 'F')
            
            if subject_code:
                existing_grade = merged_students[student_id]['subjectGrades'].get(subject_code)
                
                # If no existing grade or current is supply (priority), or existing is F and current is better
                if (not existing_grade or 
                    exam_type == 'supply' or 
                    (existing_grade.get('grade') == 'F' and grade != 'F')):
                    
                    merged_students[student_id]['subjectGrades'][subject_code] = {
                        'code': subject_code,
                        'grade': grade,
                        'subject': grade_info.get('subject', ''),
                        'credits': grade_info.get('credits', 0.0),
                        'internals': grade_info.get('internals', 0),
                        'examType': exam_type
                    }
        
        # Recalculate SGPA based on merged grades
        merged_students[student_id]['sgpa'] = calculate_merged_sgpa(
            list(merged_students[student_id]['subjectGrades'].values())
        )
    
    # Convert back to list format
    result = []
    for student_id, student_data in merged_students.items():
        # Convert subjectGrades dict back to list
        student_data['subjectGrades'] = list(student_data['subjectGrades'].values())
        result.append(student_data)
    
    return result

def calculate_merged_sgpa(subject_grades):
    """Calculate SGPA from merged subject grades."""
    grade_points = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0, 'ABSENT': 0}
    
    total_credits = 0
    weighted_points = 0
    
    for grade_info in subject_grades:
        grade = grade_info.get('grade', 'F')
        credits = float(grade_info.get('credits', 0))
        
        if credits > 0:
            points = grade_points.get(grade, 0)
            weighted_points += points * credits
            total_credits += credits
    
    return round(weighted_points / total_credits, 2) if total_credits > 0 else 0.0

def get_student_documents(student_id):
    """Get all documents (regular and supply) for a student."""
    patterns = [
        student_id,
        f"{student_id}_Unknown_Semester_1_regular",
        f"{student_id}_Unknown_Semester_1_supply",
        f"{student_id}_regular",
        f"{student_id}_supply"
    ]
    
    documents = []
    for pattern in patterns:
        try:
            doc = db.collection('student_results').document(pattern).get()
            if doc.exists:
                data = doc.to_dict()
                data['document_id'] = doc.id
                documents.append(data)
        except Exception:
            continue
    
    # Also search by student_id field
    try:
        query_docs = db.collection('student_results').where('student_id', '==', student_id).stream()
        for doc in query_docs:
            data = doc.to_dict()
            data['document_id'] = doc.id
            # Avoid duplicates
            if not any(d.get('document_id') == doc.id for d in documents):
                documents.append(data)
    except Exception:
        pass
    
    return documents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consolidate', methods=['GET', 'POST'])
def consolidate():
    if request.method == 'POST':
        try:
            from_htno = request.form['from_htno']
            to_htno = request.form['to_htno']
            
            if not db:
                flash('Firebase connection not available', 'error')
                return render_template('consolidate.html')
            
            # Get all student documents and filter by HTNO range
            students_ref = db.collection('student_results')
            all_docs = students_ref.stream()
            
            # Collect all student data within range
            raw_student_data = []
            student_ids_found = set()
            
            for doc in all_docs:
                student_data = doc.to_dict()
                student_id = student_data.get('student_id', '')
                
                # Check if student ID falls within the range
                if is_htno_in_range(student_id, from_htno, to_htno):
                    raw_student_data.append(student_data)
                    student_ids_found.add(student_id)
            
            # Merge regular and supply results to remove duplicates
            merged_student_data = merge_regular_supply_results(raw_student_data)
            
            # Process results for display - limit to 40 students
            results = []
            for student_data in merged_student_data[:40]:  # Limit to 40 students
                student_id = student_data.get('student_id', '')
                subjects = student_data.get('subjectGrades', [])
                
                # Use merged SGPA
                sgpa = student_data.get('sgpa', 0.0)
                failed_subjects = get_failed_subjects(subjects)
                
                results.append({
                    'htno': student_id,
                    'name': f"Student {student_id}",
                    'sgpa': sgpa,
                    'failed_count': len(failed_subjects),
                    'failed_subjects': failed_subjects,
                    'total_subjects': len(subjects),
                    'passed_subjects': len(subjects) - len(failed_subjects)
                })
            
            # Sort results by HTNO for better presentation
            results.sort(key=lambda x: x['htno'])
            
            # Add summary statistics
            total_students = len(results)
            students_with_failures = len([r for r in results if r['failed_count'] > 0])
            
            summary = {
                'total_students': total_students,
                'students_with_failures': students_with_failures,
                'students_passed': total_students - students_with_failures,
                'from_htno': from_htno,
                'to_htno': to_htno
            }
            
            return render_template('consolidate.html', results=results, summary=summary)
            
        except Exception as e:
            flash(f'Error processing consolidation: {str(e)}', 'error')
            return render_template('consolidate.html')
    
    return render_template('consolidate.html')

@app.route('/student_report', methods=['GET', 'POST'])
def student_report():
    if request.method == 'POST':
        try:
            student_id = request.form['student_id']
            
            if not db:
                flash('Firebase connection not available', 'error')
                return render_template('student_report.html')
            
            # Get all documents for this student (regular and supply)
            all_student_docs = get_student_documents(student_id)
            
            if all_student_docs:
                # Merge regular and supply results
                merged_data = merge_regular_supply_results(all_student_docs)
                
                if merged_data:
                    student_data = merged_data[0]  # Should be only one student after merging
                    subjects = student_data.get('subjectGrades', [])
                    
                    # Use merged SGPA
                    sgpa = student_data.get('sgpa', 0.0)
                    failed_subjects = get_failed_subjects(subjects)
                    
                    # Add exam type information to subjects for display
                    for subject in subjects:
                        if 'examType' not in subject:
                            subject['examType'] = 'regular'  # default
                    
                    report = {
                        'htno': student_data.get('student_id', student_id),
                        'name': f"Student {student_data.get('student_id', student_id)}",
                        'branch': 'N/A',  # Not available in current data
                        'year': student_data.get('year', 'Unknown'),
                        'semester': student_data.get('semester', 'N/A'),
                        'sgpa': sgpa,
                        'subjects': subjects,
                        'failed_subjects': failed_subjects,
                        'total_subjects': len(subjects),
                        'passed_subjects': len(subjects) - len(failed_subjects),
                        'exam_types_found': list(set([doc.get('examType', 'regular') for doc in all_student_docs]))
                    }
                    
                    return render_template('student_report.html', report=report)
            
            flash('Student not found', 'error')
            return render_template('student_report.html')
                
        except Exception as e:
            flash(f'Error fetching student report: {str(e)}', 'error')
            return render_template('student_report.html')
    
    return render_template('student_report.html')

@app.route('/pass_percentage', methods=['GET', 'POST'])
def pass_percentage():
    if request.method == 'POST':
        try:
            from_htno = request.form['from_htno']
            to_htno = request.form['to_htno']
            
            if not db:
                flash('Firebase connection not available', 'error')
                return render_template('pass_percentage.html')
            
            # Get all student documents and filter by HTNO range
            students_ref = db.collection('student_results')
            all_docs = students_ref.stream()
            
            # Collect all student data within range
            raw_student_data = []
            
            for doc in all_docs:
                student_data = doc.to_dict()
                student_id = student_data.get('student_id', '')
                
                # Check if student ID falls within the range
                if is_htno_in_range(student_id, from_htno, to_htno):
                    raw_student_data.append(student_data)
            
            # Merge regular and supply results to remove duplicates
            merged_student_data = merge_regular_supply_results(raw_student_data)
            
            # Process merged data for statistics
            passed_students = []
            failed_students = []
            
            for student_data in merged_student_data:
                student_id = student_data.get('student_id', '')
                subjects = student_data.get('subjectGrades', [])
                
                failed_subjects = get_failed_subjects(subjects)
                sgpa = student_data.get('sgpa', 0.0)  # Use merged SGPA
                
                student_info = {
                    'htno': student_id,
                    'name': f"Student {student_id}",
                    'sgpa': sgpa,
                    'failed_count': len(failed_subjects)
                }
                
                if len(failed_subjects) == 0:  # Passed all subjects
                    passed_students.append(student_info)
                else:
                    failed_students.append(student_info)
            
            total_students = len(merged_student_data)
            pass_percentage = (len(passed_students) / total_students * 100) if total_students > 0 else 0
            
            # Calculate statistics
            all_sgpas = [s['sgpa'] for s in passed_students + failed_students if s['sgpa'] > 0]
            avg_sgpa = statistics.mean(all_sgpas) if all_sgpas else 0
            
            stats = {
                'total_students': total_students,
                'passed_students': len(passed_students),
                'failed_students': len(failed_students),
                'pass_percentage': round(pass_percentage, 2),
                'average_sgpa': round(avg_sgpa, 2),
                'highest_sgpa': max(all_sgpas) if all_sgpas else 0,
                'lowest_sgpa': min(all_sgpas) if all_sgpas else 0
            }
            
            return render_template('pass_percentage.html', 
                                 stats=stats, 
                                 passed_students=passed_students,
                                 failed_students=failed_students)
            
        except Exception as e:
            flash(f'Error calculating pass percentage: {str(e)}', 'error')
            return render_template('pass_percentage.html')
    
    return render_template('pass_percentage.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Route to add sample student data for testing"""
    if request.method == 'POST':
        try:
            if not db:
                flash('Firebase connection not available', 'error')
                return render_template('add_student.html')
            
            student_data = {
                'name': request.form['name'],
                'branch': request.form['branch'],
                'year': request.form['year'],
                'semester': request.form['semester'],
                'subjects': []
            }
            
            # Add subjects dynamically
            subject_count = int(request.form.get('subject_count', 0))
            for i in range(subject_count):
                subject = {
                    'subject_code': request.form.get(f'subject_code_{i}', ''),
                    'subject_name': request.form.get(f'subject_name_{i}', ''),
                    'credits': int(request.form.get(f'credits_{i}', 0)),
                    'grade': request.form.get(f'grade_{i}', 'F')
                }
                student_data['subjects'].append(subject)
            
            htno = request.form['htno']
            db.collection('student_results').document(f"{htno}_Unknown_Semester_1_regular").set(student_data)
            
            flash('Student data added successfully!', 'success')
            return redirect(url_for('add_student'))
            
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'error')
            return render_template('add_student.html')
    
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
