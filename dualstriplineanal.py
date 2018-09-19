#! python3
import os, sys, math
from beatinc import *
from beatio import *
from beatcalc import *

#**************************************************************************
def DualStripAnal():
#                                                                          
# Determines the impedance and propagation #constant of dual-stripline      
# using the equation found the IPC Standard "Design standard for electronic
# packaging utilizing high speed techniques".                              
#                                                                          
# Please keep in mind that the same equations used in this def are
#   also contained in DualStripStatAnal.                                     
#**************************************************************************

#var
#   Cap, Induct,
#   ImpFactor1,ImpFactor2, ImpFactor3 : real
#   Again : boolean
    SigPlaneSep = 0.004

    Again = True
    while Again == True :
        os.system('cls')
        print ('Dual-stripline analysis')
        print ('-----------------------------------------------------------')
        print('\n')
        TraceThick, TraceWidth, TraceHeight, DiConst = GetTraceParam()        
        SigPlaneSep = GetParam('What is the signal plane separation? ',1,SigPlaneSep)
        ImpFactor1 = 80/math.sqrt(DiConst)
        ImpFactor2 = math.log(1.9*(2*TraceHeight + TraceThick)/(0.8*TraceWidth + TraceThick))
        ImpFactor3 = 1 - (TraceHeight/(4*(TraceHeight + SigPlaneSep + TraceThick)))
        IntImped = ImpFactor1 * ImpFactor2 * ImpFactor3
        IntProp = 1.017*math.sqrt(DiConst)
        Cap = IntProp/IntImped*1e3/12
        Induct = IntProp * IntImped/12
        Resist = IntResist(TraceThick, TraceWidth)
        LineAnalOut(IntImped, IntProp, Cap, Induct, Resist)
        Again = GetResponse('Another dual-stripline analysis (y/n)?', 'n')
        if (Again == False) : break


