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
   

def JetOverlap(obj,jets,ijets,objtype,dRoverlap=0.4):
   for i in ijets:
      if(jets[i].DeltaR(obj)<dRoverlap):
         if(objtype=="electron"):
	        if(abs(jets[i].Pt()-obj.Pt())/obj.Pt()<0.5): return True
         elif(objtype=="muon"):
		    if(abs(jets[i].Pt()-obj.Pt())/obj.Pt()<0.7): return True
         else: return True
   return False


cutflow = []
cutflow.append({"All":0})
cutflow.append({"Leptons.n>0":0})
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

   ### define jets and b-jets   
   jets = []
   bflags = []
   btagged = {}
   for i in xrange(event.p4_akt4jets.size()):
      if(abs(event.p4_akt4jets[i].Eta())>2.5): continue
      if(event.p4_akt4jets[i].Pt()<25):        continue
      jets.append(i)
      bflags.append(False)
      for j in xrange(event.p4_bquarks.size()):
         if(event.st_bquarks[j]!=23): continue
         dRb = event.p4_akt4jets[i].DeltaR(event.p4_bquarks[j])
         if(dRb<0.4):
            bflags[len(bflags)-1] = True
            btagged.update({event.p4_akt4jets[i].Pt() : i})
            break

      # isbtagged = False
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

      # isbtagged = False
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

   # sort b-jets
   btagged_ptsorted = collections.OrderedDict(reversed(sorted(btagged.items()))).values()   

   # get the non-b-tagged jets
   non_btagged = []
   for j in jets:
     if(j in btagged_ptsorted): continue
     non_btagged.append(j)

   # define muons
   muons = []
   for i in xrange(event.p4_muons.size()):
      if(abs(event.p4_muons[i].Eta())>2.5): continue
      if(event.p4_muons[i].Pt()<30):        continue
      if(event.st_muons[i]!=1):             continue
      # if(JetOverlap(event.p4_muons[i],event.p4_akt4jets,jets,"muon")): continue
      muons.append(i)

   # define electrons
   electrons = []
   for i in xrange(event.p4_electrons.size()):
      if(abs(event.p4_electrons[i].Eta())>2.5): continue
      if(event.p4_electrons[i].Pt()<30):        continue
      if(event.st_electrons[i]!=1):             continue
      # if(JetOverlap(event.p4_electrons[i],event.p4_akt4jets,jets,"electron")): continue
      electrons.append(i)

   mTWmu = 0
   if(len(muons)>0): mTWmu = mT(event.p4_muons[muons[0]],event.p4_MET[0])
   mTWel = 0
   if(len(electrons)>0): mTWel = mT(event.p4_electrons[electrons[0]],event.p4_MET[0])


   ############
   ### cuts ###
   ############

   if(len(muons)<1 and len(electrons)<1):
      FillCutFlow("Leptons.n>0")
      continue
   if(len(jets)<4):
      FillCutFlow("Jets.n>3")
      continue
   if(len(btagged_ptsorted)<1):
      FillCutFlow("Bjets.n>0")
      continue
   if(event.p4_MET[0].Pt()<20):
      FillCutFlow("ETmiss.eT>20")
      continue
   if(event.p4_MET[0].Pt()+mTWmu<60 and event.p4_MET[0].Pt()+mTWel<60):
      FillCutFlow("ETmiss.eT+ETmiss.mTW>60")
      continue


   FillCutFlow()

   ########################
   ### event has passed ###
   ######################## 

   graphics.histos["Muons:Mult"].Fill(len(muons))
   if(len(muons)>0): graphics.histos["Muons:pT1"].Fill(event.p4_muons[muons[0]].Pt())
   if(len(muons)>1): graphics.histos["Muons:pT2"].Fill(event.p4_muons[muons[1]].Pt())
   
   graphics.histos["Electrons:Mult"].Fill(len(electrons))
   if(len(electrons)>0): graphics.histos["Electrons:pT1"].Fill(event.p4_electrons[electrons[0]].Pt())
   if(len(electrons)>1): graphics.histos["Electrons:pT2"].Fill(event.p4_electrons[electrons[1]].Pt())

   graphics.histos["Jets:Mult"].Fill(len(jets))
   if(len(jets)>0): graphics.histos["Jets:pT1"].Fill(event.p4_akt4jets[jets[0]].Pt())
   if(len(jets)>1): graphics.histos["Jets:pT2"].Fill(event.p4_akt4jets[jets[1]].Pt())
   if(len(jets)>2): graphics.histos["Jets:pT3"].Fill(event.p4_akt4jets[jets[2]].Pt())
   if(len(jets)>3): graphics.histos["Jets:pT4"].Fill(event.p4_akt4jets[jets[3]].Pt())

   graphics.histos["BJets:Mult"].Fill(len(btagged_ptsorted))
   if(len(btagged_ptsorted)>0): graphics.histos["BJets:pT1"].Fill(event.p4_akt4jets[btagged_ptsorted[0]].Pt())
   if(len(btagged_ptsorted)>1): graphics.histos["BJets:pT2"].Fill(event.p4_akt4jets[btagged_ptsorted[1]].Pt())
   if(len(btagged_ptsorted)>2): graphics.histos["BJets:pT3"].Fill(event.p4_akt4jets[btagged_ptsorted[2]].Pt())
   if(len(btagged_ptsorted)>3): graphics.histos["BJets:pT4"].Fill(event.p4_akt4jets[btagged_ptsorted[3]].Pt())

   graphics.histos["ETmiss:eT"].Fill(event.p4_MET[0].Pt())
   if(len(muons)>0 and len(electrons)==0): graphics.histos["Muons:MWT"].Fill(mT(event.p4_muons[muons[0]],event.p4_MET[0]))
   if(len(electrons)>0 and len(muons)==0): graphics.histos["Electrons:MWT"].Fill(mT(event.p4_electrons[electrons[0]],event.p4_MET[0]))


   for j in muons:
      graphics.histos["ETmiss:dPhiMuons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_muons[j].Phi()-event.p4_MET[0].Phi())) )
   for j in electrons:
      graphics.histos["ETmiss:dPhiElectrons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_electrons[j].Phi()-event.p4_MET[0].Phi())) )
   for j in jets:
     graphics.histos["ETmiss:dPhiJets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[j].Phi()-event.p4_MET[0].Phi()))  )
     for i in muons:     graphics.histos["Muons:dRJets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
     for i in electrons: graphics.histos["Electrons:dRJets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   for j in btagged_ptsorted:
      graphics.histos["ETmiss:dPhiBjets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[j].Phi()-event.p4_MET[0].Phi())) )
      for i in muons:     graphics.histos["Muons:dRBjets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
      for i in electrons: graphics.histos["Electrons:dRBjets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   for j in non_btagged:
      for i in btagged_ptsorted:
         graphics.histos["Jets:dRBjets"].Fill(event.p4_akt4jets[j].DeltaR(event.p4_akt4jets[i]))
   
   if(len(non_btagged)>1):      graphics.histos["Jets:dR12"].Fill(event.p4_akt4jets[non_btagged[0]].DeltaR(event.p4_akt4jets[non_btagged[1]]))
   if(len(btagged_ptsorted)>1): graphics.histos["BJets:dR12"].Fill(event.p4_akt4jets[btagged_ptsorted[0]].DeltaR(event.p4_akt4jets[btagged_ptsorted[1]]))

   if(len(jets)>3 and len(btagged_ptsorted)>0 and ((len(muons)>0 and len(electrons)==0) or (len(muons)==0 and len(electrons)>0)) ):
      etmis = event.p4_MET[0]
      lep   = TLorentzVector()
      if(len(muons)>0 and len(electrons)==0): lep = event.p4_muons[0]
      if(len(muons)==0 and len(electrons)>0): lep = event.p4_electrons[0]
      ttTag = TTbarTagger(event.p4_akt4jets,jets,btagged_ptsorted,lep,etmis,1)
      if(not ttTag.MinimumInput()): continue
      graphics.histos["TopTag:mTw"].Fill(ttTag.mTw)
      graphics.histos["TopTag:mTt"].Fill(ttTag.mTt)
      graphics.histos["TopTag:mw"].Fill(ttTag.mw)
      graphics.histos["TopTag:mt"].Fill(ttTag.mt)
      graphics.histos["TopTag:mtt"].Fill(ttTag.mtt)

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
graphics.plotHist(fname,     "BJets:pT3",True)
graphics.plotHist(fname,     "BJets:pT4",True)
graphics.plotHist(fname,     "ETmiss:eT",True)
graphics.plotHist(fname,     "Muons:MWT",True)
graphics.plotHist(fname,     "Electrons:MWT",True)
graphics.plotHist(fname,     "ETmiss:dPhiMuons")  
graphics.plotHist(fname,     "ETmiss:dPhiElectrons")
graphics.plotHist(fname,     "ETmiss:dPhiJets")
graphics.plotHist(fname,     "ETmiss:dPhiBjets")  
graphics.plotHist(fname,     "Muons:dRJets")  
graphics.plotHist(fname,     "Muons:dRBjets")
graphics.plotHist(fname,     "Electrons:dRJets")
graphics.plotHist(fname,     "Jets:dRBjets")
graphics.plotHist(fname,     "Jets:dR12")
graphics.plotHist(fname,     "BJets:dR12")
graphics.plotHist(fname,     "TopTag:mTw")
graphics.plotHist(fname,     "TopTag:mTt")
graphics.plotHist(fname,     "TopTag:mw")
graphics.plotHist(fname,     "TopTag:mt")
graphics.plotHist(fname+")", "TopTag:mtt")
print "=================================================== cutflow ==================================================="
print cutflow
print "==============================================================================================================="