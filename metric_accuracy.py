#the following are metrics used for assessing accuracy of a dataset

import glob
import itertools
import time as time2
import numpy as np
import statistics
from improv_noise import func

height = 189.2785 #height chosen
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts" #path chosen
x, y, target_prev, target_next, initialtime = func(height,path) #call to func function defied in improv_noise.py

def average_absolute_distance(x,y):
    #addresses semantic accuracy
    #the following function takes mean at defined interval length (5 in this case)
    #then it uses each mean as the 'true' value for that intervals and finds the average absolute distance for set of points in that interval
    intervals = 5 #mean taken at intervald of 5
    total = 0
    list = [] #this list will store the mean value at each interval
    a = 0
    count = int(len(y) / intervals) #number of times we need to keep taking the mean
    for j in range(count):
        ynew = y[a:]
        for i,val in enumerate(ynew):
            if i < intervals:
                total = ynew[i] + total
        mean = round(total/intervals,2)
        list.append(mean) #so at the end, list will contain the means of the first set of 5 values, second set of 5 values etc..
        total = 0
        a = a + intervals
    #this below finds the absolute distance between each mean and the values of that interval
    a = 0
    total = 0
    global list_2
    list_2 = []
    for i,val in enumerate(list):
        ynew = y[a:]
        for j,val in enumerate(ynew):
            if j < intervals:
                absval = abs(ynew[j] - list[i])
                list_2.append(absval)
                #in the end, list_2 will contain the absolute distance between values of an intervals with the mean of particular interval.
                #So if first mean in list is 19.20. Then the first 5 values of y will be compared to 19.20 and differences will be
                #taken for each value and so on..
        a = a + intervals
    ##this is for the last set of values that were not given a mean value (because i did int(len(y) / intervals) at the start )
    absval = 0
    if len(list_2) != len(y):
        new = y[len(list_2):]
        for j,val in enumerate(new):
            absval = abs(new[j] - list[len(list)-1]) #the absolute distance of those last few values is compared with the mean of the last interval
            list_2.append(absval) #now list_2 is the same size as y
    for i,val in enumerate(list_2):
        total = list_2[i] + total #this takes the mean of all the values
    mean_2 = round(total/len(y),2) * 100 # the lower the value the better as this is average distance/difference between true value and outcomes.
    #0 would mean the outcome values are the same as the true values
    mean_2 = 100 - mean_2 #easier to read -> the higher, the better the quality of the data
    print('The semantic accuracy of this data set using the Average abolute distance metric is:', round(mean_2,2),'%')

def median_absolute_distance(x,y):
    #addresses syntactic accuracy
    #This is calculates the median with a range of acceptable value
    #not using absolute dstance here as syntatic accuracy checks where y belongs to a domain D.
    #The domain here is the range of acceptable values around the median.
    sorted_list = sorted(y) #sorts the list
    median = np.median(sorted_list) #gets the median value of the list
    range_of_acceptable_values = 0.25 #so if median is 19.0,
    #then the lower_limit would be 18.75 and upper_limit would be 19.25.
    #The result depends on this range. So it is upto you to decide what you want to filter out.
    lower_limit = median - range_of_acceptable_values
    upper_limit = median + range_of_acceptable_values
    count = 0
    for i,val in enumerate(y):
        if val > upper_limit or val < lower_limit:  #if value is outside the range of accptable values, then its inccurate
            count = count + 1
    print('The syntatic accuracy of this data set using the Median absolute distance metric is:' , round(100 - (count/len(y)*100),2), '%')

def mode_absolute_distance(x,y):
    #this addresses syntatic accuracy too
    #This is mode with a range of acceptable value.
    #not using absolute dstance here as syntatic accuracy checks where y belongs to a domain D.
    #The domain here is the range of acceptable values around the mode
    y_new = []
    range_of_acceptable_values = 0.25 #so if mode is 19.0, then the lower_limit would be 18.75 and upper_limit would be 19.25.
    #The result depends on this range. So it is upto you to decide what you want to filter out.
    #because the data set is very noisy, all values are very different so to successfully find th mode,
    #i have rounded values to 1 signiicant figure.
    for i, val in enumerate(y):
        y_new.append(round(val, 1))
    mode = statistics.mode(y_new)
    lower_limit = mode - range_of_acceptable_values
    upper_limit = mode + range_of_acceptable_values
    count = 0
    for i,val in enumerate(y):
        if val > upper_limit or val < lower_limit: #if value outside range of acceptable values then its inaccurate
            count = count + 1
    print('The syntatic accuracy of this data set using the Mode absolute distance metric is:' , round(100 - (count/len(y)*100),2),'%')

def relative_error(y,list_2):
    #alternatively you can also caclcutate the relative error to measure the accuracy of the data set.
    expected = np.mean(y) #expected value not given so taking mean of all values as expected value
    absolute_error = np.mean(list_2) #list_2 contains true value - estimated value for each y so we take a mean of this to calculate the absolute error
    print("The accuracy of this data set using the relative error metric is:" ,round((absolute_error/expected)*100,2),'%')

def accuracy():
    average_absolute_distance(x,y)
    median_absolute_distance(x,y)
    mode_absolute_distance(x,y)
    relative_error(y,list_2)
    print("")
    vote = input("To Go back to the main menu press: m (or press any random key to exit the program) \n ")
    if vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    accuracy()
