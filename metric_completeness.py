import glob
import itertools
import time as time2
import numpy as np
from functools import reduce
from improv_noise import func

height = 189.2785 #height chosen
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts" #path chosen
x, y, target_prev, target_next, initialtime = func(height,path) #call to func function defied in improv_noise.py

#the following code is for gaps
#x1 = [1,2,3,4,5,6,7,8,15,20,21,22,23,24,25,26]
#gaps of length 6 and 4. This one gets the lowest % because gaps are big in comparison to x2 and x3
#x2 = [1,2,3,4,5,6,7,8,11,14,17,22,23,24,25,26]
# gaps of length 2 2 2 and 4. gets a higher % than x1 because instead of gap 6, there are 3 small ones
#x3 = [1,2,3,4,5,6,7,8,9,10,13,16,19,22,25,26]
#gets highest % score because having 5 gaps of 2 is less crucial than having a big gap of 6 and 4 and seen in x1
#x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
#the aboce is to show that both weighted gaps and gap % would return the same result

def gap_percentage(x):
    gap_ratio_1 = len(x)/ x[len(x)-1] * 100 #no. of complete items/total no. of items * 100
    #diviidng len(x) with x[len(x)-1] because that is the last digit in x. Last digit in x means thats the expected length of x.
    #you can change x[len(x)-1] with whatever you want. Expected values change depending on the data set so i have used a default one here
    print('The completeness of this data using the gap percentage metri is: ' ,round(gap_ratio_1,2),'%')

def gap_ratio(x):
    gap_ratio_2 = 1 - ((x[len(x)-1] - len(x))/x[len(x)-1])  # 1 - no. of incomplete items/total no. of items
    print('The completeness of this data using the gap ratio metric is: ' ,round(gap_ratio_2,2))

def weighted_gaps(x):
    list = []
    Start = 10 #starting gap size. the first gap size looked for is 10
    diff = 1 #if start value is 10, then next value would be 9, and next 8 (difference of 1)
    start_w = 0.82 #starting weightage value. assigned to Start value
    diff_w = 0.02 #spacing betwen the start_w. so gap 10 would get weightage 0.82, gap 9 would get weightage 0.86 etc
    count = 1 #to do the multiplications
    limit = 1 # this is the limit till where you want it to keep calculating differences and assigning values.
    #so in this case, loop stops at >= 2. difference of 1 is not considered a gap example there is no gao in [1,2,3]
    for i, val in enumerate(x):
        if i != len(x)-1:
            #so in this case program loops only 9 times.
            for j in range(Start-limit): #This is important so that it does not loop for the limit-th value.
                if j == 0: #first loop looks for gap of size 10, if it finds it then it appends the corresponding weightage to it
                    if x[i+1]-x[i] >= Start:
                        list.append(start_w)
                        break
                else: #then looks for gaps of size 9, then 8 etc up until it reaches size 1.
                    if x[i+1]-x[i] >= (Start-(diff*count)):
                        list.append(round(start_w + (diff_w*count),2))
                        break
                    else:
                        count = count + 1
            count = 1 #resetting to loop through next index value.
    if list == []: #if list is empty then it means that there are no gaps
        #if there are no gaps, then the percentage is calculated in the classic way and will get same results as gap % metric
    	gap_ratio_2 = len(x)/x[len(x)-1] * 100
    	print('The completeness of this data using the weighted gap metric is: ' ,gap_ratio_2,'%')
    else:
    	list_new = reduce(lambda x, y: x*y, list) #multiple all the weights
    	gap_ratio_multiple_2 = (len(x)/x[len(x)-1] * 100) * list_new #multiple weights with % metric
    	print('The completeness of this data using the weighted gap metric is: ' ,round(gap_ratio_multiple_2,2),'%')

def gaps():
    gap_ratio(x)
    gap_percentage(x)
    weighted_gaps(x)
    print("")
    vote = input("To Go back to the main menu press: m (or press any random key to exit the program) \n ")
    if vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    gaps()
