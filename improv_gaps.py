#this code contains all the improvement methods for noise
import glob
import itertools
import time as time2
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from statsmodels.tsa.arima_model import ARMA
from sklearn import neighbors
from improv_noise import func

height = 189.2785
path = "GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_2/channel 1 20140718 *.dts"
x_old, y_old, target_next, target_prev, initialtime = func(height,path) #call to func function from the impro_noise file.
x = []
for i,val in enumerate(x_old):
    x.append(val)

y = []
for i,val in enumerate(y_old):
    y.append(val)

c = 1
#this block of cude removes some values from a complete data set so that i have something to compare the filled gaps with.
y_missing = []
for i,val in enumerate(y_old):
    if 40 < i < 50 or 60 < i < 65:
        y_missing.append(val)

del x[40:50]
del x[60:65]
del y[40:50]
del y[60:65]

#the following code is for finding the gaps and filling them with predicted missing x values so if gap is between 80 and 83, this will fill it then it would become 80,81,82,83
missing_vals = []
missing_vals_start = []
list = []
for i, val in enumerate(x):
    if i != len(x)-1:
        if x[i+1]-x[i] > 1.2:
            b = x[i+1]
            missing = np.arange(val, b, 1)
            missing_vals_start.append(i)
            value = missing[len(missing)-1]
            if b - value < 0.6:
                missing = np.delete(missing, len(missing)-1)
            missing = np.delete(missing, 0)
            list.append(len(missing))
            for i, val in enumerate(missing):
                missing_vals.append(round(missing[i],1))
#print(missing_vals) #x  all the missing x values

def x_new():
    #returns a list of complete x values by merging the original list with the missing x values found in the piece of code above
	#after merging, this list is then sorted to give a sorted x list containing no missing values
    missing = []
    for i, val in enumerate(missing_vals):
        missing.append(val)
    for j,val in enumerate(x):
    	missing.append(round(x[j],1))
    x_new = sorted(missing) #now xnew contains all the values (intial values as well as the missing ones)
    print("New x list without gaps")
    print(x_new)

def difference(l1,l2,method):
	#calculates the absolute difference between the original values that were removed from the list and the missing values filled with the technique from which the function is called
	#an average is then taken of all the differences.
	method = method
	c = 0
	sum = 0
	for j,i in enumerate(l1):
		diff = abs(l2[j] - i)
		sum += diff
		c += 1
		absreturn = sum / c
	print('The average distance between original gap values and predicted gap values using',method ,'is:' ,round(absreturn,3))

def linear_gaps(x,y):
	#using linear regression to fill gaps
    linear = np.polyfit(x, y, 1)
    line = np.poly1d(linear)

    new_y = []
    for i, val in enumerate(missing_vals):
        new_y.append(line.c[0]*missing_vals[i] + line.c[1]) #getting the correponding y values using the predicted missing x values

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    scatter = plt.scatter(x,y) # points
    plt.plot(x,line(x), color='orange') # line
    gaps = plt.scatter(missing_vals,new_y, color='purple')
    plt.legend((scatter,gaps), ('Original points', 'Filled gaps with linear reg'), loc='best')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

	#call to the difference function
    method = "Linear regression"
    difference(y_missing, new_y,method)

	#below is the new list x_new which contains all the original x values including the predicted missing x values.
    x_new()

    #below is the new list of y values which contains all the original y values including the predicted missing y values filled using linear regression
    y_new = []
    length = 0
    linear_y = []
    for i,val in enumerate(y):
        linear_y.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            var = line.c[0]*missing_vals[j+length] + line.c[1]
            y_new.append(round(var,3))
        linear_y[val+length+c:list[i]+1] = y_new
        length = list[i] + length
        y_new = []
    print("New y list without gaps")
    print(linear_y)

def cubic_gaps(x,y):
	#fillings gaps using cubic parabolas
    cubic = np.polyfit(x, y, 3)
    curve = np.poly1d(cubic)

    new_y = []
    for i, val in enumerate(missing_vals): #getting the correponding y values using the predicted missing x values
    	new_y.append(curve.c[0]*missing_vals[i]*missing_vals[i]*missing_vals[i] + curve.c[1]*missing_vals[i]*missing_vals[i] + curve.c[2]*missing_vals[i] + curve.c[3])

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    scatter = plt.scatter(x,y) # points
    plt.plot(x,curve(x), color='orange') # curve
    gaps = plt.scatter(missing_vals,new_y, color='purple')
    plt.legend((scatter,gaps), ('Original points', 'Filled gaps with cubic parabola'), loc='best')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

	#call to the difference function
    method = "Cubic parabolas"
    difference(y_missing, new_y,method)

    #below is the new list x_new which contains all the original x values including the predicted missingn x values.
    x_new()

    #below is the new list of y values  which contains all the original values including the predicted missing y values obtained from the cubic parabla curve
    y_new = []
    length = 0
    cubic_y = []
    for i,val in enumerate(y):
        cubic_y.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            var = curve.c[0]*missing_vals[j+length]*missing_vals[j+length]*missing_vals[j+length] + curve.c[1]*missing_vals[j+length]*missing_vals[j+length] + curve.c[2]*missing_vals[j+length] + curve.c[3]
            y_new.append(round(var,3))
        cubic_y[val+length+c:list[i]+1] = y_new
        length = list[i] + length
        y_new = []
    print("New y list without gaps")
    print(cubic_y)

def spline_gaps(x,y):
	#filling gaps using cubic splines
    s = interpolate.UnivariateSpline(x, y, s=5)
    xnew = np.arange(min(x), abs(max(x)-min(x)), 0.1)
    ynew = s(xnew)

    newarray2 = []
    for j in missing_vals: #getting the correponding y values using the predicted missing x values
    	newarray2.append([j, s(j)])
    newarray2 = np.array(newarray2)
    x3 = newarray2[:,0]
    y3 = newarray2[:,1]

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.plot(x, y, 'x', xnew, ynew)
    gaps = plt.scatter(missing_vals,y3, color='purple')
    plt.legend(['Original', 'Filled gaps with Splines'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

	#call to the difference function
    method = "Cubic splines"
    difference(y_missing, y3,method)

    #below is the new list x_new which contains all the original x values including the predicted x missing values.
    x_new()

    #below is the new list of y values which contains all the original values including the predicted missing y values obtained from the cubic splines
    y_new = []
    length = 0
    spline_y = []
    for i,val in enumerate(y):
        spline_y.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            y_new.append(round(y3[j+length],3))
        spline_y[val+length+c:list[i]+1] = y_new
        length = list[i] + length
        y_new = []
    print("New y list without gaps")
    print(spline_y)

def mean_imputation():
	#mean imputation. Take mean of the availalabe data and impute that into missing spaces.
    length = 0
    mean_list = []
    mean_count = []
    list_mean = []
    for i,val in enumerate(y):
        list_mean.append(val)
    mean = round(np.mean(list_mean),3)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            mean_list.append(mean)
            mean_count.append(mean)
        list_mean[val+length+c:list[i]+1] = mean_list
        length = list[i] + length
        mean_list = []

	#call to the difference function
    method = "Mean imputation"
    difference(y_missing, mean_count,method)

    plt.scatter(x,y)
    plt.scatter(missing_vals,mean_count,color='yellow')
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.legend(['Original', 'Filled gaps with mean imputation'])
    plt.show()

    #below is the new list x_new which contains all the original x values including the predicted missing x values
    x_new()

    #below is the new list of y values which contains all the original values including the predicted missing y values obtained from mean imputation
    print("New y list without gaps")
    print(list_mean)

def spline_interpolate():
    #this is similar to the previous spline method but in this, it takes the two points between whcih a gap resides and then gets the y values between them using equation of the spline
    #so the previous spline does no go through each and every point but this one does
    s = interpolate.interp1d(x, y)
    xnew = np.arange(min(x), abs(max(x)-min(x)), 0.06)
    ynew = s(xnew)

    newarray2 = []
    for j in missing_vals:
        newarray2.append(s(j)) #gets corresponding y values for predicted missing x
    newarray2 = np.array(newarray2)

    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.plot(x, y, 'x', xnew, ynew)
    gaps = plt.scatter(missing_vals,newarray2, color='purple')
    plt.legend(['Original', 'Cubic Spline','Gaps'])
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    #call to the difference function
    method = "the Cubic spline interpolation method"
    difference(y_missing, newarray2,method)

    #below is the new list x_new which contains all the original x values including the predicted x missing values.
    x_new()

    #below is the new list of y which contains all the original values including the predicted missing values filled in using splines interpolation method
    c = 1
    y_new = []
    length = 0
    inter_y = []
    for i,val in enumerate(y):
        inter_y.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            var = round(newarray2[j+length],3)
            y_new.append(var)
        inter_y[val+length+c:list[i]+1] = y_new
        length = list[i] + length
        y_new = []
    print(inter_y)

def arma():
#autoregressive moving average model. This is a machine learning model used to predict future data based on model built from past data
#model is trained on data before the gap and then predicted values used to fill the gaps
#model runs in loops  so for gap 1, it uses all the data before it as past and fills up. Then for gap 2, it considers all the past data (excluding predicted data that had been filled in) and then fills data. Then gap 3 etc..
    final_list = []
    length = 0
    predicted_vals = []
    list_y = []
    for i in y:
        list_y.append(i)
    for i,val in enumerate(missing_vals_start):
        ynew = y[:val+1]
        # fit model
        model = ARMA(ynew, order=(2, 1))
        model_fit = model.fit(disp=False)
        # make prediction for the missing y values
        prediction = model_fit.predict(len(ynew), len(ynew) + list[i] - 1)
        #appending the predicted data into the interval in y within which the gap resides.
        list_y[val+length+c:list[i]+1] = prediction
        length = list[i] + length
        for j,val in enumerate(prediction):
            predicted_vals.append(val)
    for i,val in enumerate(list_y):
        final_list.append(round(val,3))

    plt.scatter(missing_vals,predicted_vals,color='orange')
    plt.scatter(x,y)
    plt.legend(['Original', 'Filled gaps with ARMA'])
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    #call to the difference function
    method = "the Autoregressive moving average model"
    difference(y_missing, predicted_vals, method)

    #below is the new list x_new which contains all the original x values including the predicted missing values
    x_new()

	#below is the new list of y values which contains all the original values including the predicted missing y values obtained from ARMA
    print("New y list without gaps")
    print(final_list)

def k_nn(x,y):
	#filling gaps using two k-nearest neighbors methods: distance and uniform
	#parts of code gotten from https://scikit-learn.org/stable/auto_examples/neighbors/plot_regression.html#sphx-glr-auto-examples-neighbors-plot-regression-py
    x = [[i] for i in x] #converting x to list of lists
    T = [[i] for i in missing_vals] #converting missing v values into list of lists
    n_neighbors = 5 #checks the 5 nearest neighbours
    list_uniform = []
    list_distance = []

    for i, weights in enumerate(['uniform', 'distance']):
        knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
        y_ = knn.fit(x, y).predict(T) #predict y values using missing x values
        if i == 0:
            for i,val in enumerate(y_):
                list_uniform.append(round((val),3)) #add predicted y values using uniform method to new lsit
        else:
            for i,val in enumerate(y_):
                list_distance.append(round((val),3)) #add predicted y values using distance method to new list

	#below makes a new list of y values which contains all the original values including the predicted missing y values obtained from k-nn uniform
    length = 0
    uniform = []
    distance = []
    knn_list_uniform = []
    knn_list_distance = []
    for i,val in enumerate(y):
        knn_list_uniform.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            uniform.append(list_uniform[j+length])
        knn_list_uniform[val+length+c:list[i]+1] = uniform
        length = list[i] + length
        uniform = []

    plt.scatter(missing_vals,list_uniform,color='orange')
    plt.scatter(x,y)
    plt.legend(['Original', 'Filled gaps with K-nn Uniform'])
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    print("New y list without gaps using k-nn uniform")
    print(knn_list_uniform) #returns a complete list of y values containing all the original y values as well as the predictedmissing values filled with k-nn uniform
    method = "k-nn uniform method"
    difference(y_missing, list_uniform, method)

	#below makes a new list of y values which contains all the original values including the predicted missing y values obtained from k-nn distance
    length = 0
    for i,val in enumerate(y):
        knn_list_distance.append(val)
    for i,val in enumerate(missing_vals_start):
        for j in range(list[i]):
            distance.append(list_distance[j+length])
        knn_list_distance[val+length+c:list[i]+1] = distance
        length = list[i] + length
        distance = []

    plt.scatter(missing_vals,list_distance,color='orange')
    plt.scatter(x,y)
    plt.legend(['Original', 'Filled gaps with K-nn Distance'])
    plt.title('Readings at:'+ "" + str(height) + "" + 'm')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Temp (celsius)")
    plt.show()

    print("New y list without gaps using k-nn distance ")
    print(knn_list_distance) #returns a complete list of y values containing all the original y values as well as the predicted missing values filled with k-nn distance
    method ="knn distance method"
    difference(y_missing, list_distance,method)

    #below is the new list x_new which contains all the original x values including the predicted missing values
    x_new()

def inputUser2():
    method = input("Which gap improvement method would you like to visualize? You options are: \n 1) Linear regression \n 2) Cubic parabola \n 3) Cubic Splines \n 4) Splines interpolation \n 5) Mean imputation \n 6) Autoregressive moving average \n 7) K nearest neighbors \n 8) Exit \n Please enter the number of your choice: \n ")
    if method == "1":
        linear_gaps(x,y) #display linear
    elif method == "2":
        cubic_gaps(x,y) #display cubic
    elif method == "3":
        spline_gaps(x,y)#display cubic_spline
    elif method == "5":
        mean_imputation()
    elif method == "6":
        arma()
    elif method == "7":
    	k_nn(x,y)
    elif method =="4":
        spline_interpolate()
    elif method == "8":
        exit()
    else:
        print("You have entered an invalid number. Please try again")
        print("")
        inputUser2()
    vote = input("To explore a different gap method press: 0, To return back to the main menu press: m, To exit the program press any key \n")
    if vote == "0":
        inputUser2()
    elif vote == "m":
        return
    else:
        exit()

if __name__ == '__main__':
    inputUser2()
