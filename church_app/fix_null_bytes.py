import os
import glob

def remove_null_bytes(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    if b'\x00' in data:
        print(f"Null byte found in: {file_path}")
        cleaned_data = data.replace(b'\x00', b'')
        with open(file_path, 'wb') as f:
            f.write(cleaned_data)
        print(f"Null bytes removed from: {file_path}")
    else:
        print(f"No null bytes found in: {file_path}")

def main():
    project_directory = os.getcwd()
    for root, dirs, files in os.walk(project_directory):
        for file in files:
            if file.endswith('.py') or file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                remove_null_bytes(file_path)

if __name__ == "__main__":
    main()

