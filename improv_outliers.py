import glob
import itertools
import time as time2
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, signal
from sklearn.cluster import KMeans
from improv_noise import func

height = 189.2785 #choose the height/depth for which you want to retrieve all the temperature vs time values for
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts"
x, y, target_prev, target_next, initialtime = func(height,path) #to break the output of the function into two distinct/independent lists.
thersold = 0.5 #sets thresold values for all methods so that they can be compared on smilar grounds

def new_list_generator(x,y,outliers):
    #this method removes outliers and returns new x and y lists without them
    for i,val in enumerate(y):
        if val in outliers:
            y.remove(val)
            x.remove(x[i])
    print('The new x list without outliers is:')
    print(x)
    print('The new y list without outliers is:')
    print(y)
    print("")

def histogram(y):
    #histograms can also be used to detect outliers.
    #the bar with the lowest height on the very left is a oulier in this case
    histogram = plt.hist(y, bins='auto')  # arguments are passed to np.histogram
    plt.show()
    outliers = []
    outliers_new = []
    for i,val in enumerate(histogram[0]):
        if val == 1:
            outliers.append(i) #choosing bins which only have 1 value as these will be outliers
            #because outliers are not repeating values, they only occur once
    for i,val in enumerate(histogram[1]):
        if i in outliers:
            outliers_new.append(val)
    print("")
    print('The outliers in this dataset using Histograms are:',outliers_new)
    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,outliers_new)

def k_means_clustering():
    #bits of code taken from here https://jakevdp.github.io/PythonDataScienceHandbook/05.11-k-means.html
    X = [list(a) for a in zip(x, y)] #creating a 2D list containing x and y cooridnates
    kmeans = KMeans(n_clusters=4) #defining that i want 4 clusters of our data
    kmeans.fit(X) #fitting the data
    y_kmeans = kmeans.predict(X) #predicitng which y points belong to which clusters and how many. All Y points belonging to a cluster have the same numeric values
    y_kmeans = y_kmeans.tolist() #converting numpy array to list for later use
    centers = kmeans.cluster_centers_ #centers gives the x and y coordinates of the center points of each cluster
    length = [] # this list will contain the number of ys belinnging to each cluster.
    count = 0
    #the loop below extracts the number of y points that belong to each cluster
    for i,val in enumerate(y_kmeans):
        if i != len(y_kmeans)-1:
            if val == y_kmeans[i+1]:
                count = count + 1
            else:
                length.append(count+1)
                count = 0
        else:
            length.append(count+1)

    #below gets the cumulative sum of the elementsof the list in the loop above
    length_new = []
    total  = 0
    for i,val in enumerate(length):
        total = val + total
        length_new.append(total)

    centers_new = sorted(centers, key = lambda x: x[0]) #sorts centers

    #loop below is how outliers are detected
    #checks if the distance between each y point (in a particular cluster) and the center point of that cluster
    #is greater than the thersold. iF yes, then that is an outlier
    start = 0
    c = 0
    a = 0
    outliers_y = []
    for z, value in enumerate(length_new):
        ynew = y[start:value]
        for j,val in enumerate(ynew):
            if abs(val- centers_new[c][1]) > thersold:
                outliers_y.append(val) # for plotting purposes
        c =  c  + 1
        if  a != (len(length_new)-1):
            start = length_new[a]
            a = a + 1
    print("")
    print('The outlier values using k-means clustering are', outliers_y)

    outliers_x = []
    for i,val in enumerate(y):
        if val in outliers_y:
            outliers_x.append(x[i]) #gets the corresponding x co-ordinate for that outlier y value so that i can plot it

    #plotting original points. the colour groups the points by the cluster they belong to
    original_points = plt.scatter(x,y, c=y_kmeans, s=40, cmap='viridis')
    plt.scatter(outliers_x, outliers_y, c='black') #outliers are plotted as black circles
    outliers = plt.scatter(outliers_x, outliers_y, s=120, facecolors='none', edgecolors='r') #red ring around outlier points
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5) #plots center points of the clusters
    plt.legend((original_points, outliers), ('Original points', 'Outliers'), loc='best')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.show()

    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,outliers_y)

def iqr(y):
    #finding outliers using the inter qurtile range
    q1 = np.percentile(y,25)
    q3 = np.percentile(y,75)
    list_outliers_x = []
    list_outliers_y = []
    iqr = q3 - q1 #inter quartile range is third quartile - first quartile
    for i, val in enumerate(y):
        if val  < q1 - (1.5 * iqr) or val > q3 + (1.5 * iqr): #multiplied by 1.5 because thats used in many places to detect outliers
            list_outliers_y.append(val) #appending y values of outliers
            list_outliers_x.append(x[i]) #appending corresponding x values of those y values

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.scatter(list_outliers_x,list_outliers_y, color='red')
    plt.legend(['Original points', 'Outliers'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    print('The outlier values using IQR are', list_outliers_y)

    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,list_outliers_y)

def interval_outliers():

    #the following code has been done in collbaoration with Jacob Gelling studying at University of aberdeen student ID:51768261
    outliers_x = []
    outliers_y = []
    interval = 5 #5min intervals
    #mean is taken at every 5mins intervals
    div = int(len(x) / interval)
    for i in range(0, interval):
        if i == interval - 1:
            interval += len(x) - (i*div+div)
        divsum = 0
        for j in range(i*div, i*div+div):
            divsum += y[j]
        average = divsum / div
        #for each mean, if value lie outsie +-thersold of that mean then they are considered as potential outliers
        for j in range(i*div, i*div+div):
            if y[j] >= average + thersold or y[j] <= average - thersold:
                is_outlier = False
                outlier_match_band = 0.05
                # checking values obtined from this height with previous height and next height to make sure that only outliers are removed nd not systamatic noise/erros.
                #this is neccesary because desired value of temperature is not provided. If it was provided then you can just do +_thersold to find outliers.
                for key,k in enumerate(target_prev):
                    if(((time2.mktime(target_prev[key]['time']) - initialtime) / 60) == x[j]) and (target_prev[key]['temp'] >= y[j] + outlier_match_band or target_prev[key]['temp'] <= y[j] - outlier_match_band) and (((time2.mktime(target_next[key]['time']) - initialtime) / 60) == x[j]) and (target_next[key]['temp'] >= y[j] + outlier_match_band or target_next[key]['temp'] <= y[j] - outlier_match_band):
                        is_outlier = True
                        break
                if is_outlier == True:
                    outliers_y.append(y[j]) #append y value of outlirs
                    outliers_x.append(x[j]) #appends corresponding x value
    #plot of original values and outliers
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.scatter(outliers_x, outliers_y, color='red')
    plt.legend(['Original points', 'Outliers'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()
    print("")
    print('The outlier values using mean intervals outlier method are', outliers_y)

    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,outliers_y)

def moving_precision_checker(y):
    #the following function removes outlier with the help of precision dimension
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
            #So if you are comparing j with 5 values. if j is greater than lower than more than 3 of these values, only then its considered an outlier.
            #if we set limit to 1 then manyyyy values will return as outliers because data set has many flacuations/noist values
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
    print("")
    print('The outliers using the moving precision method are', list)

    #plot of original values and outliers
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.scatter(list_x, list, color='red')
    plt.legend(['Original points', 'Outliers'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,list)


def two_sided_median_method(x,y):
    #twp-sided median method
    #for each value in y, find neighbourhood of values y - size to left and y + size to the right,
    #calculate the median of the neighbourhood and then compare y with the median.
    #if absolute distance of y - median is greater than the thersold, then that value is considered an outlier
    list_values = []
    size = 5
    outliers = []
    outliers_x = []
    c = 0
    for i in range(0, size):
        for j in range(0, size+size+1): #for first set of values, only consider neighbourhood to the right
            list_values.append(y[i+j])
        del list_values[c]
        list_values = sorted(list_values)
        median = np.median(list_values)
        if abs(y[i] - median) > thersold:
            outliers.append(y[i])
            outliers_x.append(x[i])
        list_values = []
        c = c + 1
    for i in range(size, len(x)-size): #for all other values, consider  neighbourhood to the right and left
        for j in range(-size, size+1):
            list_values.append(y[i+j])
        del list_values[5]
        list_values = sorted(list_values)
        median = np.median(list_values)
        if abs(y[i] - median) > thersold:
            outliers.append(y[i])
            outliers_x.append(x[i])
        list_values = []
    for i in range(len(x)-size, len(x)): #for last set of values, only consider neighbourhood to the left
        for j in range(-(size+size+1), 0):
            list_values.append(y[i+j])
        list_values.pop()
        list_values = sorted(list_values)
        median = np.median(list_values)
        if abs(y[i] - median) > thersold:
            outliers.append(y[i])
            outliers_x.append(x[i])
        list_values = []
    print("")
    print('The outliers using the two-sided median method are', outliers)

    #plot of original values and outliers
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.scatter(x,y) # original points
    plt.scatter(outliers_x, outliers, color='red')
    plt.legend(['Original points', 'Outliers'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    #creating new x and y which do not contain outliers
    x_new = []
    for i,val in enumerate(x):
        x_new.append(round(val,3))
    y_new = []
    for i,val in enumerate(y):
        y_new.append(round(val,3))
    #call to method which removes outliers and outputs list without outliers
    new_list_generator(x_new,y_new,outliers)

def inputUser3():
    method = input("Which outlier detection method would you like to visualize? You options are: \n 1) Histogram \n 2) K-means clustering \n 3) Interquartile range \n 4) Mean interval outliers method  \n 5) Moving precision method \n 6) Two-sided median method \n 7) Exit \n Please enter the number of your choice: \n ")
    if method == "1":
        histogram(y)
    elif method == "2":
        k_means_clustering()
    elif method == "3":
        iqr(y)
    elif method == "4":
        interval_outliers()
    elif method == "5":
        moving_precision_checker(y)
    elif method == "6":
    	two_sided_median_method(x,y)
    elif method == "7":
        exit()
    else:
        print("You have entered an invalid number. Please try again")
        print("")
        inputUser3()
    vote = input("To explore a different outlier method press: 0, To return back to the main menu press: m, To exit the program press any key \n")
    if vote == "0":
        inputUser3()
    elif vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    inputUser3()
