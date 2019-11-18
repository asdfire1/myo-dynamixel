from __future__ import print_function
import myo
import serial
import time

import numpy as np
from collections import deque
from threading import Lock, Thread

channel1=6 #Channel for in
channel2=3 #Channel for out
channel1multiplier=1.5 #strength multiplier for 1st channel
minimumemg=4 #Threshold for action
maximumemg=50 #Level at which speed is max

starter=5 # This has to be like that because its retarded
ser = serial.Serial("COM5", 57600)
posevariable='0'
#ser.write(b'initx')

class Listener(myo.DeviceListener):
  def __init__(self):
    print("__init__")
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=80) #this can be changed to make the strength change slower and be more stable

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.stream_emg(True)
    event.device.vibrate(myo.VibrationType.short)
    event.device.request_battery_level()

  def get_emg_data(self):
    #print("getemgdata")
    with self.lock:
      return list(self.emg_data_queue)

  def on_battery_level(self, event):
    print("Your battery level is:", event.battery_level)

  def on_emg(self, event):
    #print("onemg")
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))

  def on_pose(self, event):
    global posevariable
    if event.pose == myo.Pose.fist:
        #ser.write(b'fistx')
        posevariable='fx'
        print('fist')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.fingers_spread:
        #ser.write(b'fingersx')
        posevariable='bx'
        print('fingers')
        event.device.vibrate(myo.VibrationType.short)


    


class readingtest(object):
  def __init__(self, listener):
    self.listener = listener
    #print("reading init")

  def main(self):
        global starter
        emg_data = self.listener.get_emg_data()
        if (starter==0):
          #this is the code that will run every time except for the 1st time is
          global channel1
          global channel2
          global maximumemg
          global minimumemg
          global channel1multiplier
          emg_data = np.array([x[1] for x in emg_data]).T
          emg_data = np.absolute(emg_data)
          emg_datal=emg_data.tolist()
          #emg_data = np.average(emg_data)
          #print(type(emg_datal))
          #emg_data = float(emg_data)
          #print(emg_datal)
          #print(emg_datal[1])
          emg_dataC1=emg_datal[channel1]
          emg_dataC2=emg_datal[channel2]
          #print(emg_datar)
          #print("average value:")
          averageC1=sum(emg_dataC1)/len(emg_dataC1) #to be changed
          averageC2=sum(emg_dataC2)/len(emg_dataC2)
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
          return(0) #This is the output of the 1st time
def myoshit():
  while hub.run(listener.on_event, 10000000):
    pass
def ourcrap():
  global posevariable
  while(True):
    millis = int(round(time.time() * 1000))
    #print (millis)
    if (posevariable !='0'):
     print(posevariable)
     ser.write(bytes(posevariable, 'utf-8')) #make it actually write the posevariable
     posevariable='0' #do we need to use string 0?
    else:
     strraw=readingtest(listener).main()
     strraw=str(strraw)+'x'
     print("Strength is: "+ strraw)
     ser.write(bytes(strraw, 'utf-8'))
    delaytime=50+millis-(int(round(time.time() * 1000)))
    if(delaytime>=0):
      time.sleep(delaytime/1000)
    ser.reset_output_buffer()
if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  time.sleep(1)
  Thread(target = myoshit).start()
  Thread(target = ourcrap).start()
  #ser.write(b'fx')
  #time.sleep(0.1)
  #readingtest(listener).main() this doesnt work if it is here
  #while(hub.run(listener.on_event, 500)): #if this is too fast then it gets fucked faster, this is somethign from myoband sdk, we need to figure out how to get this running simultainously with our stuff so that they dont inferfere
    #what is this number here?????????????????????????????????????????????????????????????????
    #timing? now it seems to be taking X+(2 or 3) milliseconds, X is the number above
    #millis = int(round(time.time() * 1000))
    #print (millis)

    #strraw=readingtest(listener).main() #the 1st one we get will be 0
    #print("Strraw is: " + str(strraw))
  #while(True):
  #   time.sleep(0.25)
  #   if (posevariable !='0'):
  #      print(posevariable)
  #      ser.write(bytes(posevariable, 'utf-8')) #make it actually write the posevariable
  #      posevariable='0' #do we need to use string 0?
  #    else:
  #      strraw=readingtest(listener).main()
  #      strraw=str(strraw)+'x'
  #      print("Strength is: "+ strraw)
  #      ser.write(bytes(strraw, 'utf-8'))
  #    time.sleep(0.25)
      #ser.write(b'x')
      
      #serial print the strength with x at the end example +99x
    #delaytime=10+millis-(int(round(time.time() * 1000)))
    #time.sleep(delaytime/1000)
    #pass
  print('Bye, bye!')


