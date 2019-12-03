# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:59:55 2019

@author: hkohli
"""

import signal
import time
import sys

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)



while True:
    time.sleep(0.1)