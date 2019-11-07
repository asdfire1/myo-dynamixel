from __future__ import print_function
import myo
import serial
import time

import numpy as np
from collections import deque
from threading import Lock, Thread

ser = serial.Serial("COM5", 57600)
posevariable='restx'
ser.write(b'initx')

class Listener(myo.DeviceListener):
  def __init__(self):
    print("__init__")
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=50) #this can be changed to make the strength change slower and be more stable

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
    if event.pose == myo.Pose.double_tap:
        #ser.write(b'doubletap')
        print("doubletap")
    elif event.pose == myo.Pose.fist:
        #ser.write(b'fistx')
        posevariable='fistx'
        #print('fist')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.fingers_spread:
        #ser.write(b'fingersx')
        posevariable='fingersx'
        #print('fingers')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.wave_in:
        #ser.write(b'inx')
        posevariable='inx'
        #print('in')
    elif event.pose == myo.Pose.wave_out:
        #ser.write(b'outx')
        posevariable='outx'
        #print('out')
    else:
        #ser.write(b'restx')
        posevariable='restx'
        #print('rest')

    


class readingtest(object):
  def __init__(self, listener):
    self.listener = listener
    emg_data=1
  def main(self):
        emg_data = self.listener.get_emg_data()
        
        emg_data = np.array([x[1] for x in emg_data]).T
        emg_data = np.absolute(emg_data)
        emg_data = np.average(emg_data)
        #emg_data = float(emg_data)
        #print(emg_data)
        return(emg_data)

if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  pastpose='restx'
  paststren='0'
  while hub.run(listener.on_event, 100):
    
    strraw=readingtest(listener).main()
    if strraw > 10: #this should be tuned (to individual person?)(or to inx and outx)
      stren = 1
    else:
      stren = 0
    if (posevariable != pastpose) or (stren!=paststren):
      if (posevariable=="restx") and (posevariable != pastpose):
          ser.write(b'restx')
          print(posevariable)
      if (posevariable=="fistx") and (posevariable != pastpose):
          ser.write(b'fistx')
          print(posevariable)
      if (posevariable=="fingersx") and (posevariable != pastpose):
          ser.write(b'fingersx')
          print(posevariable)
      if (posevariable == 'inx') and (stren==0) :
        ser.write(b'inx')
        print('in')
      if (posevariable == 'inx') and (stren==1) :
        ser.write(b'Sinx')
        print('Sin')
      if (posevariable == 'outx') and (stren==0) :
        ser.write(b'outx')
        print('out')
      if (posevariable == 'outx') and (stren==1) :
        ser.write(b'Soutx')
        print('Sout')  
    pastpose=posevariable
    paststren=stren
    pass
  print('Bye, bye!')


