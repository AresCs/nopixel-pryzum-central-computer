import os
import json
from datetime import datetime
from cryptography.fernet import Fernet

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the submodule directories and output file using absolute paths
submodule_dirs = [
    os.path.join(project_root, 'submodules/lucy'), 
    os.path.join(project_root, 'submodules/ariel'), 
    os.path.join(project_root, 'submodules/akari'), 
    os.path.join(project_root, 'submodules/aria'), 
    os.path.join(project_root, 'submodules/kenz')
]
output_file = os.path.join(project_root, 'src/secure/pryzumData.json')
key_file_path = os.path.join(project_root, 'src/secure/key.key')

# Read the key from the file
if not os.path.exists(key_file_path):
    raise FileNotFoundError(f"Key file not found: {key_file_path}")

with open(key_file_path, 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

# Initialize a dictionary to hold the combined data with unique identifiers
combined_data = {}

# Helper function to convert date string to datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        return None

# Iterate over each submodule directory
for submodule_dir in submodule_dirs:
    print(f"Processing directory: {submodule_dir}")
    # Iterate over files in the submodule directory
    for root, dirs, files in os.walk(submodule_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if "pryzumData" in data:
                        print(f"Data found in file: {file_path}")
                        for entry in data["pryzumData"]:
                            print(f"Processing entry: {entry}")
                            name = entry.get("Name")
                            date_of_entry = parse_date(entry.get("Date of Entry"))

                            if name and date_of_entry:
                                if name in combined_data:
                                    existing_date_of_entry = parse_date(combined_data[name]["Date of Entry"])
                                    if date_of_entry > existing_date_of_entry:
                                        combined_data[name] = entry
                                else:
                                    combined_data[name] = entry

# Create the final combined data structure
final_data = {
    "pryzumData": list(combined_data.values())
}

# Encrypt the combined data
json_data = json.dumps(final_data).encode('utf-8')
encrypted_data = cipher_suite.encrypt(json_data)

# Write the encrypted data to the output file
with open(output_file, 'wb') as f:
    f.write(encrypted_data)

print(f'Encrypted combined data written to {output_file}')
