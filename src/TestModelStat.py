#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TFitResultPtr
import os
import sys
import rootstyle
import collections
sys.path.append('/Users/hod/GitHub/2HDM')
import THDM

histos = {}

def addHist(name,color=ROOT.kBlack,rebin=1):
   histos.update({name:tfile.Get(name)})
   if(rebin>1): histos[name].Rebin(rebin)
   histos[name].SetLineColor(color)

gROOT.LoadMacro( "src/Loader.C+" )
ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

#### get the model
type      = THDM.model.type
sba       = THDM.model.sba
mintanb   = '%.1f' % THDM.model.mintanb
maxtanb   = '%.1f' % THDM.model.maxtanb
mX        = THDM.model.mX
nameX     = THDM.model.nameX
cuts      = THDM.model.cuts
mgpath    = THDM.model.mgpath
alphaS    = THDM.model.alphaS
nhel      = THDM.model.nhel
libmatrix = "/Users/hod/GitHub/2HDM/matrix/"+nameX+"/"+str(mX)+"/"+str(sba)+"/"
THDM.setParameters(nameX,mX,cuts,type,sba)
# THDM.setModules(libmatrix,nameX,len(THDM.parameters),"All")
# print THDM.modules

#### the root file with all the histos
path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
tfile = TFile(path+"/histograms.mu."+nameX+"."+str(mX)+"GeV.root","READ")

### rearrange the model histograms
tanbindices = {}
for i in xrange(len(THDM.parameters)):
   tanb = str(THDM.parameters[i].get("tanb"))
   tanbindices.update({tanb:i})
ihistos = collections.OrderedDict(sorted(tanbindices.items())).values()
sinba = ""
rebin = 1
ii=0
for i in ihistos:
   tanb   = '%.2f' % THDM.parameters[i].get("tanb")
   sinba  = '%.2f' % THDM.parameters[i].get("sba")
   name_xx = "HardProcess:WithSelection:mjjjlvj:"+nameX+":"+str(mX)+"GeV:"+str(i)
   name_ix = "HardProcess:WithSelection:mjjjlvj:"+nameX+":"+str(mX)+"GeV:IX:"+str(i)
   color = ROOT.kBlack
   addHist(name_xx,color,rebin)
   addHist(name_ix,color,rebin)
addHist("HardProcess:WithSelection:mjjjlvj",ROOT.kBlack,rebin)



ymin = +1.e10
ymax = -1.e10
for name, hist in histos.iteritems():
   if("IX" not in name): continue
   hist.Divide(histos["HardProcess:WithSelection:mjjjlvj"])
   hist.Scale(100)
   hist.GetYaxis().SetTitle("|SM+#it{X}|^{2}/|SM|^{2}-1 [%] (wrt |SM|^{2})")
   tmpmin = hist.GetMinimum()
   tmpmax = hist.GetMaximum()
   if(tmpmin<ymin): ymin = tmpmin
   if(tmpmax>ymax): ymax = tmpmax

hist0 = histos["HardProcess:WithSelection:mjjjlvj:"+nameX+":"+str(mX)+"GeV:IX:"+str(tanbindices["1.0"])]
hist0.SetLineColor(ROOT.kGreen)

cnv = TCanvas("cnv","",1200,1000)
cnv.Draw()
cnv.cd()

leg = TLegend(0.45,0.2,0.87,0.45,"","brNDC")
leg.SetFillStyle(4000) # will be transparent
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "")
leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "")
leg.AddEntry(0, "Resolved selection", "")
leg.AddEntry(0, "#it{m}_{#it{"+nameX+"}}="+str(mX)+" GeV", "")
leg.AddEntry(0, "sin(#beta-#alpha)="+str(sinba), "")
leg.AddEntry(histos["HardProcess:WithSelection:mjjjlvj"],mintanb+"#leqtan#beta#leq"+maxtanb,"le")
leg.AddEntry(hist0,                                      "tan#beta=1.0","le")

isfirst = True
for name, hist in histos.iteritems():
   if("IX" not in name): continue
   hist.SetMinimum(ymin*1.2)
   hist.SetMaximum(ymax*1.2)
   if(isfirst): hist.Draw("hist")
   else:        hist.Draw("hist same")
   isfirst = False
hist0.Draw("hist same")
leg.Draw("same")
cnv.Update()
cnv.RedrawAxis()
cnv.SaveAs(path+"/TestModelStat.mu."+nameX+"."+str(mX)+"GeV.pdf")

ymin = 0
bin0 = 0
for bin in range(1,hist0.GetNbinsX()+1):
   if(hist0.GetBinContent(bin)<ymin):
      ymin = hist0.GetBinContent(bin)
      bin0 = bin

print "min val =",hist0.GetBinContent(bin0)
print "SM val =",histos["HardProcess:WithSelection:mjjjlvj"].GetBinContent(bin0)
print "SM err =",histos["HardProcess:WithSelection:mjjjlvj"].GetBinError(bin0)

N = 20*histos["HardProcess:WithSelection:mjjjlvj"].GetBinContent(bin0)
err = ROOT.TMath.Sqrt(N)
print "SM rel =",err/N*100



