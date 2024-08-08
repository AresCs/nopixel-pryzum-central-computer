import os
from cryptography.fernet import Fernet

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to save the key file
key_file_path = os.path.join(project_root, 'src/secure/key.key')

# Ensure the output directory exists
os.makedirs(os.path.dirname(key_file_path), exist_ok=True)

# Generate the key and save it
key = Fernet.generate_key()
with open(key_file_path, 'wb') as key_file:
    key_file.write(key)

print(f'Key generated and saved to {key_file_path}')
