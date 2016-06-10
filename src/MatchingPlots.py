#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TFitResultPtr
import os
import rootstyle

histos = {}

def addHists(name,rebin=1):
   prefixes = ["HardProcess:NoSelection:",
               "HardProcess:WithSelection:",
               "Matched:NoSelection:",
               "Matched:WithSelection:",
               "Matched:SelectedObjects:"]
   colors = [ROOT.kOrange+7, ROOT.kAzure, ROOT.kGray+2, ROOT.kSpring-6, ROOT.kBlack]
   col = 0
   for prefix in prefixes:
      histos.update({prefix+name:tfile.Get(prefix+name)})
      histos[prefix+name].SetMarkerColor(colors[col])
      histos[prefix+name].SetMarkerStyle(20)
      histos[prefix+name].SetMarkerSize(0.5)
      histos[prefix+name].SetLineColor(colors[col])
      histos[prefix+name].SetLineWidth(1)
      if(rebin>1): histos[prefix+name].Rebin(rebin)
      ymax = -1
      for bin in range(1,histos[prefix+name].GetNbinsX()+1):
         y = histos[prefix+name].GetBinContent(bin)
         if(y>ymax): ymax = y
      histos[prefix+name].SetMaximum(ymax*1.1)
      col += 1

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

def plot(var,fnameall,fname):	
   cnv = TCanvas("cnv","",1600,800)
   cnv.Draw()
   cnv.Divide(2,1)
   p1 = cnv.cd(1)
   p1.Divide(2,2)
   p2 = cnv.cd(2)
   p2.cd()
   histos["Matched:SelectedObjects:"+var].Draw()
   histos["Matched:SelectedObjects:"+var].Draw("hist same")
   leg0 = getLeg("Reco, matched objects","Matched:SelectedObjects:"+var)
   leg0.Draw("same")
   p1.cd(1)
   histos["HardProcess:NoSelection:"+var].Draw()
   histos["HardProcess:NoSelection:"+var].Draw("hist same")
   leg1 = getLeg("Partons, before selection","HardProcess:NoSelection:"+var)
   leg1.Draw("same")
   p1.cd(2)
   histos["HardProcess:WithSelection:"+var].Draw()
   histos["HardProcess:WithSelection:"+var].Draw("hist same")
   leg2 = getLeg("Partons, after selection","HardProcess:WithSelection:"+var)
   leg2.Draw("same")
   p1.cd(3)
   histos["Matched:NoSelection:"+var].Draw()
   histos["Matched:NoSelection:"+var].Draw("hist same")
   leg3 = getLeg("Reco+Matching, before selection","Matched:NoSelection:"+var)
   leg3.Draw("same")
   p1.cd(4)
   histos["Matched:WithSelection:"+var].Draw()
   histos["Matched:WithSelection:"+var].Draw("hist same")
   leg4 = getLeg("Reco+Matchig, after selection","Matched:WithSelection:"+var)
   leg4.Draw("same")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fnameall)
   cnv.SaveAs(fname)

gROOT.LoadMacro( "src/Loader.C+" )
ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

# path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
# tfile = TFile(path+"/histograms.mu.A.root","READ")
# fnameall = path+"/histograms.mu.matching.pdf"
# fname    = path+"/histograms.mu.matching"

path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/MGPy8EG_A14N_ttbarNp012p")
tfile = TFile(path+"/histograms.HTX.A.750GeV.root","READ")
fnameall = path+"/histograms.HTX.A.750GeV.matching.pdf"
fname    = path+"/histograms.HTX.A.750GeV.matching"

addHists("mjj",2)
addHists("mjjj",2)
addHists("mlvj",2)
addHists("pTjjj",2)
addHists("pTlvj",2)
addHists("pTjjjlvj",2)
addHists("mjjjlvj",2)

plot("mjj",     fnameall+"(", fname+".mjj.pdf")
plot("mjjj",    fnameall,     fname+".mjjj.pdf")
plot("mlvj",    fnameall,     fname+".mlvj.pdf")
plot("pTjjj",   fnameall,     fname+".pTjjj.pdf")
plot("pTlvj",   fnameall,     fname+".pTlvj.pdf")
plot("pTjjjlvj",fnameall,     fname+".pTjjjlvj.pdf")
plot("mjjjlvj", fnameall+")", fname+".mjjjlvj.pdf")