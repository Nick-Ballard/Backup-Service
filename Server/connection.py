import threading
import models
import time
import json
import tqdm
from models import *
import encryption
from encryption import *
from cryptography.fernet import Fernet

class File_Transfer:
    def Send(client, file):
        obj = Transfer_Request(Request=True)
        Send_Data(client, obj)
        response = Handle_Response()
        obj = Transfer_Request(dict=response)
        if not obj.Accept:
            return False
        Send_Data(client, file)
        if not obj.Accept:
            return False
        Send_File(file)
        response = Handle_Response()
        obj = Transfer_Request(dict=response)
        return obj.Success

    def Recieve(self, client):
        print('[*] Recieving File Transfer')
        obj = Transfer_Request(Accept=True)
        Send_Data(client, obj)
        response = Handle_Response(client)
        file = FileObj(dict=response)
        if not Recieve_File(client, file):
            return False
        # Check File Hash
        obj = Transfer_Request(Success=True)
        Send_Data(client, obj)
        print('[*] File Transfer Complete')


Clients = []
Key = ''

def Start_Server(host, port, sc, key):
    global Key
    Key = key
    sc.bind((host, port))
    sc.listen(5) # Max Connections Allowed
    print("[*] Listening as {}:{}".format(host, port))
    Handle_Connections(sc)
    Stop_Server(sc)

def Stop_Server(sc):
    sc.close()

def Handle_Connections(sc):
    while True:
        client_socket, address = sc.accept()
        client = Client(address[0], address[1], client_socket, Key)
        Clients.append(client)
        args = [client]
        daemon = threading.Thread(target=New_Connection, args=(args))
        daemon.daemon = True
        daemon.start()

def Disconnect_Client(client):
    client.c.close()
    Clients.remove(client)
    print('Client Disconnected | {}:{}'.format(client.ip, client.port))

def Handle_Response(client):
    xdata = ''
    while True:
        data = client.c.recv(1024)
        if data == '':
            continue
        else:
            xdata = data
            break

    data = Decrypt_Data(xdata, Key)
    return json.loads(data)

def Process_Response(response, client):
    obj = ''
    if '__type__' not in response:
        return True

    type = response.get('__type__')
    if type == 'Command':
        try:
            obj = Command(dict=response)
        except:
            pass
    elif type == 'Transfer_Request':
        try:
            obj = Transfer_Request(dict=response)
            if obj.Request:
                File_Transfer().Recieve(client)
        except:
            pass

def New_Connection(args): # Threaded
    client = args
    print('[+] Connected to {}:{}'.format(client.ip, client.port))
    while True:
        response = Handle_Response(client)

        if not Process_Response(response, client):
            break

        #x = json.loads(data.strip())
        #d = Test(dict=eval(data))

        #print(type(d))
        #time.sleep(5)
        ##if not data:
            #break
        #client.c.send(data)
    #Disconnect_Client(client)

def Send_Data(client, obj):
    try:
        data = json.dumps(obj.__dict__)
        xdata = Encrypt_Data(data, client.key)
        client.c.send(xdata)
        return True
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return False

def Send_File(client, file):
    try:
        if type(file) is not FileObj:
            return

            progress = tqdm.tqdm(range(file.FileSize), "Sending {}".format(file.FileName), unit="B", unit_scale=True, unit_divisor=1024)
            with open(file.FilePath, "rb") as f:
                for _ in progress:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # File transmitting is done
                        break
                        data = Encrypt_Data(client, bytes_read)
                        client.c.sendall(data)
                        progress.update(len(bytes_read))
    except:
        return False
    return True

def Recieve_File(client, file):
    print('Waiting for file...')
    print(client.key)
    try:
        f = Fernet(client.key)
        progress = tqdm.tqdm(range(int(file.FileSize)), "Receiving {}".format(file.FileName), unit="B", unit_scale=True, unit_divisor=1024)
        with open(file.FileName, "wb") as f:
            print('1')
            for _ in progress:
                print('a')
                bytes_read = client.c.recv(4096)
                print('b')
                if not bytes_read:
                    print('2')
                    # File transmitting is complete
                    break

                print('3')
                #data = Decrypt_Data(bytes_read, client.key)
                #data = bytes_read
                #data = Decrypt_Data(bytes_read, Key)
                data = f.decrypt(bytes_read)
                print('4')
                f.write(data)
                print('5')
                progress.update(len(bytes_read))
    except:
        print('Failed :(')
        return False
    print('Success :D')
    return True
