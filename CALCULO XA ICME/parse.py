# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:21:49 2017

@author: Maria
"""




f1 = open('AC_H0_SWE_1619899.txt','r')
f2 = open('AC_H0_SWE_1619899_parsed.txt','w')

#while True:
    #text = f.readline()
    #if '-1.00000E+31' in text:
        #print text
index=0

for line in f1:
    #line.strip()
    #line=line.replace('-1.00000E+31', '0.00000')
    #print line
    if index >65 and index < 8166:
        #line.strip()
        
        line=line.replace('       ', ' ')
        line=line.replace('  ',' ')
        
        print line
        f2.write(line)
       
    index=index+1
    #f2.write(line.replace('-1.00000E+31', '0000000'))
    #f2.write(line.replace('       ', ','))


f2.close()