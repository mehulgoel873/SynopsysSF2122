import time
import VRPTW
import BaseCase
import csv

def maxTime(times):
    maxTime = 0
    for clusterTime in times:
        maxTime = max(maxTime, clusterTime)
    return maxTime

solveTimesNew = []
solveTimesOld = []
timeTakenNew = []
timeTakenOld = []
typesOfData = ["R", "C", "RC"]
fileNames = []
for type in typesOfData:
    #Add Other Variations of Data Here
    fileName = type + "101"
    fileNames.append(fileName)

    startTime = time.time()
    times = VRPTW.main(fileName)
    solveTimesNew.append(time.time() - startTime)
    timeTakenNew.append(maxTime(times))

    startTime = time.time()
    times = BaseCase.main(fileName)
    solveTimesOld.append(time.time() - startTime)
    timeTakenOld.append(maxTime(times))
    print("Finished: " + fileName)

with open('results.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(['FileName', 'SolveTime', 'MaxTime'])
    for i in range(len(times)):
        writer.writerow(fileNames[i], )


    # write the data
print("Finished")
