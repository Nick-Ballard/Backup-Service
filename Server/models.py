class Test:
    def __init__(self, Message='', FileTransfer=False, dict=[], *args, **kwargs):
        self.__type__ = 'Test'
        self.Message = Message
        self.FileTransfer = FileTransfer
        if len(dict) > 0:
            for k, v in dict.items():
                setattr(self, k, v)
                if(hasattr(self, k)):
                    setattr(self, k, v)

class Transfer_Request:
    def __init__(self, Request=False, Accept=False, Success=False, dict=[]):
        self.__type__ = 'Transfer_Request'
        self.Request = Request
        self.Accept = Accept
        self.Success = Success
        if len(dict) > 0:
            for k, v in dict.items():
                setattr(self, k, v)
                if(hasattr(self, k)):
                    setattr(self, k, v)

class FileObj:
    def __init__(self, FileName='', FilePath='', FileSize='', Checksum='', dict=[]):
        self.__type__ = 'FileObj'
        self.FileName = FileName
        self.FilePath = FilePath
        self.FileSize = FileSize
        self.Checksum =  Checksum
        if len(dict) > 0:
            for k, v in dict.items():
                setattr(self, k, v)
                if(hasattr(self, k)):
                    setattr(self, k, v)

class Client:
    def __init__(self, ip='', port='', c='', key=''):
        self.ip = ip
        self.port = port
        self.c = c
        self.key = key
