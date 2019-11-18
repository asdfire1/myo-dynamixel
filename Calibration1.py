from _future_ import print_function
import myo
import time
import os
import numpy as np
from collections import deque
from threading import Lock, Thread
from matplotlib import pyplot as plt


averageC = [deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200),deque(maxlen=200)]

starter=25 # This has to be like that because its retarded
#ser.write(b'initx')

class Listener(myo.DeviceListener):
  def __init__(self):
    print("_init_")
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=100) #this can be changed to make the strength change slower and be more stable

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.stream_emg(True)
    event.device.vibrate(myo.VibrationType.short)

  def get_emg_data(self):
    #print("getemgdata")
    with self.lock:
      return list(self.emg_data_queue)


  def on_emg(self, event):
    #print("onemg")
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class readingtest(object):
  def __init__(self, listener):
    self.listener = listener
    #print("reading init")
  def main(self):
        global starter
        global averageC
        averageCp = np.zeros((8,), dtype=float)
        emg_data = self.listener.get_emg_data()
        if (starter==0):
          #this is the code that will run every time except for the 1st time is
          emg_data = np.array([x[1] for x in emg_data]).T
          emg_data = np.absolute(emg_data)
          emg_datal=emg_data.tolist()
          #emg_data = np.average(emg_data)
          #print(type(emg_datal))
          #emg_data = float(emg_data)
          #print(emg_datal)
          #print(emg_datal[1])
          #emg_dataC0=emg_datal[0]
          #emg_dataC1=emg_datal[1]
          #emg_dataC2=emg_datal[2]
          #emg_dataC3=emg_datal[3]
          #emg_dataC4=emg_datal[4]
          #emg_dataC5=emg_datal[5]
          #emg_dataC6=emg_datal[6]
          #emg_dataC7=emg_datal[7]
          #cls()
          #print(emg_datar)
          #print("average value:")
          for g in range(8):
            averageCp[g]=sum(emg_datal[g])/len(emg_datal[g])
            print("C" + str(g) + ": " + str(averageCp[g]))
          
          #averageC0=sum(emg_dataC0)/len(emg_dataC0) #to be changed
          #print("C0: "+ str(averageC0))
          #averageC1=sum(emg_dataC1)/len(emg_dataC1)
          #print("C1: "+ str(averageC1))
          #averageC2=sum(emg_dataC2)/len(emg_dataC2)
          #print("C2: "+ str(averageC2)) 
          #averageC3=sum(emg_dataC3)/len(emg_dataC3)
          #print("C3: "+ str(averageC3))
          #averageC4=sum(emg_dataC4)/len(emg_dataC4) #to be changed
          #print("C4: "+ str(averageC4))
          #averageC5=sum(emg_dataC5)/len(emg_dataC5)
          #print("C5: "+ str(averageC5))
          #averageC6=sum(emg_dataC6)/len(emg_dataC6) #to be changed
          #print("C6: "+ str(averageC6))
          #averageC7=sum(emg_dataC7)/len(emg_dataC7)
          #print("C7: "+ str(averageC7))

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
    #plt.show()

  def refresh(self):
    global averageC
    print("plot refresh")
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
def garbage():
  Plot().main()


def myoshit():
  while hub.run(listener.on_event, 10000000):
    pass
def ourcrap():
  while(True):
    millis = int(round(time.time() * 1000))
    readingtest(listener).main()
    delaytime=50+millis-(int(round(time.time() * 1000)))
    if(delaytime>=0):
      time.sleep(delaytime/1000)

if _name_ == '_main_':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  time.sleep(1)
  Thread(target = myoshit).start()
  Thread(target = ourcrap).start()
  time.sleep(2)
  Thread(target = garbage).start()
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