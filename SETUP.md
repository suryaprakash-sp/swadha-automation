# Setup Guide - Google Sheets OAuth Authentication

This guide will walk you through setting up Google Sheets API access with OAuth 2.0 authentication.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click **"New Project"**
4. Enter a project name (e.g., "Swadha Automation")
5. Click **"Create"**

## Step 2: Enable Google Sheets API

1. In your Google Cloud Console, make sure your new project is selected
2. Go to **"APIs & Services"** > **"Library"** (from left sidebar)
3. Search for **"Google Sheets API"**
4. Click on it and click **"Enable"**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** > **"Credentials"** (from left sidebar)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**

### Configure OAuth Consent Screen (if prompted)

If this is your first time, you'll need to configure the OAuth consent screen:

1. Click **"Configure Consent Screen"**
2. Select **"External"** (unless you have Google Workspace)
3. Click **"Create"**
4. Fill in the required fields:
   - **App name**: Swadha Automation
   - **User support email**: Your email
   - **Developer contact information**: Your email
5. Click **"Save and Continue"**
6. On the **Scopes** page, click **"Save and Continue"** (no need to add scopes here)
7. On the **Test users** page, click **"+ Add Users"**
8. Add your Google account email (the one that has access to your spreadsheet)
9. Click **"Save and Continue"**
10. Review and click **"Back to Dashboard"**

### Create OAuth Client ID

1. Go back to **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** > **"OAuth client ID"**
3. Select **"Desktop app"** as the application type
4. Enter a name (e.g., "Swadha Automation Desktop")
5. Click **"Create"**

## Step 4: Download Credentials

1. After creating the OAuth client, a dialog will appear with your credentials
2. Click **"Download JSON"**
3. Rename the downloaded file to **`credentials.json`**
4. Move this file to your project directory: `C:\swadha-automation\`

**IMPORTANT**: The file must be named exactly `credentials.json` and placed in the project root directory.

## Step 5: First-Time Authentication

When you run the script for the first time:

1. Open a command prompt/terminal
2. Navigate to the project directory:
   ```cmd
   cd C:\swadha-automation
   ```

3. Run the main script:
   ```cmd
   python main.py
   ```

4. A browser window will automatically open
5. Sign in with your Google account (the one that has access to the spreadsheet)
6. Click **"Allow"** to grant permissions
7. You'll see a message: **"The authentication flow has completed."**
8. Close the browser and return to the terminal

9. A `token.json` file will be created automatically in your project directory
10. This token will be used for future authentication (no need to login again)

## Troubleshooting

### "Access blocked: This app's request is invalid"

This means you need to add your email to the test users list:
1. Go to Google Cloud Console > APIs & Services > OAuth consent screen
2. Scroll down to "Test users"
3. Click "Add Users" and add your email
4. Delete `token.json` if it exists and try again

### "credentials.json not found"

Make sure:
1. The file is named exactly `credentials.json` (not `credentials.json.txt` or anything else)
2. The file is in the project root directory: `C:\swadha-automation\`
3. You downloaded it from the correct OAuth client

### "Invalid grant" or "Token has been expired or revoked"

1. Delete the `token.json` file
2. Run the script again - you'll need to re-authenticate in the browser

## Security Notes

- **NEVER** commit `credentials.json` or `token.json` to git
- These files are already in `.gitignore` to prevent accidental commits
- Keep these files secure as they provide access to your Google account

## What's Next?

Once authentication is set up, you can run the automation scripts. See [README.md](README.md) for usage instructions.
