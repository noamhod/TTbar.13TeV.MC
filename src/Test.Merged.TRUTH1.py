#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TVector2
import os
import math
import subprocess
import collections
import rootstyle
import graphics
from TTbarTagger import TTbarTagger
from TTbarSelection import Jets, Leptons, HardProcessTops
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


def mT(pLep,pMET):
   mwt = math.sqrt(2*(pLep.Pt()*pMET.Pt() - pLep.Px()*pMET.Px() - pLep.Py()*pMET.Py()))
   return mwt


cutflow = []
cutflow.append({"All":0})
cutflow.append({"Muons.n=1":0})
cutflow.append({"Electrons.n=0":0})
cutflow.append({"Jets.n>3":0})
cutflow.append({"Bjets.n>0":0})
cutflow.append({"ETmiss.eT>20":0})
cutflow.append({"ETmiss.eT+ETmiss.mTW>60":0})
def FillCutFlow(cut=""):
   for c in cutflow:
      key = c.keys()[0]
      if(key==cut): break
      c[key] += 1

n=1
for event in tree:

   ### counts
   if(n%10000==0): print "processed "+str(n)+", cutflow up to previous event:",cutflow
      
   n+=1

   ### define the hard process
   hardproc = HardProcessTops(event.id_tquarks,event.p4_tquarks,event.st_tquarks,event.id_tquarks_parents,event.p4_tquarks_parents,
                              event.id_wbosons,event.p4_wbosons,event.st_wbosons,event.id_wbosons_parents,event.p4_wbosons_parents,event.id_wbosons_children,event.p4_wbosons_children)
   id_tops  = hardproc.id_tops
   p4_tops  = hardproc.p4_tops
   topdecay = hardproc.topdecay



   ### define jets and b-jets
   goodjets = Jets(event.p4_akt4jets)
   goodjets.TagBjets(event.st_bquarks,event.p4_bquarks)
   jets     = goodjets.ijets
   bjets    = goodjets.ibjets 
   nonbjets = goodjets.inonbjets

   graphics.histos["Jets:Mult"].Fill(len(jets))
   if(len(jets)>0): graphics.histos["Jets:pT1"].Fill(event.p4_akt4jets[jets[0]].Pt())
   if(len(jets)>1): graphics.histos["Jets:pT2"].Fill(event.p4_akt4jets[jets[1]].Pt())
   if(len(jets)>2): graphics.histos["Jets:pT3"].Fill(event.p4_akt4jets[jets[2]].Pt())
   if(len(jets)>3): graphics.histos["Jets:pT4"].Fill(event.p4_akt4jets[jets[3]].Pt())

   graphics.histos["BJets:Mult"].Fill(len(bjets))
   if(len(bjets)>0): graphics.histos["BJets:pT1"].Fill(event.p4_akt4jets[bjets[0]].Pt())
   if(len(bjets)>1): graphics.histos["BJets:pT2"].Fill(event.p4_akt4jets[bjets[1]].Pt())
   if(len(bjets)>2): graphics.histos["BJets:pT3"].Fill(event.p4_akt4jets[bjets[2]].Pt())
   if(len(bjets)>3): graphics.histos["BJets:pT4"].Fill(event.p4_akt4jets[bjets[3]].Pt())
   

   # define muons
   goodmuons = Leptons("muons",event.p4_muons,event.st_muons,goodjets)
   muons = goodmuons.ileptons

   graphics.histos["Muons:Mult"].Fill(len(muons))
   if(len(muons)>0): graphics.histos["Muons:pT1"].Fill(event.p4_muons[muons[0]].Pt())
   if(len(muons)>1): graphics.histos["Muons:pT2"].Fill(event.p4_muons[muons[1]].Pt())


   # define electrons
   goodelectrons = Leptons("electrons",event.p4_electrons,event.st_electrons,goodjets)
   electrons = goodelectrons.ileptons

   graphics.histos["Electrons:Mult"].Fill(len(electrons))
   if(len(electrons)>0): graphics.histos["Electrons:pT1"].Fill(event.p4_electrons[electrons[0]].Pt())
   if(len(electrons)>1): graphics.histos["Electrons:pT2"].Fill(event.p4_electrons[electrons[1]].Pt())


   # MET stuff
   mTW = 0
   graphics.histos["ETmiss:eT"].Fill(event.p4_MET[0].Pt())
   if(len(muons)>0 and len(electrons)==0):
      graphics.histos["Muons:MWT"].Fill(mT(event.p4_muons[muons[0]],event.p4_MET[0]))
      mTW = mT(event.p4_muons[muons[0]],event.p4_MET[0])
   if(len(electrons)>0 and len(muons)==0):
      graphics.histos["Electrons:MWT"].Fill(mT(event.p4_electrons[electrons[0]],event.p4_MET[0]))
      mTW = mT(event.p4_electrons[electrons[0]],event.p4_MET[0])


   ############
   ### cuts ###
   ############

   if(len(muons)!=1):
      FillCutFlow("Muons.n=1")
      continue
   if(len(electrons)>0):
      FillCutFlow("Electrons.n=0")
      continue
   if(len(jets)<4):
      FillCutFlow("Jets.n>3")
      continue
   if(len(bjets)<1):
      FillCutFlow("Bjets.n>0")
      continue
   if(event.p4_MET[0].Pt()<20):
      FillCutFlow("ETmiss.eT>20")
      continue
   if(event.p4_MET[0].Pt()+mTW<60):
      FillCutFlow("ETmiss.eT+ETmiss.mTW>60")
      continue

   ##################
   FillCutFlow() ####
   ##################



   ########################
   ### event has passed ###
   ######################## 

   # for j in muons:
   #     graphics.histos["ETmiss:dPhiMuons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_muons[j].Phi()-event.p4_MET[0].Phi())) )
   #  for j in electrons:
   #     graphics.histos["ETmiss:dPhiElectrons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_electrons[j].Phi()-event.p4_MET[0].Phi())) )
   #  for j in jets:
   #    graphics.histos["ETmiss:dPhiJets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[j].Phi()-event.p4_MET[0].Phi()))  )
   #    for i in muons:     graphics.histos["Muons:dRJets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
   #    for i in electrons: graphics.histos["Electrons:dRJets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   #  for j in bjets:
   #     graphics.histos["ETmiss:dPhiBjets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[j].Phi()-event.p4_MET[0].Phi())) )
   #     for i in muons:     graphics.histos["Muons:dRBjets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
   #     for i in electrons: graphics.histos["Electrons:dRBjets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   #  for j in nonbjets:
   #     for i in bjets:
   #        graphics.histos["Jets:dRBjets"].Fill(event.p4_akt4jets[j].DeltaR(event.p4_akt4jets[i]))
    
   if(len(nonbjets)>1): graphics.histos["Jets:dR12"].Fill(event.p4_akt4jets[nonbjets[0]].DeltaR(event.p4_akt4jets[nonbjets[1]]))
   if(len(bjets)>1):    graphics.histos["BJets:dR12"].Fill(event.p4_akt4jets[bjets[0]].DeltaR(event.p4_akt4jets[bjets[1]]))

   if(len(jets)>3 and len(bjets)>0 and ((len(muons)>0 and len(electrons)==0) or (len(muons)==0 and len(electrons)>0)) ):
      etmis = event.p4_MET[0]
      lep   = TLorentzVector()
      if(len(muons)>0 and len(electrons)==0): lep = event.p4_muons[0]
      if(len(muons)==0 and len(electrons)>0): lep = event.p4_electrons[0]
      ttTag = TTbarTagger(event.p4_akt4jets,jets,bjets,lep,etmis,1)
      if(not ttTag.MinimumInput()): continue
      graphics.histos["TopTag:mTw"].Fill(ttTag.mTw)
      graphics.histos["TopTag:mTt"].Fill(ttTag.mTt)
      graphics.histos["TopTag:mw"].Fill(ttTag.mw)
      graphics.histos["TopTag:mt"].Fill(ttTag.mt)
      graphics.histos["TopTag:mtt"].Fill(ttTag.mtt)
      graphics.histos["TopTag:pTtLep"].Fill(ttTag.p4_tT.Pt())
      graphics.histos["TopTag:pTtHad"].Fill(ttTag.p4_t.Pt())
      graphics.histos["TopTag:dRlephad"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tT))
      ######## this is process specific ########
      if(len(p4_tops)==2 and len(topdecay)==2):
         itL = -1
         itH = -1
         if(topdecay[0]=="lep"):
            itL = 0
            itH = 1
         elif(topdecay[0]=="had"):
            itH = 0
            itL = 1
         graphics.histos["HarProcessTops:dRlep"].Fill(ttTag.p4_tT.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRhad"].Fill(ttTag.p4_t.DeltaR(p4_tops[itH]))
         graphics.histos["HarProcessTops:dpTRellep"].Fill( (ttTag.p4_tT.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRelhad"].Fill( (ttTag.p4_t.Pt()-p4_tops[itH].Pt())/p4_tops[itH].Pt() )
         graphics.histos["HarProcessTops:mtt"].Fill( (p4_tops[0]+p4_tops[1]).M() )
         graphics.histos["HarProcessTops:pTlep"].Fill( p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:pThad"].Fill( p4_tops[itH].Pt() )
      else:
         print "Warning: hard process problem in event %i (EventNumber=%i and RunNumber=%i)" % (n,event.EventNumber,event.RunNumber)
         print id_tops
         print topdecay
      ###########################################

   ### end of events loop

# plot everything
fname = path+"/Test.TTree.TRUTH1."+name+".pdf"

graphics.plotHist(fname+"(", "Muons:Mult")
graphics.plotHist(fname,     "Muons:pT1",True)
graphics.plotHist(fname,     "Muons:pT2",True)
graphics.plotHist(fname,     "Electrons:Mult")
graphics.plotHist(fname,     "Electrons:pT1",True)
graphics.plotHist(fname,     "Electrons:pT2",True)
graphics.plotHist(fname,     "Jets:Mult")
graphics.plotHist(fname,     "Jets:pT1",True)
graphics.plotHist(fname,     "Jets:pT2",True)
graphics.plotHist(fname,     "Jets:pT3",True)
graphics.plotHist(fname,     "Jets:pT4",True)
graphics.plotHist(fname,     "BJets:Mult")
graphics.plotHist(fname,     "BJets:pT1",True)
graphics.plotHist(fname,     "BJets:pT2",True)
# graphics.plotHist(fname,     "BJets:pT3",True)
# graphics.plotHist(fname,     "BJets:pT4",True)
graphics.plotHist(fname,     "ETmiss:eT",True)
graphics.plotHist(fname,     "Muons:MWT",True)
graphics.plotHist(fname,     "Electrons:MWT",True)
# graphics.plotHist(fname,     "ETmiss:dPhiMuons")  
# graphics.plotHist(fname,     "ETmiss:dPhiElectrons")
# graphics.plotHist(fname,     "ETmiss:dPhiJets")
# graphics.plotHist(fname,     "ETmiss:dPhiBjets")  
# graphics.plotHist(fname,     "Muons:dRJets")  
# graphics.plotHist(fname,     "Muons:dRBjets")
# graphics.plotHist(fname,     "Electrons:dRJets")
# graphics.plotHist(fname,     "Jets:dRBjets")
graphics.plotHist(fname,     "Jets:dR12")
graphics.plotHist(fname,     "BJets:dR12")
graphics.plotHist(fname,     "TopTag:mTw")
graphics.plotHist(fname,     "TopTag:mTt")
graphics.plotHist(fname,     "TopTag:mw")
graphics.plotHist(fname,     "TopTag:mt")
graphics.plotHist(fname,     "TopTag:dRlephad")
graphics.plotHist(fname,     "HarProcessTops:dRlep")
graphics.plotHist(fname,     "HarProcessTops:dRhad")
graphics.plotHist(fname,     "HarProcessTops:dpTRellep")
graphics.plotHist(fname,     "HarProcessTops:dpTRelhad")
graphics.plotHist2(fname,    "TopTag:pTtLep","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:pTtHad","HarProcessTops:pThad")
graphics.plotHist2(fname+")","TopTag:mtt","HarProcessTops:mtt")
print "=================================================== cutflow ==================================================="
print cutflow
print "==============================================================================================================="