from cryptography.fernet import Fernet

def generate_and_save_key(key_file_path='../src/secure/key.key'):
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)
    print(f'Key generated and saved to {key_file_path}')

if __name__ == "__main__":
    generate_and_save_key()
