#! python3
# constants
ImpedOfFreeSpace = 377  # Ohms 
SpeedOfLight = 9.84e8   # Ft/sec 
pi = 3.1415927
#ResistCopper = 6.79e-7  # Ohms inch 
ScreenDepth = 24
ScreenWidth = 80
BIG = 1.0e36
SMALL = 1.0e-36
MaxOpt = 15             # Maximum number of menu selections 
MaxUnits = 10           # Number of various units required for input 
StrLen = 50             # Length of string arrays 
Iseed = 123             # Dummy constant for random0  
IterationsMax = 100     # Max Num of iterations for stat analysis

# variables
OptArray = [None] * 15
helpfile = ('')			# default helpfile

# Define default parameter values
NumPoints = 5
Time = [None] * (NumPoints + 1)
Magnitude = [None] * (NumPoints + 1)
base = [None] * 3

Ende = False
DiConst = 4.7
EffDiConst = DiConst
LoadImp = 100
LineImp = 100
IntImped = 48
EffImped = 100
IntProp = 2.5
DistCap = 0
#TraceWidth = 0.011
#TraceThick = 0.0021
#TraceHeight = 0.026
TraceSpacing = 0.089
Period = 20.0
SigPlaneSep = 0.004
