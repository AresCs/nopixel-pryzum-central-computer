import json
from cryptography.fernet import Fernet

# Path to the key file
key_file_path = '../src/secure/key.key'
with open(key_file_path, 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Path to the logins file
logins_file = '../src/Component/Login/Logins.json'

# Read the login data
with open(logins_file, 'r') as f:
    login_data = json.load(f)

# Encrypt the login data
json_data = json.dumps(login_data).encode('utf-8')
encrypted_data = cipher_suite.encrypt(json_data)

# Write the encrypted data to a new file
encrypted_logins_file = '../src/secure/Logins.enc'
with open(encrypted_logins_file, 'wb') as f:
    f.write(encrypted_data)

print(f'Encrypted login data written to {encrypted_logins_file}')
