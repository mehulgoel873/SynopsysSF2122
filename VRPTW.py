# Python program to illustrate
# creating a data frame using CSV files

# import pandas module
import pandas as pd
from numpy import *
from sklearn.datasets import *
from sklearn.cluster import KMeans
import ORTools as VRP
import pygame
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import numpy

def main(_fileName):
    fileName = _fileName
    df = pd.read_csv(fileName + ".csv")
    df.head()

    #Elbow Method
    k_max = 10
    k_rng = range(0, k_max)
    sse = []
    for k in k_rng:
        #print("Got K Value for: " + str(k))
        #KMean Cluster happens here
        km = KMeans(n_clusters=k+1)
        cluster_predicted = km.fit_predict(df[['XCord', 'YCord']])
        sse.append(km.inertia_)
    m = (sse[k_max-1]-sse[0])/(k_max-1)
    a=-m
    b=1
    c=-sse[0]
    dist = []
    maxDist = 0
    maxDistIndex = -1
    for i in k_rng:
        dist.append(abs(a * i + b * sse[i] + c)/sqrt(a*a + b*b))
        if (dist[i] > maxDist):
            maxDist = dist[i]
            maxDistIndex = i
    '''# DISPLAY ELBOW CURVE
    #print(dist)
    #print("Best K Value is: " + str(maxDistIndex))
    plt.plot(k_rng,sse)
    plt.show()'''


    #CLUSTER
    k = maxDistIndex
    km = KMeans(n_clusters=k)
    cluster_predicted = km.fit_predict(df[['XCord', 'YCord']])
    df['cluster'] = cluster_predicted
    clusterRoutes = []
    times = []
    #SOLVE
    for i in range(0,k):
        route, total_time = VRP.main(df[df.cluster == i], 1, df[df.Customer == 1])
        times.append(total_time)
        clusterRoutes.append(route)
    #print("Finished")

    # screen = Output.main(df, clusterRoutes, times, k)
    # pygame.image.save(screen, "ImprovedOutput/" + fileName + ".png")
    return times

    '''#DISPLAY CLUSTERS
    colors = ['black', 'gray','brown','maroon','red','orangered', 'tan', 'orange','yellow', 'green','turquoise','cyan','blue', 'indigo', 'pink']
    for i in range(0, k):
        dfI = df[df.cluster == i]
        plt.scatter(dfI.XCord,dfI.YCord, color = colors[(i%15//3) + 5 * (i%3)])
    plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
    plt.xlabel('XCord')
    plt.ylabel('YCord')
    plt.legend()
    plt.show()'''