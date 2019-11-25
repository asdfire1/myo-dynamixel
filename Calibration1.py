from __future__ import print_function
import myo
import time
import os
import numpy as np
from collections import deque
from threading import Lock, Thread
from matplotlib import pyplot as plt


averageC = [deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200)]
MaxCp = np.zeros((8,), dtype=float)
starter=25 # This has to be like that because its retarded

class Listener(myo.DeviceListener):
  def __init__(self):
    print("__init__")
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=100) #this can be changed to make the strength change slower and be more stable

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.stream_emg(True)
    event.device.vibrate(myo.VibrationType.short)

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)


  def on_emg(self, event):
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class emgprocessing(object):
  def __init__(self, listener):
    self.listener = listener
  def main(self):
        global starter
        global averageC #Deque
        global MaxCp
        averageCp = np.zeros((8,), dtype=float)
        emg_data = self.listener.get_emg_data()
        if (starter==0):
        
          emg_data = np.array([x[1] for x in emg_data]).T
          emg_data = np.absolute(emg_data)
          emg_datal=emg_data.tolist()
          cls()
          for g in range(8):
            
            averageCp[g]=sum(emg_datal[g])/len(emg_datal[g])
            if averageCp[g] > MaxCp[g]:
              MaxCp[g]=averageCp[g]
            print("C" + str(g) + ": " + str(averageCp[g]))
            print("Maximum: "+ str(MaxCp[g]))
          

          for g in range(8):
            averageC[g].append((averageCp[g]))
        else:
          print("Starter was 1") #This has to be like that otherwise its retarded
          starter=starter-1
          return(0) #This is the output of the 1st time

class Plot(object):
  
  def __init__(self):
    print("plot init")
    self.n = 200
    self.fig = plt.figure()
    self.axes = [self.fig.add_subplot('81' + str(i)) for i in range(1, 9)]
    [(ax.set_ylim([0, 75])) for ax in self.axes]
    self.graphs = [ax.plot(np.arange(self.n), np.zeros(self.n))[0] for ax in self.axes]
    plt.ion()

  def refresh(self):
    global averageC
    for g, data in zip(self.graphs, averageC):
      if len(data) < self.n:
        # Fill the left side with zeroes.
        data = np.concatenate([np.zeros(self.n - len(data)), data])
      g.set_ydata(data)    
    plt.draw()

  def main(self):
    print("plot main")
    while True:
      self.refresh()
      plt.pause(1.0 / 30)
def plotter():
  Plot().main()


def myobandthings():
  while hub.run(listener.on_event, 10000000):
    pass
def emgthing():
  while(True):
    millis = int(round(time.time() * 1000))
    emgprocessing(listener).main()
    delaytime=50+millis-(int(round(time.time() * 1000)))
    if(delaytime>=0):
      time.sleep(delaytime/1000)

if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  time.sleep(1)
  Thread(target = myobandthings).start()
  Thread(target = emgthing).start()
  time.sleep(1)
  Thread(target = plotter).start()

