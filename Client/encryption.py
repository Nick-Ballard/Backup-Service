import os
from cryptography.fernet import Fernet

def load_key():
    return open("key.key", "rb").read()

def Encrypt_Data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def Decrypt_Data(data, key):
    f = Fernet(key)
    return f.decrypt(data)

def Encrypt_File(filename, key):
    with open('Temp/{}.zip'.format(filename), "rb") as file:
        file_data = file.read()
    encrypted_data = Encrypt_Data(file_data, key)
    with open(os.path.join("Temp/{}.bsfx".format(filename)), "wb") as file:
        file.write(encrypted_data)

def Decrypt_File(filename, key):
    with open(os.path.join(filename), "rb") as file:
        encrypted_data = file.read()

    decrypted_data = Decrypt_Data(encrypted_data, key)

    with open(os.path.join('Temp/', filename+'.zip'), "wb") as file:
        file.write(decrypted_data)
