#this code contains all the improvement methods for noise
#parts of this code has been done in collbaoration with Jacob Gelling studying at University of aberdeen student ID:51768261

import glob
import itertools
import time as time2
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.fftpack import fft,ifft, fftfreq,fftshift
from scipy import signal


height = 189.2785 #choose the height/depth for which you want to retrieve all the temperature vs time values for
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts"
def func(height,path):
    #this function gets the temperature (y) and time (x) values for a particular depth/height
    matrix = {} #matrix of all the values in the data set.
    for datafile in glob.glob(path):
    	with open(datafile) as f:
    		time = ''
    		for line in itertools.islice(f, 8, None):
    			time = line.split("TIMESTAMP: ")[1].rstrip()
    			time = time2.strptime(time, "%Y/%m/%d %H:%M:%S")
    			break
    		for line in itertools.islice(f, 4, None):
    			splitLine = line.split("\t")
    			if float(splitLine[0]) in matrix:
    				matrix[float(splitLine[0])].append({'temp': float(splitLine[1]), 'time': time})
    			else:
    				matrix[float(splitLine[0])] = [{'temp': float(splitLine[1]), 'time': time}]
    #print(matrixx
    height = 189.2785
    target = matrix[height]
    target_prev = matrix[188.2645]
    target_next = matrix[190.2935]
    x = []
    y = []
    z = []
    for j in target:
        x.append(j['time'])
        #y.append(i)
        y.append(j['temp'])


    initialtime = 0
    points = []
    for j in target:
        if initialtime == 0:
            initialtime = time2.mktime(j['time'])
        points.append([(time2.mktime(j['time']) - initialtime) / 60, j['temp']])
    points = np.array(points)

    x = points[:,0]
    y = points[:,1]
    return x,y, target_prev, target_next, initialtime #func returns two lists: x and y. These are time vs temp values at a particular depth defined within the function

#function being called below
x, y, target_prev, target_next, initialtime = func(height,path) #to break the output of the function into two distinct/independent lists.

def entropy_change_func(y,y2,method):
    #this function calculates the average entropy change between the entropy of the original values vs new entropy of new values
    #y is original list and y2 is the new/improved list of values
    method = method
    c = 0
    sum = 0
    for j,i in enumerate(y2):
        absolute_error = abs(y[j] - i) #absolute distance of old points - new points
        entropy_change = absolute_error - 0.01 #because all values have an uncertanity of 0.01 because this is the uncertainity of the equiments used.
        sum += entropy_change
        c += 1
    average_entropy_change = round((sum / c),3)
    return print('The average absolute uncertanity increase using',method, 'is =' ,average_entropy_change)


def standard_dev(y2):
    standard_deviation = round(np.std(y2),3)
    print("The standard deviation of the improvement values is:", standard_deviation)

def linear(x,y):
    #this function performs linear regression on original y points
    linear = np.polyfit(x, y, 1)
    line = np.poly1d(linear)
    print('The equation of the line is:' ,line) #print eqation of the line

    #array containing all the improved points
    y_new = []  #new values of y caculated from x and equation of the line
    for i,val in enumerate(x):
        y_new.append(round(line.c[0]*x[i] + line.c[1],3))

    #call to the entropy change function
    method = "Linear regression"
    entropy_change_func(y,y_new,method)
    standard_dev(y_new)
    print("")

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.plot(x,line(x), color='orange') # linear regression line
    plt.scatter(x,y_new, color='red') # improved points
    plt.legend(['Linear regression','Original','Improved'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    print("The improved y points using linear regression are: \n", y_new)


def cubic(x,y):
    #this function performs cubic parabola on original y points
    cubic = np.polyfit(x, y, 3)
    curve = np.poly1d(cubic)
    print('The equation of the curve is:',curve) #print equation of the curve

    #this array contains all the improved points
    y_new = []  #new values of y caculated from x and equation of the curve
    for i,val in enumerate(x):
    	y_new.append(round(curve.c[0]*x[i]*x[i]*x[i] + curve.c[1]*x[i]*x[i] + curve.c[2]*x[i] + curve.c[3],3))


    #call to entropy change function
    method = "Cubic parabolas"
    entropy_change_func(y,y_new,method)
    standard_dev(y_new)
    print("")

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.plot(x,curve(x), color='orange') # curve
    plt.scatter(x,y_new, color='red') # improved points
    plt.legend(['Cubic parabola','Original','Improved'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    print("The improved y points using Cubic parabolas are: \n", y_new)

def cubic_spline(x,y):
    #this performa s cubic spline on the original points
    spline = interpolate.UnivariateSpline(x, y, s=5)
    x_new = np.arange(min(x), abs(max(x)-min(x)), 0.1)
    y_new = spline(x_new)

    #new array containing improved points
    newarray = []
    for j in x:
    	newarray.append([j, spline(j)])
    newarray = np.array(newarray)
    x2 = newarray[:,0]
    y2 = newarray[:,1]

    y_rounded = []
    for i,val in enumerate(y2):
        y_rounded.append(round(val,3))

    #call to entropy change function
    method = "Cubic splines"
    entropy_change_func(y,y2,method)
    standard_dev(y2)
    print("")

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.plot(x, y, 'x', x_new, y_new)
    plt.scatter(x,y2, color='red') # points
    plt.legend(['Cubic Spline','Original','Improved'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    print("The improved y points using Cubic splines are: \n", y_rounded)


def fft_func(x,y):
    y_orig = y #original points
    #below i am going to round all the x values to give a better visualization of the graph and also because fft assumes x to be in regular intervals
    x_round = []
    for i,val in enumerate(x):
        x_round.append(round(val))
    #print(x_round) #the rounding is done just to plot a more accyrate looking graph

    y = fft(y_orig) #get fft values of y
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.plot(x_round, y_orig, color='red')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    freq = fftfreq(len(y), x[1] - x[0]) #calculate the frequency

    for i, val in enumerate(freq):
    	if val == 0:
    		y[i] /= 100 #lower the fft value of the peak at 0hz
    plt.title('Frequency domain')
    plt.xlabel("Frequency")
    plt.ylabel("FFT")
    plt.plot(fftshift(freq), abs(fftshift(y)))
    plt.show()
    #this is the low pass filter
    count = 2
    cut_off = 0.02 #cut off frequency. After this frequency, the frequency values will be reduced linearly.
    for i, val in enumerate(freq):
    	if val > cut_off: #for positive frequencies.
    		y[i] = y[i] / count
    		count += 2
    		#y[ind] = 0 #uncomment this if you want to set all frequencies to 0 after the cut off. This will result into smoother improved values
    for i, val in enumerate(freq):
    	if val < -(cut_off): #for negative frequencies.
    		y[i] = y[i] / count
    		count -= 2
    		#y[ind] = 0


    for i, val in enumerate(freq):
    	if val == 0:
    		y[i] *= 100 #multiplying the fft value at 0hz with 100 because this had ben divided in the previous step.

    ynew = ifft(y) #inverse fft affter the cut off would result into smoother/less noisy y values.
    y_new = []
    for i, val in enumerate(ynew):
        y_new.append(round(val.real,3))

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.plot(x_round, y_orig, color='red')
    plt.plot(x_round, y_new) #
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.legend(['Original', 'Improved after cut off'])
    plt.show()

    method = "Fast fourier transform"
    entropy_change_func(y_orig,ynew,method)
    standard_dev(ynew)
    print("")
    print("The improved y points using Fast fourier transform are: \n", y_new)

def conv_moving_average_filter(y):
    #moving average filter of length 5 in either side of the y in question
    #idea of this code gotten from https://www.analog.com/media/en/technical-documentation/dsp-book/dsp_book_Ch15.pdf
    window = 5 #this is half the length of the window
    y_new = [None]*(len(y))
    for i in range(window, len(y)-window): #loops from 5th value of y to ((length of y) - 5)th value
        #this is a double sided loop. example if y= 6 then window is from 1 to 11
        y_new[i] = 0
        for j in range(-window, window+1):
            y_new[i] = y_new[i] + y[i+j]
        y_new[i] = y_new[i] / (window*2+1)
    for i in range(0, window): #loops from 0th to 5th value of y to cover values missed out in the first loop
        #this is a one sided window. only looks forwards from the value in question, not backwards. example if y is 2 then windowm is from 2 to 12
        y_new[i] = 0
        for j in range(window):
            y_new[i] = y_new[i] + y[i+j]
        y_new[i] = y_new[i] / window
    for i in range(len(x)-window, len(y)): # loops last 5 values of y to cover values missed in first loop
        #this is a one sided window. only looks backwards from the value in question, not forwards. example if y is 152 then windowm is from 142 to 152
        y_new[i] = 0
        for j in range(-window, 0):
            y_new[i] = y_new[i] + y[i+j]
        y_new[i] = y_new[i] / window

    plt.figure()
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y,color="orange")
    plt.plot(x, y_new, color='red')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.legend(['Original', 'Improved'])
    plt.show()
    y_final = []
    for i,val in enumerate(y_new):
        y_final.append(round(val,3))


    method = "the Moving average filter"
    entropy_change_func(y,y_new,method)
    standard_dev(y_new)
    print("")
    print("The improved y points using tge moving average filter are: \n", y_final)


def conv_salv_gal_filter(y):
    #this is the Savitzky-Golay filter.
    filter = signal.savgol_filter(y,11,3,delta=5,mode='nearest')

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y,color="orange")
    plt.plot(x, filter, color="blue")
    plt.legend(['Original', 'Improved'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    method = "the Savitzky-Golay filter"
    entropy_change_func(y,filter,method)
    standard_dev(filter)
    print("")
    y_final = []
    for i,val in enumerate(filter):
        y_final.append(round(val,3))

    print("The improved y points using the Savitzky-Golay filter are: \n", y_final)


def kalman(y):
# this code has been taken from https://scipy-cookbook.readthedocs.io/items/KalmanFiltering.html
# A Python implementation of the example given in pages 11-15 of "An
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,
# University of North Carolina at Chapel Hill, Department of Computer
# Science, TR 95-041,
# https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf
# by Andrew D. Straw

# intial parameters
    iter = 152 #no. of points
    sz = (iter,) # size of array
    Q = 1e-5 # process variance

    # allocate space for arrays
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor

    R = np.var(y) # estimate of measurement variance
    # intial guesses
    xhat[0] = y[0] #start at the first value of y
    P[0] = 1.0

    for k in range(1,iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(y[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]

    plt.figure()
    plt.plot(y,'k+',label='noisy measurements')
    plt.plot(xhat,'b-',label='a posteri estimate/improved points')
    plt.legend()
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.show()
    #size od y in these graphs is 140 because we are simply plotting y values. in linear for example, we were plotting x values agaisnt y values and that is why the size stretched upto to 170 even thought size of y is 140 after removing outliers.
    method = "the Kalman filter"
    entropy_change_func(y,xhat,method)
    standard_dev(xhat)
    print("")
    y_final = []
    for i,val in enumerate(xhat):
        y_final.append(round(val,3))

    print("The improved y points using the Kalman filter are: \n", y_final)


def binning_method(y):
    #the binning method takes mean at intervals of 5 and this mean of each interval is used to smooth that interval
    #and then merging all smoothed values into new list which would be the new improved y values and then entropy change is calculated.
    intervals = 5 #mean taken at intervals of 5
    total = 0
    new_y = []
    a = 0
    count = int(len(y) / intervals) #number of times we need to keep taking the mean
    for j in range(count):
        ynew = y[a:]
        for i,val in enumerate(ynew):
            if i < intervals:
                total = ynew[i] + total
        mean = round(total/intervals,2)
        for z in range(5):
            new_y.append(mean) #so at the end, list will contain the means of the first set of 5 values, second set of 5 values etc..
        total = 0
        a = a + intervals
    if len(new_y) != len(y): #this is for the last set of values that were not given a mean value (because i did int(len(y) / intervals) at the start )
        new = y[len(new_y):]
        for j,val in enumerate(new):
            new_y.append(mean) #the last set of values are given the latest mean values

    #call to entropy change function
    method = "the binning method"
    entropy_change_func(y, new_y,method)
    standard_dev(new_y)
    print("")

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y,color="orange")
    plt.plot(x, new_y, color="blue")
    plt.legend(['Original', 'Improved'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    y_final = []
    for i,val in enumerate(new_y):
        y_final.append(round(val,3))

    print("The improved y points using Binning are: \n", y_final)


def inputUser():
    method = input("Which noise improvement method would you like to visualize? You options are: \n 1) Linear regression \n 2) Cubic parabola \n 3) Cubic Splines \n 4) Fast fourier transform \n 5) Convolution with moving average filter \n 6) Convolution with Savitzky-Golay filter \n 7) Kalman Filter \n 8) Binning \n 9) Exit \n Please enter the number of your choice: \n ")
    if method == "1":
        linear(x,y) #display linear
    elif method == "2":
        cubic(x,y) #display cubic
    elif method == "3":
        cubic_spline(x,y)#display cubic_spline
    elif method == "4":
        fft_func(x,y)
    elif method == "5":
        conv_moving_average_filter(y)
    elif method == "6":
        conv_salv_gal_filter(y)
    elif method == "7":
        kalman(y)
    elif method == "8":
        binning_method(y)
    elif method == "9":
        exit()
    else:
        print("You have entered an invalid number. Please try again")
        print("")
        inputUser()
    vote = input("To explore a different noise method press: 0, To return back to the main menu press: m, To exit the program press any key \n")
    if vote == "0":
        inputUser()
    elif vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    inputUser()
