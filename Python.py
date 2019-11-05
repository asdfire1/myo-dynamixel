from __future__ import print_function
import myo
import serial
import time

ser = serial.Serial("COM10", 57600)

ser.write(b'initx')

class Listener(myo.DeviceListener):

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.vibrate(myo.VibrationType.short)
    event.device.request_battery_level()

  def on_battery_level(self, event):
    print("Your battery level is:", event.battery_level)

  def on_pose(self, event):
    if event.pose == myo.Pose.double_tap:
      ser.write(b'doubletap')
    elif event.pose == myo.Pose.fist:
        ser.write(b'fistx')
        print('fist')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.fingers_spread:
        ser.write(b'fingersx')
        print('fingers')
        event.device.vibrate(myo.VibrationType.short)
    elif event.pose == myo.Pose.wave_in:
        ser.write(b'inx')
        print('in')
    elif event.pose == myo.Pose.wave_out:
        ser.write(b'outx')
        print('out')
    else:
        ser.write(b'0x')
        print('0')
    
        


if __name__ == '__main__':
  myo.init()
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 500):
    pass
  print('Bye, bye!')


