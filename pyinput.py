#from pynput.mouse import Button, Controller
#from pynput.keyboard import Controller
import serial
import numpy as np
import _thread as thread

s = serial.Serial(
	port = '/dev/tty.usbmodem1411',
	baudrate = 250000,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout = 1
)


up = False
down = False
left = False
right = False

runmode = 0 # 0 - mouse, 1 - joystick

def runLoop1():
    global up
    global down
    global left
    global right
    global runmode

    from pynput.keyboard import Key, Controller
    keyboard = Controller()
    
    print('runLoop started')
    
    
    while True:
        line = s.readline()
        print(line)
        line2 = str(line)

        if('mouseclick' in line2):
            keyboard.press('z')
        
        if ('upstart' in line2):
            if(down == True):
                down = False
            up=True

        elif ('downstart' in line2):
            if(up == True):
                up = False
            down=True

        elif ('leftstart' in line2):
            if(right == True):
                right = False
            left=True

        elif ('rightstart' in line2):
            if(left == True):
                left = False
            right=True

        elif ('downstop' in line2):
            down=False

        elif ('upstop' in line2):
            up = False

        elif ('leftstop' in line2):
            left = False

        elif ('rightstop' in line2):
            right = False

        if(up == True):
            #mouse.move(0, -5)
            keyboard.press('w')

        elif(down == True):
            #mouse.move(0, 5)
            keyboard.press('s')

        elif(left == True):
            #mouse.move(-5, 0)
            keyboard.press('a')

        elif(right == True):
            #mouse.move(5, 0)
            keyboard.press('d')

def runLoop0():
    from pynput.mouse import Button, Controller
    mouse = Controller()

    mousex = 0.00
    mousey = 0.00

    print('runloop0 started')
    
    while True:
        line = s.readline()
        #print(line)
        line2 = str(line)
        line3 = line2[:-5]
        line4 = line3.replace("b' ","")

        #print(line4)
        if('mouseclick' in line4):
            mouse.click(Button.left, 1) #!!
        
        if ('mousepress' in line4):
            mouse.press(Button.left)

        if ('mouserelease' in line4):
            mouse.release(Button.left)

        if ('rollmap' in line4):
            line5 = line4.replace("rollmap","")
            line6 = line5.replace(" ","")
            print(line6)
            if(float(line6) > 10):
                mousex = float(line6) /4
            elif(float(line6) < -10):
                mousex = float(line6) /4
            else:
                mousex = 0

        if ('pitchmap' in line4):
            line5 = line4.replace("pitchmap","")
            line6 = line5.replace(" ","")
            print(line6)
            if(float(line6) > 10):
                mousey = float(line6) /4
            elif(float(line6) < -10):
                mousey = float(line6) /4
            else:
                mousey = 0

        if('lightvaldown'in line4):
            mouse.click(Button.right,1)
                    
        mouse.move(mousex,mousey)
        
        
            
if(runmode == 1):
    thread.start_new_thread(runLoop1, ())

if(runmode == 0):
    thread.start_new_thread(runLoop0, ())


