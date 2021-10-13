import socket
import tqdm
import os
import zipfile
import json
import time
import encryption
from encryption import *
import connection
from connection import *
import models
from models import *
from datetime import date

Dirs = ['/home/nick/Notes']
Files = ['Test.txt']

Exclude = ['/home/nick/Desktop/Projects/Backup-Service/Temp']

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

Host = "127.0.0.1"
Port = 5001
#filesize = os.path.getsize(filename)
key = ""

def Set_Filename():
    global Filename, ZipName
    today = date.today()
    Filename = "Backup-{}".format(today.strftime("%d-%m-%Y"))
    ZipName = Filename+'.zip'

def Zip_Dir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def Check_Dir(dir):
    path = os.path.abspath(dir)
    x = os.path.split(path)

    if path in Exclude:
        return False

    while x[1] != '':
        if x[0] in Exclude:
            return False
        x = os.path.split(x[0])

    return True

def Check_File(file):
    file = os.path.abspath(file)
    if file in Exclude:
        return False

    return True

def Zip_Dir(dir, zip):
    if not Check_Dir(dir):
        return

    for root, dirs, files in os.walk(dir):
        for file in files:
            f = os.path.join(root, file)
            file = os.path.abspath(f)
            Zip_File(file, zip)

def Zip_File(file, zip):
    file = os.path.abspath(file)
    if Check_File(file):
        zip.write(file)

def Compress_Data():
    Set_Filename()
    zip = zipfile.ZipFile('Temp/{}.zip'.format(Filename), 'w', zipfile.ZIP_DEFLATED)

    for file in Files:
        Zip_File(file, zip)

    for dir in Dirs:
        Zip_Dir(dir, zip)

    zip.close()

def Create_BSF():
    zip = zipfile.ZipFile('Temp/{}.bsf'.format(Filename), 'w', zipfile.ZIP_DEFLATED)
    zip.write('Temp/{}.bsfx'.format(Filename), Filename+'.bsfx')
    zip.close()
    os.remove('Temp/{}.bsfx'.format(Filename))

def Pack_File():
    Compress_Data()
    Encrypt_File(Filename, key)
    Create_BSF()



    os.remove('Temp/{}.zip'.format(Filename))
    #os.remove('Temp/{}.bsf'.format(Filename))

def UnPack_File(filename):
    with zipfile.ZipFile(filename, 'r') as file:
        file.extractall('Temp/')
    x = os.path.split(filename)
    x = filename.split('.')
    Decrypt_File('{}.bsfx'.format(x[0]), key)
    os.remove('Temp/{}.bsfx'.format(Filename))
    os.remove('Temp/{}.bsf'.format(Filename))

if __name__ == "__main__":
    #DataKey = load_key()
    #MessageKey = load_key()
    connection_socket = socket.socket()
    Set_Filename()
    key = load_key()
    Connect(Host, Port, connection_socket, key)
    test = Test('I am client 2 :)')
    while True:
        Send_Data(test)
        time.sleep(1)
    #Disconnect()
    #write_key()
    #Create_File()
    #Pack_File()
    #UnPack_File('Temp/{}.bsf'.format(Filename))
    #Decrypt_File(filename, key)
