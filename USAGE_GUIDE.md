# Counselor Application - Complete Setup and Usage Guide

## 🎓 Overview

The Counselor Application is a comprehensive student performance analysis system built with Flask and Firebase. It provides three main functionalities:

1. **Consolidate Reports** - Analyze multiple students from HTNO range
2. **Student Grade Report** - Detailed individual student analysis  
3. **Pass Percentage Analysis** - Statistical analysis of student performance

## 🚀 Quick Start

### 1. Firebase Setup (IMPORTANT)

Before running the application, you must set up Firebase:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Enable **Firestore Database**
4. Go to **Project Settings > Service Accounts**
5. Click **Generate New Private Key**
6. Download the JSON file
7. Replace the content of `firebase-service-account.json` with your downloaded file

### 2. Running the Application

**Option A: Using Batch File (Windows)**
```bash
# Double-click start_app.bat or run in command prompt
start_app.bat
```

**Option B: Manual Command**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

**Option C: Using VS Code Task**
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Select "Run Counselor Application"

### 3. Access the Application
Open your browser and go to: **http://localhost:5000**

## 📊 Application Features

### 🏠 Home Dashboard
- Overview of all features
- Quick navigation to different modules
- System status and Firebase connection info

### 📈 Consolidate Reports
**Purpose**: Analyze multiple students in a range

**How to Use**:
1. Enter starting HTNO (e.g., `21A91A0501`)
2. Enter ending HTNO (e.g., `21A91A0510`)
3. Click "Generate Report"

**What You Get**:
- SGPA for each student
- Failed subjects count
- Detailed breakdown of failed subjects
- Overall statistics (total students, pass/fail counts, average SGPA)

### 👤 Student Grade Report
**Purpose**: Detailed analysis of individual student

**How to Use**:
1. Enter student HTNO (e.g., `21A91A0501`)
2. Click "Get Report"

**What You Get**:
- Complete student information
- Subject-wise grades and credits
- Calculated SGPA
- Performance summary
- Failed subjects (if any)
- Grade legend

### 📊 Pass Percentage Analysis
**Purpose**: Statistical analysis of student ranges

**How to Use**:
1. Enter HTNO range (from and to)
2. Click "Calculate Statistics"

**What You Get**:
- Overall pass percentage
- Passed vs failed student lists
- SGPA distribution analysis
- Performance rankings
- Statistical insights

### ➕ Add Student Data
**Purpose**: Add new student records to the system

**How to Use**:
1. Fill in student basic information
2. Add subject details (code, name, credits, grade)
3. Use "Fill Sample Data" for quick testing
4. Submit the form

## 📚 Data Structure

### Student Record Format
```json
{
  "name": "Student Name",
  "branch": "CSE",
  "year": "2",
  "semester": "3",
  "subjects": [
    {
      "subject_code": "CS201",
      "subject_name": "Data Structures",
      "credits": 4,
      "grade": "A"
    }
  ]
}
```

### Grade System
| Grade | Points | Description |
|-------|--------|-------------|
| O     | 10     | Outstanding |
| A+    | 9      | Excellent   |
| A     | 8      | Very Good   |
| B+    | 7      | Good        |
| B     | 6      | Above Average |
| C     | 5      | Average     |
| P     | 4      | Pass        |
| F     | 0      | Fail        |
| Ab    | 0      | Absent      |

### SGPA Calculation
```
SGPA = (Sum of (Credits × Grade Points)) / Total Credits
```

## 🛠️ Setting Up Sample Data

To test the application with sample data:

```bash
python setup_sample_data.py
```

This will create 5 sample students with different performance levels.

## 🔧 Troubleshooting

### Common Issues and Solutions

**1. Firebase Connection Error**
- Ensure `firebase-service-account.json` has valid credentials
- Check if Firestore is enabled in Firebase Console
- Verify project ID matches in credentials file

**2. Module Not Found Error**
```bash
pip install -r requirements.txt
```

**3. Port Already in Use**
- Change port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`
- Or kill the process using port 5000

**4. No Students Found**
- Add sample data using `setup_sample_data.py`
- Or manually add students using the "Add Student" form
- Check HTNO format (e.g., 21A91A0501)

**5. Template Not Found**
- Ensure `templates/` folder exists
- Check all HTML files are in the templates directory

## 📱 Usage Examples

### Example 1: Analyzing Class Performance
1. Go to "Pass Percentage"
2. Enter range: `21A91A0501` to `21A91A0520`
3. Review overall statistics and student listings

### Example 2: Individual Counseling
1. Go to "Student Report"
2. Enter specific HTNO: `21A91A0503`
3. Review detailed performance and failed subjects

### Example 3: Generating Consolidated Report
1. Go to "Consolidate"
2. Enter range for your section/class
3. Export or print the detailed report

## 🔒 Security Best Practices

1. **Never commit Firebase credentials** to version control
2. **Use environment variables** in production
3. **Implement authentication** for sensitive data
4. **Regular backup** of Firebase data
5. **Monitor access logs** in Firebase Console

## 🎯 Advanced Features

### Custom Grade Calculations
Modify the `calculate_sgpa()` function in `app.py` to implement:
- Different grade scales
- Weighted calculations
- Semester-wise analysis

### Adding New Reports
1. Create new route in `app.py`
2. Add corresponding HTML template
3. Update navigation in `base.html`

### Database Extensions
- Add more student fields (phone, email, etc.)
- Implement semester-wise tracking
- Add faculty and course management

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Review Firebase Console for data structure
3. Verify all dependencies are installed
4. Check file permissions and paths

## 🔄 Updates and Maintenance

### Regular Tasks
- Monitor Firebase usage and billing
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Backup student data regularly
- Review and update security settings

### Performance Optimization
- Index frequently queried fields in Firestore
- Implement pagination for large datasets
- Add caching for repeated calculations
- Optimize database queries

---

**Happy Counseling! 🎓**
