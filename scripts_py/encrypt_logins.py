import os
import json
import bcrypt
import time

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to the logins file
logins_file = os.path.join(project_root, 'src/secure/Logins.json')
if not os.path.exists(logins_file):
    raise FileNotFoundError(f"Logins file not found: {logins_file}")

# Read the login data
with open(logins_file, 'r') as f:
    login_data = json.load(f)

# Hash the passwords in the login data
for user in login_data:
    plain_password = user['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    user['password'] = hashed_password.decode('utf-8')  # Store as a string

# Ensure the output directory exists
output_directory = os.path.join(project_root, 'src/secure')
os.makedirs(output_directory, exist_ok=True)

# Write the hashed data to a new encrypted file
hashed_logins_file = os.path.join(output_directory, 'Logins.enc')
with open(hashed_logins_file, 'w') as f:
    json.dump(login_data, f, indent=4)

print(f'Hashed and secured login data written to {hashed_logins_file}')
