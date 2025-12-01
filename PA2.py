# CSC2400 Design of Algorithms - Travel Planner (Checkpoint 2)
# Authors: Dylan Myers, Jackson Young, Joyce Khamis
# Credit Statement: We used the internet to understand how to read files, how to measure clock-time, and how to plot graphs in Python.
# We did not receive any outside help from TAs or the instructor on this submission.

import math
import time
import matplotlib.pyplot as pyplot

citiesFile = open("cities.txt")
citiesArray = []
for i, line in enumerate(citiesFile):
    splitTxt = line.split()
    citiesArray.append([int(splitTxt[0]), float(splitTxt[1]), float(splitTxt[2])])

#outputs
bf_output = open("BF-Closest.txt", 'w')
dc_output= open("DC-Closest.txt", 'w')
runTimes = open("runtimes.txt", 'w')

#helper func
def euclidianDistance(coord1, coord2):
    xSqr = coord1[0] - coord2[0]
    xSqr = xSqr * xSqr

    ySqr = coord1[1] - coord2[1]
    ySqr = ySqr * ySqr

    dist = math.sqrt(xSqr + ySqr)

    return dist

#helper func
def sqr(x):
    return x*x

#re-using merge sort code from last checkpoint 
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



#Brute Force
def bruteForceClosest(cityArray, i):
    cityArray = cityArray[:i]
    minDist = math.inf
    closestCities = [0, 0]
    #we just go over each city and every city after it and compare to find the minimum
    for i in range(len(cityArray)):
        for j in range(i + 1, len(cityArray)):
            cityInfoLine1 = cityArray[i]
            cityInfoLine2 = cityArray[j]

            if cityInfoLine1[0] == cityInfoLine2[0]: continue
            curDist = euclidianDistance([cityInfoLine1[1], cityInfoLine1[2]], [cityInfoLine2[1], cityInfoLine2[2]])
            if curDist < minDist:
                minDist = curDist
                closestCities = [cityInfoLine1[0], cityInfoLine2[0]]
    return [closestCities, minDist]


#Divide and Conquer
def efficientClosestPair(cityArray):
    xSortedArray = mergeSort(cityArray, 1)
    ySortedArray = mergeSort(cityArray, 2)
    return efficientClosestPairRecurse(xSortedArray, ySortedArray)

def efficientClosestPairRecurse(xSortedArray, ySortedArray):
    #base case (since theres only 3, brute force is fine)
    if len(xSortedArray) <= 3:
        return bruteForceClosest(xSortedArray, len(xSortedArray))
    

    xFirstHalf = xSortedArray[:math.ceil(len(xSortedArray)/2)]
    xLastHalf = xSortedArray[math.ceil(len(xSortedArray)/2):]

    medianX = xFirstHalf[-1][1]

    #we pass a sorted array and pick from it instead of sorting xfirst and xlast by y (n vs 2nlogn)
    yRelevantFirstHalf = []
    yRelevantLastHalf = []
    for cityInfo in ySortedArray:
        if cityInfo[1] <= medianX:
            yRelevantFirstHalf.append(cityInfo)
        else:
            yRelevantLastHalf.append(cityInfo)

    #recurse
    firstClosest, firstHalfDist = efficientClosestPairRecurse(xFirstHalf, yRelevantFirstHalf)
    lastClosest, lastHalfDist = efficientClosestPairRecurse(xLastHalf, yRelevantLastHalf)

    #cant just use min() because we need to keep track of the closest cities too
    minDist = 0
    if firstHalfDist < lastHalfDist:
        minDist = firstHalfDist
        closestCities = firstClosest
    else:
        minDist = lastHalfDist
        closestCities = lastClosest
    minDistSqr = minDist*minDist

    #add all the points in the y sorted array that are closer to the median than our two current closest points
    # (we have to check other side of median incase theres a closer point, so we use these)
    stripArray = []
    for cityInfo in ySortedArray:
        if abs(cityInfo[1] - medianX) < minDist:
            stripArray.append(cityInfo)

    #i dont really fully understand the underlying logic, but some geometric law says the while loop will only run 7 times, so we have (n * O(1)) 
    for i in range(len(stripArray) - 1):
        k = i + 1
        while k <= len(stripArray) - 1 and sqr(stripArray[k][2] - stripArray[i][2]) < minDistSqr:
            yDistSqr = sqr(stripArray[k][2] - stripArray[i][2])
            xDistSqr = sqr(stripArray[k][1] - stripArray[i][1])

            currentDistSqr = xDistSqr + yDistSqr
            minDistSqr = min(xDistSqr + yDistSqr, minDistSqr)
            if currentDistSqr < minDistSqr:
                minDistSqr = currentDistSqr
                closestCities = [stripArray[k][0], stripArray[i][0]]
            k = k + 1
    return [closestCities, math.sqrt(minDistSqr)]

bf_times, dc_times = [], []
ind_values = list(range(50, 101)) # for graph

for i in ind_values:
    subCities = citiesArray[:i]

    # BF Timing
    startClockBF = time.perf_counter_ns()
    bfPair, bfDist = bruteForceClosest(subCities, i)
    endClockBF = time.perf_counter_ns()
    bfRuntime = endClockBF - startClockBF

    # D&C Timing
    startClockDC = time.perf_counter_ns()
    dcPair, dcDist = efficientClosestPair(subCities)
    endClockDC = time.perf_counter_ns()
    dcRuntime = endClockDC - startClockDC

    bf_times.append(bfRuntime)
    dc_times.append(dcRuntime)

    bf_output.write(f"{bfPair[0]} {bfPair[1]} {bfDist:0.6f}\n")
    dc_output.write(f"{dcPair[0]} {dcPair[1]} {dcDist:0.6f}\n")

    # Runtimes
    runTimes.write(f"({bfRuntime}, {dcRuntime})\n")

bf_output.close()
dc_output.close()
runTimes.close()


# Graph Plot (praying this works)
pyplot.figure(figsize=(10, 6))
pyplot.plot(ind_values, bf_times, label="Brute Force Time")
pyplot.plot(ind_values, dc_times, label="Divide & Conquer Time")
pyplot.xlabel("Number of Cities (i)")
pyplot.ylabel("Clock time (nanoseconds)")
pyplot.legend()
pyplot.show()