#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList
import os
import subprocess
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name')
args = parser.parse_args()
name = args.n
print 'name : ',name

path = "/afs/cern.ch/user/h/hod/data/MC/ttbar/ntup"
fmerged = path+"/tops.SM."+name+".merged.root"
p = subprocess.Popen("rm -f  "+path+"/tops.SM."+name+".merged.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("hadd  "+path+"/tops.SM."+name+".merged.root  "+path+"/tops.SM."+name+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

gROOT.LoadMacro( "src/Loader.C+" )

tfile = TFile(path+"/tops.SM."+name+".merged.root","READ")
tree = tfile.Get("SM")

hmSM = TH1D("hmSM", ";Truth #it{m}_{#it{t}#bar{#it{t}}} [GeV];Events",25,350,850)
hmSM.Sumw2()
hmSM.SetLineWidth(2)
hmSM.SetLineColor(ROOT.kAzure+9)
hmSM.SetMarkerColor(ROOT.kAzure+9)
hmSM.SetMarkerStyle(24)

n=1
for event in tree:
   if(n%20000==0): print "processed |SM+X|^2 generated ", n
   t1=event.p4[2]
   t2=event.p4[3]
   mtt = (t1+t2).M()
   hmSM.Fill(mtt)
   n+=1

cnv = TCanvas("cnv","",600,600)
cnv.Draw()
cnv.cd()
hmSM.SetMinimum(0.1)
hmSM.Draw()
cnv.Update()
cnv.RedrawAxis()
cnv.SaveAs(path+"/Test.TTree."+name+".pdf")
