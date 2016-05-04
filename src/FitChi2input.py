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

def plotAll(fname,prefix,legtxt):	
   cnv = TCanvas("cnv","",1000,1000)
   cnv.Draw()
   cnv.Divide(2,2)
   cnv.cd(1)
   histos[prefix+"mjj-mW"].Draw()
   leg1 = getLeg(legtxt,prefix+"mjj-mW")
   leg1.Draw("same")
   cnv.cd(2)
   histos[prefix+"mjjj-mjj-(mt-mW)"].Draw()
   leg2 = getLeg(legtxt,prefix+"mjjj-mjj-(mt-mW)")
   leg2.Draw("same")
   cnv.cd(3)
   histos[prefix+"mlvj-mt"].Draw()
   leg3 = getLeg(legtxt,prefix+"mlvj-mt")
   leg3.Draw("same")
   cnv.cd(4)
   histos[prefix+"pTjjj-pTlvj"].Draw()
   leg4 = getLeg(legtxt,prefix+"pTjjj-pTlvj")
   leg4.Draw("same")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

gROOT.LoadMacro( "src/Loader.C+" )
ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
tfile = TFile(path+"/histograms.mu.A.root","READ")

hfitnmae = path+"/histograms.mu.fits.pdf"
fnameall = path+"/histograms.mu.fits.all"

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
r0_mtL = FitPlot(histos["Matched:SelectedObjects:mlvj-mt"],hfitnmae,-4,+3)
r0_dpT = FitPlot(histos["Matched:SelectedObjects:pTjjj-pTlvj"],hfitnmae,-20,+10)

r1_mW  = FitPlot(histos["Matched:WithSelection:mjj-mW"],hfitnmae,-5,+5)
r1_mtH = FitPlot(histos["Matched:WithSelection:mjjj-mt"],hfitnmae,-8,+6)
r1_mWt = FitPlot(histos["Matched:WithSelection:mjjj-mjj-(mt-mW)"],hfitnmae,-4,+3)
r1_mtL = FitPlot(histos["Matched:WithSelection:mlvj-mt"],hfitnmae,-4,+3)
r1_dpT = FitPlot(histos["Matched:WithSelection:pTjjj-pTlvj"],hfitnmae,-20,+8)

r2_mW  = FitPlot(histos["Matched:NoSelection:mjj-mW"],hfitnmae,-5,+5)
r2_mtH = FitPlot(histos["Matched:NoSelection:mjjj-mt"],hfitnmae,-8,+6)
r2_mWt = FitPlot(histos["Matched:NoSelection:mjjj-mjj-(mt-mW)"],hfitnmae,-4,+3)
r2_mtL = FitPlot(histos["Matched:NoSelection:mlvj-mt"],hfitnmae,-4,+4)
r2_dpT = FitPlot(histos["Matched:NoSelection:pTjjj-pTlvj"],hfitnmae+")",-20,+20)

plotAll(fnameall+"MatchedWithSelection.pdf","Matched:WithSelection:","Reco+Matchig, after selection")
plotAll(fnameall+"MatchedSelectedObjects.pdf","Matched:SelectedObjects:","Matched selected objects")


print "--------------------------- Matched:SelectedObjects ---------------------------"
print "mjj-mW:           mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r0_mW.Value(1), r0_mW.Value(2), r0_mW.Chi2() /r0_mW.Ndf() , ROOT.TMath.Prob(r0_mW.Chi2() ,r0_mW.Ndf() ))
print "mjjj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r0_mtH.Value(1),r0_mtH.Value(2),r0_mtH.Chi2()/r0_mtH.Ndf(), ROOT.TMath.Prob(r0_mtH.Chi2(),r0_mtH.Ndf()))
print "mjjj-mjj-(mt-mW): mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r0_mWt.Value(1),r0_mWt.Value(2),r0_mWt.Chi2()/r0_mWt.Ndf(), ROOT.TMath.Prob(r0_mWt.Chi2(),r0_mWt.Ndf()))
print "mlvj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r0_mtL.Value(1),r0_mtL.Value(2),r0_mtL.Chi2()/r0_mtL.Ndf(), ROOT.TMath.Prob(r0_mtL.Chi2(),r0_mtL.Ndf()))
print "pTjjj-pTlvj:      mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r0_dpT.Value(1),r0_dpT.Value(2),r0_dpT.Chi2()/r0_dpT.Ndf(), ROOT.TMath.Prob(r0_dpT.Chi2(),r0_dpT.Ndf()))

print "--------------------------- Matched:WithSelection ---------------------------"
print "mjj-mW:           mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r1_mW.Value(1), r1_mW.Value(2), r1_mW.Chi2() /r1_mW.Ndf() , ROOT.TMath.Prob(r1_mW.Chi2() ,r1_mW.Ndf() ))
print "mjjj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r1_mtH.Value(1),r1_mtH.Value(2),r1_mtH.Chi2()/r1_mtH.Ndf(), ROOT.TMath.Prob(r1_mtH.Chi2(),r1_mtH.Ndf()))
print "mjjj-mjj-(mt-mW): mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r1_mWt.Value(1),r1_mWt.Value(2),r1_mWt.Chi2()/r1_mWt.Ndf(), ROOT.TMath.Prob(r1_mWt.Chi2(),r1_mWt.Ndf()))
print "mlvj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r1_mtL.Value(1),r1_mtL.Value(2),r1_mtL.Chi2()/r1_mtL.Ndf(), ROOT.TMath.Prob(r1_mtL.Chi2(),r1_mtL.Ndf()))
print "pTjjj-pTlvj:      mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r1_dpT.Value(1),r1_dpT.Value(2),r1_dpT.Chi2()/r1_dpT.Ndf(), ROOT.TMath.Prob(r1_dpT.Chi2(),r1_dpT.Ndf()))

print "--------------------------- Matched:NoSelection ---------------------------"
print "mjj-mW:           mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r2_mW.Value(1), r2_mW.Value(2), r2_mW.Chi2() /r2_mW.Ndf() , ROOT.TMath.Prob(r2_mW.Chi2() ,r2_mW.Ndf() ))
print "mjjj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r2_mtH.Value(1),r2_mtH.Value(2),r2_mtH.Chi2()/r2_mtH.Ndf(), ROOT.TMath.Prob(r2_mtH.Chi2(),r2_mtH.Ndf()))
print "mjjj-mjj-(mt-mW): mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r2_mWt.Value(1),r2_mWt.Value(2),r2_mWt.Chi2()/r2_mWt.Ndf(), ROOT.TMath.Prob(r2_mWt.Chi2(),r2_mWt.Ndf()))
print "mlvj-mt:          mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r2_mtL.Value(1),r2_mtL.Value(2),r2_mtL.Chi2()/r2_mtL.Ndf(), ROOT.TMath.Prob(r2_mtL.Chi2(),r2_mtL.Ndf()))
print "pTjjj-pTlvj:      mean=%g,  sigma=%g,  chi2/NDF=%g,  p-value=%g" % (r2_dpT.Value(1),r2_dpT.Value(2),r2_dpT.Chi2()/r2_dpT.Ndf(), ROOT.TMath.Prob(r2_dpT.Chi2(),r2_dpT.Ndf()))