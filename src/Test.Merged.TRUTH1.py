#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList
import os
import math
import subprocess
import collections
import rootstyle
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name [lep/had]')
parser.add_argument('-r', metavar='<re-hadd ntupe>', required=True, help='Re-hadd ntuple ? [yes/no]')
args = parser.parse_args()
name = args.n
hadd = args.r
print 'name : ',name
print 're-hadd : ',hadd

ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = "/afs/cern.ch/user/h/hod/data/MC/ttbar/ntup"
fmerged = path+"/tops.SM.TRUTH1."+name+".merged.root"
if(hadd=="yes"):
   p = subprocess.Popen("rm -f  "+path+"/tops.SM.TRUTH1."+name+".merged.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   p = subprocess.Popen("hadd  "+fmerged+"  "+path+"/tops.SM.TRUTH1."+name+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   print out


gROOT.LoadMacro( "src/Loader.C+" )

tfile = TFile(path+"/tops.SM.TRUTH1."+name+".merged.root","READ")
tree = tfile.Get("SM")

def MWT(pLep,pMET):
   mwt = math.sqrt(2*(pLep.Pt()*pMET.Pt() - pLep.Px()*pMET.Px() - pLep.Py()*pMET.Py()))
   return mwt

histos = {}
def addHist(name,title,nbins,xmin,xmax,color=ROOT.kBlack,marker=20):
   h = TH1D(name,title,nbins,xmin,xmax)
   h.Sumw2()
   h.SetLineWidth(2)
   h.SetLineColor(color)
   h.SetMarkerColor(color)
   h.SetMarkerStyle(marker)
   histos.update({name:h})

addHist("Muons:Mult",     ";Muon multiplicity;Events",5,0,5)
addHist("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,30,530)
addHist("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,30,530)
addHist("Muons:MWT",  ";MWT (Muon) [GeV];Events",50,0,630)

addHist("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
addHist("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,30,530)
addHist("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,30,530)
addHist("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,630)

addHist("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
addHist("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,30,630)

addHist("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
addHist("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,30,630)

addHist("ETmiss:eT",  ";#it{E}_{T}^{miss} [GeV];Events",50,0,630)

n=1
for event in tree:

   muons = []
   for i in xrange(event.p4_muons.size()):
      if(abs(event.p4_muons[i].Eta())>2.5): continue
      if(event.p4_muons[i].Pt()<30):        continue
      if(event.st_muons[i]!=1):             continue
      muons.append(i)
   histos["Muons:Mult"].Fill(len(muons))
   if(len(muons)>0): histos["Muons:pT1"].Fill(event.p4_muons[muons[0]].Pt())
   if(len(muons)>1): histos["Muons:pT2"].Fill(event.p4_muons[muons[1]].Pt())

   electrons = []
   for i in xrange(event.p4_electrons.size()):
      if(abs(event.p4_electrons[i].Eta())>2.5): continue
      if(event.p4_electrons[i].Pt()<30):        continue
      if(event.st_electrons[i]!=1):             continue
      electrons.append(i)
   histos["Electrons:Mult"].Fill(len(electrons))
   if(len(electrons)>0): histos["Electrons:pT1"].Fill(event.p4_electrons[electrons[0]].Pt())
   if(len(electrons)>1): histos["Electrons:pT2"].Fill(event.p4_electrons[electrons[1]].Pt())

   jets = []
   btagged = {}
   for i in xrange(event.p4_akt4jets.size()):
      if(abs(event.p4_akt4jets[i].Eta())>2.5): continue
      if(event.p4_akt4jets[i].Pt()<25):        continue
      jets.append(i)
      isbtagged = False

      for j in xrange(event.p4_bquarks.size()):
         if(event.st_bquarks[j]!=23): continue
         dRb = event.p4_akt4jets[i].DeltaR(event.p4_bquarks[j])
         if(dRb<0.4):
            btagged.update({event.p4_akt4jets[i].Pt() : i})
            break

      # if(event.id_bquarks_children[j].size()==0): continue
      # for k in xrange(event.id_bquarks_children[j].size()):
      #    if(event.id_bquarks_children[j][k]==21):                  continue
      #    if(event.id_bquarks_children[j][k]==event.id_bquarks[j]): continue
      #    dRb = event.p4_akt4jets[i].DeltaR(event.p4_bquarks_children[j][k])
      #    # print "b-decay["+str(k)+"] id = "+str(event.id_bquarks_children[j][k])+" -> dR="+str(dRb)
      #    if(dRb<0.4):
      #       isbtagged = True
      #       btagged.append(i)
      #       break
      # if(isbtagged): break

      # for j in xrange(event.p4_tquarks.size()):
      # if(event.id_tquarks_children[j].size()==0): continue
      # for k in xrange(event.id_tquarks_children[j].size()):
      #    if(abs(event.id_tquarks_children[j][k])!=5): continue
      #    dRb = event.p4_akt4jets[i].DeltaR(event.p4_tquarks_children[j][k])
      #    print "jet["+str(i)+"]: b["+str(j)+"] from t-decay["+str(k)+"] id = "+str(event.id_tquarks_children[j][k])+" -> dR="+str(dRb)
      #    if(dRb<1.0):
      #       isbtagged = True
      #       btagged.append(i)
      #       break
      # if(isbtagged): break

   histos["Jets:Mult"].Fill(len(jets))
   if(len(jets)>0): histos["Jets:pT1"].Fill(event.p4_akt4jets[jets[0]].Pt())
   if(len(jets)>1): histos["Jets:pT2"].Fill(event.p4_akt4jets[jets[1]].Pt())
   if(len(jets)>2): histos["Jets:pT3"].Fill(event.p4_akt4jets[jets[2]].Pt())
   if(len(jets)>3): histos["Jets:pT4"].Fill(event.p4_akt4jets[jets[3]].Pt())

   btagged_ptsorted = collections.OrderedDict(reversed(sorted(btagged.items()))).values()
   histos["BJets:Mult"].Fill(len(btagged_ptsorted))
   if(len(btagged_ptsorted)>0): histos["BJets:pT1"].Fill(event.p4_akt4jets[btagged_ptsorted[0]].Pt())
   if(len(btagged_ptsorted)>1): histos["BJets:pT2"].Fill(event.p4_akt4jets[btagged_ptsorted[1]].Pt())
   if(len(btagged_ptsorted)>2): histos["BJets:pT3"].Fill(event.p4_akt4jets[btagged_ptsorted[2]].Pt())
   if(len(btagged_ptsorted)>3): histos["BJets:pT4"].Fill(event.p4_akt4jets[btagged_ptsorted[3]].Pt())

   histos["ETmiss:eT"].Fill(event.p4_MET[0].Pt())

   if(len(muons)>0 and len(electrons)==0): histos["Muons:MWT"].Fill(MWT(event.p4_muons[muons[0]],event.p4_MET[0]))
   if(len(electrons)>0 and len(muons)==0): histos["Electrons:MWT"].Fill(MWT(event.p4_electrons[electrons[0]],event.p4_MET[0]))
   

   if(n%20000==0): print "processed |SM+X|^2 generated ",n
   n+=1


def plot(fname,name,logy=False):
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   if(logy): cnv.SetLogy()
   histos[name].Draw()
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

fname = path+"/Test.TTree.TRUTH1."+name+".pdf"

plot(fname+"(", "Muons:Mult")
plot(fname,     "Muons:pT1",True)
plot(fname,     "Muons:pT2",True)
plot(fname,     "Electrons:Mult")
plot(fname,     "Electrons:pT1",True)
plot(fname,     "Electrons:pT2",True)
plot(fname,     "Jets:Mult")
plot(fname,     "Jets:pT1",True)
plot(fname,     "Jets:pT2",True)
plot(fname,     "Jets:pT3",True)
plot(fname,     "Jets:pT4",True)
plot(fname,     "BJets:Mult")
plot(fname,     "BJets:pT1",True)
plot(fname,     "BJets:pT2",True)
plot(fname,     "BJets:pT3",True)
plot(fname,     "BJets:pT4",True)
plot(fname,     "ETmiss:eT",True)
plot(fname,     "Muons:MWT",True)
plot(fname+")", "Electrons:MWT",True)
