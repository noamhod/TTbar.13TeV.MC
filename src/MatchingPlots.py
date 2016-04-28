#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TFitResultPtr
import os
import rootstyle

histos = {}

def adHists(name):
   prefixes = ["HardProcess:NoSelection:",
               "HardProcess:WithSelection:",
               "Matched:NoSelection:",
               "Matched:WithSelection:",
               "Matched:SelectedObjects:"]
   for prefix in prefixes:
      histos.update({prefix+name:tfile.Get(prefix+name)})
      histos[prefix+name].SetMarkerStyle(20)
      histos[prefix+name].SetMarkerSize(0.5)
      histos[prefix+name].SetLineWidth(1)

def getLeg(legtxt,hname):
   leg = TLegend(0.45,0.65,0.87,0.9,"","brNDC")
   leg.SetFillStyle(4000) # will be transparent
   leg.SetFillColor(0)
   leg.SetTextFont(42)
   leg.SetBorderSize(0)
   leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "")
   leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "")
   leg.AddEntry(0, "Resolved selection", "")
   leg.AddEntry(histos[hname],legtxt,"ple")
   return leg

def plot(var,fname):	
   cnv = TCanvas("cnv","",1600,800)
   cnv.Draw()
   cnv.Divide(2,1)
   p1 = cnv.cd(1)
   p2 = cnv.cd(2)
   p2.Divide(2,2)
   p1.cd()
   histos["Matched:SelectedObjects:"+var].Draw()
   histos["Matched:SelectedObjects:"+var].Draw("hist same")
   leg0 = getLeg("Reco, matched objects","Matched:SelectedObjects:"+var)
   leg0.Draw("same")
   p2.cd(1)
   histos["HardProcess:NoSelection:"+var].Draw()
   histos["HardProcess:NoSelection:"+var].Draw("hist same")
   leg1 = getLeg("Partons, before selection","HardProcess:NoSelection:"+var)
   leg1.Draw("same")
   p2.cd(2)
   histos["HardProcess:WithSelection:"+var].Draw()
   histos["HardProcess:WithSelection:"+var].Draw("hist same")
   leg2 = getLeg("Partons, after selection","HardProcess:WithSelection:"+var)
   leg2.Draw("same")
   p2.cd(3)
   histos["Matched:NoSelection:"+var].Draw()
   histos["Matched:NoSelection:"+var].Draw("hist same")
   leg3 = getLeg("Reco+Matching, before selection","Matched:NoSelection:"+var)
   leg3.Draw("same")
   p2.cd(4)
   histos["Matched:WithSelection:"+var].Draw()
   histos["Matched:WithSelection:"+var].Draw("hist same")
   leg4 = getLeg("Reco+Matchig, after selection","Matched:WithSelection:"+var)
   leg4.Draw("same")

   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

gROOT.LoadMacro( "src/Loader.C+" )
ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
tfile = TFile(path+"/histograms.mu.A.root","READ")

hfitnmae = path+"/histograms.mu.matching.pdf"

adHists("mjj")
adHists("mjjj")
adHists("mlvj")
adHists("pTjjj")
adHists("pTlvj")
adHists("pTjjjlvj")
adHists("mjjjlvj")

plot("mjj",hfitnmae+"(")
plot("mjjj",hfitnmae)
plot("mlvj",hfitnmae)
plot("pTjjj",hfitnmae)
plot("pTlvj",hfitnmae)
plot("mjjjlvj",hfitnmae+")")


'''
Processessed:  499985
[{'All': 499984}, {'Muons.n=1': 306107}, {'Electrons.n=0': 306065}, {'Jets.n>3': 175992}, {'Bjets.n>0': 172388}, {'ETmiss.eT>20': 151428}, {'ETmiss.eT+ETmiss.mTW>60': 143648}]
nTruMatch_before_selection =  339635
nTruMatch_after_selection  =  57378
nTruMatch_selected_objects =  42012
'''

'''
---------------------  Matched:SelectedObjects:mjj-mW
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
 FCN=3.64316 FROM MINOS     STATUS=SUCCESSFUL     46 CALLS         245 TOTAL
                     EDM=2.90286e-09    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     2.55435e+03   2.38831e+01  -4.01107e-01   7.12709e-05
   2  Mean        -1.49900e+00   7.16134e-02  -1.37398e-03  -2.08990e-02
   3  Sigma        4.37764e+00   8.76173e-02   8.76173e-02  -1.85194e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      3.64316
Chi2                      =      7.20117
NDf                       =            7
Edm                       =  2.90286e-09
NCalls                    =          131
Constant                  =      2554.35   +/-   23.8831
Mean                      =       -1.499   +/-   0.0716134
Sigma                     =      4.37764   +/-   0.0876173    	 (limited)
Info in <TCanvas::Print>: pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf has been created
---------------------
---------------------  Matched:SelectedObjects:mjjj-mt
 FCN=9.35559 FROM MINOS     STATUS=SUCCESSFUL     47 CALLS         249 TOTAL
                     EDM=3.06768e-07    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     1.47960e+03   1.49945e+01  -3.62920e-01  -3.00082e-06
   2  Mean        -3.34725e+00   1.43037e-01  -3.94917e-03   2.08108e-03
   3  Sigma        6.80898e+00   1.79545e-01   1.79545e-01   3.51671e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      9.35559
Chi2                      =      18.8364
NDf                       =           11
Edm                       =  3.06768e-07
NCalls                    =          133
Constant                  =       1479.6   +/-   14.9945
Mean                      =     -3.34725   +/-   0.143037
Sigma                     =      6.80898   +/-   0.179545     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:mjjj-mjj-(mt-mW)
 FCN=2.6391 FROM MINOS     STATUS=SUCCESSFUL     52 CALLS         303 TOTAL
                     EDM=3.82418e-09    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     2.22660e+03   2.65814e+01  -1.24002e+00  -3.32570e-06
   2  Mean        -1.34198e+00   9.75999e-02  -3.67902e-03   9.45282e-03
   3  Sigma        4.05299e+00   1.69604e-01   1.69604e-01  -1.42128e-02
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =       2.6391
Chi2                      =      5.31361
NDf                       =            4
Edm                       =  3.82418e-09
NCalls                    =          155
Constant                  =       2226.6   +/-   26.5814
Mean                      =     -1.34198   +/-   0.0975999
Sigma                     =      4.05299   +/-   0.169604     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:mlvj-mt
 FCN=4.79177 FROM MINOS     STATUS=SUCCESSFUL     51 CALLS         254 TOTAL
                     EDM=3.5286e-08    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     2.34926e+03   2.64000e+01  -8.18243e-01  -3.43623e-05
   2  Mean        -6.35795e-01   6.46524e-02  -1.16962e-03   1.19009e-02
   3  Sigma        3.91675e+00   1.09136e-01   1.09136e-01  -5.46205e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      4.79177
Chi2                      =      9.45287
NDf                       =            5
Edm                       =   3.5286e-08
NCalls                    =          134
Constant                  =      2349.26   +/-   26.4
Mean                      =    -0.635795   +/-   0.0646524
Sigma                     =      3.91675   +/-   0.109136     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
---------------------  Matched:SelectedObjects:pTjjj-pTlvj
 FCN=7.58007 FROM MINOS     STATUS=SUCCESSFUL     40 CALLS         347 TOTAL
                     EDM=3.21416e-11    STRATEGY= 1      ERROR MATRIX ACCURATE
  EXT PARAMETER                                   STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  Constant     1.41324e+03   1.44964e+01  -4.75165e-01  -1.38835e-05
   2  Mean        -1.35906e+00   3.05045e-01  -3.70799e-03  -6.98466e-03
   3  Sigma        2.08774e+01   6.20725e-01   6.20725e-01  -2.98951e-03
                               ERR DEF= 0.5

****************************************
Minimizer is Minuit / MigradImproved
MinFCN                    =      7.58007
Chi2                      =      15.3416
NDf                       =           13
Edm                       =  3.21416e-11
NCalls                    =          245
Constant                  =      1413.24   +/-   14.4964
Mean                      =     -1.35906   +/-   0.305045
Sigma                     =      20.8774   +/-   0.620725     	 (limited)
TCanvas::Constructor:0: RuntimeWarning: Deleting canvas with same name: cnv
Info in <TCanvas::Print>: Current canvas added to pdf file /Users/hod/Downloads/tops/histograms.mu.fits.pdf
---------------------
'''