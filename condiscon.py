

import socket
import pickle

import import1

from threading import Thread


sPORT = 9999
cPORT = 5050

status = {}
request = {}
confirmation = {}

print('Starting Server...')


def enquiry(user_socket):
    global enq
    enquiry.find_spot = {}
    try:
        enq = user_socket.recv(112)
        enquiry.find_spot = pickle.loads(enq)
    except:
        pass



def get_status(server_stationsocket):
    get_status.msg = b''
    global status, transfer_status
    
    try:
        get_status.msg = server_stationsocket.recv(112)
        
        status = pickle.loads(get_status.msg)
        print('Status:',status)
           
    except:
        pass



def get_request(user_socket):
    global request
    global station_request
    
    try:
        #get_request.rmsg = user_socket.recv(112)
        
        request = user_socket.recv(112)
        station_request = pickle.loads(request)
        
       
    except:
        pass



def get_confirmation(station_socket):
    get_confirmation.cmsg = b''
    global confirmation
    
    
    try:
        get_confirmation.cmsg = station_socket.recv(112)
            
        confirmation = pickle.loads(get_confirmation.cmsg)
        print('Confirmation:',confirmation)
      
        
    except:
        pass



def request_handler(user_socket):
    global transfer_status
    enquiry(user_socket)
    print('jajaj',enquiry.find_spot)
    if  enquiry.find_spot["findparkingSpot"] == 1:
        server_stationsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_stationsocket.connect((import1.IP,import1.stationPORT))
        
        print('connected with station')
        server_stationsocket.send(enq)
        
        get_status(server_stationsocket)
        
        print('closing socket after receiving status')
        server_stationsocket.close()                
            
        get_request(user_socket)
        print('zz',station_request)
                        
        if  request != b'':
            server_stationsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_stationsocket.connect((import1.IP,import1.stationPORT))
            print('sending spot req')
                    
            try:
                server_stationsocket.send(request)
            except:
                print('cannt send')
            
                
            try:
                get_confirmation(server_stationsocket)
            except:
                print('no confirmation')
                pass
            
            print('closing socket after receiving confirmation')
            server_stationsocket.close()    
        
                
        else:
            pass
        #print('\n')
        #print(station_list)




def user_connections():
    global station_list
    global station_request
    while True:
    
        server_usersocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_usersocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        
        
        server_usersocket.bind((import1.IP, import1.userPORT))
        
        server_usersocket.listen()
        
                
        user_socket, user_address = server_usersocket.accept()
                
        print(f"Connection from {user_address} has been established.")
        #user_socket.setblocking(True)
        
        #request_handler(user_socket)
        
        t1 = Thread(target = request_handler, args = (user_socket,))
    
        t1.start()


t = Thread(target = user_connections)
    
t.start()

   
    
