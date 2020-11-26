#William Yager
#Leap Python mouse controller POC
import sys
from leap import Leap, Mouse
from Leap_listener import Control_Listener
import time

def show_help():
    print "----------------------------------LeapMotion----------------------------------"


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return

    for i in range(0,len(sys.argv)):
        arg = sys.argv[i].lower()

    listener = None

    listener = Control_Listener(True) # Bool to set verbose
    controller = Leap.Controller()  #Get a Leap controller {frameEventName: 'deviceFrame'}
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    print "Adding Listener."
    controller.add_listener(listener)  #Attach the listener

    #Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    #Remove the sample listener when done
    controller.remove_listener(listener)

main()
