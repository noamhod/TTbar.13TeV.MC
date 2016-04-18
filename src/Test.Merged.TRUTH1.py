#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TChain, TLorentzVector, TMath, TVirtualPad, TEventList, TVector2
import sys
sys.path.append('/Users/hod/GitHub/2HDM')
import kinematics
import THDM
import os
import math
import subprocess
import collections
import rootstyle
from graphics import Graphics
from TTbarTagger import TTbarTagger
from TTbarSelection import Jets, Leptons, HardProcessTops
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name [lep/had]')
parser.add_argument('-r', metavar='<re-hadd ntupe>', required=True, help='Re-hadd ntuple ? [yes/no]')
parser.add_argument('-a', metavar='<append weights>', required=True, help='Append 2HDM weights ? [yes/no]')
args = parser.parse_args()
name = args.n
hadd = args.r
apnd = args.a
print 'process name : ',name
print 'redo hadd ? : ',hadd
print 'append weights ? : ',apnd

ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = ROOT.gSystem.ExpandPathName("$HOME/Downloads/tops")
# path = "/afs/cern.ch/user/h/hod/data/MC/ttbar/ntup"
fmerged = path+"/tops.SM.TRUTH1."+name+".merged.root"
if(hadd=="yes"):
   p = subprocess.Popen("rm -f  "+path+"/tops.SM.TRUTH1."+name+".merged.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   p = subprocess.Popen("hadd  "+fmerged+"  "+path+"/tops.SM.TRUTH1."+name+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   print out


gROOT.LoadMacro( "src/Loader.C+" )
# tfile = TFile(path+"/tops.SM.TRUTH1."+name+".merged.root","READ")
# tree = tfile.Get("SM")
tree = TChain("SM")
tree.Add(path+"/tops.SM.TRUTH1."+name+".*.root")


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


#### get the model
type      = THDM.model.type
sba       = THDM.model.sba
mX        = THDM.model.mX
nameX     = THDM.model.nameX
cuts      = THDM.model.cuts
mgpath    = THDM.model.mgpath
alphaS    = THDM.model.alphaS
nhel      = THDM.model.nhel
libmatrix = "/Users/hod/GitHub/2HDM/matrix/"+nameX+"/"+str(mX)+"/"
THDM.setParameters(nameX,mX,cuts,type,sba)
THDM.setModules(libmatrix,nameX,len(THDM.parameters),"All")
print THDM.modules



### output tree
Nk = tree.GetEntries()
sNk = str(Nk/1000)+"k"
wgt   = ROOT.std.vector("double")()
tnb   = ROOT.std.vector("double")()
wdtA  = ROOT.std.vector("double")()
wdtH  = ROOT.std.vector("double")()
ymt   = ROOT.std.vector("double")()
ymb   = ROOT.std.vector("double")()
ymc   = ROOT.std.vector("double")()
ymtau = ROOT.std.vector("double")()
ymmu  = ROOT.std.vector("double")()

outFile = ""
newFile = TFile()
newtree = TTree()

if(apnd=="yes"):
   outFile = path+"/2HDM."+nameX+"."+str(mX)+"GeV.tree."+sNk+".root" 
   newFile = TFile(outFile,"RECREATE") 
   newtree = tree.CloneTree(0)
   newtree.Branch("wgt",wgt)
   newtree.Branch("tnb",tnb)
   newtree.Branch("wdtA",wdtA)
   newtree.Branch("wdtH",wdtH)
   newtree.Branch("ymt",ymt)
   newtree.Branch("ymb",ymb)
   newtree.Branch("ymc",ymc)
   newtree.Branch("ymtau",ymtau)
   newtree.Branch("ymmu",ymmu)


#### histograms, plotters etc.
#### must be aware of the model properties
graphics = Graphics()
graphics.setModel(len(THDM.parameters),str(mX)+"GeV",nameX)
graphics.bookHistos()



#### begin runing over events
n=1
for event in tree:

   ### counts
   if(n%10000==0):
      print "processed "+str(n)+", cutflow up to previous event:"
      print cutflow
   # if(n==10000): break
   n+=1

   ### define the hard process
   hardproc = HardProcessTops(event.id_tquarks,event.p4_tquarks,event.st_tquarks,event.id_tquarks_parents,event.p4_tquarks_parents,
                              event.id_wbosons,event.p4_wbosons,event.st_wbosons,event.id_wbosons_parents,event.p4_wbosons_parents,event.id_wbosons_children,event.p4_wbosons_children)
   id_tops  = hardproc.id_tops
   p4_glus  = hardproc.p4_gluons
   p4_tops  = hardproc.p4_tops
   topdecay = hardproc.topdecay

   #### beginning of 2HDM stuff
   if(apnd=="yes"):
      g1=p4_glus[0]
      g2=p4_glus[1]
      t1=p4_tops[0]
      t2=p4_tops[1]
      mtt = (t1+t2).M()
      p = [[ g1.E(), g1.Px(), g1.Py(), g1.Pz() ],
           [ g2.E(), g2.Px(), g2.Py(), g2.Pz() ],
           [ t1.E(), t1.Px(), t1.Py(), t1.Pz() ],
           [ t2.E(), t2.Px(), t2.Py(), t2.Pz() ]]
      P=THDM.invert_momenta(p)
      ## the ME^2 and the weight (once, not per tanb or similar)
      me2SM = THDM.modules['matrix2SMpy'].get_me(P,alphaS,nhel)  ### calculate the SM ME^2
      ### clear decoration branches
      wgt.clear()
      tnb.clear()
      wdtA.clear()
      wdtH.clear()
      ymt.clear()
      ymb.clear()
      ymc.clear()
      ymtau.clear()
      ymmu.clear()
      ### loop over all model points
      for i in xrange(len(THDM.parameters)):
         ## the ME^2 and the weight
         me2XX = THDM.modules['matrix2'+nameX+str(i)+'py'].get_me(P,alphaS,nhel) ### calculate the X ME^2
         weightX = me2XX/me2SM                                                   ### calculate the weight
         wgt.push_back(weightX)
         tnb.push_back(THDM.parameters[i].get("tanb"))
         wdtA.push_back(THDM.parameters[i].get("wA"))
         wdtH.push_back(THDM.parameters[i].get("wH"))
         ymt.push_back(THDM.parameters[i].get("YMT"))
         ymb.push_back(THDM.parameters[i].get("YMB"))
         ymc.push_back(THDM.parameters[i].get("YMC"))
         ymtau.push_back(THDM.parameters[i].get("YMTAU"))
         ymmu.push_back(THDM.parameters[i].get("YMM"))
      newtree.Fill()
   #### end of 2HDM stuff


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
      ttTag = TTbarTagger(event.p4_akt4jets,jets,bjets,lep,etmis,event.EventNumber,1)
      if(not ttTag.MinimumInput()): continue

      # print "MET=(%g,%g,%g,%g), E=%g, M=%g" % (etmis.Pt(),etmis.Eta(),etmis.Phi(),etmis.M(),etmis.E(),etmis.M())
      # print "nu1=(%g,%g,%g,%g), pT=%g, M=%g" % (ttTag.p4_nu1.Px(),ttTag.p4_nu1.Py(),ttTag.p4_nu1.Pz(),ttTag.p4_nu1.E(),ttTag.p4_nu1.Pt(),ttTag.p4_nu1.M())
      # print "nu2=(%g,%g,%g,%g), pT=%g, M=%g" % (ttTag.p4_nu2.Px(),ttTag.p4_nu2.Py(),ttTag.p4_nu2.Pz(),ttTag.p4_nu2.E(),ttTag.p4_nu2.Pt(),ttTag.p4_nu2.M())
      # print "mW1=",(ttTag.p4_lepton+ttTag.p4_nu1).M()
      # print "mW2=",(ttTag.p4_lepton+ttTag.p4_nu2).M()
      # print "cost1=",ttTag.p4_lepton.Vect().Dot(ttTag.p4_nu1.Vect())/(ttTag.p4_lepton.Vect().Mag()*ttTag.p4_nu1.Vect().Mag())
      # print "cost2=",ttTag.p4_lepton.Vect().Dot(ttTag.p4_nu2.Vect())/(ttTag.p4_lepton.Vect().Mag()*ttTag.p4_nu2.Vect().Mag())
      for k in xrange(event.p4_wbosons.size()):
         if(event.id_wbosons_children[k].size()!=2): continue
         id0 = abs(event.id_wbosons_children[k][0])
         id1 = abs(event.id_wbosons_children[k][1])
         if((id0==14 and id1==13) or (id0==13 and id1==14)): continue
         v = TLorentzVector()
         l = TLorentzVector()
         if(id0==14 and id1==13):
            v = event.p4_wbosons_children[k][0]
            l = event.p4_wbosons_children[k][1]
         else:
            v = event.p4_wbosons_children[k][1]
            l = event.p4_wbosons_children[k][0]
         # cost = v.Vect().Dot(l.Vect())/(v.Vect().Mag()*l.Vect().Mag())
         # print "cost=",cost
         # print "v=(%g,%g,%g,%g), pT=%g, M=%g" % (v.Px(),v.Py(),v.Pz(),v.E(),v.Pt(),v.M())
         # print "l=(%g,%g,%g,%g), pT=%g, M=%g" % (l.Px(),l.Py(),l.Pz(),l.E(),l.Pt(),l.M())
         # print "mW=",(l+v).M()
         # print ""

      graphics.histos["TopTag:mTw"].Fill(ttTag.mTw)
      graphics.histos["TopTag:mLw"].Fill(ttTag.p4_Wl.M())
      graphics.histos["TopTag:mLw0"].Fill(ttTag.p4_Wl.M())
      graphics.histos["TopTag:mLw1"].Fill(ttTag.p4_Wl1.M())
      graphics.histos["TopTag:mLw2"].Fill(ttTag.p4_Wl2.M())
      graphics.histos["TopTag:dRLw12"].Fill(ttTag.p4_Wl1.DeltaR(ttTag.p4_Wl2))
      graphics.histos["TopTag:mTt"].Fill(ttTag.mTt)
      graphics.histos["TopTag:mLt"].Fill(ttTag.p4_tl.M())
      graphics.histos["TopTag:mLt0"].Fill(ttTag.p4_tl.M())
      graphics.histos["TopTag:mLt1"].Fill(ttTag.p4_tl1.M())
      graphics.histos["TopTag:mLt2"].Fill(ttTag.p4_tl2.M())
      graphics.histos["TopTag:dRLt12"].Fill(ttTag.p4_tl1.DeltaR(ttTag.p4_tl2))
      graphics.histos["TopTag:mwHad"].Fill(ttTag.p4_w.M())#(ttTag.mw)
      graphics.histos["TopTag:mtHad"].Fill(ttTag.p4_t.M())#(ttTag.mt)
      graphics.histos["TopTag:mTtt"].Fill( (ttTag.p4_t+ttTag.p4_tT).M() )#(ttTag.mtt)
      graphics.histos["TopTag:mtt"].Fill( (ttTag.p4_t+ttTag.p4_tl).M() )#(ttTag.mtt)
      graphics.histos["TopTag:mtt0"].Fill( (ttTag.p4_t+ttTag.p4_tl).M() )
      graphics.histos["TopTag:mtt1"].Fill( (ttTag.p4_t+ttTag.p4_tl1).M() )
      graphics.histos["TopTag:mtt2"].Fill( (ttTag.p4_t+ttTag.p4_tl2).M() )
      graphics.histos["TopTag:pTtTLep"].Fill(ttTag.p4_tT.Pt())
      graphics.histos["TopTag:pTtLep"].Fill(ttTag.p4_tl.Pt())
      graphics.histos["TopTag:pTtLep0"].Fill(ttTag.p4_tl.Pt())
      graphics.histos["TopTag:pTtLep1"].Fill(ttTag.p4_tl1.Pt())
      graphics.histos["TopTag:pTtLep2"].Fill(ttTag.p4_tl2.Pt())
      graphics.histos["TopTag:pTtHad"].Fill(ttTag.p4_t.Pt())
      graphics.histos["TopTag:dRlepThad"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tT))
      graphics.histos["TopTag:dRlephad"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tl))#(ttTag.p4_t.DeltaR(ttTag.p4_tT))
      graphics.histos["TopTag:dRlep0had"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tl))
      graphics.histos["TopTag:dRlep1had"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tl1))
      graphics.histos["TopTag:dRlep2had"].Fill(ttTag.p4_t.DeltaR(ttTag.p4_tl2))

      ### model histograms - "reco" level
      for i in xrange(wgt.size()):
         hname1 = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname2 = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         graphics.histos[hname1].Fill( (ttTag.p4_t+ttTag.p4_tl).M() ,wgt[i])
         graphics.histos[hname2].Fill( (ttTag.p4_t+ttTag.p4_tl).M() ,wgt[i]-1.)

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
         graphics.histos["HarProcessTops:dRlepT"].Fill(ttTag.p4_tT.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRlep"].Fill(ttTag.p4_tl.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRlep0"].Fill(ttTag.p4_tl.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRlep1"].Fill(ttTag.p4_tl1.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRlep2"].Fill(ttTag.p4_tl2.DeltaR(p4_tops[itL]))
         graphics.histos["HarProcessTops:dRhad"].Fill(ttTag.p4_t.DeltaR(p4_tops[itH]))
         graphics.histos["HarProcessTops:dpTRellepT"].Fill( (ttTag.p4_tT.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRellep"].Fill( (ttTag.p4_tl.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRellep0"].Fill( (ttTag.p4_tl.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRellep1"].Fill( (ttTag.p4_tl1.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRellep2"].Fill( (ttTag.p4_tl2.Pt()-p4_tops[itL].Pt())/p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:dpTRelhad"].Fill( (ttTag.p4_t.Pt()-p4_tops[itH].Pt())/p4_tops[itH].Pt() )
         graphics.histos["HarProcessTops:mtt"].Fill( (p4_tops[0]+p4_tops[1]).M() )
         graphics.histos["HarProcessTops:pTlep"].Fill( p4_tops[itL].Pt() )
         graphics.histos["HarProcessTops:pThad"].Fill( p4_tops[itH].Pt() )
         graphics.histos["HarProcessTops:dmRellepT"].Fill( (ttTag.p4_t+ttTag.p4_tT).M()/(p4_tops[0]+p4_tops[1]).M()-1. )
         graphics.histos["HarProcessTops:dmRellep"].Fill( (ttTag.p4_t+ttTag.p4_tl).M()/(p4_tops[0]+p4_tops[1]).M()-1. )
         graphics.histos["HarProcessTops:dpTRel:dRtru:lepT"].Fill( ttTag.p4_tT.DeltaR(p4_tops[itL]) , ttTag.p4_tT.Pt()/p4_tops[itL].Pt()-1. )
         graphics.histos["HarProcessTops:dpTRel:dRtru:lep"].Fill( ttTag.p4_tl.DeltaR(p4_tops[itL]) , ttTag.p4_tl.Pt()/p4_tops[itL].Pt()-1. )
         graphics.histos["HarProcessTops:dpTRel:dRtru:had"].Fill( ttTag.p4_t.DeltaR(p4_tops[itH]) , ttTag.p4_t.Pt()/p4_tops[itH].Pt()-1. )

         ### model histograms - hard process
         for i in xrange(wgt.size()):
            hname1 = "HarProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname2 = "HarProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            graphics.histos[hname1].Fill( (p4_tops[0]+p4_tops[1]).M() ,wgt[i])
            graphics.histos[hname2].Fill( (p4_tops[0]+p4_tops[1]).M() ,wgt[i]-1.)
	   

      else:
         print "Warning: hard process problem in event %i (EventNumber=%i and RunNumber=%i)" % (n,event.EventNumber,event.RunNumber)
         print id_tops
         print topdecay
      ###########################################

   ### end of events loop

if(apnd=="yes"):
   # use GetCurrentFile just in case we went over the
   # (customizable) maximum file size
   newtree.GetCurrentFile().Write() 
   newtree.GetCurrentFile().Close()

# plot everything
fname = path+"/Test.TTree.TRUTH1."+name+".pdf"
graphics.plotHist(fname+"(", "Muons:Mult")
graphics.plotHist(fname,     "Muons:pT1",True)
graphics.plotHist(fname,     "Muons:pT2",True)
graphics.plotHist(fname,     "Electrons:Mult")
#graphics.plotHist(fname,     "Electrons:pT1",True)
#graphics.plotHist(fname,     "Electrons:pT2",True)
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
graphics.plotHist(fname,     "Muons:MWT",False)
#graphics.plotHist(fname,     "Electrons:MWT",True)
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
graphics.plotHist(fname,     "TopTag:mwHad")
graphics.plotHist(fname,     "TopTag:mTw")
graphics.plotHist(fname,     "TopTag:mLw")
graphics.plotHist(fname,     "TopTag:mLw0")
graphics.plotHist(fname,     "TopTag:mLw1")
graphics.plotHist(fname,     "TopTag:mLw2")
graphics.plotHist(fname,     "TopTag:dRLw12")
graphics.plotHist(fname,     "TopTag:mtHad")
graphics.plotHist(fname,     "TopTag:mTt")
graphics.plotHist(fname,     "TopTag:mLt")
graphics.plotHist(fname,     "TopTag:mLt0")
graphics.plotHist(fname,     "TopTag:mLt1")
graphics.plotHist(fname,     "TopTag:mLt2")
graphics.plotHist(fname,     "TopTag:dRLt12")
graphics.plotHist(fname,     "TopTag:dRlepThad")
graphics.plotHist(fname,     "TopTag:dRlephad")
graphics.plotHist(fname,     "TopTag:dRlep0had")
graphics.plotHist(fname,     "TopTag:dRlep1had")
graphics.plotHist(fname,     "TopTag:dRlep2had")
graphics.plotHist(fname,     "HarProcessTops:dRhad")
graphics.plotHist(fname,     "HarProcessTops:dRlepT")
graphics.plotHist(fname,     "HarProcessTops:dRlep")
graphics.plotHist(fname,     "HarProcessTops:dRlep0")
graphics.plotHist(fname,     "HarProcessTops:dRlep1")
graphics.plotHist(fname,     "HarProcessTops:dRlep2")
graphics.plotHist(fname,     "HarProcessTops:dpTRelhad")
graphics.plotHist(fname,     "HarProcessTops:dpTRellepT")
graphics.plotHist(fname,     "HarProcessTops:dpTRellep")
graphics.plotHist(fname,     "HarProcessTops:dpTRellep0")
graphics.plotHist(fname,     "HarProcessTops:dpTRellep1")
graphics.plotHist(fname,     "HarProcessTops:dpTRellep2")
graphics.plotHist2(fname,    "TopTag:pTtHad","HarProcessTops:pThad")
graphics.plotHist2(fname,    "TopTag:pTtTLep","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:pTtLep","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:pTtLep0","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:pTtLep1","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:pTtLep2","HarProcessTops:pTlep")
graphics.plotHist2(fname,    "TopTag:mTtt","HarProcessTops:mtt")
graphics.plotHist2(fname,    "TopTag:mtt","HarProcessTops:mtt")
graphics.plotHist2(fname,    "TopTag:mtt0","HarProcessTops:mtt")
graphics.plotHist2(fname,    "TopTag:mtt1","HarProcessTops:mtt")
graphics.plotHist2(fname,    "TopTag:mtt2","HarProcessTops:mtt")
graphics.plotHist(fname,     "HarProcessTops:dmRellepT")
graphics.plotHist(fname,     "HarProcessTops:dmRellep")
graphics.plotHist2D(fname,     "HarProcessTops:dpTRel:dRtru:had",True)
graphics.plotHist2D(fname,     "HarProcessTops:dpTRel:dRtru:lepT",True)
graphics.plotHist2D(fname+")", "HarProcessTops:dpTRel:dRtru:lep",True)

fname1 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.pdf"
fname2 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.ratio.reconstructed.pdf"
fname3 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.ratio.hardprocess.pdf"
### model histograms
tanbindices = {}
for i in xrange(len(THDM.parameters)):
   tanb = str(THDM.parameters[i].get("tanb"))
   tanbindices.update({tanb:i})
ihistos = collections.OrderedDict(sorted(tanbindices.items())).values()
ii=0
for i in ihistos:
   name1 = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
   name1i = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
   name2 = "HarProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
   name2i = "HarProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
   name3 = "TopTag:mtt"
   name4 = "HarProcessTops:mtt"
   tanb = '%.2f' % THDM.parameters[i].get("tanb")
   wX = THDM.parameters[i].get("w"+nameX)/mX*100
   model = "m_{"+nameX+"}="+str(mX)+" GeV, tan#beta="+str(tanb)
   suff = ""
   if(ii==0):                        suff = "("
   elif(ii==len(THDM.parameters)-1): suff = ")"
   else:                             suff = ""
   graphics.plotHist4(fname1+suff,model,name1,name2,name3,name4)
   graphics.plotRatio(fname2+suff,'"Reconstructed" level tops',  name3,name1,name1i,wX,tanb,nameX,mX)
   graphics.plotRatio(fname3+suff,"Hard-process level tops",     name4,name2,name2i,wX,tanb,nameX,mX)
   ii += 1

# hfname = path+"/histograms."+name+"."+nameX+".root"
# graphics.writeHistos(hfname)

print "=================================================== cutflow ==================================================="
print "Processessed: ",n
print cutflow
print "==============================================================================================================="