#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:59:46 2019

@author: CathrineKiel
"""

import pandas as pd
import numpy as np
import sys 

file=pd.read_csv(sys.argv[1],header=None,sep=" ")
row,col=file.shape
print("file read succesfully")

geno=np.array(file)
geno[0:1,]

# remove first four columns
geno1=np.copy(geno[:,4:col])
np.shape(geno1)

geno1[0:1,]

geno2=pd.DataFrame(geno1)


# now for each row take value in i and i+1 and sum up. 
# If sum =4 then it is a 2 
# If sum= 3 then it is a 1
# if sum = 2 then it is a 0
# if sum =0 then it is NA
newgenotype=np.empty((row,(col-4)/2,))

count=0
for i in range(0,len(geno2.columns),2): 
    currentcol=geno2[i]
    nextcol=geno2[i+1]
    new=currentcol+nextcol
    newgenotype[:, count] = new
    count+=1

newgenotype_=pd.DataFrame(newgenotype)
newgenotype_new=newgenotype_.replace([0, 2, 3, 4], ['NaN', -1, 0, 1])
newgenotype_new_np=np.array(newgenotype_new,dtype=np.float64)
newgenotype_new_df=pd.DataFrame(newgenotype_new_np)


pedfile=pd.read_csv("pedsixcol.txt",header=None,sep=",")
accession_names=pedfile.iloc[:, 0]
newgenotype_new_df.columns = accession_names

newgenotype_new_df.to_csv("genotypes_for_GRM.csv",index = None, header=True,na_rep='NaN')

