unit beatwork;

interface

procedure LineImped (var LineImp : extended; Prop,LowCap,UpCap1,UpCap2,FringeCap1,FringeCap2 : extended);
procedure PropConst (var IntProp : extended; LowCap, UpCap1, UpCap2, FringeCap1, FringeCap2 : extended);
procedure LinCap (var LowCap, UpCap, FringeCap : extended);
procedure EvenLineCap ( var EvenUpCap, EvenFringeCap : extended);
procedure OddLineCap ( var OddUpCap, OddFringeCap : extended);
function IntCapac( IntImped,IntProp : extended) : extended;
function IntInduct( IntImped,IntProp : extended) : extended;
function IntResist( TraceThick,TraceWidth : extended) : extended;
function LoadAdjust (IntCap, DistCap : extended) : extended;
procedure reflectcoef;
procedure StripLineAnal;
procedure DualStripAnal;
procedure MicroStripAnal;
procedure Crosstalk;
procedure DistCapAnal;
procedure StatIterNum;
procedure StripLineStatAnal;
procedure MicroStripStatAnal;
procedure DualStripStatAnal;
procedure StatAnal;
procedure SetUnit;
procedure LadderNetAnal;


implementation
 uses crt, beatio, beatinc, beatmath;

 
(**************************************************************************)
function RNDNormal(center, sigma :extended) : extended;
(*
    This routine uses the built-in random number generator (which generates
    a uniform distribution between 0 and +1) and transforms this into
    a normal distribution with parameters mean (center) and standard
    deviation (sigma).
    This routine was derived from a similar algorithm by D.E. Knuth in
    "The Art of Computer Programming", volume 2, chapter 3.4.1,
    algorithm P                                                           *)
(**************************************************************************)

var u1,u2,v1,v2,s : real;

begin
  repeat
    u1 := random(5);   (* The argument of random0() is irrelevant *)
    u2 := random(5);
    v1 := 2*u1-1;   (* Shift distribution from 0 .. +1  to  -1 .. +1 *)
    v2 := 2*u2-1;
    s := v1*v1 + v2*v2;
  until s<1;
  RNDNormal := v1 * sqrt((-2)*ln(s)/s) * sigma + center;
end; (* RNDNormal *)

(****************************************************************************)
procedure LineImped;
(*                                                                          *)
(* Calculates the line impedance of a microstrip trace using the model      *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs". He breaks the line capacitance up into:             *)
(*                                                                          *)
(*   Cppu := the upper plate capacitance (UpCap1 and UpCap2)                *)
(*   Cpp  := the lower plate capacitance (LowCap)                           *)
(*   Cf1  & Cf2 := the fringe capacitances (FringeCap1 & FringeCap2)        *)
(*                                                                          *)
(* The capacitance values passed depend on the presense of adjacent traces  *)
(* such as bus structures or whether we are calculated the odd or even mode *)
(* impednaces.                                                              *)
(*                                                                          *)
(* The impedance is then equal to the propagation constant divided by the   *)
(* total line capacitance (TotalCap).  The propagation constant passed      *)
(* will be different for different line coatings and odd and even modes.    *)
(*                                                                          *)
(****************************************************************************)

var
   TotalCap : real;

begin
   TotalCap := LowCap + FringeCap1 + FringeCap2 + UpCap1 + UpCap2;
   LineImp := (Prop*1e-9) / (TotalCap*1e-12);
end (* LineImped *);

(****************************************************************************)
procedure PropConst;
(*                                                                          *)
(* Calculates the propagation constant of a microstrip trace using the model*)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs". He breaks the line capacitance up into:             *)
(*                                                                          *)
(*   Cppu := the upper plate capacitance (UpCap1 and UpCap2)                *)
(*   Cpp  := the lower plate capacitance (LowCap)                           *)
(*   Cf1  & Cf2 := the fringe capacitances (FringeCap1 & FringeCap2)        *)
(*                                                                          *)
(* The capacitance values passed depend on the presense of adjacent traces  *)
(* such as bus structures or whether we are calculated the odd or even mode *)
(* impednaces.                                                              *)
(*                                                                          *)
(* The impedance is then equal to the propagation constant divided by the   *)
(* total line capacitance (TotalCap).  The propagation constant passed      *)
(* will be different for different line coatings and odd and even modes.    *)
(*                                                                          *)
(****************************************************************************)

var
   Cap,
   VelSub,
   VelConst : real;

begin
   Cap := LowCap + FringeCap1 + FringeCap2 + UpCap1 + UpCap2;
   VelSub :=1/(1 + ((FringeCap1 + FringeCap2)*(DiConst/EffDiConst - 1) + (UpCap1 + UpCap2)*(sqrt(DiConst) - 1))/Cap);
   VelConst :=1/sqrt(1 + sqr(VelSub)*(DiConst -1));
   IntProp :=1/(SpeedOfLight * VelConst) * 1e9;
end (* PropConst *);


(****************************************************************************)
procedure LinCap;
(*                                                                          *)
(* Calculates the capacitances of a microstrip trace using the model        *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs" for an isolated conductor. He breaks the line        *)
(* capacitance up into:                                                     *)
(*                                                                          *)
(*   Cppu := the upper plate capacitance                                    *)
(*   Cpp  := the lower plate capacitance                                    *)
(*   Cf   := the fringe capacitance                                         *)
(*                                                                          *)
(****************************************************************************)

var
   CommonTerm : real;

begin
   CommonTerm :=DiConst / (SpeedOfLight * ImpedOfFreeSpace);
   LowCap := CommonTerm * TraceWidth / TraceHeight * 1e12;
   UpCap := 2/6 * (LowCap/sqrt(DiConst));
   FringeCap := CommonTerm*(EffDiConst/DiConst) * pi / ln(4*TraceHeight/TraceThick) * 1e12;
end (* LinCap *);

(****************************************************************************)
procedure EvenLineCap;
(*                                                                          *)
(* Calculates the capacitances of a microstrip trace using the model        *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs" two conductors - even-mode.  He defines two new line *)
(* capacitances:                                                            *)
(*                                                                          *)
(*   Cppue := the even-mode upper plate capacitance (EvenUpCap)             *)
(*   Cfe  := the even-mode fringe capacitance (EvenFringeCap)               *)
(*                                                                          *)
(****************************************************************************)

var
   EvenCoupConst : real;

begin
   EvenCoupConst :=1 / ((TraceWidth / TraceSpacing) + 1);
   EvenUpCap := UpCap * EvenCoupConst;
   EvenFringeCap := FringeCap * EvenCoupConst;
end (* EvenLineCap *);

(****************************************************************************)
procedure OddLineCap;
(*                                                                          *)
(* Calculates the capacitances of a microstrip trace using the model        *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs" two conductors - odd-mode.  He defines two new line  *)
(* capacitances:                                                            *)
(*                                                                          *)
(*   Cppuo := the odd-mode upper plate capacitance (OddUpCap)               *)
(*   Cfo  := the odd-mode fringe capacitance (OddFringeCap)                 *)
(*                                                                          *)
(****************************************************************************)

var
   OddCoupConst,
   OddFringeDenom,
   CommonTerm : real;

begin
   CommonTerm :=DiConst / (SpeedOfLight * ImpedOfFreeSpace);
   OddCoupConst := 1 / ((TraceSpacing / TraceWidth) + 1);
   OddUpCap := 8/6 * ((CommonTerm * OddCoupConst)/sqrt(DiConst)) * 1e12;
   OddFringeDenom :=ln(4*TraceSpacing * tanh(4*TraceHeight/TraceSpacing) / (pi*TraceThick));
   OddFringeCap := (CommonTerm*(EffDiConst/DiConst)*pi/OddFringeDenom)*1e12;
end (* OddLineCap *);

(****************************************************************************)
function IntCapac;
(* Calculates the capacitance of a trace per unit of measure *)
(****************************************************************************)

begin
   IntCapac := IntProp/IntImped;
end; (* IntCapac *)

(****************************************************************************)
function IntInduct;
(* Calculates the inductance of a trace per unit of measure *)
(****************************************************************************)

begin
   IntInduct := IntImped * IntProp;
end; (* IntInduct *)

(****************************************************************************)
function IntResist;
(* Calculates the trace resist in mohms per inch of copper trace *)
(****************************************************************************)

begin
   IntResist := ResistCopper/(TraceThick * TraceWidth)*1000;
end; (* IntResist *)

(****************************************************************************)
function LoadAdjust;
(****************************************************************************)

(* This function calculates the constant used to adjust the impedance or  *)
(* propagation delay based on the added load capacitance per unit length *)

begin
   LoadAdjust := sqrt(1 + (DistCap/IntCap));
end;

(****************************************************************************)
procedure reflectcoef;
(****************************************************************************)

(* This program calculates the reflection coefficient given the load
impedance and the line impedance *)

var

   Again : boolean;

begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('This program calculates the reflection coefficient');
      writeln ('-----------------------------------------------------------');
      writeln;
      GetParam('Line impedance ? ',2,LineImp);
      GetParam('Load impedance ? ',2,LoadImp);
      ReflectionCoef := (LoadImp - LineImp)/(LoadImp + LineImp);
      writeln ('Reflection coeffiecient = ', ReflectionCoef:1:2);
      writeln ;
      GetResponse('Another reflection calculation (y/n)?',Again);
   end;
end;

(****************************************************************************)
procedure StripLineAnal;
(*                                                                          *)
(* Determines the impedance and propagation constant of a stripline         *)
(* using the standard equation found in Motorola's MECL Handbook or a       *)
(* hundred other books.                                                     *)
(*                                                                          *)
(* Please keep in mind that the same equations used in this procedure are
   also contained in StripLineStatAnal.                                     *)
(****************************************************************************)

var
   Cap, Induct,
   PlaneSpace,
   ImpFactor1,ImpFactor2 : real;
   Again : boolean;

begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('Stripline analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      GetTraceParam;
      PlaneSpace := 2*TraceHeight + TraceThick;
      ImpFactor1 := 60/sqrt(DiConst);
      ImpFactor2 := ln(4*PlaneSpace/(0.67*pi*TraceWidth*(0.8 + TraceThick/TraceWidth)));
      IntImped := ImpFactor1 * ImpFactor2;
      IntProp := 1.017*sqrt(DiConst);
      Cap := IntCapac(IntImped, IntProp)*1e3/12;
      Induct := IntInduct(IntImped, IntProp)/12;
      Resist := IntResist(TraceThick, TraceWidth);
      LineAnalOut(IntImped, IntProp, Cap, Induct, Resist);
      GetResponse('Another stripline analysis (y/n)?',Again);
   end;
end; (* StripLineAnal *)

(****************************************************************************)
procedure DualStripAnal;
(*                                                                          *)
(* Determines the impedance and propagation constant of dual-stripline      *)
(* using the equation found the IPC Standard "Design standard for electronic*)
(* packaging utilizing high speed techniques".                              *)
(*                                                                          *)
(* Please keep in mind that the same equations used in this procedure are
   also contained in DualStripStatAnal.                                     *)
(****************************************************************************)

var
   Cap, Induct,
   ImpFactor1,ImpFactor2, ImpFactor3 : real;
   Again : boolean;

begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('Dual-stripline analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      GetTraceParam;
      GetParam('What is the signal plane separation? ',1,SigPlaneSep);
      ImpFactor1 := 80/sqrt(DiConst);
      ImpFactor2 := ln(1.9*(2*TraceHeight + TraceThick)/(0.8*TraceWidth + TraceThick));
      ImpFactor3 := 1 - (TraceHeight/(4*(TraceHeight + SigPlaneSep + TraceThick)));
      IntImped := ImpFactor1 * ImpFactor2 * ImpFactor3;
      IntProp := 1.017*sqrt(DiConst);
      Cap := IntCapac(IntImped, IntProp)*1e3/12;
      Induct := IntInduct(IntImped, IntProp)/12;
      Resist := IntResist(TraceThick, TraceWidth);
      LineAnalOut(IntImped, IntProp, Cap, Induct, Resist);
      GetResponse('Another dual-stripline analysis (y/n)?',Again);
   end;
end; (* DualStripAnal *)

(****************************************************************************)
procedure MicroStripAnal;
(*                                                                          *)
(* Calculates the line impedance of a microstrip trace using the model      *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs" for an isolated conductor. He breaks the line        *)
(* capacitance up into:                                                     *)
(*                                                                          *)
(*   Cppu := the upper plate capacitance (UpCap)                            *)
(*   Cpp  := the lower plate capacitance (LowCap)                           *)
(*   Cf   := the fringe capacitances (FringeCap)                            *)
(*                                                                          *)
(* Corrections to the propagation constant (because of solder mask have     *)
(* been added based on emperical data from GS2 boards.  The correction      *)
(* factor was derived similar to the techinique in "Characteristics of      *)
(* Microstrip Transmission Lines", by H. R. Kaupp.                          *)
(*                                                                          *)
(* Please keep in mind that the same equations used in this procedure are
   also contained in MicroStripStatAnal.                                    *)
(****************************************************************************)

var
   Cap, Induct : real;
   Again: boolean;
   temp : char;

begin
   Again :=true;
   while Again = true do
   begin
      ClrScr;
      writeln ('Micro-stripline analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      GetTraceParam;
      write ('Solder mask? (w-wet, d-dry, n-none)  [', SoldMask,']');
      repeat
      	temp := Readkey;
      until(temp = 'n') OR (temp = 'w') OR (temp = 'd') OR (temp = ^M);
      if (temp <> ^M) then SoldMask := temp;
      case SoldMask of
         'n' : EffDiConst := 0.475*DiConst + 0.67;
         'w' : EffDiConst := 0.58*DiConst + 0.55;
         'd' : EffDiConst := DiConst;
      end;
      LinCap (LowCap, UpCap, FringeCap);
      PropConst (IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap);
      LineImped (IntImped, IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap);
      Cap := (2*(UpCap + FringeCap) + LowCap)/12;
      Induct := IntInduct(IntImped, IntProp)/12;
      Resist := IntResist(TraceThick, TraceWidth);
      LineAnalOut(IntImped, IntProp, Cap, Induct, Resist);
      GetResponse('Another micro-stripline analysis (y/n)?',Again);
   end;
end;

(****************************************************************************)
procedure Crosstalk;
(*                                                                          *)
(* This procedure calculates the backward and forward crosstalk for         *)
(* microstrip.  It allows for bus structures, distributed capacitance,      *)
(* termination values, different solder mask, and interlaced grounds.       *)
(*                                                                          *)
(* Several papers were used to derive the crosstalk calculation algorithms  *)
(* used in this procedure.  First, the microstrip characteristics are for   *)
(* even and odd modes are determined using the models defined by Schwarzmann*)
(* in his paper "Microstrip plus equations adds up to fast designs".        *)
(* Second, papers by Ivor Catt, "Crosstalk in Digital Systems" and John     *)
(* Defalco were used for basic crosstalk theory and crosstalk reflection    *)
(* analysis.  Data in these papers were also used for verification of the   *)
(* single line to line crosstalk.  Extrapolations to multiple lines and     *)
(* ground interlacing were primarily intuitive derviations and have been    *)
(* verified against GS2 processor board and backplane data.                 *)
(*                                                                          *)
(* Corrections to the propagation constant (because of solder mask have     *)
(* been added based on emperical data from GS2 boards.  The correction      *)
(* factor was derived similar to the techinique in "Characteristics of      *)
(* Microstrip Transmission Lines", by H. R. Kaupp.                          *)
(*                                                                          *)
(****************************************************************************)

var
   TraceSpace,
   RiseTime,
   VoltStep,
   BackVolt,
   ForVolt,
   BackPulWid,
   ForPulWid,
   VoltOdd,
   FCrC,
   BCrC : extended;
   Count,
   CountLimit,
   ActLines : integer;
   BusStruct,
   Update,
   Again,IntGnd : boolean;
   SoldMask : char;

begin
   Again :=true;
   VoltStep := 3.0; (*v*)
   RiseTime := 2.8; (*ns*)
   TraceLength := 10.5; (*in*)
   while Again = true do
   begin
      IntGnd := false;
      BusStruct := false;
      ActLines := 1;
      BCrC := 0;
      FCrC := 0;
      BackCrossConst := 0;
      ForCrossConst := 0;
      BackVolt := 0;
      ForVolt := 0;
      VoltOdd := 0;
      SoldMask := 'w';
      EffDiConst := 0.58*DiConst + 0.55; (* Set for wet solder mask *)
      ClrScr;
      writeln ('Crosstalk Analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      TraceParamOut;
      GetResponse ('New trace parameters (y/n)? ', Update );
      if Update = true then
         begin
            GetTraceParam;

            (* Adjust the dielectric constant for solder mask *)

            write ('Solder mask? (w-wet, d-dry, n-none) ', SoldMask);
            readln (SoldMask);
            case SoldMask of
               'n' : EffDiConst := 0.475*DiConst + 0.67;
               'w' : EffDiConst := 0.58*DiConst + 0.55;
               'd' : EffDiConst := DiConst;
            end
      end;

      (* Request data essential for crosstalk analysis *)

      GetParam ('Trace spacing from edge to edge ?',1, TraceSpacing);
      GetParam ('Trace length ?',1, TraceLength);
      GetParam ('What is the distributed cap.?',3, DistCap);
      GetParam ('Signal Rise time ?',4, RiseTime);
      GetParam ('Voltage step ?',5, VoltStep);
      GetParam ('What is the load impedance ? ',2, LoadImp);
      GetResponse ('Interlaced grounds (y/n)? ',  IntGnd);
      GetResponse ('Bus Structure (y/n)? ',  BusStruct);

      (* For a bus structure *)

      if BusStruct = true then
         begin

         (* Request the number of active lines *)

         writeln;
         write ('Number of active lines (1,2,4,6)? ', '[', ActLines:1,' ]');
         readln (ActLines);
         if (IntGnd = true) or (ActLines = 1) then
            CountLimit := 1
          else
            CountLimit := ActLines div 2;

         (* For the number of active lines divided by two, interatively add *)
         (* up the crosstalk constants                                      *)

         for Count := CountLimit downto 1 do
            begin
            TraceSpace := TraceSpacing;
            TraceSpacing := Count*TraceSpacing + (Count-1)*TraceWidth;
            LinCap ( LowCap, UpCap, FringeCap);
            EvenLineCap ( EvenUpCap, EvenFringeCap);
            OddLineCap (OddUpCap, OddFringeCap);
            PropConst (EvenIntProp, LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap);
            PropConst (OddIntProp, LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap);
            LineImped (EvenLineImp, EvenIntProp, LowCap, EvenUpCap, EvenUpCap, EvenFringeCap, EvenFringeCap);
            LineImped (OddLineImp, OddIntProp, LowCap, OddUpCap, OddUpCap, OddFringeCap, OddFringeCap);
            BCrC := (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp);
            if BCrC >= 0 then
               BackCrossConst := BackCrossConst + BCrC;
            FCrC := (EvenIntProp - OddIntProp);
            if FCrC >= 0 then
               ForCrossConst := ForCrossConst + FCrC;
            TraceSpacing := TraceSpace
            end (* Loop *);

            (* If bus structure and interlaced grounds then iteratively add *)
            (* the squares of the backward constants and divide the odd mode*)
            (* voltage by 2                                                 *)

            if IntGnd = true then
               begin

               (* Adjust backward constant for a single adjacent bus trace  *)

               BCrC := BackCrossConst/2;

               BackCrossConst := 0;
               if ActLines >= 2 then
                  CountLimit := ActLines div 2;
               for Count := CountLimit downto 1 do
                  begin
                  BCrC := sqr(BCrC);
                  BackCrossConst := BackCrossConst + BCrC;
                  VoltOdd := VoltOdd/4 + VoltStep/4
                  end;

               (* Correct for bus symmetry *)

               BackCrossConst := BackCrossConst*2;

               end
              else (* if no interlaced ground *)
               VoltOdd := VoltStep/2;

            if ActLines = 1 then (* Correct for no bus symmetry *)
               BackCrossConst := BackCrossConst/2;

         end (*Bustruct = true *)

       else (* BusStruct = false *)
         begin
            LinCap ( LowCap, UpCap, FringeCap);
            EvenLineCap ( EvenUpCap, EvenFringeCap);
            OddLineCap (OddUpCap, OddFringeCap);
            PropConst (EvenIntProp, LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap);
            PropConst (OddIntProp, LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap);
            LineImped (EvenLineImp, EvenIntProp, LowCap, UpCap, EvenUpCap, FringeCap, EvenFringeCap);
            LineImped (OddLineImp, OddIntProp, LowCap, UpCap, OddUpCap, FringeCap, OddFringeCap);
            BackCrossConst := (EvenLineImp - OddLineImp) / (EvenLineImp + OddLineImp);
            ForCrossConst := (EvenIntProp - OddIntProp);

(* If not bus structure but interlaced ground *)

            if IntGnd = true then
               begin
                  BackCrossConst := sqr(BackCrossConst);
                  VoltOdd := VoltOdd/4 + VoltStep/4
               end
             else
               VoltOdd := VoltStep/2;  (* End interlaced ground *)
         end (* BusStruct = false *);

      (* Determine the line impedance *)

      LineImp := sqrt(EvenLineImp * OddLineImp);

      (* Determine the max. backward crosstalk amplitude and pulse width *)

      BackVolt := BackCrossConst*VoltStep;
      BackPulWid := 2*EvenIntProp*TraceLength/12;

      (* Adjust the amplitude for the edge rate and trace length if needed *)

      if  RiseTime > 2*(EvenIntProp*TraceLength/12) then
         BackVolt := BackVolt*(2*(EvenIntProp*TraceLength/12)/RiseTime);

      (* Determine the forward crosstalk amplitude and pulse width *)

      ForPulWid := RiseTime;
      if (ForCrossConst*TraceLength/12) > RiseTime then
         ForVolt := VoltOdd
       else
         ForVolt := ((TraceLength/12)*ForCrossConst*VoltOdd)/RiseTime;

(* Correct for termination mismatch *)

      ReflectionCoef := (LoadImp - LineImp)/(LoadImp + LineImp);
      BackVolt := BackVolt * (1 + ReflectionCoef);
      ForVolt := ForVolt *  (1 + ReflectionCoef);

(* Output the test conditions and results *)

      ClrScr;
      writeln ('Test Parameters');
      writeln ('-------------------------');
      writeln ('RiseTime:      ',RiseTime:3:2,'ns');
      writeln ('Voltage Step:  ',VoltStep:4:2,'v');
      writeln ('Dist. Cap.:    ',DistCap:4:2,' pf/in');
      writeln ('Trace Length:  ',TraceLength:4:2);
      if IntGnd = true then
        writeln ( 'Interlaced grounds');
      writeln;
      writeln ('Crosstalk Data');
      writeln ('-------------------------');
      writeln ('Backward Crosstalk Constant:    ',BackCrossConst:4:3);
      writeln ('Backward Crosstalk Voltage:     ',BackVolt:4:3,' v');
      writeln ('Backward Crosstalk Pulse Width: ',BackPulWid:4:3,' ns');
      writeln ('Forward Crosstalk Constant:     ',ForCrossConst:4:3,' ns/ft');
      writeln ('Forward Crosstalk Voltage:      ',ForVolt:4:3,' v');
      writeln ('Forward Crosstalk Pulse Width:  ',ForPulWid:4:3,' ns');
      writeln ('Even Line Impedance:            ',EvenLineImp:4:2,' ohms');
      writeln ('Odd Line Impedance:             ',OddLineImp:4:2,' ohms');
      writeln ('Even Prop Const:                ',EvenIntProp:4:3,' ns/ft');
      writeln ('Odd Prop Const:                 ',OddIntProp:4:3,' ns/ft');
      writeln;
      GetResponse('Another crosstalk analysis? (y/n) ',Again);
   end;
end; (* Crosstalk *)


(****************************************************************************)
procedure DistCapAnal;
(*
   Determines the effects of distributed capacitances on effective
   impediance and propagation delay of a transmission line. The equations
   can be found in any applicable textbook and also easily be derived.      *)
(****************************************************************************)

var
   Again : boolean;

begin (* Distributed Capacitance Analysis *)

   Again := true;
   while Again =true do
   begin
      ClrScr;
      writeln ('Calculates the effective impedance and prop delay');
      writeln ('-----------------------------------------------------------');
      writeln;
      GetParam('What is the intrinsic impedance ?',2,IntImped);
      GetParam('What is the intrinsic delay ? ',6,IntProp);
      GetParam('What is the distributed capacitance ?',3,DistCap);
      IntCap := IntCapac(IntImped, IntProp)*1e3/12;
      EffImped := IntImped / LoadAdjust(IntCap, DistCap);
      EffProp := IntProp * LoadAdjust(IntCap, DistCap);
      writeln;
      writeln ('Line analysis:');
      writeln ('--------------');
      writeln ('Impedance (ohms):                = ',EffImped:3:1);
      writeln ('Propagation Delay (ns/ft):       = ',EffProp:2:2);
      writeln ('Intrinsic Capacitance (pf/in):   = ',IntCap:2:2);
      writeln ('Distributed Capacitance (pF/in): = ',DistCap:2:2);
      writeln;
      GetResponse('Another calculation (y/n)? ',Again);
   end;
end;



(**************************************************************************)
procedure StatIterNum;
(*
    Asks the user for the number of iterations which the statistics
    routines should run to obtain a normal distribution of the output
    parameters.                                                           *)
(**************************************************************************)

var answer : boolean;
var NumIterations, IterationsMax : integer;

begin
  repeat
    begin
      GetIParam('Enter number of iterations : ',NumIterations);
      if (NumIterations <= 0) or (NumIterations > IterationsMax) then begin
        writeln;
        writeln ('The number of iterations must be more than 1.');
        writeln ('If you want to exceed ',IterationsMax,' Iterations,');
        writeln ('you will have to change the constant "IterationsMax"');
        writeln ('in "beat.h" and recompile the program.');
        writeln;
        GetResponse ('Hit >RETURN< to continue',answer);
      end;
    end;
  until (NumIterations >0) and (NumIterations <= IterationsMax);
end;


(**************************************************************************)
procedure StripLineStatAnal;
(*                                                                          *)
(* Determines the impedance and propagation constant of a stripline         *)
(* using the standard equation found in Motorola's MECL Handbook or a       *)
(* hundred other books.                                                     *)
(*                                                                          *)
(* Containes the same equations as StripLineAnal, however this routine
   is controlled by some statistics code.                                   *)
(****************************************************************************)

var
   Cap,CapMean,CapSigma,Induct,InductMean,InductSigma,
   ResistMean,ResistSigma,
   PlaneSpace,
   ImpFactor1,ImpFactor2 : real;
   i : integer;
   Again : boolean;

begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('S t a t i s t i c a l    Strip Line Analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      StatIterNum;
      GetTraceStatParam;
      writeln;
      writeln ('Working');

      for i := 1 to NumIterations do begin         (* Main Loop *)
        TraceThickVal := RNDNormal(TraceThickMean,TraceThickSigma);  (* Get *)
        TraceWidthVal := RNDNormal(TraceWidthMean,TraceWidthSigma);  (*Value*)
        TraceHeightVal := RNDNormal(TraceHeightMean,TraceHeightSigma);(*for*)
        DiConstVal := RNDNormal(DiConstMean,DiConstSigma);  (*each parameter*)

        PlaneSpace := 2*TraceHeightVal + TraceThickVal; (*calculate output*)
        ImpFactor1 := 60/sqrt(DiConstVal);  (*for these input data *)
        ImpFactor2 := ln(4*PlaneSpace/(0.67*pi*TraceWidthVal*(0.8 + TraceThickVal/TraceWidthVal)));
        IntImped := ImpFactor1 * ImpFactor2;
        IntProp := 1.017*sqrt(DiConstVal);
        Cap := IntCapac(IntImped, IntProp)*1e3/12;
        Induct := IntInduct(IntImped, IntProp)/12;
        Resist := IntResist(TraceThickVal, TraceWidthVal);

        StatData[1][i] := IntImped;   (* store resulting data *)
        StatData[2][i] := IntProp;
        StatData[3][i] := Cap;
        StatData[4][i] := Induct;
        StatData[5][i] := Resist;
      end;    (* Main Loop *)

      IntImpedMean := 0;  (* initialize variables to determine mean value *)
      IntPropMean := 0;   (* of each output parameter *)
      CapMean := 0;
      InductMean := 0;
      ResistMean := 0;
      for i := 1 to NumIterations do begin  (* determine mean *)
        IntImpedMean := IntImpedMean + StatData[1][i];
        IntPropMean := IntPropMean + StatData[2][i];
        CapMean := CapMean + StatData[3][i];
        InductMean := InductMean + StatData[4][i];
        ResistMean := ResistMean + StatData[5][i];
      end;
      IntImpedMean := IntImpedMean / NumIterations;
      IntPropMean := IntPropMean / NumIterations;
      CapMean := CapMean/ NumIterations;
      InductMean := InductMean / NumIterations;
      ResistMean := ResistMean / NumIterations;

      IntImpedSigma := 0;  (* initialize variables for determining *)
      IntPropSigma := 0;   (* standard deviation for each output parameter *)
      CapSigma := 0;
      InductSigma := 0;
      ResistSigma := 0;
      for i := 1 to NumIterations do begin  (* determine standard deviation *)
        IntImpedSigma := IntImpedSigma + sqr(StatData[1][i]-IntImpedMean);
        IntPropSigma := IntPropSigma + sqr(StatData[2][i]-IntPropMean);
        CapSigma := CapSigma + sqr(StatData[3][i]-CapMean);
        InductSigma := InductSigma + sqr(StatData[4][i]-InductMean);
        ResistSigma := ResistSigma + sqr(StatData[5][i]-ResistMean);
      end;
      IntImpedSigma := sqrt(IntImpedSigma / (NumIterations-1));
      IntPropSigma := sqrt(IntPropSigma / (NumIterations-1));
      CapSigma := sqrt(CapSigma/ (NumIterations-1));
      InductSigma := sqrt(InductSigma / (NumIterations-1));
      ResistSigma := sqrt(ResistSigma / (NumIterations-1));
      LineAnalStatOut(IntImpedMean,IntImpedSigma, IntPropMean,IntPropSigma,
        CapMean,CapSigma, InductMean,InductSigma, ResistMean,ResistSigma);

      GetResponse('Another statistical stripline analysis (y/n)?',Again);
   end;
end; (* StripLineStatAnal *)



(**************************************************************************)
procedure MicroStripStatAnal;
(*                                                                          *)
(* Calculates the line impedance of a microstrip trace using the model      *)
(* defined by Schwarzmann in his paper "Microstrip plus equations adds      *)
(* up to fast designs" for an isolated conductor. He breaks the line        *)
(* capacitance up into:                                                     *)
(*                                                                          *)
(*   Cppu := the upper plate capacitance (UpCap)                            *)
(*   Cpp  := the lower plate capacitance (LowCap)                           *)
(*   Cf   := the fringe capacitances (FringeCap)                            *)
(*                                                                          *)
(* Corrections to the propagation constant (because of solder mask have     *)
(* been added based on emperical data from GS2 boards.  The correction      *)
(* factor was derived similar to the techinique in "Characteristics of      *)
(* Microstrip Transmission Lines", by H. R. Kaupp.                          *)
(*                                                                          *)
(*  Containes the same equations as MicroStripAnal, however this routine
    is controlled by some statistics code.
    For comments on program statements, please refer to StripLineStatAnal,
    which is structured similarly                                           *)
(****************************************************************************)

var
   Cap,CapMean,CapSigma, Induct,InductMean,InductSigma,
   ResistMean,ResistSigma : real;
   i : integer;
   Again : boolean;
   temp : char;
   begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('S t a t i s t i c a l    Microstrip Line Analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      StatIterNum;
      GetTraceStatParam;
      write ('Solder mask ? (w-wet, d-dry, n-none)   [',SoldMask,']');

      repeat
	temp := Readkey;
      until(temp = 'n') OR (temp = 'w') OR (temp = 'd') OR (temp = ^M);
      if (temp <> ^M) then SoldMask := temp;

                  (* Here I cannot use TraceThickVal etc. as in the other
                  statistical routines, because the called procedures,
                  such as LinCap etc. expect TraceThick etc.
                  In order not to destroy the defaults contained in
                  TraceThick etc. by putting the output of the random
                  generator in these variables, I save them first and
                  then restore them to their original value lateron.   *)

      TraceThickVal := TraceThick;
      TraceWidthVal := TraceWidth;
      TraceHeightVal := TraceHeight;
      DiConstVal := DiConst;
      writeln;
      writeln ('Working');

      for i := 1 to NumIterations do begin
        TraceThick := RNDNormal(TraceThickMean,TraceThickSigma);
        TraceWidth := RNDNormal(TraceWidthMean,TraceWidthSigma);
        TraceHeight := RNDNormal(TraceHeightMean,TraceHeightSigma);
        DiConst := RNDNormal(DiConstMean,DiConstSigma);

        case SoldMask of
          'n' : EffDiConst := 0.475*DiConst + 0.67;
          'w' : EffDiConst := 0.58*DiConst + 0.55;
          'd' : EffDiConst := DiConst;
        end;

        LinCap (LowCap, UpCap, FringeCap);
        PropConst (IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap);
        LineImped (IntImped, IntProp, LowCap, UpCap, UpCap, FringeCap, FringeCap);
        Cap := (2*(UpCap + FringeCap) + LowCap)/12;
        Induct := IntInduct(IntImped, IntProp)/12;
        Resist := IntResist(TraceThick, TraceWidth);

        StatData[1][i] := IntImped;
        StatData[2][i] := IntProp;
        StatData[3][i] := Cap;
        StatData[4][i] := Induct;
        StatData[5][i] := Resist;
      end;

      TraceThick := TraceThickVal;
      TraceWidth := TraceWidthVal;
      TraceHeight := TraceHeightVal;
      DiConst := DiConstVal;

      IntImpedMean := 0;
      IntPropMean := 0;
      CapMean := 0;
      InductMean := 0;
      ResistMean := 0;
      for i := 1 to NumIterations do begin
        IntImpedMean := IntImpedMean + StatData[1][i];
        IntPropMean := IntPropMean + StatData[2][i];
        CapMean := CapMean + StatData[3][i];
        InductMean := InductMean + StatData[4][i];
        ResistMean := ResistMean + StatData[5][i];
      end;
      IntImpedMean := IntImpedMean / NumIterations;
      IntPropMean := IntPropMean / NumIterations;
      CapMean := CapMean/ NumIterations;
      InductMean := InductMean / NumIterations;
      ResistMean := ResistMean / NumIterations;

      IntImpedSigma := 0;
      IntPropSigma := 0;
      CapSigma := 0;
      InductSigma := 0;
      ResistSigma := 0;
      for i := 1 to NumIterations do begin
        IntImpedSigma := IntImpedSigma + sqr(StatData[1][i]-IntImpedMean);
        IntPropSigma := IntPropSigma + sqr(StatData[2][i]-IntPropMean);
        CapSigma := CapSigma + sqr(StatData[3][i]-CapMean);
        InductSigma := InductSigma + sqr(StatData[4][i]-InductMean);
        ResistSigma := ResistSigma + sqr(StatData[5][i]-ResistMean);
      end;
      IntImpedSigma := sqrt(IntImpedSigma / (NumIterations-1));
      IntPropSigma := sqrt(IntPropSigma / (NumIterations-1));
      CapSigma := sqrt(CapSigma/ (NumIterations-1));
      InductSigma := sqrt(InductSigma / (NumIterations-1));
      ResistSigma := sqrt(ResistSigma / (NumIterations-1));

      LineAnalStatOut(IntImpedMean,IntImpedSigma, IntPropMean,IntPropSigma,
        CapMean,CapSigma, InductMean,InductSigma, ResistMean,ResistSigma);
      GetResponse('Another statistical stripline analysis (y/n)?',Again);
   end;
end; (* MicroStripAnal *)



(**************************************************************************)
procedure DualStripStatAnal;
(*                                                                          *)
(* Determines the impedance and propagation constant of dual-stripline      *)
(* using the equation found the IPC Standard "Design standard for electronic*)
(* packaging utilizing high speed techniques".                              *)
(*                                                                          *)
(*  Containes the same equations as DualStripAnal, however this routine
    is controlled by some statistics code.
    For comments on program statements, please refer to StripLineStatAnal,
    which is structured similarly                                           *)
(****************************************************************************)

var
   Cap,CapMean,CapSigma, Induct,InductMean,InductSigma,
   ResistMean,ResistSigma,
   ImpFactor1,ImpFactor2, ImpFactor3 : real;
   i : integer;
   Again : boolean;

begin
   Again := true;
   while Again = true do
   begin
      ClrScr;
      writeln ('S t a t i s t i c a l    Dual-strip Line Analysis');
      writeln ('-----------------------------------------------------------');
      writeln;
      StatIterNum;
      GetTraceStatParam;
      SigPlaneSepMean := SigPlaneSep;  (* Get default value *)
      GetParam('What is the mean signal plane separation? ',1,SigPlaneSepMean);
      GetParam('What is the standard deviation? ',1,SigPlaneSepSigma);
      SigPlaneSep := SigPlaneSepMean;  (* Keep as default value *)
      writeln;
      writeln('Working');

      for i := 1 to NumIterations do begin
        TraceThickVal := RNDNormal(TraceThickMean,TraceThickSigma);
        TraceWidthVal := RNDNormal(TraceWidthMean,TraceWidthSigma);
        TraceHeightVal := RNDNormal(TraceHeightMean,TraceHeightSigma);
        DiConstVal := RNDNormal(DiConstMean,DiConstSigma);
        SigPlaneSepVal := RNDNormal(SigPlaneSepMean,SigPlaneSepSigma);


        ImpFactor1 := 80/sqrt(DiConstVal);
        ImpFactor2 := ln(1.9*(2*TraceHeightVal + TraceThickVal)/(0.8*TraceWidthVal + TraceThickVal));
        ImpFactor3 := 1 - (TraceHeightVal/(4*(TraceHeightVal + SigPlaneSepVal + TraceThickVal)));
        IntImped := ImpFactor1 * ImpFactor2 * ImpFactor3;
        IntProp := 1.017*sqrt(DiConstVal);
        Cap := IntCapac(IntImped, IntProp)*1e3/12;
        Induct := IntInduct(IntImped, IntProp)/12;
        Resist := IntResist(TraceThickVal, TraceWidthVal);

        StatData[1][i] := IntImped;
        StatData[2][i] := IntProp;
        StatData[3][i] := Cap;
        StatData[4][i] := Induct;
        StatData[5][i] := Resist;
      end;

      IntImpedMean := 0;
      IntPropMean := 0;
      CapMean := 0;
      InductMean := 0;
      ResistMean := 0;
      for i := 1 to NumIterations do begin
        IntImpedMean := IntImpedMean + StatData[1][i];
        IntPropMean := IntPropMean + StatData[2][i];
        CapMean := CapMean + StatData[3][i];
        InductMean := InductMean + StatData[4][i];
        ResistMean := ResistMean + StatData[5][i];
      end;
      IntImpedMean := IntImpedMean / NumIterations;
      IntPropMean := IntPropMean / NumIterations;
      CapMean := CapMean/ NumIterations;
      InductMean := InductMean / NumIterations;
      ResistMean := ResistMean / NumIterations;

      IntImpedSigma := 0;
      IntPropSigma := 0;
      CapSigma := 0;
      InductSigma := 0;
      ResistSigma := 0;
      for i := 1 to NumIterations do begin
        IntImpedSigma := IntImpedSigma + sqr(StatData[1][i]-IntImpedMean);
        IntPropSigma := IntPropSigma + sqr(StatData[2][i]-IntPropMean);
        CapSigma := CapSigma + sqr(StatData[3][i]-CapMean);
        InductSigma := InductSigma + sqr(StatData[4][i]-InductMean);
        ResistSigma := ResistSigma + sqr(StatData[5][i]-ResistMean);
      end;
      IntImpedSigma := sqrt(IntImpedSigma / (NumIterations-1));
      IntPropSigma := sqrt(IntPropSigma / (NumIterations-1));
      CapSigma := sqrt(CapSigma/ (NumIterations-1));
      InductSigma := sqrt(InductSigma / (NumIterations-1));
      ResistSigma := sqrt(ResistSigma / (NumIterations-1));

      LineAnalStatOut(IntImpedMean,IntImpedSigma, IntPropMean,IntPropSigma,
        CapMean,CapSigma, InductMean,InductSigma, ResistMean,ResistSigma);
      GetResponse('Another statistical stripline analysis (y/n)?',Again);
   end;
end; (* DualStripStatAnal *)



(**************************************************************************)
procedure StatAnal;
(**************************************************************************)

var Ende : boolean;

begin
  Ende := false;
  while Ende = false do begin
    Header := 'Statistical Analysis';
    OptArray[1] := 'Exit to Main Menue';
    OptArray[2] := 'Strip Line Analysis';
    OptArray[3] := 'Microstrip Line Analysis';
    OptArray[4] := 'Dual-Strip Line Analysis'; 
   (* OptArray[5] := 'Embedded Strip Line Analysis'; *)
    menu(4,Header,OptArray,SelOpt);
    case SelOpt of
      1 : Ende := true;
      2 : StripLineStatAnal;
      3 : MicroStripStatAnal;
      4 : DualStripStatAnal;
  (*    5 : EmbedMicroStripStatAnal; *)
    end;
  end;
end;


(**************************************************************************)
procedure SetUnit;
(*                                                                        *)
(*  This routine enables the user to select whether he wants to enter     *)
(*  his input data in the metric or in the imperial system of measurement *)
(*  units.                                                                *)
(*  Added 6/89 , Ulf Schlichtmann                                         *)
(**************************************************************************)

var
   UnitChar, temp : char;

begin     (* SetUnit *)
     ClrScr;
     writeln ('Set the Unit System for your input data');
     writeln ('---------------------------------------');
     writeln;
     writeln ('You may now select whether you want to input your data in ');
     writeln ('the Metric or in the Imperial system.');
     writeln;
     writeln ('Please keep in mind that the data in the library are in ');
     writeln ('the Imperial system');
     writeln;
     writeln ('Currently selected: ',base[UnitSys]);
     writeln;
     writeln;
     case UnitSys of
       1 : UnitChar := 'm';
       2 : UnitChar := 'i';
     end;
     write ('Metric or Imperial system?  (m or i)   [',UnitChar,'] ');

     repeat
      	temp := Readkey;
      until(temp = 'm') OR (temp = 'i') OR (temp = ^M);
      if (temp <> ^M) then UnitChar := temp;


	case UnitChar of
       'm' : UnitSys := 1;
       'i' : UnitSys := 2;
     end;
end;      (* SetUnit *)


(****************************************************************************)
procedure LadderNetAnal;
(* Completely modified 6/89, Ulf Schlichtmann *)
(* This procedure requests as input the line impedance and propagation delay
   constant of a line as well as the total length of the line and the rise
   time of the signal that needs to be analyzed.
   It then proceeds to compute the cutoff frequency of that signal and the
   number of RLC segments this line has to be split up into if it is to be
   modelled correctly by SPICE. The values for the R, L and C elements of each
   segment are also calcutlated and output.
   To calculate the number of required segments, a "rule of thumb" is used  *)
(****************************************************************************)

var
   Again:boolean;
   SegCap, SegInd, SegRes,  (* values per segment *)
   CornerFrequ :real;
   NumSeg:integer;


(***************************************************************************)
procedure GetNetInfo;
(***************************************************************************)

begin
     GetParam('What is the line impedance?',2,IntImped);
     GetParam('What is the propagation delay?',6,IntProp);
     GetParam('What is the intrinsic resistance?',10,Resist);
     GetParam('What is the line length?',1,TraceLength);
     GetParam('What is the rise time?',4,TRise);
end;



begin  (* LadderNetAnal *)
   Again := true;
   while Again = true do begin
     ClrScr;
     writeln ('Trace Pi Model Generation');
     writeln ('-----------------------------------------');
     writeln;
     GetNetInfo;
     CornerFrequ := 2/TRise;         (* Cutoff Frequency *)
     IntCap := IntProp*TraceLength/IntImped*1000/12;
                                     (*1000:Conversion to pF*)
                                     (*12: Conversion from ft to inch *)
     IntInd := IntProp*TraceLength*IntImped/12;
                                     (*12: Conversion from ft to inch *)
     NumSeg := trunc(5/2*CornerFrequ* sqrt(IntCap*IntInd)*sqrt(0.001))+1;
                                     (* "Rule of Thumb" *)
                                     (* sqrt(.001): unit correction factor *)
     writeln;
     writeln ('Trace Pi Model Analysis');
     writeln ('------------------------');
     writeln ('Calculations have determined the following number of segments.');
     writeln ('Confirm this number by hitting RETURN or change it.');
     GetIParam ('Number of segments:                ',NumSeg);

     SegCap := IntCap/NumSeg;        (* Capacitance per segment *)
     SegInd := IntInd/NumSeg;        (* Inductance per segment *)
     SegRes := Resist*TraceLength/NumSeg/1000;  (* Resistance per segment *)
                                     (* 1000 : Conversion mohms --> ohms *)

     writeln ('Capacitance per segment (pF):      ',SegCap:2:2);
     writeln ('Inductance per segment (nH):       ',SegInd:2:2);
     writeln ('Resistance per segment (ohms):     ',SegRes:2:2);
     writeln;

     GetResponse('One More Time !?',Again)
   end;
end;

end.


