# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 21:16:40 2016

@author: Administrator
"""

f=open('true_result.txt','r')
sourceinlines=f.readlines()
f.close()
new=[]
for line in sourceinlines:
    temp1=line.replace('\n','').split(',')

    new.append(temp1)
    
a=[]
for i in range(len(new)):
    if i%2==0:
        a.append(new[i])

f1=open('my_result.txt','r')
sourceinlines1=f1.readlines()
f1.close()
new1=[]
for line in sourceinlines1:
    temp2=line.replace('\n','').split(',')

    new1.append(temp2)
    
test= new1
true=new

m=0
for i in range(len(test)):
    if test[i] == true[i]:
        m+=1
    else:
        print test[i]

accuracy = m*1.0/len(test)
print ('accuracy is %f%%') %  (accuracy*100)