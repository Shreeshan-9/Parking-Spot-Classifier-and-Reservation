

import socket

import pickle

import import1

user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

# Connect to a given ip and port
user_socket.connect((import1.IP, import1.stationPORT))


d = {"findparkingSpot":1}
user_socket.send(pickle.dumps(d))

status = user_socket.recv(112)
#user_socket.close()
print(pickle.loads(status))

z = x = int(input('Choose a parking station->[0/1]:'))
x = int(input('Choose a parking spot->[1/2/3/4/5]:'))
y = int(input('How long do you wanna reserve?:'))
                
spot_req = {"parkingstation_id":z, "spot":x, "time":y, "vehicleNo":"ba12pa1234"}
print(spot_req)
msg = pickle.dumps(spot_req)
         
'''
user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)       
user_socket.connect((import1.IP, import1.stationPORT))
'''
user_socket.send(msg)
user_socket.close()
