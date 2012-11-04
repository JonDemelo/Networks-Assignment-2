'''
@Program: Proxy.py
@author: Jonathan Demelo 250519903
@Assignment: 2
@Course: cs3357a
'''
#IMPORTS
import socket # socket programming
import sys # system calls
import os.path # file path usage
import threading # multithreading
import httplib # http requests
import string # string functions

class Proxy(object):
    def __init__(self): # constructor
        global _port
        global _host
        _port = 5000
        _host = ''
    # handles the proxy thread requests from the browser
    def proxyHandler(self, _conn, _bannedList, _port):
        try:
            _rec = _conn.recv(10096) # GET request by browser
            _rec = _rec.replace('\r\n', ' ')
            _splitReq = string.split(_rec,' ') # build listing of GET headers
            _urlConn = httplib.HTTPConnection(_splitReq[4]) # GET to web server
            _urlConn.request(_splitReq[0], _splitReq[1])
            _urlRes = _urlConn.getresponse() # retrieve GET response
            _htmltext = _urlRes.read() # grab text of response
            
            if '\0' in _htmltext: # if binary object
                _conn.send(_htmltext)
            else: # not binary object
                _found = False
                for _i in _bannedList: # check for each banned word
                    if _i in _htmltext: _found = True
                if _found: 
                    _errorHTML = Proxy.buildErrorMSG # build error message
                    _conn.send(_errorHTML) # display error message to the browser
                else: _conn.send(_htmltext) # no banned words detected
        except:
            pass
    
    # sees if the error file exists, if it does, output html code, else basic error messages 
    def buildErrorMSG(self):
        if os.path.isfile("/Users/Jon/Documents/Code/NetASN2Py/error.html"):
            _inputFile = open("/Users/Jon/Documents/Code/NetASN2Py/error.html", "r") # open file
            return _inputFile
        else : return 'banned word(s) found, you cannot view this page.'
    
    # grabs the file from the local drive and builds the words into an array
    def buildBannedList(self, _location):
        _inputFile = open(_location, "r") # open file
        _bannedList = []
        for _line in _inputFile: # for each line in the file
            _bannedList.append(_line) # add the line as an element of array
        _inputFile.close() 
        return _bannedList
        
    def buildSocket(self, _host, _port, _type = 1): # defaulted to standard connection
        # try making the server socket
        if type == 1: # if standard connection
            try: _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            except socket.error:
                print 'Error: Socket could not be created..'
                sys.exit()
        else: # if browser connection
            try: 
                _socket = socket.socket()
                _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       
            except socket.error:
                print 'Error: Socket could not be created..'
                sys.exit()
        
        # try binding the server socket to the host and port
        try: _socket.bind((_host, _port))
        except socket.error:
            print 'Could not bind socket as port is in use..'
            sys.exit()

        _socket.listen(5) # set the server to listen to up to 5 connections
        print 'Server is listening..'
        return _socket

    def run(self): # run the proxy object
        _socket = Proxy.buildSocket(self, _host, _port)
        _conn, _address = _socket.accept() # accept the socket request from client
        print 'Connection to client made..'
        
        # ask the client what port they want to use for the browser
        while True:
            _conn.sendall('What browser port number would you like to use? responseKey')
            _browser = _conn.recv(4096)
            try: # make sure port is an integer
                _browser = int(_browser)
                break
            except: pass
        # ask the client what the file location is for the banned list
        while True:
            _conn.sendall('What is the location of the banned list file? responseKey')
            _banned = _conn.recv(4096)
            if os.path.isfile(_banned): break # if file exists
        _bannedList = Proxy.buildBannedList(self, _banned)
        _socketPr = Proxy.buildSocket(self, 'localhost', _browser, 0)
        
        while True:
            _connPr, _addressPr = _socketPr.accept() # accept the socket request from client
            print 'Connection to client made..'
            threading.Thread(target = Proxy.proxyHandler, args = (self, _connPr, _bannedList, _browser)).start()

        # EXIT COMMANDS
        _conn.sendall('exitKey') # notify client of exit 
        _socket.close() # close connection
        _socketPr.close() 
        print 'Closing Server..'
        sys.exit() # end server

# main method
if __name__ == '__main__':
    _proxy = Proxy() # create object
    _proxy.run() # run object