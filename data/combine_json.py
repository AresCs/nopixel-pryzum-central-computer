import os
import json

# Define the submodule directories and output file
submodule_dirs = ['Shameless', 'Monstrum']
output_file = 'pryzumData.json'

# Initialize an empty list to hold the events
combined_data = []

# Iterate over each submodule directory
for submodule_dir in submodule_dirs:
    # Iterate over files in the submodule directory
    for root, dirs, files in os.walk(submodule_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Assuming each file contains a dict with an "upcomingEvents" key
                    if "pryzumData" in data:
                        combined_data.extend(data["pryzumData"])

# Create the final combined data structure
final_data = {
    "pryzumData": combined_data
}

# Write the combined data to the output file
with open(output_file, 'w') as f:
    json.dump(final_data, f, indent=4)

print(f'Combined data written to {output_file}')
