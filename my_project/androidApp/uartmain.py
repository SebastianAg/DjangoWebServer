"""
Retreives serial data from UART buffer,
get the UTC time and stores values in a textfile
"""
import serial
import time
import array
import readuart as ure

uart = serial.Serial("/dev/ttyAMA0",baudrate=9600)	#define UART channel

#uart.write(str.encode("0A0G300K30G240K30GXX"))

command = 1 #global variable for command from application, default 2 (2 - none command)

#####################################################################
# Writes direction command to pico via UART
#####################################################################
def write_dir_command(direction):
    uart.write(str.encode('S'))
    if direction == 5:
        #forward direction
        uart.write(str.encode('F'))
        pass
    elif direction == 4:
        #right turn
        uart.write(str.encode('R'))
        pass
    elif direction == 6:
        # backwards direction
        uart.write(str.encode('B'))
        pass
    elif direction == 2:
        # Left turn
        uart.write(str.encode('L'))
        pass

###################################################################
#	main loop
###################################################################
while True:
    buffer = uart.in_waiting 		#checks if something is waiting in the buffer
    if command == 0:
        command = 2
        if buffer > 0:					#if more then zero bytes in buffer
            data = uart.read(1)			#reads Rx buffer
            data = data.decode('utf_8')	#change format
            file = open("myfile.txt", "a")
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
    elif command == 1:
        command = 2
        array = ure.read_uart_file()
        for i in range(len(array)):
            if i == 0:
                # Sends start direction
                start = array[i+1]
                write_dir_command(start)
                print('start')
            elif i%2 == 1:
                direction = array[i]
                if direction == 0:
                    break
                stop_time = array[i+1]  
                tic = time.perf_counter()
                while int(time.perf_counter()) < tic + stop_time:
                    #check for ultrasound flags
                    if buffer > 0:
                        data = uart.read(1)
                        if data == 'U' or data == 'J':
                            pass
                        else:
                            pass
                    #check for shutdown message
                    pass
                write_dir_command(direction)
                print('end')
            else:
                pass
        


