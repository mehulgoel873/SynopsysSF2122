import time
from tracemalloc import start
import VRPTW
import BaseCase

def maxTime(times):
    maxTime = 0
    for cluster in times:
        clusterTime = 0
        for time in cluster:
            clusterTime += time
        maxTime = max(maxTime, clusterTime)
    return maxTime

solveTimesNew = []
solveTimesOld = []
timeTakenNew = []
timeTakenOld = []
typesOfData = ["R", "C", "RC"]
for type in typesOfData:
    #Add Other Variations of Data Here
    fileName = type + "101"

    startTime = time.time()
    times = VRPTW.main(fileName)
    solveTimesNew.append(time.time() - startTime)
    timeTakenNew.append(maxTime(times))

    startTime = time.time()
    times = BaseCase.main(fileName)
    solveTimesOld.append(time.time() - startTime)
    timeTakenOld.append(maxTime(times))
print("Finished")
