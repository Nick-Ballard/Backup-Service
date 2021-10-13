import json
import models
import encryption
import threading
import time
import tqdm
from models import *
from encryption import *

sc = ''
Key = ''

def Connect(host, port, socket, key):
    global sc, Key
    Key = key
    sc = socket
    print("[+] Connecting to {}:{}".format(host, port))
    sc.connect((host, port))
    print("[+] Connected.")

def Disconnect():
    sc.close()

def Handle_Response():
    xdata = ''
    while True:
        data = sc.recv(1024)
        if data == '':
            continue
        else:
            xdata = data
            break

    data = Decrypt_Data(xdata, Key)
    return json.loads(data)

def File_Transfer(file):
    print('[*] Initiating File Transfer')
    obj = Transfer_Request(Request=True)
    Send_Data(obj)
    response = Handle_Response()
    obj = Transfer_Request(dict=response)
    if not obj.Accept:
        return False
    Send_Data(file)
    if not obj.Accept:
        return False
    print('File Sent: {}'.format(Send_File(file)))
    response = Handle_Response()
    obj = Transfer_Request(dict=response)
    print('[*] File Transfer Success: {}'.format(obj.Success))
    return obj.Success

def Send_Data(obj):
    try:
        data = json.dumps(obj.__dict__)
        xdata = Encrypt_Data(data, Key)
        sc.send(xdata)
        return True
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return False

def Send_File(file):
    if file.__type__ is not 'FileObj':
        print('File Type: {}'.format(file.__type__))
        return False
    # start sending the file
    progress = tqdm.tqdm(range(file.FileSize), "Sending {}".format(file.FileName), unit="B", unit_scale=True, unit_divisor=1024)
    with open(file.FilePath, "rb") as f:
        for _ in progress:
            bytes_read = f.read(4096)
            if not bytes_read:
                # file transmitting is done
                break
            data = Encrypt_Data(bytes_read, Key)
            sc.sendall(data)
            progress.update(len(bytes_read))
    return True
