import glob
import itertools
import time as time2
import numpy as np
import statistics
import matplotlib.pyplot as plt
from improv_noise import func

height = 189.2785 #heght chosen
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts" #path chosen
x, y, target_prev, target_next, initialtime = func(height,path) #call to func function defied in improv_noise.py

thersold = 0.2

def standard_dev(y):
    #this is a very good way of checkin the precision of a dataset.
    #standard deviation tells you the dispersion of the values in your dataset
    #the higher the s.d, the lower the precision of your dataset.
    mean = round(np.mean(y,dtype=np.float64),2)
    standard_deviation = round(np.std(y),2)
    print('The mean and the standard deviation of the data set is' , mean ,'+-' , standard_deviation)
    print('The precision of this dataset using the fractional uncertainity metric is:' , round((standard_deviation/mean)*100,2) ,'%')
    #denominator of the above formular is supposed to be expected value
    #but because this is being done for the whole data set, i've taken the average expected value


def moving_precision_checker(y):
    #the following function checks the precision of dataset
    #each y value is compared to 5 surrounding values (the number of surrounding values compared with depends on the interval set)
    #each of the 5 values is given a range of values defined by the thresold.
    #if the value in question exceeds the range for more than the 'limit', then it is considered to be inprecise
    a = 0
    list = []
    list_x = []
    intervals = 5 #the number of progressive/concecutive values you want to compare your current value with
    count = 0
    limit = int(intervals/2) + 1 #this will to grow as intervals grow
    for j,val in enumerate(y):
        if j < (len(y)-intervals):
            for q in range(intervals): #compares each value with 5 values consective from it
                if y[j] > y[j+q+1] + thersold or y[j] < y[j+q+1] - thersold: #if value is above or below a range of a speicfic value, then increment count
                    count = count + 1
            if count >= limit:
                list.append(y[j]) # j can be greater or lower than more than 1 value. So we need to set thersold to this.
            #So if you are comparing j with 5 values. if j is greater than lower than more than 3 of these values, only then its considered to be imprecise
            #if we set limit to 1 then manyyyy values will return as imprecise because data set has many flacuations/noist values
                list_x.append(x[j]) #appending corresponding x value
            count = 0
        else:
            #this is for values for which 5 concecutive values don't exist.
            #for example if j is at index 149 then there are only two values to compare because last index is 151
            #so in this case 150, 151, 152, 148 and 147 are compared
            #if j is at 151 then 146,147,148,149 and 150 are compared
            diff = len(y) - j - 1
            inverse_count = intervals - diff
            for p in range(diff):
                if y[j] > y[j+p+1] + thersold or y[j] < y[j+p+1] - thersold:
                    count = count + 1
            for s in range(inverse_count): #backwards loop. if j is ar 149, then it will be compared with 2 values ahead of it and two values before it. if j = 151 then it will be compared with 4 values before it,
                if y[j] > y[j-s-1] + thersold or y[j] < y[j-s-1] - thersold:
                    count = count + 1
            if count >= limit:
                    list.append(y[j])
                    list_x.append(x[j])
                    #print(list)
            count = 0
    # this precision metric can be used to determine the outliers in a data set
    percentage_outliers = 100 -((len(list)/len(x)) * 100)
    print('The precision of this dataset using the precision checker method is:' ,round(percentage_outliers,2),'%')

def precision():
    standard_dev(y)
    moving_precision_checker(y)
    print("")
    vote = input("To Go back to the main menu press: m (or press any random key to exit the program) \n ")
    if vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    precision()
