#! python3
import os, sys
from beatinc import *
from beatio import *
from beatcalc import *


#****************************************************************************
def StripLineAnal() :
#                                                                          
# Determines the impedance and propagation constant of a stripline         
# using the standard equation found in Motorola's MECL Handbook or a       
# hundred other books.                                                     
#                                                                          
# Please keep in mind that the same equations used in this procedure are
#also contained in StripLineStatAnal.                                     
#****************************************************************************
#var
#   Cap, Induct,
#   PlaneSpace,
#   ImpFactor1,ImpFactor2 : real;
#   Again : boolean;
    ResistCopper = 6.79e-7  		 # Ohms inch
	
    Again = True
    while Again == True :
        os.system('cls')
        print('Stripline analysis')
        print('-----------------------------------------------------------')
        print('\n')
        TraceThick = GetTraceParamThick()
        TraceWidth = GetTraceParamWidth()
        TraceHeight = GetTraceParamHeight()
        DiConst = GetTraceParamConst()
        PlaneSpace = 2*TraceHeight + TraceThick
        ImpFactor1 = 60/math.sqrt(DiConst)
        ImpFactor2 = math.log(4*PlaneSpace/(0.67*pi*TraceWidth*(0.8 + TraceThick/TraceWidth)))
        IntImped = ImpFactor1 * ImpFactor2      
        IntProp = 1.017*math.sqrt(DiConst)
        Cap = IntProp/IntImped * 1e3/12
        Induct = IntProp * IntImped/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(IntImped, IntProp, Cap, Induct, Resist)
        Again = GetResponse('Another stripline analysis (y/n)?')
        if (Again == False) : break
     #end while
#end StripLineAnal
