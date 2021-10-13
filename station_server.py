# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:03:26 2021

@author: shan
"""



import socket
import pickle
import time
import array as arr
import cv2 as cv
import numpy as np

from keras.models import load_model
from threading import Thread

import import1

req = b''
request = {}

def establish_connection():
    global server_socket
    while True:
        server_stationsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        server_stationsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
        server_stationsocket.bind((import1.IP, import1.stationPORT))
    
        server_stationsocket.listen()
    
        
        server_socket, server_address = server_stationsocket.accept()
        
        print(f"Connection to {server_address} has been established.")
        
        
connect_to_server = Thread(target = establish_connection)
    
connect_to_server.start()
 

#path = 'D:/Engn/MAJOR PROJECT/project_dir/video/'
path = 'video/'
imgpath = 'capture/'

#cap = cv.VideoCapture(path+'sauravdaikovideo.mp4')

#ret, frame = cap.read()

avail_slots = []

reserveFlag = arr.array('i', [])
for n in range(6):
    reserveFlag.append(0)


prediction = arr.array('i', [])
for m in range(6):
    prediction.append(0)


spot_thread = []
for o in range(6):
    spot_thread.append(0)
 


def prepare(filepath):
    img_array = cv.imread(filepath,cv.IMREAD_GRAYSCALE)
    new_array = cv.resize(img_array,(70,70))
    return new_array.reshape(-1,70, 70,1)



classifier_model = load_model('Classifiers_Testing.h5')

CATEGORIES = ["Occupied","Vacant"]


def parkingspot_classify():
      
    if reserveFlag[0]==0:
        prediction[0] = int(classifier_model.predict([prepare(imgpath+'px1.jpg')]))
        
        if (prediction[0]==0):
            cv.rectangle(frame,(225,342),(301,381),(0,0,255),2)
        else:
            cv.rectangle(frame,(225,342),(301,381),(0,255,0),2)
    
    elif reserveFlag[0]==1:
        prediction[0] = 2
        cv.rectangle(frame,(225,342),(301,381),(255,0,0),2)
    
    
      
    pts = np.array([[196,313],[237,327],[292,345],[287,301],[240,285],[200,274]], np.int32)

    if reserveFlag[1]==0:
        prediction[1] = int(classifier_model.predict([prepare(imgpath+'px2.jpg')]))
        
        if (prediction[1]==0):
            #cv.rectangle(frame,(222,291),(306,331),(0,0,255),2)
            cv.polylines(frame,[pts],True,(0,0,255),2)
        else:
            #cv.rectangle(frame,(222,291),(306,331),(0,255,0),2)
            cv.polylines(frame,[pts],True,(0,255,0),2)
    
    elif reserveFlag[1]==1:
        prediction[1] = 2
        cv.polylines(frame,[pts],True,(255,0,0),2)
    
    
     
    if reserveFlag[2]==0:
        prediction[2] = int(classifier_model.predict([prepare(imgpath+'px3.jpg')]))
        
        if (prediction[2]==0):
            cv.rectangle(frame,(207,232),(309,280),(0,0,255),2)
        else:
            cv.rectangle(frame,(207,232),(309,280),(0,255,0),2)
    
    elif reserveFlag[2]==1:
        prediction[2] = 2
        cv.rectangle(frame,(207,232),(309,280),(255,0,0),2)
    
    
      
    if reserveFlag[3]==0:
        prediction[3] = int(classifier_model.predict([prepare(imgpath+'px18.jpg')]))
        
        if (prediction[3]==0):
            cv.rectangle(frame,(420,304),(483,367),(0,0,255),2)
        else:
            cv.rectangle(frame,(420,304),(483,367),(0,255,0),2)
    
    elif reserveFlag[3]==1:
        prediction[3] = 2 
        cv.rectangle(frame,(420,304),(483,367),(255,0,0),2)
        
        
      
    if reserveFlag[4]==0:
        prediction[4] = int(classifier_model.predict([prepare(imgpath+'px25.jpg')]))
        
        if (prediction[4]==0):
            cv.rectangle(frame,(440,153),(469,188),(0,0,255),2)
        else:
            cv.rectangle(frame,(440,153),(469,188),(0,255,0),2)
            
    elif reserveFlag[4]==1:
        prediction[4] = 2
        cv.rectangle(frame,(440,153),(469,188),(255,0,0),2)
    
    
    
    if reserveFlag[5]==0:
        prediction[5] = int(classifier_model.predict([prepare(imgpath+'px4.jpg')]))
        
        if (prediction[5]==0):
            cv.rectangle(frame,(516, 394),(563,457),(0,0,255),2)
        else:
            cv.rectangle(frame,(516, 394),(563,457),(0,255,0),2)
            
    elif reserveFlag[5]==1:
        prediction[5] = 2
        cv.rectangle(frame,(516, 394),(563,457),(255,0,0),2)


    
def reserve_spot(reserved_spot,reserved_time):
    reserveFlag[reserved_spot-1] = 1
    time.sleep(reserved_time)
        
    reserveFlag[reserved_spot-1] = 0
    spot_thread[reserved_spot-1] = 0

   
'''
def display_slots(spots_info):
    global avail_slots
    for key, value in spots_info.items():
        if value == 1:
            avail_slots.append(key)
    return avail_slots
'''


def get_request():
        
        try:
            req = server_socket.recv(112)
            
            if req:
                print(req)
                request = pickle.loads(req)
                print(request)
                req = b''
            
                if request == {"findparkingSpot":1}:
                    status = {"parkingstation_id":0, "spots":{1:prediction[0], 2:prediction[1], 3:prediction[2], 
                                                                   4:prediction[3], 5:prediction[4], 6:prediction[5]}}
                    
                                
                    try:
                        server_socket.send(pickle.dumps(status)) 
                                                
                    except:
                        print('couldnot send status')
                        pass
                    #print('closing socket')
                    #server_socket.close()
                
                elif request != {"findparkingSpot":1}:
                    valid_spotrequest = 1
                    try:
                        r_spot = request["spot"]
                        r_time = request["time"]
                        
                        print(r_spot)
                        
                        if r_spot < 0 or r_spot > 6 :
                            print('insideif')
                            valid_spotrequest = 0
                            print(valid_spotrequest,r_spot)
                            confirmation = {'message':'invalid parking station'}
                                                        
                            try:
                                server_socket.send(pickle.dumps(confirmation))
                            except:
                                print('couldnot send confirmation')
                            return
                        
                    except:
                        valid_spotrequest = 0
                        print('Invalid request')
                        return
                        pass
                    
                                    
                    if valid_spotrequest == 1:   
                        print("naaunuparne thau")
                        spot_thread[r_spot-1] = Thread(target = reserve_spot,args=(r_spot,r_time))
                        spot_thread[r_spot-1].start()
                                        
                                                                                
                        confirmation = {"parkingstation_id":0,"spot":r_spot,"reserve":1,"time":r_time}
                                                        
                        try:
                            server_socket.send(pickle.dumps(confirmation))
                        except:
                            print('couldnot send confirmation')
                            
                        #server_socket.close()
                    
                    else:
                        pass
                    
                else:
                    pass
            
            else:
                pass

        
        except:
            pass
        


while True:
    stop = 0
    cap = cv.VideoCapture(path+'videofeed.avi')

    #ret, frame = cap.read()
    while True:
        ret, frame = cap.read()
        if ret == True:
            #imgCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            #        = frame[x:x+w, y:y+h]
            try:
                crop1=frame[342:381,225:301]
                cv.imwrite(imgpath+'px1.jpg', crop1)
                
                crop2 = frame[291:331,222:306]
                cv.imwrite(imgpath+'px2.jpg', crop2)
                
                crop3 = frame[232:280,207:309]
                cv.imwrite(imgpath+'px3.jpg', crop3)
                
                crop4 = frame[394:457,516:563]
                cv.imwrite(imgpath+'px4.jpg', crop4)
                
                crop18 = frame[304:367,420:483]
                cv.imwrite(imgpath+'px18.jpg', crop18)
                
                crop25 = frame[153:188,440:469]
                cv.imwrite(imgpath+'px25.jpg', crop25)
            
            except:
                print('end')
                pass
            
            
            parkingspot_classify()
                
            get_request()
            
            cv.imshow('parking station:0',frame)
            
            if cv.waitKey(150) & 0xFF == ord('q'):
                stop = 1
                break
        else:
            break
    
    if stop:
        break
    


cap.release()
cv.destroyAllWindows()
        

