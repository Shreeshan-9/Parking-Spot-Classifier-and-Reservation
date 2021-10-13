import socket
import pickle
from threading import Thread
import variables
import reserve


def establish_connection():
    global server_socket
    while True:
        server_stationsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        server_stationsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
        server_stationsocket.bind((variables.IP, variables.stationPORT))
    
        server_stationsocket.listen()
    
        
        server_socket, server_address = server_stationsocket.accept()
        
        print(f"Connection to {server_address} has been established.")
        
        server_socket.setblocking(0)




def get_request():
    
        valid_spotrequest = 1
    
        try:
            req = server_socket.recv(112)
            
            if req:
                print(req)
                request = pickle.loads(req)
                print(request)
                req = b''
            
                if request == {"findparkingSpot":1}:
                    status = {"parkingstation_id":0, "spots":{6:reserve.prediction[0], 
                                                              7:reserve.prediction[1], 
                                                              8:reserve.prediction[2], 
                                                                  9:reserve.prediction[3],
                                                                  10:reserve.prediction[4]}}
                    
                                
                    try:
                        server_socket.send(pickle.dumps(status)) 
                                                
                    except:
                        print('couldnot send status')
                        pass
                    #print('closing socket')
                    #server_socket.close()
                
                elif request != {"findparkingSpot":1}:
                    try:
                        r_spot = request["spot"]
                        r_time = request["time"]
                        print(r_spot)
                        
                        if r_spot < 6 or r_spot > 10:
                            valid_spotrequest = 0
                    except:
                        valid_spotrequest = 0
                        print('Invalid request')
                        pass
                    
                                    
                    if valid_spotrequest == 1:                
                        reserve.spot_thread[r_spot-6] = Thread(target = reserve.reserve_spot,
                                                               args=(r_spot,r_time))
                        reserve.spot_thread[r_spot-6].start()
                                        
                                                                                
                        confirmation = {"parkingstation_id":1,"spot":r_spot,"reserve":1,"time":r_time}
                                                        
                        try:
                            server_socket.send(pickle.dumps(confirmation))
                        except:
                            print('couldnot send confirmation')
                            
                        #server_socket.close()
                    
                    else:
                        print('Invalid spot number')
                        pass
                    
                else:
                    pass
            
            else:
                pass

        
        except:
            pass
  