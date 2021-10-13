import array as arr
import time


reserveFlag = arr.array('i', [])
for n in range(6):
    reserveFlag.append(0)


prediction = arr.array('i', [])
for m in range(6):
    prediction.append(0)


spot_thread = []
for o in range(6):
    spot_thread.append(0)
    
    
    
def reserve_spot(reserved_spot,reserved_time):
    reserveFlag[reserved_spot-6] = 1
    time.sleep(reserved_time)
        
    reserveFlag[reserved_spot-6] = 0
    spot_thread[reserved_spot-6] = 0
