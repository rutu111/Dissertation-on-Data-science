#the following measuress the consistency of the dataset
import glob
import itertools
import time as time2
import numpy as np
import statistics
from improv_noise import func

height = 189.2785 #choose the height/depth for which you want to retrieve all the temperature vs time values for
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts" #path chosen
x, y, target_prev, target_next, initialtime = func(height,path) #call to func function defied in improv_noise.py

y_prev = []
for j in target_prev:
    y_prev.append(j['temp'])

y_next = []
for j in target_next:
    y_next.append(j['temp'])

def consistency_systamatic():
    #checks if the potential noisy values are systamatic
    #the loop below gets the means of values at intervals of 5
    intervals = 5 #mean taken at intervald of 5
    total = 0
    list = []
    a = 0
    thersold = 0.2
    count = int(len(y) / intervals) #number of times we need to keep taking the mean
    for j in range(count):
        ynew = y[a:]
        for i,val in enumerate(ynew):
            if i < intervals:
                total = ynew[i] + total
        mean = round(total/intervals,2)
        list.append(mean)
        #so at the end, list will contain the means of the first set of 5 values, second set of 5 values etc..
        total = 0
        a = a + intervals
    #loop below checks distance between each value of an interval with its corresponding mean value
    a = 0
    total = 0
    list_2 = []
    for i,val in enumerate(list):
        ynew = y[a:]
        for j,val in enumerate(ynew):
            if j < intervals:
                absval = abs(ynew[j] - list[i])
                list_2.append(absval)
                #in the end, list_2 will contain the absolute distance between values of an intervals with the mean of particular interval. So if first mean in list is 19.20. Then the first 5 values of y will be compared to 19.20 and differences will be taken for each value and so on..
        a = a + intervals
    absval = 0
    if len(list_2) != len(y):
        #this is for the last set of values that were not given a mean value (because i did int(len(y) / intervals) at the start )
        new = y[len(list_2):]
        for j,val in enumerate(new):
            absval = abs(new[j] - list[len(list)-1]) #for the last few values of y for which absolte distance was not calculated
            list_2.append(absval) #now list_2 is the same size as y
    list_count = []
    for i,val in enumerate(list_2):
        if val > thersold:
            list_count.append(i)
            #list_count contains the indexes of the potential noisy values at this height. But are they systamatic noise? Let's see
    #print(list_count)
    thresold = 0.1
    count = 0
    list_count_2 = []
    #to check if potential noisy values in list_count are systamatic noise or not
    #we have to compare them with potential noisy values from the height above and below it
    #if they match, its systamatic noise
    for i, val in enumerate(list_count):
        if  (y_prev[val] - thresold  <= y[val] <= y_prev[val] + thresold ) and (y_next[val] - thresold  <= y[val] <= y_next[val] + thresold ): #checks if the noisy value in y exists in yprev AS WELL AS ynext. If it does, then it is a systamatic outlier/noise
            list_count_2.append(y[val])
            count = count + 1
    if count != 0:
        print('The points subject to systamatic noise are:', list_count_2, 'Hence,The % of systamatic noise in this data set is:', (count/len(list_count))*100)
        #this returns the systamatic outlier/noise points if they exist
    else:
        print("The depth examined does not contain systamatic noise")

def consistency_checker(y):
#this code checks consistency within intervals. So for an interval of 5, it takes the first 5 values and calculates
#the difference between i and i+1 and so on
#it then sums the differences/intervals and gets the mean.
#If mean is greater than thersold, then it means these 5 values aren't quite consistent
#and if thats the case, then its added to count. Now the same process is repeated for the next set of values and so on
#at the end, count is divide by the no. of intervals  x 100 to get the % precision of the whole dataset
#changes in the value of thersold and intervals would produce different results
    intervals = 5
    total = 0
    a = 0
    thersold = 0.2 #thersold abovewhich something would be considered unprecise
    count_2 = 0
    count = int(len(y) / intervals) #number of times we need to keep taking the mean
    #loop below calculates differnce between a set of 5 values and checks if the mean exceeds a thresold
    for j in range(count):
        ynew = y[a:]
        for i,val in enumerate(ynew):
            if i < intervals:
                difference = abs(ynew[i+1] - ynew[i])
                total = difference + total
        mean = round(total/intervals,2) #mean of the differences
        if mean > thersold:
            count_2 = count_2 +  1 #because if mean > thersold, its not precise
        total = 0
        a = a + intervals

         #for the values that were not included because of the int in int(len(y) / intervals):
    if (count*intervals) != len(y):
        diff = len(y) - (count*intervals)
        ynew = y[(count*intervals):]
        for j,val in enumerate(ynew):
            if j < (diff - 1):
                difference = abs(ynew[j+1] - ynew[j])
                total = difference + total
        mean = round(total/(diff-1),2)
        if mean > thersold:
            count_2 = count_2 +  1
    consistency = 100 - ((count_2/(len(y) / intervals)) * 100)
    print('The consistency of this dataset using a consistency checker is:' ,consistency, '%')

def consistency():
    consistency_systamatic()
    consistency_checker(y)
    print("")
    vote = input("To Go back to the main menu press: m (or press any random key to exit the program) \n ")
    if vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    consistency()
