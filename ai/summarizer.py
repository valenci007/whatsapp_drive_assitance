import openai
import PyPDF2
import docx
import os
from config import Config

class AISummarizer:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.AI_MODEL
    
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, file_content):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_content)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_text_from_txt(self, file_content):
        """Extract text from TXT file"""
        try:
            return file_content.read().decode('utf-8')
        except:
            file_content.seek(0)
            return file_content.read().decode('latin-1')
    
    def summarize_content(self, text, max_length=500):
        """Summarize text using AI"""
        if not text or text.startswith("Error reading"):
            return text
            
        try:
            prompt = f"Please provide a concise summary of the following content. Focus on key points and main ideas. Limit to {max_length} characters:\n\n{text}"
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary[:max_length]
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def summarize_folder(self, drive_client, folder_path):
        """Summarize all files in a folder"""
        folder_id = drive_client.get_folder_id(folder_path)
        
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_client.service.files().list(
            q=query, 
            spaces='drive',
            fields='files(id, name, mimeType)'
        ).execute()
        
        files = results.get('files', [])
        if not files:
            return "No files found in this folder to summarize."
        
        summary_response = f"📊 Summary of files in '{folder_path}':\n\n"
        
        for file in files:
            file_content = None
            text_content = ""
            
            # Download and extract text based on file type
            if file['mimeType'] == 'application/pdf':
                file_content = drive_client.download_file(file['id'], file['name'])
                if file_content:
                    text_content = self.extract_text_from_pdf(file_content)
            elif file['mimeType'] in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
                                     'application/msword']:
                file_content = drive_client.download_file(file['id'], file['name'])
                if file_content:
                    text_content = self.extract_text_from_docx(file_content)
            elif file['mimeType'] == 'text/plain':
                file_content = drive_client.download_file(file['id'], file['name'])
                if file_content:
                    text_content = self.extract_text_from_txt(file_content)
            else:
                text_content = f"File type not supported for summarization: {file['mimeType']}"
            
            # Generate summary
            if text_content and not text_content.startswith("Error") and not text_content.startswith("File type"):
                summary = self.summarize_content(text_content)
                summary_response += f"📄 **{file['name']}:**\n{summary}\n\n"
            else:
                summary_response += f"📄 **{file['name']}:** {text_content}\n\n"
        
        return summary_response
