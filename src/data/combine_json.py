import os
import json
from datetime import datetime

# Define the submodule directories and output file
submodule_dirs = [
    'submodules/lucy', 
    'submodules/ariel', 
    'submodules/akari', 
    'submodules/aria', 
    'submodules/kenz'
]
output_file = 'src/data/pryzumData.json'

# Initialize a dictionary to hold the combined data with unique identifiers
combined_data = {}

# Helper function to convert date string to datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")  # Updated to match the format in your example
    except ValueError:
        return None

# Iterate over each submodule directory
for submodule_dir in submodule_dirs:
    # Iterate over files in the submodule directory
    for root, dirs, files in os.walk(submodule_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Assuming each file contains a dict with a "pryzumData" key
                    if "pryzumData" in data:
                        for entry in data["pryzumData"]:
                            name = entry.get("Name")
                            date_of_entry = parse_date(entry.get("Date of Entry"))

                            if name and date_of_entry:
                                # If the entry already exists, compare timestamps
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

# Write the combined data to the output file
with open(output_file, 'w') as f:
    json.dump(final_data, f, indent=4)

print(f'Combined data written to {output_file}')
