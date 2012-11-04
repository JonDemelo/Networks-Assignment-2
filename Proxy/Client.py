'''
Created on Oct 15, 2012

@author: Jonathan Demelo
'''
import socket
import sys

class Client(object):
    def __init__(self):
        global _port
        global _host
        _port = 5000
        _host = 'localhost'

    def run(self):
        try: _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Error: Socket could not be created..'
            sys.exit()
        
        try: _ip = socket.gethostbyname(_host)
        except socket.error:
            print 'Error: IP could not be retrieved..'
            sys.exit()
        
        try: _socket.connect((_ip, _port))
        except socket.error:
            print 'Error: Server did not connect..'
            sys.exit()
            
        while True:
            try:
                _recieved = _socket.recv(4096)
                if 'exitKey' in _recieved:
                    print 'Ending Program..'
                    _socket.close()
                    sys.exit()
                elif 'responseKey' in _recieved:
                    print _recieved.replace('responseKey', '');
                    _temp = raw_input('Client: ')
                    _socket.sendall(_temp)
            except socket.error: pass
        _socket.close();
        
if __name__ == '__main__':
    _client = Client()
    _client.run()   