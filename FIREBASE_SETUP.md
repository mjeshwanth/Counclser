# 🔥 Firebase Configuration Setup

## 🔧 **Firebase Service Account Setup**

### **Step 1: Get Firebase Credentials**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Go to **Project Settings** → **Service Accounts**
4. Click **"Generate New Private Key"**
5. Download the JSON file

### **Step 2: Setup Credentials**
1. Rename the downloaded file to `firebase-service-account.json`
2. Place it in the root directory of this project
3. **Never commit this file to Git** - it contains sensitive information

### **Step 3: File Structure**
```
firebase-service-account.json  ← Your actual credentials (ignored by Git)
firebase-service-account.json.example  ← Template file (safe to commit)
```

### **Step 4: Template Reference**
Use the `firebase-service-account.json.example` file as a template. Replace all placeholder values with your actual Firebase credentials:

- `YOUR_PROJECT_ID` → Your Firebase project ID
- `YOUR_PRIVATE_KEY_ID` → From your downloaded JSON
- `YOUR_PRIVATE_KEY` → From your downloaded JSON  
- `YOUR_SERVICE_ACCOUNT_EMAIL` → From your downloaded JSON
- `YOUR_CLIENT_ID` → From your downloaded JSON
- `YOUR_CERT_URL` → From your downloaded JSON

## 🛡️ **Security Notes**
- ✅ The actual credentials file is in `.gitignore`
- ✅ Only the example template is committed to Git
- ✅ Replace the example file with your actual credentials locally
- ⚠️ Never share or commit the actual credentials file

## 🚀 **Quick Setup Command**
After downloading your Firebase credentials:
```bash
# Rename your downloaded file
mv path/to/downloaded/file.json firebase-service-account.json

# Verify the file is ignored by Git
git status
# Should not show firebase-service-account.json in changes
```

Your application will now connect to Firebase successfully! 🎯
