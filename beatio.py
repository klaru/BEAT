#! python3
import os, sys, math
from beatinc import *

#procedure GetParam (question : str; UnitSel : integer; var number : extended);
#procedure GetIParam (question : str; var number : integer);
#procedure GetResponse (question : str; var response : boolean);
#procedure GetTraceParam;
#procedure GetTraceStatParam;
#procedure TraceParamOut;
#procedure LineAnalOut(EffImped, EffProp, IntCap, IntInduct, IntRes : extended);
#procedure LineAnalStatOut(EffImpedMean,EffImpedSigma,EffPropMean,
#	EffPropSigma,IntCapMean,IntCapSigma,IntInductMean,
#	IntInductSigma,IntResMean,IntResSigma: real);
#procedure LoadParameters
#procedure menu(NumOpt : integer; Header : str; OptArray : strgarray; var SelOpt : opt);
#procedute StatIterNum;

#****************************************************************************
def GetParam(question, UnitSel, number) :
#****************************************************************************
   
   print(question,'[%3.4f] ' %(number), end='')			  
   string = input()
   if string != '' :
       number = float(string)
   return number
#end GetParam 

#****************************************************************************
def GetIParam (question, number) :
#****************************************************************************

   print(question,'[%6i] ' %(number), end='')				
   string = input()
   if string != '' :
       number = int(string)
   return number
#end GetIParam

#****************************************************************************
def GetResponse (question, yn) :
#****************************************************************************

    Query = yn
    print (question, '[',yn,'] ', end='')
    while True :
        string = input()
        if ((string == 'y') 
		 or (string == 'Y') 
		 or (string == 'n') 
		 or (string == 'N') 
		 or (string == '')) : break
    if string != '' :
	    Query = string
    if ((Query == 'y') 
	 or (Query == 'Y')) :
        Response = True
    else :
        Response = False
    return Response
#end  GetResponse

#****************************************************************************
def GetTraceParam() :
#****************************************************************************
    UnitSys = 0
    global TraceThick, TraceWidth, TraceHeight, DiConst
    if UnitSys == 1 :
        TraceThick  = TraceThick * 25.4
        TraceWidth  = TraceWidth * 25.4
        TraceHeight = TraceHeight * 25.4
        TraceThick = GetParam('What is the trace thickness? [mm]  ',1, TraceThick)
        TraceWidth = GetParam('What is the trace width? [mm]  ',1, TraceWidth)
        TraceHeight = GetParam('What is the trace height? [mm]  ',1, TraceHeight)
    else :
        TraceThick = GetParam('What is the trace thickness? [in]  ',1, TraceThick)
        TraceWidth = GetParam('What is the trace width? [in]  ',1, TraceWidth)
        TraceHeight = GetParam('What is the trace height? [in]  ',1, TraceHeight)
    DiConst = GetParam('What is the dielectric constant? ',0, DiConst)
    return TraceThick, TraceWidth, TraceHeight, DiConst
#end GetTraceParam

#**************************************************************************
def GetTraceStatParam() :
#**************************************************************************
#    These routines were derived from GetTraceParamXXX                             
#**************************************************************************

	# initialize default values first
    global TraceThick, TraceWidth, TraceHeight, DiConst, \
           TraceThickSigma, TraceWidthSigma, TraceHeightSigma, DiConstSigma
    TraceWidthMean = TraceWidth 
    TraceThickMean = TraceThick
    TraceHeightMean = TraceHeight
    DiConstMean = DiConst
    TraceThickMean = GetParam('What is the mean trace thickness? ',1, TraceThickMean)
    TraceThickSigma = GetParam('What is the standard deviation for thickness? ',1, TraceThickSigma)
    TraceWidthMean = GetParam('What is the mean trace width? ',1, TraceWidthMean)
    TraceWidthSigma = GetParam('What is the standard deviation for width? ',1, TraceWidthSigma)
    TraceHeightMean = GetParam('What is the mean trace height? ',1, TraceHeightMean)
    TraceHeightSigma = GetParam('What is the standard deviation for height? ',1, TraceHeightSigma)
    DiConstMean = GetParam('What is the mean dielectric constant? ',0, DiConstMean)
    DiConstSigma = GetParam('What is the standard deviation for DiConst? ',0, DiConstSigma)
    TraceThick = TraceThickMean  # Keep the entered values as defaults
    TraceWidth = TraceWidthMean
    TraceHeight = TraceHeightMean
    DiConst = DiConstMean
    return TraceThickMean, TraceThickSigma, TraceWidthMean, TraceWidthSigma, TraceHeightMean, TraceHeightSigma, \
           DiConstMean, DiConstSigma 
#end GetTraceStatParam

#****************************************************************************
def TraceParamOut() :
#****************************************************************************

      print ('Micro-strip Trace Parameters')
      print ('-----------------------------')
      print ('Thickness:  %5.4f' %(TraceThick), ' in.')			
      print ('Width:      %4.3f' %(TraceWidth), ' in.')       
      print ('Height:     %4.3f' %(TraceHeight), ' in.')         
      print ('Spacing:    %4.3f' %(TraceSpacing), ' in.')       
      print ('Er:         %3.2f' %(DiConst))                    
      print ('DistCap     %5.4f' %(DistCap))                    
      print ('\n')
# end TraceParamOut


#****************************************************************************
def LineAnalOut(EffImped, EffProp, IntCap, IntInduct, IntRes) :
#****************************************************************************

   print ('\n')
   print ('Line analysis:')
   print ('--------------')
   print ('Impedance (ohms):                = %3.1f' %(EffImped)) 
   print ('Propagation Delay (ns/ft):       = %2.2f' %(EffProp))   
   print ('Intrinsic Capacitance (pf/in):   = %2.2f' %(IntCap))    
   print ('Intrinsic Inductance (nH/in):    = %2.2f' %(IntInduct))
   print ('Intrinsic Resistance (mohms/in)  = %2.2f' %(IntRes)) 
   print ('\n')
#end LineAnalOut


#**************************************************************************
def LineAnalStatOut(EffImpedMean,EffImpedSigma,EffPropMean,EffPropSigma,IntCapMean,IntCapSigma,IntInductMean,IntInductSigma,IntResistMean,IntResistSigma) :
#
#    output of the data which resulted from statistical analysis. This is
#    basically a modified version of LineAnalOut.                          
#**************************************************************************

    print ('\n')
    print ('Line analysis:')
    print ('--------------')
    print ('Impedance (ohms):               mean = %3.1f' %(EffImpedMean), '   sigma = %3.3f' %(EffImpedSigma))  
    print ('Propagation Delay (ns/ft):      mean = %2.2f' %(EffPropMean), '   sigma = %2.4f' %(EffPropSigma))     
    print ('Intrinsic Capacitance (pf/in):  mean = %2.2f' %(IntCapMean), '   sigma = %2.4f' %(IntCapSigma))       
    print ('Intrinsic Inductance (nH/in):   mean = %2.2f' %(IntInductMean), '   sigma = %2.4f' %(IntInductSigma))
    print ('Intrinsic Resistance (mohms/in) mean = %2.2f' %(IntResistMean), '   sigma = %2.4f' %(IntResistSigma)) 
    print ('\n')
# end LineAnalStatOut


#***************************************************************************
def LoadParameters() :
#   This procedures accesses the database "library.bea".
#   The database contains specifications of multilayer boards and may
#   be changed or appended at any time.
#   However, when modifying the database please take the rather stringent
#   data structure into account. It is described in the user's manual.
#   Deviating from this structure may very likely casuse BEAT to either
#   run into one of the traps incorporated in this procedure or just
#   crash.
#    Ulf Schlichtmann, 6/89                                                 
#***************************************************************************

#const
    LibStringLength = 70  # no database entry may exceed 70 characters 
    LayerTypeLength = 10  # keyword for layer type : 10 chars max 
                          # Note: if this parameter is changed, the
                          #         comparisons between LayerType and some
                          #         string constants below will have to be
                          #         changed also                           
    LayerTypeMax = 10     # Max number of layer that can be stored. Since boards
                          # are assumed to be symmetrical, boards with twice
                          # as many layers can be handled                
    SpecMax = 20          # Current max number of specs that can be handled   

#type
#   LibString = array[1..LibStringLength] of char;
#   LayerTypeString = array[1..LayerTypeLength] of char;

#var
#   i, j, k, l,
#   NumSpecs,SpecSelect,
#   NumLayers,LayerNum,LayerSelect,
#   TempIndex : integer;
#   dummy : char;
#   InRange, LayerTypeOK, LoadOK : boolean;
#   SpecDocNum,SpecDescription : array[1..SpecMax] of LibString;
#   LayerType : array[1..LayerTypeMax] of LayerTypeString;
#   lib:text;


#        First part of this procedure reads all available specs from the
#         library, displays the titles and gets a user selection 
    LoadOK = True
    os.system('cls')
    print ('Load Library Parameters:');
    print ('Listing of currently available Specifications');
    print ('--------------------------------------------------------------');

    lib = open('lib.bea', 'a+')
    NumSpecs = lib.readline()  # number of available specs
    dummy = lib.readline()     # 'blank' line

    if NumSpecs > SpecMax :	   # too many specs in database
        LoadOK = False
        print ('\n')
        print ('Database contains %3i' %(NumSpecs),' specs.')				
        print ('Currently BEAT can handle only %3i' %(SpecMax),' specs, however')
        print ('Please change the parameter "SpecMax" and recompile BEAT')
        print ('\n')
        print ('Hit RETURN to continue')
        dummy = input()
    #end if




    for i in range(1, NumSpecs + 1) :  			# read Doc-number and -description for 
        for j in range(1, LibStringLength+1) :  	# all specs 
            SpecDocNum[i][j] = ' '
            SpecDescription[i][j] = ' '
        #end for
        j = 1
        while True:
            SpecDescription[i][j] = lib.read(1)
            if not SpecDescription[i][j] : break
            j = j + 1
        #end while
        #dummy = lib.read(1)  					    read EOLN character
        j = 1
        while True:
            SpecDescription[i][j] = lib.read(1)
            if not SpecDescription[i][j] : break
            j = j + 1
        #end while
        #dummy = lib.read(1)   				    read EOLN character
        print (i,' : ',SpecDocNum[i])  	    	# print out information     i:2
        print ('     ',SpecDescription[i])
    #end for

    SpecSelect = 1   							# Get user selection 
    print ('\n')
    while True:
        InRange = True
        SpecSelect = GetIParam ('Select by entering a number : ')
        if ((SpecSelect < 1) 
		 or (SpecSelect > NumSpecs)) :
            InRange = False
            print ('Incorrect Selection!   Try Again')
        if InRange == True : break

#           Second part of this procedure reads and displays the available
#           layers for the selected spec and gets a user selection.
#           Only first 50% of layers are displayed since boards are
#           assumed to be symmectrical.                                    
    os.system('cls')
    print ('Load Library Parameters:')
    print (SpecDescription[SpecSelect])
    print ('Listing of available layers')
    print ('--------------------------------------------------------------')

    lib=open('lib.bea', 'a+')
    dummy = lib.readline()                     		 # skip thru listing of available specs 
    dummy = lib.readline()
    for i in range(1, NumSpecs + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
    #end for
    dummy = lib.readline ()                   	     # go thru this loop for all specs up to the 
    for i in range (1, SpecSelect + 1) :      	     # selected spec. Only the data for
        dummy = lib.readline()         	      		 # the selected spec are displayed, however
        dummy = lib.readline()
        NumLayers = lib.readline() 		      		 # number of layers for this spec
        if NumLayers/2 != math.trunc(NumLayers/2) :  # only even number allowed
            LoadOK = False
            print ('\n')
            print ('Database shows %2i' %(NumLayers), ' layers for spec. # %2.i' %(i), '.')
            print ('This is incorrect. Only even numbers are allowed.')
            print ('The boards are assumed to be symmetrical.')
            print ('Please check the manual and correct the database')
            print ('\n')
            print ('Hit RETURN to continue')
            dummy = input()
        #end if
        dummy = lib.readline()  			                    # number of this layer 
        for j in range(1, math.trunc(NumLayers/2) + 1) : 	    # type of this layer
            readln (lib, LayerNum);
            for k in range(1, LayerTypeLength + 1) :
                LayerType[j][k] = ' '
            k = 1
            while True :
                LayerType[j][k] = lib.read(1)
                if not LayerType[j][k] : break
                k = k + 1
            #end while
            #dummy = lib.readline(1)				             read EOLN character

            LayerTypeOK = False  								 # make sure it is permitted layer type 
# skip next data depending on	   
            if ((LayerType[j] == 'strip     ') 
			 or (LayerType[j] == 'embedmicro')) :  				 # type of layer
                for l in range(1, 4 + 1) :
                    dummy = lib.readline()
                LayerTypeOK = True
            #end if
            if ((LayerType[j] == 'microstrip') 
			 or (LayerType[j] == 'dualstrip ')) :
                for l in range (1, 5 + 1) : 
                    dummy = lib.readline()
                LayerTypeOK = True
            #end if
            if ((LayerType[j] == 'gnd       ') 
			 or (LayerType[j] == 'pwr       ')					
			 or (LayerType[j] == 'gnd/pwr   ')) :
	            LayerTypeOK = True

            if LayerTypeOK == False :
                LoadOK = True
                print ('\n')
                print (LayerType[j])
                print ('This is not a recognized layer type.')
                print ('Please check the manual and correct the database')
                print ('\n')
                print ('Hit RETURN to continue');
                dummy = input()
            #end if

            dummy = lib.readline()
            if i == SpecSelect :
	            print (j,' : ',LayerType[j])			#:2
        #end for NumLayers
    #end for SpecSelect

            #  The third part of this procedure loads the data for the
            #  selected layer of the selected board into the applicable
            #  variables.                                                
            #  Please note:
            #  Because of the way this is handled - all data up to the
            #  selected layer are loaded into the variables, only the selec-
            #  ted layer will not be overwritten, all variables involved in
            #  this probably will be clobbered.                          
    LayerSelect = 1
    print ('\n')
    while True :
        InRange = True
        LayerSelect = GetIParam ('Select by entering a number : ')
        if ((LayerSelect < 1) 
		 or (LayerSelect > NumLayers/2)) :
            InRange = False
            print ('Incorrect Selection!   Try Again')
        #end if
        if ((LayerType[LayerSelect] == 'gnd       ') 
		 or (LayerType[LayerSelect] == 'pwr       ') 
		 or (LayerType[LayerSelect] == 'gnd/pwr   ')) :
            InRange = False
            print (LayerType[LayerSelect],':')
            print ('This layer cannot be selected for analysis!    Try Again')
        #end if		   
        if InRange == True : break
    #end while

    lib = open('lib.bea','a+')
    dummy = lib.readline()
    dummy = lib.readline()
    for i in range(1, NumSpecs + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
    #end for
    dummy = lib.readline()
    for i in range(1, SpecSelect + 1) :
        dummy = lib.readline()
        dummy = lib.readline()
        NumLayers = lib.readline()
        dummy = lib.readline()
        if i == SpecSelect :
	        TempIndex = LayerSelect
        else :
            TempIndex = math.trunc(NumLayers/2)
        for j in range(1, TempIndex + 1) :
            LayerNum = lib.readline()
            for k in range(1, LayerTypeLength + 1) :
	            LayerType[j][k] = ' '
            k = 1
            while True :
                LayerType[j][k] = lib.read(1)
                if not LayerType[j][k] : break
                k = k + 1
            #end while
            #dummy = lib.readline()				read EOLN character
            if ((LayerType[j] == 'strip     ') 
			 or (LayerType[j] == 'embedmicro')) :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                DiConst = lib.readline()
                SoldMask = lib.readline()
		   
            if LayerType[j] == 'microstrip' :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                DiConst = lib.readline()
                SoldMask = lib.readline()
 
            if LayerType[j] == 'dualstrip ' :
                TraceThick = lib.readline()
                TraceWidth = lib.readline()
                TraceHeight = lib.readline()
                SigPaneSep = lib.readline()
                DiConst = lib.readline()
            dummy = lib.readline()
        #end for
    #end for
    if LoadOK == True :
        print ('\n')
        print ('Parameter have been loaded into variables.')
        print ('\n')
        print ('Hit RETURN to continue.')
        dummy = input()

# end LoadParameters

#****************************************************************************)
def menu(NumOpt, Header, OptArray):
#****************************************************************************)

# This procedure provides the ability to generate a menu driven program *)
# Options are limited to ten selections.  The Option number selected is *)
# returned to the main program.                                         *)

#var
#  Temp,
#  DepthMargin,
#  WidthMargin : integer;
#  Option : opt;

   Temp = 0
   os.system('cls')   #  Clear Screen 
   for Temp in range(1, (ScreenWidth - 48)//2 + 1) :
       str(' ')
   print('Board Electrical Analysis Tool - BEAT (Rev 4.0)')
   DepthMargin = (ScreenDepth - NumOpt - 5)//2
   WidthMargin = (ScreenWidth - 40)//2
   for Temp in range(1, DepthMargin + 1) :
       print('\n')
   for Temp in range (1, WidthMargin + 1) :
       str(' ')
   print(Header)
   for Temp in range(1, WidthMargin + 1) :
       str(' ')
   print('------------------------------------------------')
   print('\n')
   for Option in range(1, NumOpt + 1) :
      for Temp in range(1, (WidthMargin - 3 + 1)) :
          out = str(' ')
          print(out, end='')
      out = str(Option)
      print(out, end='')
      out = str(') ')
      print(out, end='')
      print(OptArray[Option])
   print('\n')
   for Temp in range(1, WidthMargin + 1) :
       str(' ')
   SelOpt = input("Select Option number: ")
   return SelOpt
   os.system('cls')

#************************************************************************
def StatIterNum(NumIterations) :
#************************************************************************           
        while True:    
            NumIterations = GetIParam('Enter number of iterations :', NumIterations)
            if (NumIterations <= 0) or (NumIterations > IterationsMax) :
                print('\n')
                print('The number of iterations must be more than 1.')
                print('If you want to exceed ',IterationsMax,' Iterations,')
                print('you will have to change the #constant "IterationsMax"')
                print('in "beatinc.py" and recompile the program.')
                print('\n')
                answer = GetResponse('Hit >RETURN< to continue','y')            
            if (NumIterations > 0) and (NumIterations <= IterationsMax) : break
        return NumIterations            

            
