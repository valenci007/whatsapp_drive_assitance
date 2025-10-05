import io
import os
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from .auth import GoogleDriveAuth

class GoogleDriveClient:
    def __init__(self, credentials_file, token_file):
        self.service = GoogleDriveAuth(credentials_file, token_file).authenticate()
    
    def get_folder_id(self, folder_path):
        """Get folder ID from path"""
        if folder_path == '/':
            return 'root'
            
        folders = folder_path.strip('/').split('/')
        current_id = 'root'
        
        for folder_name in folders:
            if not folder_name:
                continue
                
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{current_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            items = results.get('files', [])
            
            if not items:
                # Folder doesn't exist, create it
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [current_id]
                }
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                current_id = folder.get('id')
            else:
                current_id = items[0]['id']
                
        return current_id
    
    def list_files(self, folder_path='/'):
        """List files in a folder"""
        folder_id = self.get_folder_id(folder_path)
        
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query, 
            spaces='drive',
            fields='files(id, name, mimeType, size, modifiedTime)',
            orderBy='name'
        ).execute()
        
        files = results.get('files', [])
        if not files:
            return "No files found in this folder."
        
        response = f"Files in '{folder_path}':\n"
        for file in files:
            file_type = "📁" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄"
            response += f"{file_type} {file['name']}\n"
        
        return response
    
    def delete_file(self, file_path):
        """Delete a file or folder"""
        if '/' in file_path:
            folder_path = '/'.join(file_path.split('/')[:-1])
            file_name = file_path.split('/')[-1]
            folder_id = self.get_folder_id(folder_path)
            
            query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
        else:
            query = f"name='{file_path}' and 'root' in parents and trashed=false"
        
        results = self.service.files().list(q=query, fields='files(id)').execute()
        items = results.get('files', [])
        
        if not items:
            return f"File '{file_path}' not found."
        
        try:
            self.service.files().delete(fileId=items[0]['id']).execute()
            return f"✅ Successfully deleted '{file_path}'"
        except Exception as e:
            return f"❌ Error deleting file: {str(e)}"
    
    def move_file(self, source_path, dest_folder_path):
        """Move file to another folder"""
        # Extract file name and source folder
        source_folder_path = '/'.join(source_path.split('/')[:-1])
        file_name = source_path.split('/')[-1]
        
        # Get source folder ID and file
        source_folder_id = self.get_folder_id(source_folder_path or '/')
        query = f"name='{file_name}' and '{source_folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields='files(id, parents)').execute()
        items = results.get('files', [])
        
        if not items:
            return f"File '{source_path}' not found."
        
        file_id = items[0]['id']
        dest_folder_id = self.get_folder_id(dest_folder_path)
        
        try:
            # Get current parents to remove
            file = self.service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents', []))
            
            # Move the file
            self.service.files().update(
                fileId=file_id,
                addParents=dest_folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            
            return f"✅ Successfully moved '{file_name}' to '{dest_folder_path}'"
        except Exception as e:
            return f"❌ Error moving file: {str(e)}"
    
    def rename_file(self, current_name, new_name):
        """Rename a file"""
        query = f"name='{current_name}' and trashed=false"
        results = self.service.files().list(q=query, fields='files(id)').execute()
        items = results.get('files', [])
        
        if not items:
            return f"File '{current_name}' not found."
        
        try:
            self.service.files().update(
                fileId=items[0]['id'],
                body={'name': new_name}
            ).execute()
            return f"✅ Successfully renamed '{current_name}' to '{new_name}'"
        except Exception as e:
            return f"❌ Error renaming file: {str(e)}"
    
    def upload_file(self, file_path, file_content, mime_type='application/octet-stream'):
        """Upload a file to Google Drive"""
        folder_path = '/'.join(file_path.split('/')[:-1])
        file_name = file_path.split('/')[-1]
        folder_id = self.get_folder_id(folder_path)
        
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_content, mimetype=mime_type)
        
        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return f"✅ Successfully uploaded '{file_name}' to '{folder_path}'"
        except Exception as e:
            return f"❌ Error uploading file: {str(e)}"
    
    def download_file(self, file_id, file_name):
        """Download file content for processing"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_content.seek(0)
            return file_content
        except Exception as e:
            return None
