# 🚨 CRITICAL SECURITY FIX GUIDE

## ⚠️ **IMMEDIATE ACTION REQUIRED**

Your Firebase service account credentials were exposed! Here's how to fix this immediately:

### 🔥 **Step 1: Revoke Compromised Credentials**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `plant-ec218`
3. Go to **IAM & Admin** → **Service Accounts**
4. Find: `firebase-adminsdk-fbsvc@plant-ec218.iam.gserviceaccount.com`
5. Click **Actions** → **Manage Keys**
6. **DELETE** the compromised key immediately
7. **Generate a new private key**

### 🛡️ **Step 2: Generate New Secure Credentials**
1. In Service Accounts, click **Create Key**
2. Choose **JSON** format
3. Download the new key file
4. Rename it to `firebase-service-account.json`
5. Place it in your project root directory

### 🔒 **Step 3: Verify Security (COMPLETED)**
✅ `.gitignore` updated to exclude `firebase-service-account.json`
✅ Only `firebase-service-account.json.example` is in repository
✅ Real credentials are protected locally

### 🧹 **Step 4: Clean Up Repository History (if needed)**
If the credentials were ever committed to GitHub:
```bash
# Remove from all Git history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch firebase-service-account.json' \
--prune-empty --tag-name-filter cat -- --all

# Force push to update remote
git push origin --force --all
```

### 🔧 **Step 5: Environment Variables (Recommended)**
For production, use environment variables instead:
```bash
# Set environment variables
FIREBASE_PROJECT_ID=plant-ec218
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@plant-ec218.iam.gserviceaccount.com
```

### 📋 **Step 6: Update Application Code (Optional)**
Modify `app.py` to use environment variables:
```python
import os
from firebase_admin import credentials

# Use environment variables in production
if os.getenv('FIREBASE_PRIVATE_KEY'):
    cred_dict = {
        "type": "service_account",
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        # ... other fields
    }
    cred = credentials.Certificate(cred_dict)
else:
    # Use local file for development
    cred = credentials.Certificate('firebase-service-account.json')
```

## ✅ **Current Security Status**
- 🔒 Real credentials file excluded from Git
- 🔒 .gitignore properly configured
- 🔒 Only example template in repository
- ⚠️ **ACTION NEEDED**: Revoke and regenerate Firebase keys

## 🎯 **Priority Actions**
1. **IMMEDIATE**: Revoke the exposed key in Google Cloud Console
2. **IMMEDIATE**: Generate new Firebase credentials
3. **SOON**: Consider using environment variables for production
4. **OPTIONAL**: Clean Git history if credentials were ever committed

Your application will continue to work once you replace the credentials file with new ones!
