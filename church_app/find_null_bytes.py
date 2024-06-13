import os

def find_files_with_null_bytes(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    if b'\x00' in f.read():
                        print(f"Null byte found in: {file_path}")
            except Exception as e:
                print(f"Could not read file: {file_path} due to {e}")

# Set the project directory to your current project path
project_directory = 'C:/Users/Admin/freelance-projects/church-app-backend/church_app'
find_files_with_null_bytes(project_directory)


