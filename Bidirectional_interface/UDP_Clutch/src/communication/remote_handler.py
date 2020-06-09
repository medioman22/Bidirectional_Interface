# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 23:40:29 2018

@author: macchini
"""
   
from threading import Thread
from time import sleep

#from msvcrt import kbhit

# import pywinusb.hid as hid

HOBBYKING = 'HID-compliant game controller'
LOGITECH_510 = 'Rumble Gamepad F510'

class remote_handler():
    
    def __init__(self):
        self.device = None
        self.device_name = None
        self.data = None
        self.read_done = False
        self.kill_read_thread = False
        
        self.desired_device = HOBBYKING

    def update_read(self, data):
        self.raw_data = data
        
        # get values in this order [left joy : vertical, left joy : horizontal, right joy : vertical, right joy : horizontal]
        if HOBBYKING in self.device_name:
            self.data = [data[3], data[6], data[2], data[1]]
        elif LOGITECH_510 in self.device_name:
            self.data = data
            self.data = [data[3], data[1], data[7], data[5]]
        else:
            self.data = data
        self.read_done = True
        
    def print_data(self):
        print("Raw data: {0}".format(self.data))
    
    def connect(self):
        
        # simple test
        # browse devices...
        all_hids = hid.find_all_hid_devices()
        all_hids_str = [str(x) for x in all_hids]
        if all_hids:
            self.all_devices = all_hids_str
            if [self.desired_device in x for x in all_hids_str].index(True) is not None:         
                try:
                    self.device = all_hids[[self.desired_device in x for x in all_hids_str].index(True)]    # finds first occurency of substring (ex.Rumble Gamepad F510)
                    self.device_name = str(self.device)
                    print("Connected to RC remote")
                except:
                    print("There's not any non system HID class device available")
                
    def read_once(self):
        self.open_device()
        
        while not self.read_done:
            sleep(0.001)
        
        self.read_done = False
        
        return self.data
                
    def read_background(self):
        self.open_device()
        
        thread = Thread(target = self.threaded_read_background)
        thread.start()
#        thread.join()

    def threaded_read_background(self):
        while self.device is not None and self.device.is_plugged() and not self.kill_read_thread:
            #just keep the device opened to receive events
            sleep(0.001)
        self.kill_read_thread = False
            
    def stop_read_background(self):
        self.kill_read_thread = True
                
    def open_device(self):
        
        try:
            self.device.open()
        except:
            raise ValueError('Could not connect to remote')


        #set custom raw data handler
        self.device.set_raw_data_handler(self.update_read)

#        while not kbhit() and device.is_plugged():
#            #just keep the device opened to receive events
#            sleep(0.01)
#        return
            
    def close_device(self):
        self.device.close()
        self.device = None