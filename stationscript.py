import cv2 as cv
import numpy as np
from keras.models import load_model
from threading import Thread
import reserve
import station_connector
import roi

classifier_model = load_model('Classifiers_Testing.h5')
path = 'video/'
imgpath = 'capture/'
crop = {}


connect_to_server = Thread(target = station_connector.establish_connection)
    
connect_to_server.start()
 


def prepare(filepath):
    img_array = cv.imread(filepath,cv.IMREAD_GRAYSCALE)
    new_array = cv.resize(img_array,(70,70))
    return new_array.reshape(-1,70, 70,1)



def parkingspot_classify():
      
    if reserve.reserveFlag[0]==0:
        reserve.prediction[0] = int(classifier_model.predict([prepare(imgpath+'px1.jpg')]))
        
        if (reserve.prediction[0]==0):
            cv.rectangle(frame,(225,342),(301,381),(0,0,255),2)
        else:
            cv.rectangle(frame,(225,342),(301,381),(0,255,0),2)
    
    elif reserve.reserveFlag[0]==1:
        reserve.prediction[0] = 2
        cv.rectangle(frame,(225,342),(301,381),(255,0,0),2)
    
    
      
    pts = np.array([[196,313],[237,327],[292,345],[287,301],[240,285],[200,274]], np.int32)

    if reserve.reserveFlag[1]==0:
        reserve.prediction[1] = int(classifier_model.predict([prepare(imgpath+'px2.jpg')]))
        
        if (reserve.prediction[1]==0):
            #cv.rectangle(frame,(222,291),(306,331),(0,0,255),2)
            cv.polylines(frame,[pts],True,(0,0,255),2)
        else:
            #cv.rectangle(frame,(222,291),(306,331),(0,255,0),2)
            cv.polylines(frame,[pts],True,(0,255,0),2)
    
    elif reserve.reserveFlag[1]==1:
        reserve.prediction[1] = 2
        cv.polylines(frame,[pts],True,(255,0,0),2)
    
    
     
    if reserve.reserveFlag[2]==0:
        reserve.prediction[2] = int(classifier_model.predict([prepare(imgpath+'px3.jpg')]))
        
        if (reserve.prediction[2]==0):
            cv.rectangle(frame,(207,232),(309,280),(0,0,255),2)
        else:
            cv.rectangle(frame,(207,232),(309,280),(0,255,0),2)
    
    elif reserve.reserveFlag[2]==1:
        reserve.prediction[2] = 2
        cv.rectangle(frame,(207,232),(309,280),(255,0,0),2)
    
    
      
    if reserve.reserveFlag[3]==0:
        reserve.prediction[3] = int(classifier_model.predict([prepare(imgpath+'px5.jpg')]))
        
        if (reserve.prediction[3]==0):
            cv.rectangle(frame,(420,304),(483,367),(0,0,255),2)
        else:
            cv.rectangle(frame,(420,304),(483,367),(0,255,0),2)
    
    elif reserve.reserveFlag[3]==1:
        reserve.prediction[3] = 2 
        cv.rectangle(frame,(420,304),(483,367),(255,0,0),2)
        
        
      
    if reserve.reserveFlag[4]==0:
        reserve.prediction[4] = int(classifier_model.predict([prepare(imgpath+'px6.jpg')]))
        
        if (reserve.prediction[4]==0):
            cv.rectangle(frame,(440,153),(469,188),(0,0,255),2)
        else:
            cv.rectangle(frame,(440,153),(469,188),(0,255,0),2)
            
    elif reserve.reserveFlag[4]==1:
        reserve.prediction[4] = 2
        cv.rectangle(frame,(440,153),(469,188),(255,0,0),2)
    
    
    
    if reserve.reserveFlag[5]==0:
        reserve.prediction[5] = int(classifier_model.predict([prepare(imgpath+'px4.jpg')]))
        
        if (reserve.prediction[5]==0):
            cv.rectangle(frame,(516, 394),(563,457),(0,0,255),2)
        else:
            cv.rectangle(frame,(516, 394),(563,457),(0,255,0),2)
            
    elif reserve.reserveFlag[5]==1:
        reserve.prediction[5] = 2
        cv.rectangle(frame,(516, 394),(563,457),(255,0,0),2)



'''
listen_for_request = Thread(target = connector.get_request)
    
listen_for_request.start()
'''



while True:
    stop = 0
    cap = cv.VideoCapture(path+'videofeed.avi')

    #ret, frame = cap.read()
    while True:
        ret, frame = cap.read()
        if ret == True:
            #        = frame[x:x+w, y:y+h]
            try:
                '''
                crop1=frame[342:381,225:301]
                cv.imwrite(imgpath+'px1.jpg', crop1)
                
                crop2 = frame[291:331,222:306]
                cv.imwrite(imgpath+'px2.jpg', crop2)
                
                crop3 = frame[232:280,207:309]
                cv.imwrite(imgpath+'px3.jpg', crop3)
                
                crop4 = frame[394:457,516:563]
                cv.imwrite(imgpath+'px4.jpg', crop4)
                
                crop5 = frame[304:367,420:483]
                cv.imwrite(imgpath+'px5.jpg', crop5)
                
                crop6 = frame[153:188,440:469]
                cv.imwrite(imgpath+'px6.jpg', crop6)
                
                
                '''
                for i in range(1,7):
                    crop[i] = frame[roi.coordinates[i-1][0]:roi.coordinates[i-1][0]+roi.coordinates[i-1][2],
                                    roi.coordinates[i-1][1]:roi.coordinates[i-1][1]+roi.coordinates[i-1][3]]
                    cv.imwrite(imgpath+f'px{i}.jpg', crop[i])
                
                
            
            except:
                print('end')
                pass
            
            
            parkingspot_classify()
                
            station_connector.get_request()
            
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
        
