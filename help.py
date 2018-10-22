#! python3
import os, sys
from beatinc import *
from beatio import *

#****************************************************************************)
def Help():
#****************************************************************************)

    def print_help(file) :    	
        helpfile = open(file)
        os.system('cls')
        while True:
            line = helpfile.readline()
            if not line: break
            print(line, end='')  
        helpfile.close()       	
        print('\n')
        
# Reset selected help file and display the file
    while True : # begin
        Header = 'Electrical Analysis - Help Menu - BEAT (Rev 4.1)'
        OptArray[1] = 'Return to Main Menu'
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
        SelOpt = menu (13, Header, OptArray)
		
        if SelOpt == '1': break
        elif SelOpt == '2':
            print_help('reflect.hlp')		# reflectcoef
        elif SelOpt == '3':
            print_help('stripanal.hlp')   	# StripLineAnal
        elif SelOpt == '4':
            print_help('microanal.hlp')	    # MicroStripAnal										
        elif SelOpt == '5':
            print_help('dualanal.hlp')		# DualaStripAnal
        elif SelOpt == '6':
            print_help('embedmicro.hlp')	# EmbedMicroStripAnal
        elif SelOpt == '7':
            print_help('distcap.hlp')		# DistCapAnal
        elif SelOpt == '8':
            print_help('crosstalk.hlp')	    # Crosstalk
        elif SelOpt == '9':						
            print_help('tmodel.hlp')		# LadderNetAnal
        elif SelOpt == '10':					
            print_help('fourier.hlp')		# FourierAnal
        elif SelOpt == '11':				
            print_help('statistics.hlp')	# StatAnal
        elif SelOpt == '12':			
            print_help('unitsel.hlp')		# SetUnit
        elif SelOpt == "13":
            print_help('library.hlp')		# LoadParameters

        Again = input("Hit <Return> to return to Help Menu: ")
# end help
