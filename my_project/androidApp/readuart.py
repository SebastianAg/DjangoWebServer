"""
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
"""
import array
import time

dir_to_pico = [] #time and direction array

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
        with open("myfile.txt") as file:
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
                    elif item[i] == 'X':
                        #stop indicator
                        loop = False
                    else:
                        pass
        return dir_to_pico
        


        
     

    
    

