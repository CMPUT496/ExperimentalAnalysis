# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 19:51:48 2014

@author: Touqir
"""


"""It is in python 2.7 and so make sure to use print as a function during compiling"""

from __future__ import division

from numpy import *
from random import *


def Student():
    
    Student_file=open('C:\Users\Touqir\Documents\Python\student.txt','r')
    S_string=Student_file.read()
    S_list=S_string.split()
    no_row=len(S_list)/2
    no_col=2
    Student_matrix=zeros((no_row,no_col))
    i=0
    for ID,Caliber in zip(S_list[::2],S_list[1::2]):   
        
        Student_matrix[i,:]=[ID,Caliber]
        i+=1    
        
    return Student_matrix
    
def Problem():
        
    Problem_file=open('C:\Users\Touqir\Documents\Python\problem.txt','r')
    P_string=Problem_file.read()
    P_list=P_string.split()
    no_row=len(P_list)/4
    no_col=4
    Problem_matrix=zeros((no_row,no_col))
    i=0
    for Ta_r,Li_r,Ti_n,Fr_c in zip(P_list[::4],P_list[1::4],P_list[2::4],P_list[3::4]):   
    #Ta_r is target representation which is 0 for decimal and 1 for fraction
    #Li_r is line representation which is 0 for decimal and 1 for fraction
    #Ti_n is number of ticks
    #Fr_c is fraction complexity
        
        Problem_matrix[i,:]=[Ta_r,Li_r,Ti_n,Fr_c]
        i+=1
    return Problem_matrix
    
def Problem_extract(data,train_n,test_n):
#The function randomly extracts n configurations from the problem matrix
    train=zeros([train_n,data.shape[1]])
    test=zeros([test_n,data.shape[1]])
    row_no=data.shape[0]
    row_list=list(range(row_no))
    for i in range(train_n):
        row=choice(row_list)
        row_list.remove(row)
        train[i,:]=data[row,:]
        
    for i in range(test_n):
        row=choice(row_list)
        row_list.remove(row)
        test[i,:]=data[row,:]
    
    return train,test

def similarity(arm,test):
#cosine similarity measure function
    return dot(arm,test.T)/(linalg.norm(arm)*linalg.norm(test.T,axis=0))
    

            
def reward(arm,test,r_param):
#returns reward 
#r_param[0]=student_caliber
#r_param[1]=similarity_threshold
    student_caliber=r_param[0]
    similarity_threshold=r_param[1]
    cos_sim=similarity(arm,test)
    success=0
    test_num=test.shape[0]
    
    for i in range(test_num):
        
        if cos_sim[i]>similarity_threshold:
            if random.uniform(0,1)<student_caliber:
                success+=1
                
    return success/test_num
                
            

#data=Problem()
#train,test=Problem_extract(data,3,2)
#print 'train matrix is: '
#print train
#print 'test matrix is: '
#print test

arm=array([1,4,6])
test=array([[1,2,100],[1,2,6],[5,0,2]])
sim=similarity(arm,test)
print sim[1]
print similarity(arm,test)        
