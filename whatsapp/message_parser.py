import re

class WhatsAppMessageParser:
    @staticmethod
    def parse_message(message):
        """Parse WhatsApp message and extract command and parameters"""
        message = message.strip()
        
        # LIST command
        list_match = re.match(r'^LIST\s+(.+)$', message, re.IGNORECASE)
        if list_match:
            return {'command': 'LIST', 'folder_path': list_match.group(1)}
        
        # DELETE command
        delete_match = re.match(r'^DELETE\s+(.+)$', message, re.IGNORECASE)
        if delete_match:
            return {'command': 'DELETE', 'file_path': delete_match.group(1)}
        
        # MOVE command
        move_match = re.match(r'^MOVE\s+([^\s]+)\s+([^\s]+)$', message, re.IGNORECASE)
        if move_match:
            return {
                'command': 'MOVE', 
                'source_path': move_match.group(1),
                'dest_path': move_match.group(2)
            }
        
        # SUMMARY command
        summary_match = re.match(r'^SUMMARY\s+(.+)$', message, re.IGNORECASE)
        if summary_match:
            return {'command': 'SUMMARY', 'folder_path': summary_match.group(1)}
        
        # RENAME command
        rename_match = re.match(r'^RENAME\s+([^\s]+)\s+([^\s]+)$', message, re.IGNORECASE)
        if rename_match:
            return {
                'command': 'RENAME',
                'current_name': rename_match.group(1),
                'new_name': rename_match.group(2)
            }
        
        # UPLOAD command (for text-based upload instructions)
        upload_match = re.match(r'^UPLOAD\s+([^\s]+)\s+([^\s]+)$', message, re.IGNORECASE)
        if upload_match:
            return {
                'command': 'UPLOAD_TEXT',
                'folder_path': upload_match.group(1),
                'file_name': upload_match.group(2)
            }
        
        # HELP command
        if message.upper() == 'HELP':
            return {'command': 'HELP'}
        
        return {'command': 'UNKNOWN', 'message': message}
    
    @staticmethod
    def get_help_message():
        """Generate help message with all commands"""
        return """🤖 *Google Drive Assistant Help* 🤖

Here are the available commands:

*📁 LIST Commands:*
• `LIST /FolderName` - List files in a folder
• `LIST /` - List files in root directory

*🗑️ DELETE Commands:*
• `DELETE /FolderName/file.pdf` - Delete a file
• `DELETE /FolderName` - Delete a folder

*📦 MOVE Commands:*
• `MOVE /FolderName/file.pdf /Archive` - Move file to another folder

*📊 SUMMARY Commands:*
• `SUMMARY /FolderName` - AI summary of all files in folder

*✏️ RENAME Commands:*
• `RENAME file.pdf new_file.pdf` - Rename a file

*⬆️ UPLOAD Commands:*
• Send a file with caption: `UPLOAD /FolderName new_filename.pdf`

*Need help?* Just type `HELP`"""
