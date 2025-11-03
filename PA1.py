# CSC2400 Design of Algorithms - Project Assignment 1 (Travel Planner)
# Authors: Dylan Myers, Jackson Young, Joyce Khamis
# Credit Statement: We did not receive any outside help on this submission.

import math
import ast
import time
import matplotlib.pyplot as plt

flightsFile = open("flights.txt")
flightsArray = []
for i, line in enumerate(flightsFile):
    flightsArray.append(ast.literal_eval(line))
# each line is a flight: 
#                                 0                 1                           2
#           cityFlightInfo = [otherCity, flightTimeToOtherCity (hours), flightCost (USD)]   - technically its (otherCity, flightTimeToOtherCity (hours), flightCost (USD)) but whatever
#           flight[i] is cityFlightInfo for city i


# Merge Sort
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

# Bubble Sort
def bubble(array, index):
    for i in range(len(array)):
        swapped = False

        for j in range(len(array)-1):
            if array[j][index] > array[j+1][index]:
                array[j], array[j+1] = array[j+1], array[j]
                swapped = True

        if swapped == False:
            break

def bubbleSort(array, index):
    array_copy = array.copy()
    bubble(array_copy, index)
    return array_copy

fileBubbleByTime = open("TtimeBubSort.txt", "w")
fileBubbleByCost = open("TcostBubSort.txt", "w")

for i, line in enumerate(flightsArray):
    fileBubbleByTime.write(str(bubbleSort(line, 1)) + "\n")
    fileBubbleByCost.write(str(bubbleSort(line, 2)) + "\n")
    pass

