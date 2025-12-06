# CSC2400 Design of Algorithms - Travel Planner (Checkpoint 3)
# Authors: Dylan Myers, Jackson Young, Joyce Khamis
# Credit Statement: We used the internet to understand how to read files, how to measure clock-time, and how to plot graphs in Python.
# We did not receive any outside help from TAs or the instructor on this submission.

import math
import time
import matplotlib.pyplot as pyplot
import ast

citiesFile = open("roundtrip_costs.txt")
citiesArray = []
for i, line in enumerate(citiesFile):
    citiesArray.append(ast.literal_eval(line))



'''
Theory Part

Assuming I am reading the question right (I have re-read it 8 times now). We can find the solution by first simply sorting the trips by travel cost (Or by the given definitions, sorting A) and then
iterating through the list, saving the total travel cost for all cities before city j. So TotalCostArray[j] = (TravelCostArray[j] + TotalCostArray[j - 1]). [We could also just overwrite into A, which is what I will be doing to save space]
                                                                                                                    ^- A
We can then either stop iterating through the list once the total cost exceeds our budget (B), or completely iterate and use a binary search lookup on a completed travel cost array.
The first option will be faster for checking 1 budget (B), but if we want to check multiple budgets (B) from the same city, the second option will be faster.

I will be the first option as the instructions only state a budget of 5000

We could also simply use a variable to store the total cost up to right before we go over budget, but I am assuming we are expected to demonstrate dynamic programming with arrays so I will be using the array method.


Input: An array (A) with the round trip costs from a city, a budget B
Output: Total amount of cities we can visit given budget B

findMaxCities(A, B)
    A = sortByCost(A)   -    nlogn if we use mergesort

    if A[0] > B   - constant time
        return 0

    citiesVisited = 0 
    totalCosts = [A[0]]  - space complexity of O(n)       (using a single variable would make it constant)
    i = 0
    while i < len(A):          - O(n) 
        
        if totalCosts[i - 1] + A[i] < B  - constant time
            totalCosts[i] = totalCosts[i - 1] + A[i]
            citiesVisited = citiesVisited + 1
            i = i + 1
        else
            break
        
    return citiesVisited
    
nlogn supersedes other runtimes, so we have a runtime of nlogn
        
'''

#re-using merge sort code from last checkpoint again
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

def mergeSort(array, index):
    halfArrayLen = math.floor(len(array)/2)
    if len(array) == 1:
        return array
    return merge(mergeSort(array[:halfArrayLen], index), mergeSort(array[halfArrayLen:], index), index)





#changed the function to also save an array of cities visited for the extra credit
def MaxCitiesFromBudget(cityArray, budget):
    sortedCities = mergeSort(cityArray, 1)

    if sortedCities[0][1] > budget:
        return 0
    
    visitedCities = []
    totalCosts = [sortedCities[0][1]]
    i = 1
    while i < len(sortedCities):

        if sortedCities[i][1] + totalCosts[i - 1] > budget:
            break
        else:
            totalCosts.append(sortedCities[i][1] + totalCosts[i - 1])
            visitedCities.append(sortedCities[i])
            i = i + 1
            

    return visitedCities

tripFile = open("trip_nums.txt", "w")
destinationsFile = open("destinations.txt", "w")
for city in citiesArray:
    visitedCities = MaxCitiesFromBudget(city, 5000)
    tripFile.write(str(len(visitedCities)) + "\n")
    destinationsFile.write(str(visitedCities) + "\n")



