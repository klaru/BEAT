#! python3
#              BOARD ELECTRICAL ANALYSIS TOOL (BEAT)                       
#                             7-1-88                                         
#                                                                            
#  This is a program which assist the engineer in dealing with transmission  
#  line issues such as the line impedance, propagation delay, reflection     
#  coefficient, distributed capacitance, etc.                                
#                                                                            
#  Modifications to BEAT:                                                    
#  6/89, Ulf Schlichtmann                                                    
#  Comments on details of the modifications appear throughout the program    
#									     
#  8/1989, Klaus Ruff							     
#  Ported to Turbo-Pascal 5 on PC					     
#  4/1991 Klaus Ruff								     
#  Ported to Turbo Pascal Windows (Text Mode)
#  9/2018 Klaus Ruff
#  Ported to Free Pascal 3.0 (Text Mode)   
#
#  9/2018 Klaus Ruff
#  Ported to Python 3                                                                  
#                                                                            
#  Key Global Variables:                                                     
#                                                                            
# 	IntImped (ohms)  = Intrinsic impedance of a line (no dist. cap.)      
#	EffImped (ohms)	 = Effective impedance after dist. cap. considered.   
#	IntProp (ns/ft)  = Intrinsic prop. delay of a line (no dist. cap.)    
#	EffProp (ns/ft)  = Effective prop. delay after dist. cap. considered.
#	IntCap (pf/in)	 = Intrinsic capacitance of the line.                 
#	DistCap	(pf/in)  = Extra capacitance distributed along a line.        
#	IntInd (nH/in)	 = Intrinsic inductance of the line.                  
#	IntRes (ohms/in) = Intrinsic resistance of the line.                  
#                                                                            
#*****************************************************************************

import os, sys
from beatinc import *
from beatio import *
from beatcalc import *
from help import Help
from reflectcoef import Reflectcoef
from striplineanal import StripLineAnal
from microstriplineanal import MicroStripAnal
from dualstriplineanal import DualStripAnal
from embedmicrostriplineanal import EmbeddedMicroStripAnal
from setunit import SetUnit
from statanal import StatAnal
from distcapanal import DistCapAnal
from crosstalk import CrossTalk
from laddernetanal import LadderNetAnal
from loadparameters import LoadParameters 
from beatfourier import FourierValues, FourierAnal


def main ():       # begin Main Program

    Time[1] =  0.0
    Magnitude[1] = 0.0
   
    Time[2] =  1.0
    Magnitude[2] = 0.0
  
    Time[3] =  2.0
    Magnitude[3] = 5.0
   
    Time[4] = 12.0
    Magnitude[4] = 5.0
   
    Time[5] = 13.0
    Magnitude[5] = 0.0
	
    InputUnits = [[0 for x in range(11)] for y in range(3)]
    UnitConversion = [[0 for x in range(11)] for y in range(3)]

# texts to prompt the user to use the correct unit
    InputUnits[1][1] = '(mm)'
    InputUnits[1][2] = '(ohms)'
    InputUnits[1][3] = '(pF/mm)'
    InputUnits[1][4] = '(ns)'
    InputUnits[1][5] = '(volts)'
    InputUnits[1][6] = '(ns/mm)'
    InputUnits[1][7] = '(mohms)'
    InputUnits[1][8] = '(pF)'
    InputUnits[1][9] = '(nH)'
    InputUnits[1][10] = 'mohms/mm'
	
    InputUnits[2][1] = '(inch)'
    InputUnits[2][2] = '(ohms)'
    InputUnits[2][3] = '(pF/in)'
    InputUnits[2][4] = '(ns)'
    InputUnits[2][5] = '(volts)'
    InputUnits[2][6] = '(ns/ft)'
    InputUnits[2][7] = '(mohms)'
    InputUnits[2][8] = '(pF)'
    InputUnits[2][9] = '(nH)'
    InputUnits[2][10] = 'mohms/inch'
   
# conversion factors from metric to the respective imperial units 
    UnitConversion[1][1] = 25.4
    UnitConversion[1][2] = 1
    UnitConversion[1][3] = 1/25.4
    UnitConversion[1][4] = 1
    UnitConversion[1][5] = 1
    UnitConversion[1][6] = 1/304.8
    UnitConversion[1][7] = 1
    UnitConversion[1][8] = 1
    UnitConversion[1][9] = 1
    UnitConversion[1][10] = 1/25.4

    UnitConversion[2][1] = 1
    UnitConversion[2][2] = 1
    UnitConversion[2][3] = 1
    UnitConversion[2][4] = 1
    UnitConversion[2][5] = 1
    UnitConversion[2][6] = 1
    UnitConversion[2][7] = 1
    UnitConversion[2][8] = 1
    UnitConversion[2][9] = 1
    UnitConversion[2][10] = 1

    NumIterations = IterationsMax  # Default for Iterations for Stat. Anal.
						
# Setup the main menu for BEAT and go to selected routine
    while True : # begin
        Header = 'Electrical Analysis - Main Menu - BEAT (Rev 4.1)'
        OptArray[1] = 'Exit'
        OptArray[2] = 'Reflection Analysis'
        OptArray[3] = 'Strip Line Analysis'
        OptArray[4] = 'Microstrip Line Analysis'
        OptArray[5] = 'Dual-strip Line Analysis'
        OptArray[6] = 'Embedded Microstrip Line Analysis'
        OptArray[7] = 'Dist. Cap. Analysis'
        OptArray[8] = 'Crosstalk Analysis'
        OptArray[9] = 'Trace Pi Model Generation'
        OptArray[10] = 'Fourier Analysis'
        OptArray[11] = 'Statistical Analysis'
        OptArray[12] = 'Metric / Imperial System'
        OptArray[13] = 'Load Library Parameters'
        OptArray[14] = 'Help'
        SelOpt = menu (14, Header, OptArray)
		
        if SelOpt == '1':
	        break
        elif SelOpt == '2':
            Reflectcoef()
        elif SelOpt == '3':
	        StripLineAnal()
        elif SelOpt == '4':
            MicroStripAnal()									
        elif SelOpt == '5':
            DualStripAnal()
        elif SelOpt == '6':
            EmbeddedMicroStripAnal()
        elif SelOpt == '7':
           DistCapAnal()
        elif SelOpt == '8':
            CrossTalk()
        elif SelOpt == '9':						
            LadderNetAnal()
        elif SelOpt == '10':					
            FourierAnal()
        elif SelOpt == '11':				
            StatAnal()
        elif SelOpt == '12':			
            SetUnit()
        elif SelOpt == "13":
            LoadParameters()
        elif SelOpt == '14':
            Help()

if __name__ == '__main__': main ()	


