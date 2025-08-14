# Counselor Application

A comprehensive Flask-based counselor application for student performance analysis and reporting, integrated with Firebase for data storage.

## Features

### 1. Consolidate Reports
- Generate consolidated reports for a range of students (HTNO to HTNO)
- Calculate SGPA for each student automatically
- Identify and list failed subjects
- Display comprehensive performance statistics

### 2. Student Grade Report
- View detailed grade reports for individual students
- Complete subject-wise performance analysis
- SGPA calculation and display
- Failed subjects identification
- Performance summary with visual indicators

### 3. Pass Percentage Analysis
- Calculate pass percentage for student ranges
- Detailed statistics including:
  - Total students analyzed
  - Number of passed/failed students
  - Overall pass percentage
  - Average SGPA
  - SGPA distribution analysis
- Student rankings and performance comparisons

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: Firebase Firestore
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Authentication**: Firebase Admin SDK

## Installation

1. **Clone or download the project**
   ```bash
   cd counselor-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Firebase Setup**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Firestore Database
   - Go to Project Settings > Service Accounts
   - Generate a new private key (JSON file)
   - Replace the content of `firebase-service-account.json` with your actual credentials

4. **Set up sample data (optional)**
   ```bash
   python setup_sample_data.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Database Structure

### Students Collection
```json
{
  "htno": {
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
}
```

## Grade Scale

| Grade | Description | Points |
|-------|-------------|--------|
| O     | Outstanding | 10     |
| A+    | Excellent   | 9      |
| A     | Very Good   | 8      |
| B+    | Good        | 7      |
| B     | Above Average | 6    |
| C     | Average     | 5      |
| P     | Pass        | 4      |
| F     | Fail        | 0      |
| Ab    | Absent      | 0      |

## SGPA Calculation

SGPA = (Sum of (Credits × Grade Points)) / Total Credits

## Usage

### Adding Students
1. Navigate to "Add Student" page
2. Fill in student information and subjects
3. Use "Fill Sample Data" for quick testing
4. Submit the form to save to Firebase

### Generating Reports
1. **Consolidate**: Enter HTNO range (e.g., 21A91A0501 to 21A91A0510)
2. **Student Report**: Enter individual HTNO
3. **Pass Percentage**: Enter HTNO range for analysis

### Features Overview
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Data**: Fetches data directly from Firebase
- **Interactive UI**: Bootstrap-based interface with hover effects
- **Error Handling**: Comprehensive error messages and validation
- **Performance Analytics**: Detailed statistics and visualizations

## File Structure

```
counselor-app/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── firebase-service-account.json   # Firebase credentials (replace with actual)
├── setup_sample_data.py           # Script to populate sample data
├── README.md                       # Project documentation
└── templates/
    ├── base.html                   # Base template
    ├── index.html                  # Home page
    ├── consolidate.html            # Consolidate reports page
    ├── student_report.html         # Individual student report
    ├── pass_percentage.html        # Pass percentage analysis
    └── add_student.html            # Add student form
```

## Security Notes

- Keep your Firebase service account key secure
- Do not commit `firebase-service-account.json` to version control
- Use environment variables for production deployment
- Implement proper authentication for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository or contact the development team.

---

**Note**: This application is designed for educational and counseling purposes. Ensure compliance with your institution's data privacy policies when implementing in production.
