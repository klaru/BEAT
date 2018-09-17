#! python3
import os, sys, math
from beatinc import *
from beatio import *
# uses crt, beatinc, beatio;

#procedure FourierValues(var Cmag, Cphase:extendedvector);
#procedure FourierAnal;


def FourierValues():
#var
#  Csub,
#  Slope : extendedvector;
#  X,K : integer;
#  NumHarmonics,NumPoints : integer;
#  A,B : real;
#  Period : extended;

    print('\n')
    NumHarmonics = GetIParam('Number of Harmonics? ')
    NumPoints = GetIParam('Number of Points? ')
    Period = GetParam('Enter Period : ',4)
    for X in range(1, NumPoints + 1) :
        print('\n')
        Time[X] = GetParam('Enter time : ',4)
        Magnitude[X] = GetParam('Enter magnitude: ',0)
    #end for

    Magnitude[NumPoints + 1] = Magnitude[1]
    Time[NumPoints + 1] = Period
    Cmag[0] = 0 ;
    Cphase[0] = 0
    for X in range(1, NumPoints + 1) :
        Cmag[0] = Cmag[0] + 0.5*(Magnitude[X+1]+Magnitude[X])*(Time[X+1]-Time[X])/Period
        Slope[X] = (Magnitude[X+1] - Magnitude[X])/(Time[X+1] - Time[X])
    #end for
    Csub[1] = Slope[1]-Slope[NumPoints]
    for X in range(1, NumPoints) :
        Csub[X+1] = Slope[X+1] - Slope[X]
    for K in range(1, NumHarmonics + 1) :
        A = 0
        B = 0
        for X in range(1, NumPoints + 1) :
            A = -Csub[X] * cos(2*pi*K*Time[X]/Period) + A
            B = Csub[X] * sin(2*pi*K*Time[X]/Period) + B
        #end for
        Cmag[K] = (Period/(sqr(2*pi*K)))*math.sqrt(sqr(A) + sqr(B))
        Cphase[K] = atan2(B,A)
    #end for
    os.system('cls')
    print('FUNCTION DEFINITION')
    print('------------------------------')
    print('Period(ns) ', Period)
    print('\n')
    print('| Point | Time(ns)| Magnitude |')
    print('------------------------------')
    for X in range(1, NumPoints + 1) :
        print('|',X,' |',Time[X], ' |',Magnitude[X],' |')			#X:6 Time[X]:7 Magnitude[X]:10
    print('\n')
    return Cmag, Cphase
#end FourierValues

#****************************************************************************
def FourierAnal():
#****************************************************************************

#var
#   Cmag,Cphase : extendedvector;
#   Again : boolean;
#   K : integer;
#   FourierCoefDat : File of extended;

    Again = True
    while Again == True :
        FourierCoefDat =open('FourierCoef.dat','w')
        os.system('cls')
        print('This program executes a fourier analysis')
        print('-----------------------------------------------------------')
        Cmag, Cphase = FourierValues()
        print('\n')
        print('| Harmonic | C_Mag     | C_Phase    |')
        print('-------------------------------------')
        print(FourierCoefDat,NumHarmonics,Period)
        for K in range(NumHarmonics) :
            print('|',K,' |',Cmag[K], ' |',Cphase[K],' |')		#K:9 Cmag[K]:10 Cphase[K]:10
            print(FourierCoefDat,K,Cmag[K],Cphase[K],end='')
        #end for
        print('(Coefficient data written to file "FourierCoefDat".)')
        print('\n')
        FourierCoefDat.close()
        Again = GetResponse('Another fourier analysis (y/n)? ')
    #end while
#end FourierAnal

