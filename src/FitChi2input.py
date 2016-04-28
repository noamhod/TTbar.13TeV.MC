#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TF1, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TFitResultPtr
import os
import rootstyle

histos = {}

def adHist(name):
   histos.update({name:tfile.Get(name)})

def FitPlot(h,fname,xmin=0,xmax=0):
   print "--------------------- ",h.GetName()
   # h.Rebin(2)
   r = TFitResultPtr()
   if(xmin==xmax): r = h.Fit("gaus","MLES","")
   else:           r = h.Fit("gaus","MLES","",xmin,xmax)
   r.Print()
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   h.Draw()
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)
   print "--------------------- "
   return r

gROOT.LoadMacro( "src/Loader.C+" )
ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
tfile = TFile(path+"/histograms.mu.A.root","READ")

hfitnmae = path+"/histograms.mu.fits.pdf"

adHist("Matched:SelectedObjects:mjj-mW")
adHist("Matched:SelectedObjects:mjjj-mt")
adHist("Matched:SelectedObjects:mjjj-mjj-(mt-mW)")
adHist("Matched:SelectedObjects:mlvj-mt")
adHist("Matched:SelectedObjects:pTjjj-pTlvj")

adHist("Matched:WithSelection:mjj-mW")
adHist("Matched:WithSelection:mjjj-mt")
adHist("Matched:WithSelection:mjjj-mjj-(mt-mW)")
adHist("Matched:WithSelection:mlvj-mt")
adHist("Matched:WithSelection:pTjjj-pTlvj")

adHist("Matched:NoSelection:mjj-mW")
adHist("Matched:NoSelection:mjjj-mt")
adHist("Matched:NoSelection:mjjj-mjj-(mt-mW)")
adHist("Matched:NoSelection:mlvj-mt")
adHist("Matched:NoSelection:pTjjj-pTlvj")

r0_mW  = FitPlot(histos["Matched:SelectedObjects:mjj-mW"],hfitnmae+"(",-5,+5)
r0_mtH = FitPlot(histos["Matched:SelectedObjects:mjjj-mt"],hfitnmae,-8,+6)
r0_mWt = FitPlot(histos["Matched:SelectedObjects:mjjj-mjj-(mt-mW)"],hfitnmae,-4,+3)
r0_mtL = FitPlot(histos["Matched:SelectedObjects:mlvj-mt"],hfitnmae,-4,+4)
r0_dpT = FitPlot(histos["Matched:SelectedObjects:pTjjj-pTlvj"],hfitnmae,-20,+20)

r1_mW  = FitPlot(histos["Matched:WithSelection:mjj-mW"],hfitnmae,-5,+5)
r1_mtH = FitPlot(histos["Matched:WithSelection:mjjj-mt"],hfitnmae,-8,+6)
r1_mWt = FitPlot(histos["Matched:WithSelection:mjjj-mjj-(mt-mW)"],hfitnmae,-4,+3)
r1_mtL = FitPlot(histos["Matched:WithSelection:mlvj-mt"],hfitnmae,-4,+4)
r1_dpT = FitPlot(histos["Matched:WithSelection:pTjjj-pTlvj"],hfitnmae,-20,+20)

r2_mW  = FitPlot(histos["Matched:NoSelection:mjj-mW"],hfitnmae,-5,+5)
r2_mtH = FitPlot(histos["Matched:NoSelection:mjjj-mt"],hfitnmae,-8,+6)
r2_mWt = FitPlot(histos["Matched:NoSelection:mjjj-mjj-(mt-mW)"],hfitnmae,-4,+3)
r2_mtL = FitPlot(histos["Matched:NoSelection:mlvj-mt"],hfitnmae,-4,+4)
r2_dpT = FitPlot(histos["Matched:NoSelection:pTjjj-pTlvj"],hfitnmae+")",-20,+20)


print "--------------------------- Matched:SelectedObjects ---------------------------"
print "mjj-mW:           mean=%g, sigma=%g, chi2/NDF=%g" % (r0_mW.Value(1), r0_mW.Value(2), r0_mW.Chi2() /r0_mW.Ndf())
print "mjjj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r0_mtH.Value(1),r0_mtH.Value(2),r0_mtH.Chi2()/r0_mtH.Ndf())
print "mjjj-mjj-(mt-mW): mean=%g, sigma=%g, chi2/NDF=%g" % (r0_mWt.Value(1),r0_mWt.Value(2),r0_mWt.Chi2()/r0_mWt.Ndf())
print "mlvj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r0_mtL.Value(1),r0_mtL.Value(2),r0_mtL.Chi2()/r0_mtL.Ndf())
print "pTjjj-pTlvj:      mean=%g, sigma=%g, chi2/NDF=%g" % (r0_dpT.Value(1),r0_dpT.Value(2),r0_dpT.Chi2()/r0_dpT.Ndf())

print "--------------------------- Matched:WithSelection ---------------------------"
print "mjj-mW:           mean=%g, sigma=%g, chi2/NDF=%g" % (r1_mW.Value(1), r1_mW.Value(2), r1_mW.Chi2() /r1_mW.Ndf())
print "mjjj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r1_mtH.Value(1),r1_mtH.Value(2),r1_mtH.Chi2()/r1_mtH.Ndf())
print "mjjj-mjj-(mt-mW): mean=%g, sigma=%g, chi2/NDF=%g" % (r1_mWt.Value(1),r1_mWt.Value(2),r1_mWt.Chi2()/r1_mWt.Ndf())
print "mlvj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r1_mtL.Value(1),r1_mtL.Value(2),r1_mtL.Chi2()/r1_mtL.Ndf())
print "pTjjj-pTlvj:      mean=%g, sigma=%g, chi2/NDF=%g" % (r1_dpT.Value(1),r1_dpT.Value(2),r1_dpT.Chi2()/r1_dpT.Ndf())

print "--------------------------- Matched:NoSelection ---------------------------"
print "mjj-mW:           mean=%g, sigma=%g, chi2/NDF=%g" % (r2_mW.Value(1), r2_mW.Value(2), r2_mW.Chi2() /r2_mW.Ndf())
print "mjjj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r2_mtH.Value(1),r2_mtH.Value(2),r2_mtH.Chi2()/r2_mtH.Ndf())
print "mjjj-mjj-(mt-mW): mean=%g, sigma=%g, chi2/NDF=%g" % (r2_mWt.Value(1),r2_mWt.Value(2),r2_mWt.Chi2()/r2_mWt.Ndf())
print "mlvj-mt:          mean=%g, sigma=%g, chi2/NDF=%g" % (r2_mtL.Value(1),r2_mtL.Value(2),r2_mtL.Chi2()/r2_mtL.Ndf())
print "pTjjj-pTlvj:      mean=%g, sigma=%g, chi2/NDF=%g" % (r2_dpT.Value(1),r2_dpT.Value(2),r2_dpT.Chi2()/r2_dpT.Ndf())



'''
[hod@Noams-MacBook-Pro-2] ~/GitHub/TTbar.13TeV.MC> python src/FitChi2input.py
---------------------  Matched:SelectedObjects:mjj-mW
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
 FCN=4.38415 FROM MINOS     STATUS=SUCCESSFUL     41 CALLS         233 TOTAL
                     EDM=3.74842e-09    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     2.07648e+03   2.20088e+01  -3.61623e-01   6.48008e-05
   2  Mean        -1.34007e+00   6.34440e-02  -1.07836e-03  -2.18073e-02
   3  Sigma        3.98041e+00   7.55945e-02   7.55945e-02  -4.19796e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      4.38415
Chi2                      =      8.78815
NDf                       =            7
Edm                       =  3.74842e-09
NCalls                    =          124
Constant                  =      2076.48   +/-   22.0088
Mean                      =     -1.34007   +/-   0.063444
Sigma                     =      3.98041   +/-   0.0755945    	 (limited)
Info in <TCanvas::Print>: pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf has been created
---------------------
---------------------  Matched:SelectedObjects:mjjj-mt
 FCN=7.13613 FROM MINOS     STATUS=SUCCESSFUL     52 CALLS         275 TOTAL
                     EDM=4.08662e-08    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     1.15807e+03   1.34396e+01  -3.41583e-01  -1.65974e-05
   2  Mean        -3.20116e+00   1.39641e-01  -3.71853e-03   1.70618e-03
   3  Sigma        6.41700e+00   1.72781e-01   1.72781e-01   3.15996e-04
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      7.13613
Chi2                      =      14.2143
NDf                       =           11
Edm                       =  4.08662e-08
NCalls                    =          134
Constant                  =      1158.07   +/-   13.4396
Mean                      =     -3.20116   +/-   0.139641
Sigma                     =        6.417   +/-   0.172781     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:mjjj-mjj-(mt-mW)
 FCN=3.18131 FROM MINOS     STATUS=SUCCESSFUL     52 CALLS         272 TOTAL
                     EDM=3.89507e-08    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     1.65609e+03   2.32112e+01  -1.17982e+00   9.36039e-07
   2  Mean        -1.24549e+00   9.86655e-02  -3.64529e-03   9.13168e-03
   3  Sigma        3.86932e+00   1.72351e-01   1.72351e-01  -2.00687e-02
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      3.18131
Chi2                      =      6.43307
NDf                       =            4
Edm                       =  3.89507e-08
NCalls                    =          130
Constant                  =      1656.09   +/-   23.2112
Mean                      =     -1.24549   +/-   0.0986655
Sigma                     =      3.86932   +/-   0.172351     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:mlvj-mt
 FCN=1.74456 FROM MINOS     STATUS=SUCCESSFUL     51 CALLS         267 TOTAL
                     EDM=2.16658e-07    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     1.68700e+03   2.23001e+01  -7.45809e-01  -3.55399e-05
   2  Mean        -7.49717e-01   7.36471e-02  -1.64094e-03   9.45093e-03
   3  Sigma        3.74553e+00   1.14392e-01   1.14392e-01  -8.40422e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      1.74456
Chi2                      =       3.5147
NDf                       =            5
Edm                       =  2.16658e-07
NCalls                    =          127
Constant                  =         1687   +/-   22.3001
Mean                      =    -0.749717   +/-   0.0736471
Sigma                     =      3.74553   +/-   0.114392     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:pTjjj-pTlvj
 FCN=5.33664 FROM MINOS     STATUS=SUCCESSFUL     40 CALLS         419 TOTAL
                     EDM=3.71191e-10    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     9.51916e+02   1.19671e+01  -4.39667e-01  -4.62190e-06
   2  Mean        -7.09219e-01   3.32636e-01  -2.38360e-03  -3.57602e-03
   3  Sigma        1.98348e+01   6.55863e-01   6.55863e-01  -1.75862e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      5.33664
Chi2                      =      10.7637
NDf                       =           13
Edm                       =  3.71191e-10
NCalls                    =          317
Constant                  =      951.916   +/-   11.9671
Mean                      =    -0.709219   +/-   0.332636
Sigma                     =      19.8348   +/-   0.655863     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
'''