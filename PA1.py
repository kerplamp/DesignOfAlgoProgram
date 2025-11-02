import math
import ast
import time
import matplotlib.pyplot as plt
import numpy as np

flightsFile = open("flights.txt")
flightsArray = []
for i, line in enumerate(flightsFile):
    flightsArray.append(ast.literal_eval(line))
# each line is a flight: 
#                                 0                 1                           2
#           cityFlightInfo = [otherCity, flightTimeToOtherCity (hours), flightCost (USD)]   - technically its (otherCity, flightTimeToOtherCity (hours), flightCost (USD)) but whatever
#           flight[i] is cityFlightInfo for city i



def merge(array1, array2, index):
    i = 0
    j = 0
    mergedList = []
    while i < len(array1) and j < len(array2):
        if array1[i][index] < array2[j][index]:
            mergedList.append(array1[i])
            i = i + 1
        else:
            mergedList.append(array2[j])
            j = j + 1
    if i == len(array1):
        mergedList.extend(array2[j:])
    else:
        mergedList.extend(array1[i:])
    return mergedList


#since we are passing an array (A) of arrays/lists (many A') and want to sort by some index in each A', we need an index variable
def mergeSort(array, index):
    halfArrayLen = math.floor(len(array)/2)
    if len(array) == 1:
        return array
    return merge(mergeSort(array[:halfArrayLen], index), mergeSort(array[halfArrayLen:], index), index)


#file setup
fileMergeByTime = open("TtimeMerSort.txt", "w")
fileMergeByCost = open("TcostMerSort.txt", "w")
runTimes = open("runtimes.txt", "w")

#plotting setup
fig = plt.figure()
plt.xlabel('City')
plt.ylabel('Time')
ax = fig.gca()

major_ticks = np.arange(0, 101, 5)
minor_ticks = np.arange(0, 101, 1)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='both')

x = []
y = []


#looping through flights
for i, line in enumerate(flightsArray):

    #merge stuff
    mergeByTime = mergeSort(line, 1)
    mergeByCost = mergeSort(line, 2)

    fileMergeByCost.write(str(mergeByCost) + "\n")

    startClockTimeMerge = time.perf_counter()
    fileMergeByTime.write(str(mergeByTime) + "\n")
    endClockTimeMerge = time.perf_counter()

    y.append(endClockTimeMerge-startClockTimeMerge)
    x.append(i+1)

    #bubble stuff


    bubbleRunTimePlaceholder = 0

    #both
    runTimes.write("(" + str(endClockTimeMerge-startClockTimeMerge) + ", " + str(bubbleRunTimePlaceholder) + ")\n")
    
    
#file closing
fileMergeByCost.close()
fileMergeByTime.close()
runTimes.close()

#plot 
plt.plot(x, y, label="Merge By Time")
plt.legend()
plt.show()