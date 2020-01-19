import sys
import utm
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import time as t

if len(sys.argv) <= 3:
	csvFile = sys.argv[1]
	print ("csvFile ="+csvFile)
	plotfile = sys.argv[2]
	print ("plotfile ="+plotfile)

df = pd.read_csv(csvFile)
u=list(df)
s=0;
while(s<len(u)):
    if(u[s]=='latitude'or u[s]=="Latitude" or u[s]=='lat'):
        aj=u[s];
    if(u[s]=='Longitude'or u[s]=="longitude" or u[s]=='lon'):
        bh=u[s];
    s=s+1
    
coords = df.as_matrix(columns=[aj,bh])


kms_per_radian = 6371.0088
epsilon = 1.5 / kms_per_radian

#epsilon parameter is the max distance (1.5 km in this example) 
#that points can be from each other to be considered a cluster

#min_samples parameter is the minimum cluster size 
#everything else gets classified as noise
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

cluster_labels = db.labels_
num_clusters = len(set(cluster_labels))
clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)]) 
#'clusters' is pandas series object
print 'Number of clusters:'+str(num_clusters)
x=[];y=[]               
b=clusters
cm = plt.cm.get_cmap('jet')
xi=[];yi=[];dk=[];o=0;
for j in b:
    for i in j:
       xi.append(i[1])
       yi.append(i[0])
       dk.append(len(j))
    dr=len(j)
    if dr>o:
        o=dr
lon1=max(xi)
lon2=min(xi)
lat=0
zone1=utm.from_latlon(lat,lon1)
zone2=utm.from_latlon(lat,lon2) 
fig, ax = plt.subplots(figsize=(6,10))
fe=ax.scatter(xi,yi,c=dk,vmin=1,vmax=o,s=20,cmap=cm,label="go")
tfd=fe.get_array()
if (zone1[2]-zone2[2]==1):
    ax.set_title('Plot Spreads Within Zone number '+str(zone2[2])+" and Zone number "+str(zone1[2]))
elif(zone1[2]-zone2[2]>=2):
    ax.set_title("Plot Spreads from Zone Number "+str(zone2[2])+" To Zone Number "+str(zone1[2]))
else:
    ax.set_title('Plot present in Zone Number '+str(zone1[2]))
ax.set_xlabel('Longitude (West of Greenwich Meridian)')
ax.set_ylabel('Latitude (North of Equator)')
tr=plt.colorbar(fe)
#tr.ax.tick_params(direction='in', pad=0)
tr.ax.set_ylabel('number of points in the cluster')
plt.savefig(plotfile)



