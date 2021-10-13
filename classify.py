import elements
import cv2 as cv
from keras.models import load_model


classifier_model = load_model('Classifiers_Testing.h5')
imgpath = 'capture/'

def prepare(filepath):
    img_array = cv.imread(filepath,cv.IMREAD_GRAYSCALE)
    new_array = cv.resize(img_array,(70,70))
    return new_array.reshape(-1,70, 70,1)




def parkingspot_classify():
      
    if elements.reserveFlag[0]==0:
        elements.prediction[0] = int(classifier_model.predict([prepare(imgpath+'px1.jpg')]))
        
        if (elements.prediction[0]==0):
            cv.rectangle(frame,(225,342),(301,381),(0,0,255),2)
        else:
            cv.rectangle(frame,(225,342),(301,381),(0,255,0),2)
    
    elif elements.reserveFlag[0]==1:
        elements.prediction[0] = 2
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

