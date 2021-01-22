import serial

threshold = 1

serial_name = serial.Serial('COM11', 115200, timeout=0.5)
print("Connected to {}".format(serial_name))

newVoltage = 300
toSend = "V{:d}\n".format(newVoltage)
print(toSend)
toSend = bytearray(toSend, encoding="utf-8")
serial_name.write(toSend)

newFrequency = 20
toSend = "F{:d}\n".format(newFrequency)
print(toSend)
toSend = bytearray(toSend, encoding="utf-8")
serial_name.write(toSend)

# Set all clutches to zero voltage
state = "C990\n"    
print('state = {}'.format(state))
toSend = bytearray(state, encoding="utf-8")
serial_name.write(toSend)


print("enter current distance from the obstacle?")
dist = float(input())

if dist <= threshold:
    print("activate all clutches (yes/no)?")
    response = str(input())

    if response == "yes":
        state = "C991\n"
    elif response == "no":
        print("which clutch to activate (0-7)")
        clutch_no = int(input())
    
        if clutch_no == 0:
            state = "C001\n"
        if clutch_no == 1:
            state = "C011\n" 
        if clutch_no == 2:
            state = "C021\n" 
        if clutch_no == 3:
            state = "C031\n" 
        if clutch_no == 4:
            state = "C041\n" 
        if clutch_no == 5:
            state = "C051\n" 
        if clutch_no == 6:
            state = "C061\n" 
        if clutch_no == 7:
            state = "C071\n"       
    print('state = {}'.format(state))
    toSend = bytearray(state, encoding="utf-8")
    serial_name.write(toSend)

elif dist > threshold:
    state = "C990\n"    
    print('state = {}'.format(state))
    toSend = bytearray(state, encoding="utf-8")
    serial_name.write(toSend)

