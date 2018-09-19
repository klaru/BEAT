#! python3
import os, sys
from beatinc import *
from beatio import *
from beatcalc import *

#**************************************************************************
def MicroStripAnal():
#                                                                          
# Calculates the line impedance of a microstrip trace using the model      
# defined by Schwarzmann in his paper "Microstrip plus equations adds      
# up to fast designs" for an isolated conductor. He breaks the line        
# capacitance up into:                                                     
#                                                                          
#   Cppu = the upper plate capacitance (UpCap)                            
#   Cpp  = the lower plate capacitance (LowCap)                           
#   Cf   = the fringe capacitances (FringeCap)                            
#                                                                          
# Corrections to the propagation #constant (because of solder mask have     
# been added based on emperical data from GS2 boards.  The correction      
# factor was derived similar to the techinique in "Characteristics of      
# Microstrip Transmission Lines", by H. R. Kaupp.                          
#                                                                          
# Please keep in mind that the same equations used in this def are
#   also contained in MicroStripStatAnal.                                    
#**************************************************************************

#var
#   Cap, Induct : real
#   Again: boolean
#   temp : char
    
    SoldMask = 'n'
    Again = True
    while Again == True :
        os.system('cls')
        print('Micro-stripline analysis')
        print('-----------------------------------------------------------')
        print('\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()        
        print('Solder mask? (w-wet, d-dry, n-none)  [', SoldMask,']', end="")
        while True :
            temp = input()
            if (temp == 'n') or (temp == 'w') or (temp == 'd') or (temp == ''): break
        if temp == "" : temp = 'n'
        if (temp != '') : 
            SoldMask = temp
            if SoldMask == 'n' : EffDiConst = 0.475*DiConst + 0.67
            elif SoldMask == 'w' : EffDiConst = 0.58*DiConst + 0.55
            elif SoldMask == 'd' : EffDiConst = DiConst
        LowCap, UpCap, FringeCap = LineCap(TraceThick, TraceWidth, TraceHeight, DiConst, EffDiConst)
        IntProp = PropConst(LowCap, UpCap, UpCap, FringeCap, FringeCap, DiConst, EffDiConst)
        IntImped = LineImped(IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap)
        Cap = (2*(UpCap + FringeCap) + LowCap)/12
        Induct = IntProp * IntImped/12
        Resist = ResistCopper/(TraceThick * TraceWidth)*1000
        LineAnalOut(IntImped, IntProp, Cap, Induct, Resist)
        Again = GetResponse('Another micro-stripline analysis (y/n)?', 'n')
        if (Again == False) : break
