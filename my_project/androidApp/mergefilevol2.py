#for mergeing with server

"""
Retreives serial data from UART buffer,
get the UTC time and stores values in a textfile
"""
import serial
import time
import array
import socket

uart = serial.Serial("/dev/ttyAMA0",baudrate=9600)	#define UART channel

#uart.write(str.encode("0A0G300K30G240K30GXX"))

command = 2 #global variable for command from application, default 2 (2 - none command)

"""
LÄS OCH SKRIV OM FÖRVIRRANDE TEXT

IR-mapping:
open and read file for direction data,
select and differentiate direction from time

In file the direction variable is:
Right motor is CW = A, CCW = E
Left motor is CW = G, CCW = K

Time is saved in dir_time for each motor,
and direction is saved in dir_motor.
For A and E storage are in dir_motor[0] and dir_time[0].
For G and K storage are in dir_motor[1] and dir_time[1].
Each time element is compared and then the direction and
time are stored in dir_to_poico.

Auto drive mode:
Reads the stored direction data from dir_to_pico
and sends direction commands for each time stamp.

Stop:
Both motors in non motion state
"""

dir_to_pico = [] #time and direction array

def set_command(data):
    if data == 'start':
        #send M to pico for mapping
        return 0
    elif data == 'stop':
        #send S to pico for stop
        return 3
    elif data == 'step':
        #use stored map for direction to pico
        return 1

##################################################################
# Convert string digits to integers
##################################################################
def save_time(var_time, int_time2):
    for i in range(len(var_time)):
        int_time = int(var_time[i])*(10**(len(var_time)-(i+1))) #multiply the integer by 10th
        int_time2 = int_time2 + int_time
    return int_time2

##################################################################
#	Saves the minimal time in dir_to_pico array
##################################################################
def get_time_diff(dir_time, idx_p, dir_to_pico):
    time_diff = 0
    if dir_time[0] < dir_time[1]:
        time_diff = dir_time[1] - dir_time[0]
    elif dir_time[0] > dir_time[1]:
        time_diff = dir_time[0] - dir_time[1]
    else:
        time_diff = dir_time[0]
    dir_to_pico[idx_p] = time_diff

##################################################################
#	Converts string to integer as following:
#	AG - 5, AK - 4, EK - 6, EG - 2
#	and stores in dir_to_pico
##################################################################
def create_byte(dir_motor, dir_time, idx_p, dir_to_pico):
    if dir_motor[0] == 'A' and dir_motor[1]== 'G':
        get_time_diff(dir_time, idx_p, dir_to_pico)
        dir_to_pico[idx_p + 1] = 5
    elif dir_motor[0] == 'A' and dir_motor[1]== 'K':
        get_time_diff(dir_time, idx_p, dir_to_pico)
        dir_to_pico[idx_p + 1] = 4
    elif dir_motor[0] == 'E' and dir_motor[1]== 'G':
        get_time_diff(dir_time, idx_p, dir_to_pico)
        dir_to_pico[idx_p + 1] = 2
    elif dir_motor[0] == 'E' and dir_motor[1]== 'K':
        get_time_diff(dir_time, idx_p, dir_to_pico)
        dir_to_pico[idx_p + 1] = 6
    idx_p += 1

##################################################################
#	Reads UART textfile code
#	and convert it to an array(dir_to_pico) of only integers
##################################################################
def read_uart_file():
    loop = True #for limiting the while loop
    idx_r = 0
    idx_l = 0
    idx_p = 0
    idx = 0
    dir_time = array.array('q',[0,0])
    dir_motor = array.array('u',[' ',' '])
    int_time2 = 0 
    while loop:
        with open("/home/jakob/DjangoWebServer-main/my_project/androidApp/myfile.txt") as file:
            for item in file:
                var_time = str()
                dir_to_pico = array.array('q', [0]*len(item)) #construct an array of zeros in size of the data
                for i in range(len(item)):
                    if item[i].isdigit():
                        var_time = var_time + item[i]
                    elif item[i] == 'A' or item[i] == 'E':   
                        int_time2 = save_time(var_time, int_time2)
                        dir_motor[ 0] = item[i]
                        dir_time[0] = int_time2
                        idx += 1
                        if idx == 2:
                            create_byte(dir_motor, dir_time, idx_p, dir_to_pico)
                            idx = 1
                            idx_p += 2
                            if idx_p == len(item):
                                idx_p = 0    
                        var_time = ""
                        int_time2 = 0
                    elif item[i] == 'G' or item[i] == 'K':
                        int_time2 = save_time(var_time, int_time2)
                        dir_motor[1] = item[i]
                        dir_time[1] = int_time2
                        idx += 1
                        if idx == 2:
                            create_byte(dir_motor, dir_time, idx_p, dir_to_pico)
                            idx = 1
                            idx_p += 2
                            if idx_p == (len(item)-1):
                                idx_p = 0
                        var_time = ""
                        int_time2 = 0
                    elif item[i] == 'X': #ändra till S? JENNIE
                        #stop indicator
                        loop = False
                    else:
                        pass
        return dir_to_pico
        
#####################################################################
# Writes direction command to pico via UART, via encoded commands:
# F - Forward (both motors CW motions)
# R - Right turn (one motor Cw and the other CCW motion)
# L - Left turn (one motor CCW and the other CW motion)
# B - Backwards (both motors CCW motions)
# S - stop (both motors in non motion state)
# For every command a stop command are send throught UART to pico,
# so that you get more control over the motion
#####################################################################
def write_dir_command(direction):
    uart.write(str.encode('S'))
    if direction == 5:
        uart.write(str.encode('F'))
        #pass
    elif direction == 4:
        uart.write(str.encode('R'))
        #pass
    elif direction == 6:
        uart.write(str.encode('B'))
        #pass
    elif direction == 2:
        uart.write(str.encode('L'))
        #pass
    else:
        pass

###################################################################
#							main loop
# 	Creates a socker for communication to webserver,
# 	webserver sends manually chooses command through socket.
# 	Retrievs socket input and ether establish
# 	IR-mapping, Auto drive mode or stop
###################################################################
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('localhost',8080))
serv.listen(5)
while True:
    c, addr = serv.accept() #accepts communication socket
    data = c.recv(4096).decode() #recives data through socket and saves it
    print(data)
    c.close() #close the connection
    buffer = uart.in_waiting 		#checks if something is waiting in the buffer
    if set_command(data) == 0:
        if buffer > 0:					#if more then zero bytes in buffer
            data = uart.read(1)			#reads Rx buffer
            data = data.decode('utf_8')	#change format
            file = open("/home/jakob/DjangoWebServer-main/my_project/androidApp/myfile.txt", "a")
            if data.isdigit():
                file.write(data)       
            elif data == 'U' or data == 'J':
                #ultrasounds flags
                #retrieve information of position using localisation tools
                #send solutions to pico
                """
                Alternativ för lösning, vid flagga, så hämtas information om senaste positionering från karta
                """
                pass
            elif data == 'A' or data == 'E' or data == 'G' or data == 'K':
                file.write(data)
            elif data == 'X':
                file.write(data)
            else:
                file.write('B') #byte error message
                file.close()
    elif set_command(data) == 1:
        array = read_uart_file()
        for i in range(len(array)):
            if i == 0:
                start = array[i+1]
                write_dir_command(start) # Sends start direction
                print('begins')
            elif i%2 == 1:
                direction = array[i]
                if direction == 0: #first element in array is always 0
                    break
                stop_time = array[i+1]  
                tic = time.perf_counter()
                while int(time.perf_counter()) < tic + stop_time:
                    if buffer > 0:
                        data = uart.read(1)
                        if data == 'U' or data == 'J': #check for ultrasound flags
                            pass
                        else: #check for shutdown message
                            pass
                    pass
                write_dir_command(direction)
            else:
                pass
    elif set_command(data) == 3:
        write_dir_sommand(3) #send stop command to pico
        
        



