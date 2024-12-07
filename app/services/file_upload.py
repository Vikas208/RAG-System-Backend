from dotenv import load_dotenv
import os 
import time

load_dotenv()
class FileUpload:
    def __init__(self):
        self.SUPPORTED_EXTENSIONS = os.getenv("FILE_EXTENSION")
        self.DIRECTORY_PATH = os.getenv("UPLOAD_PATH")

    def cehck_file_type(self, file):
        # Check File Extension and store it in the file
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported file type. Only PDF, DOC, DOCX, TXT, XLSX, PPTX and CSV files are allowed.")
        return file
    
    def upload_file(self, file, session_data):
        
        # Check File Type
        file = self.cehck_file_type(file)
        file_extension = file.filename.split(".")[-1].lower()

        # generate unique filename e.g {session-id}-{timestamp}
        filename = f'{session_data["session_id"]}-{int(time.time())}.{file_extension}'

        # Save the file to the directory
        file_path = os.path.join(self.DIRECTORY_PATH, filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Return the filename
        return filename

