#the following displays a heapmap of the chosen dataset/folder
#the x-asix is time, y-axis are all the 2000+ depths and the colour/z are the temperature value
#this code has been developd by Jacob Gelling studying at University of aberdeen student ID:51768261

import glob, itertools
import time as time2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def heatmap():
	matrix = {}
	count = 0
	for datafile in glob.glob("GG_DTS_ASCII/Post-B_G01/DTS_G1_BLEED_1/channel 1 20140718 *.dts"):
		count = count + 1
		with open(datafile) as f:
			time = ''
			for line in itertools.islice(f, 8, None):
				time = line.split("TIMESTAMP: ")[1].rstrip()
				time = time2.strptime(time, "%Y/%m/%d %H:%M:%S")
				break
			for line in itertools.islice(f, 4, None):
				splitLine = line.split("\t")
				if float(splitLine[0]) in matrix: #adding temp and time values for each depth in a matrix
					matrix[float(splitLine[0])].append({'temp': float(splitLine[1]), 'time': time})
				else:
					matrix[float(splitLine[0])] = [{'temp': float(splitLine[1]), 'time': time}]


	z = []
	for k in matrix:
		for j in matrix[k]:
			z.append(j['temp'])

	min_z = min(z) #for colours when plotted

	x = []
	y = []
	z = []
	count = 0
	original_z = []
	#reteiving time and temp values for each depth and adding to new array
	#converting time from time (example :17:15) to minutes and initilizing it
	origtime = 0
	for k in matrix:
		z_row = []
		for j in matrix[k]:
			if origtime == 0:
				origtime = time2.mktime(j['time'])
			x.append((time2.mktime(j['time']) - origtime) / 60) #converting to minutes
			z_row.append(j['temp'])
			original_z.append(j['temp'])

			y.append(k)
		z.append(z_row)
	z = np.array(z)

	#create matrix based on time. so for every time slice, get all depths and corresponding temperatures
	timematrix = {}
	for indx, valx in enumerate(x):
		if valx in timematrix:
			timematrix[valx].append({'temp': original_z[indx], 'depth': y[indx]})
		else:
			timematrix[valx] = [{'temp': original_z[indx], 'depth': y[indx]}]

	fig, ax = plt.subplots()
	norm = colors.Normalize(vmin=min_z,vmax=35) #normalizing colours for heat map

	count = 0
	for k in timematrix:
		next = False
		for b in timematrix:
			if next == True:
				next = b
				break
			if b == k:
				next = True
		if next == True:
			next = k + 1
		if next - k > 1.5: #if the difference between one time slice and the next is greater than 1.5 and show a gap on the heat map
			next = k + 1
		x = []
		z = []
		z_row = []
		y = []
		min_depth = timematrix[k][0]['depth']
		max_depth = timematrix[k][0]['depth']
		for j in timematrix[k]:
			z_row.append([j['temp']])
			x.append(k)
			y.append(j['depth'])
			if j['depth'] > max_depth:
				max_depth = j['depth']
			if j['depth'] < min_depth:
				min_depth = j['depth']
		z = z_row
		z = np.array(z)
		pcm = ax.pcolorfast((k, next), (min_depth, max_depth), z,
	                   norm=norm,
	                   cmap='plasma')
		count += 1

	plt.xlabel("Time")
	plt.ylabel("Depth")
	plt.show()

if __name__ == '__main__':
    heatmap()
