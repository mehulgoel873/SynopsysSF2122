# Python program to illustrate
# creating a data frame using CSV files

# import pandas module
import pandas as pd
from numpy import *
from sklearn.datasets import *
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import numpy
df = pd.read_csv("C101.csv")
df.head()

#Elbow Method
k_rng = range(1, 100)
sse = []
for k in k_rng:
    print("Got K Value for: " + str(k))
    km = KMeans(n_clusters=k)
    cluster_predicted = km.fit_predict(df[['XCord', 'YCord']])
    sse.append(km.inertia_)

print(sse)
plt.plot(k_rng,sse)
plt.show()



# #Clustering Code
# km = KMeans(n_clusters=3)
# cluster_predicted = km.fit_predict(df[['XCord', 'YCord']])
# df['cluster'] = cluster_predicted
# df1 = df[df.cluster==0]
# df2 = df[df.cluster==1]
# df3 = df[df.cluster==2]
#
# #Displaying Clusters
# plt.scatter(df1.XCord,df1['YCord'],color='green')
# plt.scatter(df2.XCord,df2['YCord'],color='red')
# plt.scatter(df3.XCord,df3['YCord'],color='black')
# plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
# plt.xlabel('XCord')
# plt.ylabel('YCord')
# plt.legend()
# plt.show()