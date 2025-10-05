from google_drive.auth_fixed import GoogleDriveAuthFixed
from config import Config


def setup_drive():
    print("🔧 Setting up Google Drive authentication...")

    try:
        drive_auth = GoogleDriveAuthFixed(Config.GOOGLE_CREDENTIALS_FILE, Config.DRIVE_TOKEN_FILE)
        service = drive_auth.authenticate()

        print("✅ Google Drive authentication successful!")
        print("📁 Testing drive access...")

        # Test the connection
        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        files = results.get('files', [])

        if files:
            print(f"📄 Found {len(files)} files in your Drive:")
            for file in files[:5]:  # Show first 5 files
                print(f"   - {file['name']} ({file['id']})")
        else:
            print("📁 No files found in Drive (this is normal for new accounts)")

        return True

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False


if __name__ == "__main__":
    setup_drive()