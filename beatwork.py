#unit beatwork

#interface

def Crosstalk
def DistCapAnal
def LadderNetAnal


#implementation
 import crt, beatio, beatinc, beatmath

#**************************************************************************
def Crosstalk
#                                                                          
# This def calculates the backward and forward crosstalk for         
# microstrip.  It allows for bus structures, distributed capacitance,      
# termination values, different solder mask, and interlaced grounds.       
#                                                                          
# Several papers were used to derive the crosstalk calculation algorithms  
# used in this def.  First, the microstrip characteristics are for   
# even and odd modes are determined using the models defined by Schwarzmann
# in his paper "Microstrip plus equations adds up to fast designs".        
# Second, papers by Ivor Catt, "Crosstalk in Digital Systems" and John     
# Defalco were used for basic crosstalk theory and crosstalk reflection    
# analysis.  Data in these papers were also used for verification of the   
# single line to line crosstalk.  Extrapolations to multiple lines and     
# ground interlacing were primarily intuitive derviations and have been    
# verified against GS2 processor board and backplane data.                 
#                                                                          
# Corrections to the propagation #constant (because of solder mask have     
# been added based on emperical data from GS2 boards.  The correction      
# factor was derived similar to the techinique in "Characteristics of      
# Microstrip Transmission Lines", by H. R. Kaupp.                          
#                                                                          
#**************************************************************************

#var
   TraceSpace,
   RiseTime,
   VoltStep,
   BackVolt,
   ForVolt,
   BackPulWid,
   ForPulWid,
   VoltOdd,
   FCrC,
   BCrC : extended
   Count,
   CountLimit,
   ActLines : integer
   BusStruct,
   Update,
   Again,IntGnd : boolean
   SoldMask : char

#begin
   Again =True
   VoltStep = 3.0 #v
   RiseTime = 2.8 #ns
   TraceLength = 10.5 #in
   while Again == True do
   #begin
      IntGnd = False
      BusStruct = False
      ActLines = 1
      BCrC = 0
      FCrC = 0
      BackCrossConst = 0
      ForCrossConst = 0
      BackVolt = 0
      ForVolt = 0
      VoltOdd = 0
      SoldMask = 'w'
      EffDiConst = 0.58*DiConst + 0.55 # Set for wet solder mask 
      os.system('cls')
      print ('Crosstalk Analysis')
      print ('-----------------------------------------------------------')
      print('\n')
      TraceParamOut
      GetResponse ('New trace parameters (y/n)? ', Update )
      if Update == True :
         #begin
            GetTraceParam

            # Adjust the dielectric #constant for solder mask 

            write ('Solder mask? (w-wet, d-dry, n-none) ', SoldMask)
            readln (SoldMask)
            case SoldMask of
               'n' : EffDiConst = 0.475*DiConst + 0.67
               'w' : EffDiConst = 0.58*DiConst + 0.55
               'd' : EffDiConst = DiConst
            #end
      #end

      # Request data essential for crosstalk analysis 

      GetParam ('Trace spacing from edge to edge ?',1, TraceSpacing)
      GetParam ('Trace length ?',1, TraceLength)
      GetParam ('What is the distributed cap.?',3, DistCap)
      GetParam ('Signal Rise time ?',4, RiseTime)
      GetParam ('Voltage step ?',5, VoltStep)
      GetParam ('What is the load impedance ? ',2, LoadImp)
      GetResponse ('Interlaced grounds (y/n)? ',  IntGnd)
      GetResponse ('Bus Structure (y/n)? ',  BusStruct)

      # For a bus structure 

      if BusStruct == True :
         #begin

         # Request the number of active lines 

         print('\n')
         write ('Number of active lines (1,2,4,6)? ', '[', ActLines:1,' ]')
         readln (ActLines)
         if (IntGnd == True) or (ActLines == 1) :
            CountLimit = 1
          else:
            CountLimit = ActLines div 2

         # For the number of active lines divided by two, interatively add 
         # up the crosstalk #constants                                      

         for Count = CountLimit downto 1 do
            #begin
            TraceSpace = TraceSpacing
            TraceSpacing = Count*TraceSpacing + (Count-1)*TraceWidth
            LinCap ( LowCap, UpCap, FringeCap)
            EvenLineCap ( EvenUpCap, EvenFringeCap)
            OddLineCap (OddUpCap, OddFringeCap)
            PropConst (EvenIntProp, LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap)
            PropConst (OddIntProp, LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap)
            LineImped (EvenLineImp, EvenIntProp, LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap)
            LineImped (OddLineImp, OddIntProp, LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap)
            BCrC = (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp)
            if BCrC >= 0 :
               BackCrossConst = BackCrossConst + BCrC
            FCrC = (EvenIntProp - OddIntProp)
            if FCrC >= 0 :
               ForCrossConst = ForCrossConst + FCrC
            TraceSpacing = TraceSpace
            #end  Loop 

            # If bus structure and interlaced grounds : iteratively add 
            # the squares of the backward #constants and divide the odd mode
            # voltage by 2                                                 

            if IntGnd == True :
               #begin

               # Adjust backward #constant for a single adjacent bus trace  

               BCrC = BackCrossConst/2

               BackCrossConst = 0
               if ActLines >= 2 :
                  CountLimit = ActLines div 2
               for Count = CountLimit downto 1 do
                  #begin
                  BCrC = sqr(BCrC)
                  BackCrossConst = BackCrossConst + BCrC
                  VoltOdd = VoltOdd/4 + VoltStep/4
                  #end

               # Correct for bus symmetry 

               BackCrossConst = BackCrossConst*2

               #end
              else: # if no interlaced ground 
               VoltOdd = VoltStep/2

            if ActLines == 1 : # Correct for no bus symmetry 
               BackCrossConst = BackCrossConst/2

         #end Bustruct == True 

       else: # BusStruct == False 
         #begin
            LinCap ( LowCap, UpCap, FringeCap)
            EvenLineCap ( EvenUpCap, EvenFringeCap)
            OddLineCap (OddUpCap, OddFringeCap)
            PropConst (EvenIntProp, LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap)
            PropConst (OddIntProp, LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap)
            LineImped (EvenLineImp, EvenIntProp, LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap)
            LineImped (OddLineImp, OddIntProp, LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap)
            BackCrossConst = (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp)
            ForCrossConst = (EvenIntProp - OddIntProp)

# If not bus structure but interlaced ground 

            if IntGnd == True :
               #begin
                  BackCrossConst = sqr(BackCrossConst)
                  VoltOdd = VoltOdd/4 + VoltStep/4
               #end
             else:
               VoltOdd = VoltStep/2  # End interlaced ground 
         #end  BusStruct == False 

      # Determine the line impedance 

      LineImp = math.sqrt(EvenLineImp * OddLineImp)

      # Determine the max. backward crosstalk amplitude and pulse width 

      BackVolt = BackCrossConst*VoltStep
      BackPulWid = 2*EvenIntProp*TraceLength/12

      # Adjust the amplitude for the edge rate and trace length if needed 

      if  RiseTime > 2*(EvenIntProp*TraceLength/12) :
         BackVolt = BackVolt*(2*(EvenIntProp*TraceLength/12)/RiseTime)

      # Determine the forward crosstalk amplitude and pulse width 

      ForPulWid = RiseTime
      if (ForCrossConst*TraceLength/12) > RiseTime :
         ForVolt = VoltOdd
       else:
         ForVolt = ((TraceLength/12)*ForCrossConst*VoltOdd)/RiseTime

# Correct for termination mismatch 

      ReflectionCoef = (LoadImp - LineImp)/(LoadImp + LineImp)
      BackVolt = BackVolt * (1 + ReflectionCoef)
      ForVolt = ForVolt *  (1 + ReflectionCoef)

# Output the test conditions and results 

      os.system('cls')
      print ('Test Parameters')
      print ('-------------------------')
      print ('RiseTime:      ',RiseTime:3:2,'ns')
      print ('Voltage Step:  ',VoltStep:4:2,'v')
      print ('Dist. Cap.:    ',DistCap:4:2,' pf/in')
      print ('Trace Length:  ',TraceLength:4:2)
      if IntGnd == True :
        print ( 'Interlaced grounds')
      print('\n')
      print ('Crosstalk Data')
      print ('-------------------------')
      print ('Backward Crosstalk Constant:    ',BackCrossConst:4:3)
      print ('Backward Crosstalk Voltage:     ',BackVolt:4:3,' v')
      print ('Backward Crosstalk Pulse Width: ',BackPulWid:4:3,' ns')
      print ('Forward Crosstalk Constant:     ',ForCrossConst:4:3,' ns/ft')
      print ('Forward Crosstalk Voltage:      ',ForVolt:4:3,' v')
      print ('Forward Crosstalk Pulse Width:  ',ForPulWid:4:3,' ns')
      print ('Even Line Impedance:            ',EvenLineImp:4:2,' ohms')
      print ('Odd Line Impedance:             ',OddLineImp:4:2,' ohms')
      print ('Even Prop Const:                ',EvenIntProp:4:3,' ns/ft')
      print ('Odd Prop Const:                 ',OddIntProp:4:3,' ns/ft')
      print('\n')
      GetResponse('Another crosstalk analysis? (y/n) ',Again)
   #end
#end  Crosstalk 


#**************************************************************************
def DistCapAnal
#
#   Determines the effects of distributed capacitances on effective
#   impediance and propagation delay of a transmission line. The equations
#   can be found in any applicable textbook and also easily be derived.      
#**************************************************************************

#var
   Again : boolean

#begin  Distributed Capacitance Analysis 

   Again = True
   while Again ==True do
   #begin
      os.system('cls')
      print ('Calculates the effective impedance and prop delay')
      print ('-----------------------------------------------------------')
      print('\n')
      GetParam('What is the intrinsic impedance ?',2,IntImped)
      GetParam('What is the intrinsic delay ? ',6,IntProp)
      GetParam('What is the distributed capacitance ?',3,DistCap)
      IntCap = IntCapac(IntImped, IntProp)*1e3/12
      EffImped = IntImped / LoadAdjust(IntCap, DistCap)
      EffProp = IntProp * LoadAdjust(IntCap, DistCap)
      print('\n')
      print ('Line analysis:')
      print ('--------------')
      print ('Impedance (ohms):                == ',EffImped:3:1)
      print ('Propagation Delay (ns/ft):       == ',EffProp:2:2)
      print ('Intrinsic Capacitance (pf/in):   == ',IntCap:2:2)
      print ('Distributed Capacitance (pF/in): == ',DistCap:2:2)
      print('\n')
      GetResponse('Another calculation (y/n)? ',Again)
   #end
#end


#**************************************************************************
def LadderNetAnal
# Completely modified 6/89, Ulf Schlichtmann 
# This def requests as input the line impedance and propagation delay
#   #constant of a line as well as the total length of the line and the rise
#   time of the signal that needs to be analyzed.
#   It : proceeds to compute the cutoff frequency of that signal and the
#   number of RLC segments this line has to be split up into if it is to be
#   modelled correctly by SPICE. The values for the R, L and C elements of each
#   segment are also calcutlated and output.
#   To calculate the number of required segments, a "rule of thumb" is used  
#**************************************************************************

#var
   Again:boolean
   SegCap, SegInd, SegRes,  # values per segment 
   CornerFrequ :real
   NumSeg:integer


#*************************************************************************
def GetNetInfo
#*************************************************************************

#begin
     GetParam('What is the line impedance?',2,IntImped)
     GetParam('What is the propagation delay?',6,IntProp)
     GetParam('What is the intrinsic resistance?',10,Resist)
     GetParam('What is the line length?',1,TraceLength)
     GetParam('What is the rise time?',4,TRise)
#end



#begin   LadderNetAnal 
   Again = True
   while Again == True : #begin
     os.system('cls')
     print ('Trace Pi Model Generation')
     print ('-----------------------------------------')
     print('\n')
     GetNetInfo
     CornerFrequ = 2/TRise         # Cutoff Frequency 
     IntCap = IntProp*TraceLength/IntImped*1000/12
                                     #1000:Conversion to pF
                                     #12: Conversion from ft to inch 
     IntInd = IntProp*TraceLength*IntImped/12
                                     #12: Conversion from ft to inch 
     NumSeg = trunc(5/2*CornerFrequ* math.sqrt(IntCap*IntInd)*math.sqrt(0.001))+1
                                     # "Rule of Thumb" 
                                     # math.sqrt(.001): #unit correction factor 
     print('\n')
     print ('Trace Pi Model Analysis')
     print ('------------------------')
     print ('Calculations have determined the following number of segments.')
     print ('Confirm this number by hitting RETURN or change it.')
     GetIParam ('Number of segments:                ',NumSeg)

     SegCap = IntCap/NumSeg        # Capacitance per segment 
     SegInd = IntInd/NumSeg        # Inductance per segment 
     SegRes = Resist*TraceLength/NumSeg/1000  # Resistance per segment 
                                     # 1000 : Conversion mohms --> ohms 

     print ('Capacitance per segment (pF):      ',SegCap:2:2)
     print ('Inductance per segment (nH):       ',SegInd:2:2)
     print ('Resistance per segment (ohms):     ',SegRes:2:2)
     print('\n')

     GetResponse('One More Time !?',Again)
   #end
#end

end.


