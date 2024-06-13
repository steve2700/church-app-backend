import os

def find_null_bytes_in_file(file_path):
    with open(file_path, 'rb') as file:
        if b'\x00' in file.read():
            print(f'Null byte found in: {file_path}')

def scan_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                find_null_bytes_in_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_directory('.')

