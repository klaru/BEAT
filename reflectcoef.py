#! python3
import os, sys
from beatinc import *
from beatio import *

 
#****************************************************************************
def Reflectcoef() :
#****************************************************************************
# This program calculates the reflection coefficient given the load
# impedance and the line impedance

    while True :
        os.system('cls')
        print('This program calculates the reflection coefficient')
        print('-----------------------------------------------------------')
        print('\n')
        LineImp = GetParam('Line impedance ? ',2)
        LoadImp = GetParam('Load impedance ? ',2)
        ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
        print('Reflection coeffiecient = ', ReflectionCoef)						#ReflectionCoef:1:2
        print('\n')
        Again = GetResponse('Another reflection calculation (y/n)?')
        if (Again == False) : break
     #end while
#end Reflectcoef