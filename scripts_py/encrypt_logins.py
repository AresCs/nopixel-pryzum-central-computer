import os
import json
from cryptography.fernet import Fernet
import time

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to the key file
key_file_path = os.path.join(project_root, 'src/secure/key.key')

# Wait and check for the key file
max_wait_time = 10  # seconds
wait_time = 0
while not os.path.exists(key_file_path) and wait_time < max_wait_time:
    print(f"Waiting for key file to be generated: {key_file_path}")
    time.sleep(1)
    wait_time += 1

if not os.path.exists(key_file_path):
    raise FileNotFoundError(f"Key file not found: {key_file_path}")

with open(key_file_path, 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Path to the logins file
logins_file = os.path.join(project_root, 'src/secure/Logins.json')
if not os.path.exists(logins_file):
    raise FileNotFoundError(f"Logins file not found: {logins_file}")

# Read the login data
with open(logins_file, 'r') as f:
    login_data = json.load(f)

# Encrypt the login data
json_data = json.dumps(login_data).encode('utf-8')
encrypted_data = cipher_suite.encrypt(json_data)

# Ensure the output directory exists
output_directory = os.path.join(project_root, 'src/secure')
os.makedirs(output_directory, exist_ok=True)

# Write the encrypted data to a new file
encrypted_logins_file = os.path.join(output_directory, 'Logins.enc')
with open(encrypted_logins_file, 'wb') as f:
    f.write(encrypted_data)

print(f'Encrypted login data written to {encrypted_logins_file}')
