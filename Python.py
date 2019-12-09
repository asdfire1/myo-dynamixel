from __future__ import print_function
import myo
import serial
import time

import numpy as np
from collections import deque
from threading import Lock, Thread

channel1=6 #Channel for in
channel2=3 #Channel for out
channel1multiplier=0.9 #strength multiplier for 1st channel
minimumemg=4 #Threshold for action
maximumemg=50 #Level at which speed is max

starter=50 # This has to be like that because its retarded
ser = serial.Serial("COM5", 115200)
posevariable='0'

class Listener(myo.DeviceListener):
  def __init__(self):
    print("__init__")
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=40) #this can be changed to make the strength change slower and be more smooth (but also delayed)

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.stream_emg(True)
    event.device.vibrate(myo.VibrationType.short)
    event.device.request_battery_level()

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)

  def on_battery_level(self, event):
    print("Your battery level is:", event.battery_level)

  def on_emg(self, event):
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))

  def on_pose(self, event):
    global posevariable
    if event.pose == myo.Pose.fist:
        posevariable='fx'
        print('fist')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.fingers_spread:
        posevariable='bx'
        print('fingers')
        event.device.vibrate(myo.VibrationType.short)


    


class emgprocessing(object):
  def __init__(self, listener):
    self.listener = listener

  def main(self):
        global starter
        emg_data = self.listener.get_emg_data()
        if (starter==0):
          #this is the code that will run every time except for the first few times until starter is 0
          global channel1
          global channel2
          global maximumemg
          global minimumemg
          global channel1multiplier
          emg_data = np.array([x[1] for x in emg_data]).T
          emg_data = np.absolute(emg_data)
          emg_datal=emg_data.tolist()
          averageC1=sum(emg_datal[channel1])/len(emg_datal[channel1]) #to be changed
          averageC2=sum(emg_datal[channel2])/len(emg_datal[channel2])
          emg_diff=averageC1*channel1multiplier-averageC2

          if (abs(emg_diff)<minimumemg):
            return(0)

          if (abs(emg_diff)>=maximumemg) and (emg_diff>0):
            return(99)

          if (abs(emg_diff)>=maximumemg) and (emg_diff<0):
            return(-99)

          else:
            return(int(((np.sign(emg_diff)*(abs(emg_diff)-minimumemg)*100)/(maximumemg-minimumemg))))

        else:
          print("Starter was 1") #This has to be like that otherwise its retarded
          starter=starter-1
          return(0) #This is the output for the first few times until starter is 0

def myobandthings():
  while hub.run(listener.on_event, 10000000):
    pass

def ourthings():
  global posevariable
  period=0.005
  t=time.time()
  while(True):
    t+=period
    #print (time.time()*1000) # This can be used to verify the timing
    if (posevariable !='0'):
     print(posevariable)
     ser.write(bytes(posevariable, 'utf-8'))
     posevariable='0'

    else:
     strength=emgprocessing(listener).main()
     strength=str(strength)+'x'
     print("Strength is: "+ strength)
     ser.write(bytes(strength, 'utf-8'))
    time.sleep(max(0,t-time.time()))

if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  time.sleep(1)
  Thread(target = myobandthings).start()
  Thread(target = ourthings).start()


