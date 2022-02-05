# -*- coding: utf-8 -*-
import zipfile
import matplotlib.pyplot as plt

import os
import csv

import config
import support_classes.data_manager as data_manager

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#- INPUT ----------------------------------------------------------------------
input_data = "%s\\_users_info\\course_vision" %(config.PATH_OUTPUT)

#-- data manager: gestiore dei dati
dm = data_manager.Data_manager()
dm.load_data()
#------------------------------------------------------------------------------
n_clust = 3

for id_course in dm.get_courses():
    print("\n%s %s:" %(id_course, dm.get_course_name(id_course)))
    
    #- UTENTI -----------------------------------------------------------------
    users = list()
    users_info = dict()
    
    file_name = "%s\\%s-%s.csv" %(input_data, id_course, dm.get_course_name(id_course))
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            users.append(row[-1])
            users_info[row[-1]] = list()
            for i,l in enumerate(dm.get_lectures_by_course(id_course)):
                if float(row[i])>0.50:
                    users_info[row[-1]].append((i,row[i]))
            users_info[row[-1]].sort(key=lambda x:x[1], reverse=True)
            
    if len(users)<3:
        continue
    
    features = dm.get_lectures_by_course(id_course)
    features_names = list()
    for l in features:
        features_names.append(dm.get_lecture_name(l)) 
    
    df = pd.read_csv(file_name, names=features+['target'])
    
    x = df.loc[:, features].values# Separating out the target
    y = df.loc[:,['target']].values# Standardizing the features
    x = StandardScaler().fit_transform(x)
    #--------------------------------------------------------------------------
    
    #- PCA SCELTA COMPONENTI --------------------------------------------------
    """
    scaler = MinMaxScaler()
    x = scaler.fit_transform(x)
    
    pca = PCA().fit(x)
    
    xi = np.arange(1,min(10,len(x)+1), step=1)
    y = np.cumsum(pca.explained_variance_ratio_)
    
    n_comp = min(10,len(x)+1)
    for i,val in enumerate(y):
        if val > 0.75:
            n_comp = i+1
            break
    if len(x)<=n_comp:
        continue"""
    #--------------------------------------------------------------------------
    
    #- PCA --------------------------------------------------------------------
    """pca = PCA(n_components=n_comp)
    principalComponents = pca.fit_transform(x)
    
    x = principalComponents
    
    loadings = pd.DataFrame(pca.components_.T, columns=['pc%d'%i for i in range(n_comp)], index=features_names)
    print(loadings)
    """
    #--------------------------------------------------------------------------
    
    #- CLUSTERING SCELTA NUMERO COMPONETI -------------------------------------
    sil = []
    kmax = len(users)
    
    for k in range(2, kmax):
      kmeans = KMedoids(n_clusters=k, method='alternate', random_state=0).fit(x)
      labels = kmeans.labels_
      sil.append(silhouette_score(x, labels, metric = 'euclidean'))
    max_val = max(sil)
    n_clust = sil.index(max_val)+2
    #--------------------------------------------------------------------------
    
    #- CLUSTERING -------------------------------------------------------------
    
    kmedoids = KMedoids(n_clusters=n_clust, method='alternate', random_state=0).fit(x)

    results = kmedoids.labels_
    
    clusters = [[] for _ in range(n_clust)]
    for i,r in enumerate(results):
        clusters[r].append(users[i])
    
    for i,c in enumerate(clusters):
        print("\tCluster%d:" %(i))
        for u in c:
            print("\t\t%s" %(u))
            txt = ""
            for l,p in users_info[u]:
                txt = "%s - %s" %(txt, l)
            print("\t\t%s" %(txt[3:]))
    
    #--------------------------------------------------------------------------