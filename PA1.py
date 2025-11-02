import math
import ast
import time

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



fileMergeByTime = open("TtimeMerSort.txt", "w")
fileMergeByCost = open("TcostMerSort.txt", "w")

for i, line in enumerate(flightsArray):
    fileMergeByTime.write(str(mergeSort(line, 1)) + "\n")
    fileMergeByCost.write(str(mergeSort(line, 2)) + "\n")
    pass