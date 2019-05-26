import serial
import time
import csv
import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,y2_data,line1,line2,ylabel="Title",identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.4,ms=2,label='voltage')
        line2, = ax.plot(x_vec,y2_data,'-o',alpha=0.4,ms=2,label='current')            
        #update plot label/title
        #plt.legend(loc=2, ncol=2)
        plt.title('Solar Output: {}'.format(identifier))
        ax.legend()
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    # adjust limits if new data goes beyond bounds
    if np.min([y1_data,y2_data])<=line1.axes.get_ylim()[0] or np.max([y1_data,y2_data])>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min([y1_data,y2_data])-np.std([y1_data,y2_data]),np.max([y1_data,y2_data])+np.std([y1_data,y2_data])])
    # if np.min(y2_data)<=line2.axes.get_ylim()[0] or np.max(y2_data)>=line2.axes.get_ylim()[1]:
    #     plt.ylim([np.min(y2_data)-np.std(y2_data),np.max(y2_data)+np.std(y2_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return [line1,line2]

ser = serial.Serial(
    port='COM3',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
print("connected to: " + ser.portstr)

# plt.ion() ## Note this correction
# fig=plt.figure()
# plt.axis([0,1000,0,1])

#this will store the line
seq = []
amperage = []
voltage = []

size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.ones(len(x_vec))
z_vec = np.ones(len(x_vec))
line1 = []
line2 = []

if __name__ == '__main__':
    t_end = time.time() + 60 * 5 #run for 5 minutes
    try:
        while time.time() < t_end:
            for c in ser.read():
                seq.append(chr(c)) #convert from ANSII
                joined_seq = ''.join(str(v) for v in seq) #Make a string from array
                
                if chr(c) == '\n':
                    #print(joined_seq)
                    readings = joined_seq.split(' ', 2)
                    amperage.append(readings[0])
                    voltage.append(readings[1])
                    # plt.scatter(i, readings[0])
                    # i+=1
                    seq = []
                    y_vec[-1] = float(readings[0])
                    z_vec[-1] = float(readings[1][0:-2])
                    #print(float(readings[1][0:-2]))
                    [line1,line2] = live_plotter(x_vec,y_vec,z_vec,line1,line2)
                    y_vec = np.append(y_vec[1:],0.0)
                    z_vec = np.append(z_vec[1:],0.0)
                    break
            # plt.show()
            # plt.pause(0.0001)

        # with open("test_data.csv","a") as f:
        #         writer = csv.writer(f,delimiter=",")
        #         writer.writerow([time.time(),decoded_bytes])
    except KeyboardInterrupt:
        print('Interrupted')
        ser.flushInput()
        sys.exit(0)
