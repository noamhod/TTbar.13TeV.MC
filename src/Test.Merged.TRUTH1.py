#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TChain, TLorentzVector, TMath, TVirtualPad, TEventList, TVector2, TRandom3
import sys
sys.path.append('/Users/hod/GitHub/2HDM')
import kinematics
import THDM
import os
import math
import cmath
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

rand = TRandom3(0)

def mT(pLep,pMET):
   mwt = math.sqrt(2*(pLep.Pt()*pMET.Pt() - pLep.Px()*pMET.Px() - pLep.Py()*pMET.Py()))
   return mwt

def WmassConstraint(lepton,etmis,wMass):
   mL = lepton.M()
   # dphi = lepton.Phi() - etmis.Phi()
   # A = (wMass*wMass-mL*mL)/2. + etmis.Pt()*lepton.Pt()*math.cos(dphi)
   A = (wMass*wMass-mL*mL)/2. + etmis.Px()*lepton.Px() + etmis.Py()*lepton.Py()
   a = math.pow(lepton.Pz(),2) - math.pow(lepton.E(),2)
   b = 2.*A*lepton.Pz()
   c = A*A - math.pow(etmis.Pt(),2)*math.pow(lepton.E(),2)
   d = b*b-4.*a*c
   z = cmath.sqrt(d)
   nuz1 = 0
   nuz2 = 0
   if(d==0):
      nuz1 = -b/(2.*a)
      nuz2 = -b/(2.*a)
   if(d>0):
      nuz1 = (-b + math.sqrt(d))/(2.*a)
      nuz2 = (-b - math.sqrt(d))/(2.*a)
   if(d<0):
      nuz1 = (-b + z.real)/(2.*a)
      nuz2 = (-b - z.real)/(2.*a)
   Enu1 = math.sqrt( math.pow(etmis.Pt(),2) + math.pow(nuz1,2) )
   Enu2 = math.sqrt( math.pow(etmis.Pt(),2) + math.pow(nuz2,2) )
   nu1 = TLorentzVector()
   nu2 = TLorentzVector()
   nu1.SetPxPyPzE(etmis.Px(),etmis.Py(),nuz1,Enu1)
   nu2.SetPxPyPzE(etmis.Px(),etmis.Py(),nuz2,Enu2)
   return (nu1,nu2)

def SetPzNu(lepton,etmis,nmaxsteps=1000):
   mW0 = 80.385
   wW0 = 2.085
   nu1,nu2 = WmassConstraint(lepton,etmis,mW0)
   isOK = (nu1.Pz()!=0 and nu2.Pz()!=0)
   if(not isOK):
      for i in xrange(1,nmaxsteps+1):
         mW = rand.BreitWigner(mW0,wW0)
         nu1,nu2 = WmassConstraint(lepton,etmis,mW)
         isOK = (nu1.Pz()!=0 and nu2.Pz()!=0)
         if(isOK):
            isOK = True
            break
   if(not isOK): nu1,nu2 = WmassConstraint(lepton,etmis,mW0)
   return (nu1,nu2)


#### get the model
type      = THDM.model.type
sba       = THDM.model.sba
mX        = THDM.model.mX
nameX     = THDM.model.nameX
cuts      = THDM.model.cuts
mgpath    = THDM.model.mgpath
alphaS    = THDM.model.alphaS
nhel      = THDM.model.nhel
libmatrix = "/Users/hod/GitHub/2HDM/matrix/"+nameX+"/"+str(mX)+"/"+str(sba)+"/"
THDM.setParameters(nameX,mX,cuts,type,sba)
THDM.setModules(libmatrix,nameX,len(THDM.parameters),"All")
print THDM.modules

#### histograms, plotters etc.
#### must be aware of the model properties
graphics = Graphics("#mu+jets","Resolved selection")
graphics.setModel(len(THDM.parameters),str(mX)+"GeV",nameX)
graphics.bookHistos()



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


cutflow = []
cutflow.append({"All":0})
cutflow.append({"Muons.n=1":0})
cutflow.append({"Electrons.n=0":0})
cutflow.append({"Jets.n>3":0})
cutflow.append({"Bjets.n>1":0})
cutflow.append({"ETmiss.eT>20":0})
cutflow.append({"ETmiss.eT+ETmiss.mTW>60":0})
def FillCutFlow(cut=""):
   for c in cutflow:
      key = c.keys()[0]
      if(key==cut): break
      c[key] += 1


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



#### begin runing over events
ngg = 0
nLepHad = 0
nTruMatch_selected_objects = 0
nTruMatch_before_selection = 0
nTruMatch_after_selection  = 0
n=1
for event in tree:

   ### counts
   if(n%10000==0):
      print "processed "+str(n)+", cutflow up to previous event:"
      print "ngg =",ngg
      print "nLepHad =",nLepHad
      print cutflow
      print "nTruMatch_before_selection =",nTruMatch_before_selection
      print "nTruMatch_after_selection  =",nTruMatch_after_selection
      print "nTruMatch_selected_objects =",nTruMatch_selected_objects
   # if(n==20000): break
   n+=1

   ### define the hard process
   hardproc = HardProcessTops(event.id_tquarks,event.p4_tquarks,event.st_tquarks,event.bc_tquarks,
                              event.id_tquarks_parents,event.p4_tquarks_parents,event.bc_tquarks_parents,
                              event.id_tquarks_children,event.p4_tquarks_children,event.bc_tquarks_children,
                              event.id_wbosons,event.p4_wbosons,event.st_wbosons,event.bc_wbosons,
                              event.id_wbosons_parents,event.p4_wbosons_parents,event.bc_wbosons_parents,
                              event.id_wbosons_children,event.p4_wbosons_children,event.bc_wbosons_children,
                              event.id_bquarks,event.p4_bquarks,event.st_bquarks,event.bc_bquarks,
                              event.id_bquarks_parents,event.p4_bquarks_parents,event.bc_bquarks_parents,
                              event.id_bquarks_children,event.p4_bquarks_children,event.bc_bquarks_children)
   # print ""
   # hardproc.PrintHardProcess()
   # print "diagram0: ",hardproc.diagrams["t"]
   # print "diagram1: ",hardproc.diagrams["tbar"]
 
   tru_mu       = TLorentzVector()
   tru_nu       = TLorentzVector()
   tru_bL_prod  = TLorentzVector()
   tru_bL_decay = TLorentzVector()
   tru_qW       = TLorentzVector()
   tru_qbarW    = TLorentzVector()
   tru_bH_prod  = TLorentzVector()
   tru_bH_decay = TLorentzVector()

   itP = [ hardproc.diagrams["t"]["t-production"], hardproc.diagrams["tbar"]["t-production"] ]
   itR = [ hardproc.diagrams["t"]["t-radiation"],  hardproc.diagrams["tbar"]["t-radiation"]  ]
   itD = [ hardproc.diagrams["t"]["t-decay"],      hardproc.diagrams["tbar"]["t-decay"]      ]
   ibP = [ hardproc.diagrams["t"]["b-production"], hardproc.diagrams["tbar"]["b-production"] ]
   ibR = [ hardproc.diagrams["t"]["b-radiation"],  hardproc.diagrams["tbar"]["b-radiation"]  ]
   ibD = [ hardproc.diagrams["t"]["b-decay"],      hardproc.diagrams["tbar"]["b-decay"]      ]
   iW  = [ hardproc.diagrams["t"]["W-decay"],      hardproc.diagrams["tbar"]["W-decay"]      ]

   #### beginning of 2HDM stuff
   if(event.id_tquarks_parents[itP[0]][0]!=21 and event.id_tquarks_parents[itP[0]][1]!=21): continue ## not a gg production
   ngg += 1

   if(abs(event.id_wbosons_children[iW[0]][0])>10):
      tru_bL_prod = event.p4_bquarks[ibP[0]]
      tru_bH_prod = event.p4_bquarks[ibP[1]]
      tru_bL_decay = event.p4_bquarks[ibD[0]]
      tru_bH_decay = event.p4_bquarks[ibD[1]]
      ## leptons
      if(event.id_wbosons_children[iW[0]][0]%2!=0):
         tru_mu = event.p4_wbosons_children[iW[0]][0]
         tru_nu = event.p4_wbosons_children[iW[0]][1]
      else:
         tru_mu = event.p4_wbosons_children[iW[0]][1]
         tru_nu = event.p4_wbosons_children[iW[0]][0]
      ## quarks
      if(event.id_wbosons_children[iW[1]][0]>0):
         tru_qW    = event.p4_wbosons_children[iW[1]][0]
         tru_qbarW = event.p4_wbosons_children[iW[1]][1]
      else:
         tru_qW    = event.p4.wbosons_children[iW[1]][1]
         tru_qbarW = event.p4.wbosons_children[iW[1]][0]
   else:
      tru_bL_prod = event.p4_bquarks[ibP[1]]
      tru_bH_prod = event.p4_bquarks[ibP[0]]
      tru_bL_decay = event.p4_bquarks[ibD[1]]
      tru_bH_decay = event.p4_bquarks[ibD[0]]
      ## leptons
      if(event.id_wbosons_children[iW[1]][0]%2!=0):
         tru_mu = event.p4_wbosons_children[iW[1]][0]
         tru_nu = event.p4_wbosons_children[iW[1]][1]
      else:
         tru_mu = event.p4_wbosons_children[iW[1]][1]
         tru_nu = event.p4_wbosons_children[iW[1]][0]
      ## quarks
      if(event.id_wbosons_children[iW[0]][0]>0):
         tru_qW    = event.p4_wbosons_children[iW[0]][0]
         tru_qbarW = event.p4_wbosons_children[iW[0]][1]
      else:
         tru_qW    = event.p4_wbosons_children[iW[0]][1]
         tru_qbarW = event.p4_wbosons_children[iW[0]][0]
   isLepHad = (abs(event.id_wbosons_children[iW[0]][0])<10 or abs(event.id_wbosons_children[iW[1]][0])<10)
   ###############################
   if(not isLepHad): continue ####
   nLepHad += 1 ##################
   ###############################

   # ilephad = [-1,-1]
   # if(abs(event.id_wbosons_children[iW[0]][0])>10): ilephad = ["lep","had"]
   # else:                                            ilephad = ["had","lep"]
   # if(itR[0]>-1):
   #    print "t-radiation, ",ilephad[0]
   #    print "  child1=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_tquarks_children[itR[0]][0], event.p4_tquarks_children[itR[0]][0].Pt(), event.p4_tquarks_children[itR[0]][0].Eta(), event.p4_tquarks_children[itR[0]][0].Phi(), event.p4_tquarks_children[itR[0]][0].E())
   #    print "  child2=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_tquarks_children[itR[0]][1], event.p4_tquarks_children[itR[0]][1].Pt(), event.p4_tquarks_children[itR[0]][1].Eta(), event.p4_tquarks_children[itR[0]][1].Phi(), event.p4_tquarks_children[itR[0]][1].E())
   #    print "   dR=",event.p4_tquarks_children[itR[0]][0].DeltaR(event.p4_tquarks_children[itR[0]][1])
   # if(itR[1]>-1):
   #    print "tbar-radiation, ",ilephad[1]
   #    print "  child1=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_tquarks_children[itR[1]][0], event.p4_tquarks_children[itR[1]][0].Pt(), event.p4_tquarks_children[itR[1]][0].Eta(), event.p4_tquarks_children[itR[1]][0].Phi(), event.p4_tquarks_children[itR[1]][0].E())
   #    print "  child2=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_tquarks_children[itR[1]][1], event.p4_tquarks_children[itR[1]][1].Pt(), event.p4_tquarks_children[itR[1]][1].Eta(), event.p4_tquarks_children[itR[1]][1].Phi(), event.p4_tquarks_children[itR[1]][1].E())
   #    print "   dR=",event.p4_tquarks_children[itR[1]][0].DeltaR(event.p4_tquarks_children[itR[1]][1])
   # if(ibR[0]>-1):
   #    print "b-radiation (%g), ",ilephad[0]
   #    print "  child1=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_bquarks_children[ibR[0]][0], event.p4_bquarks_children[ibR[0]][0].Pt(), event.p4_bquarks_children[ibR[0]][0].Eta(), event.p4_bquarks_children[ibR[0]][0].Phi(), event.p4_bquarks_children[ibR[0]][0].E())
   #    print "  child2=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_bquarks_children[ibR[0]][1], event.p4_bquarks_children[ibR[0]][1].Pt(), event.p4_bquarks_children[ibR[0]][1].Eta(), event.p4_bquarks_children[ibR[0]][1].Phi(), event.p4_bquarks_children[ibR[0]][1].E())
   #    print "   dR=",event.p4_bquarks_children[ibR[0]][0].DeltaR(event.p4_bquarks_children[ibR[0]][1])
   # if(ibR[1]>-1):
   #    print "bbar-radiation (%g), ",ilephad[1]
   #    print "  child1=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_bquarks_children[ibR[1]][0], event.p4_bquarks_children[ibR[1]][0].Pt(), event.p4_bquarks_children[ibR[1]][0].Eta(), event.p4_bquarks_children[ibR[1]][0].Phi(), event.p4_bquarks_children[ibR[1]][0].E())
   #    print "  child2=%i: ptetaphie=(%g,%g,%g,%g)" % (event.id_bquarks_children[ibR[1]][1], event.p4_bquarks_children[ibR[1]][1].Pt(), event.p4_bquarks_children[ibR[1]][1].Eta(), event.p4_bquarks_children[ibR[1]][1].Phi(), event.p4_bquarks_children[ibR[1]][1].E())
   #    print "   dR=",event.p4_bquarks_children[ibR[1]][0].DeltaR(event.p4_bquarks_children[ibR[1]][1])

   if(apnd=="yes"):
      # g1=p4_glus[0]
      # g2=p4_glus[1]
      # t1=p4_tops[0]
      # t2=p4_tops[1]
      g1 = event.p4_tquarks_parents[itP[0]][0] # = event.p4_tquarks_parents[itP[1]][0] or event.p4_tquarks_parents[itP[1]][1]
      g2 = event.p4_tquarks_parents[itP[0]][1] # = event.p4_tquarks_parents[itP[1]][1] or event.p4_tquarks_parents[itP[1]][0]
      t1 = event.p4_tquarks[itP[0]]
      t2 = event.p4_tquarks[itP[1]]
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


   tru_pjj     = tru_qW   + tru_qbarW
   tru_pjjj    = tru_pjj  + tru_bH_decay # tru_bH_prod
   tru_plv     = tru_mu   + tru_nu
   tru_plvj    = tru_plv  + tru_bL_decay # tru_bL_prod
   tru_pjjjlvj = tru_pjjj + tru_plvj
   truth = { "mjj":tru_pjj.M(), "mjjj":tru_pjj.M(), "pTjjj":tru_pjjj.Pt(),
             "mlvj":tru_plvj.M(),"pTlvj":tru_plvj.Pt(),
             "mjjjlvj":tru_pjjjlvj.M(),"pTjjjlvj":tru_pjjjlvj.Pt() }
   
   graphics.histos["HardProcess:NoSelection:mjjjlvj"].Fill( tru_pjjjlvj.M() )
   graphics.histos["HardProcess:NoSelection:mjj"].Fill( tru_pjj.M() )
   graphics.histos["HardProcess:NoSelection:mjj-mW"].Fill( tru_pjj.M()-hardproc.mW )
   graphics.histos["HardProcess:NoSelection:mjjj"].Fill( tru_pjjj.M() )
   graphics.histos["HardProcess:NoSelection:mjjj-mt"].Fill( tru_pjjj.M()-hardproc.mt )
   graphics.histos["HardProcess:NoSelection:mjjj-mjj"].Fill( tru_pjjj.M() - tru_pjj.M() )
   graphics.histos["HardProcess:NoSelection:mjjj-mjj-(mt-mW)"].Fill( tru_pjjj.M() - tru_pjj.M() - (hardproc.mt-hardproc.mW) )
   graphics.histos["HardProcess:NoSelection:mlvj"].Fill( tru_plvj.M() )
   graphics.histos["HardProcess:NoSelection:mlvj-mt"].Fill( tru_plvj.M()-hardproc.mt )
   graphics.histos["HardProcess:NoSelection:pTjjjlvj"].Fill( tru_pjjjlvj.Pt() )
   graphics.histos["HardProcess:NoSelection:pTjjj"].Fill( tru_pjjj.Pt() )
   graphics.histos["HardProcess:NoSelection:pTlvj"].Fill( tru_plvj.Pt() )
   graphics.histos["HardProcess:NoSelection:pTjjj-pTlvj"].Fill( tru_pjjj.Pt() - tru_plvj.Pt() )
   graphics.histos["HardProcess:NoSelection:dRlephad"].Fill( tru_plvj.DeltaR(tru_pjjj) )
   graphics.histos["HardProcess:NoSelection:dRwbhad"].Fill( tru_bH_decay.DeltaR(tru_pjj) ) #tru_bH_prod.DeltaR(tru_pjj)
   graphics.histos["HardProcess:NoSelection:dRwblep"].Fill( tru_bL_decay.DeltaR(tru_plv) ) #tru_bL_prod.DeltaR(tru_plv)
   ### model histograms - "reco" level
   for i in xrange(wgt.size()):
      hname1 = "HardProcess:NoSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
      hname2 = "HardProcess:NoSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
      hname3 = "HardProcess:NoSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
      hname4 = "HardProcess:NoSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
      hname5 = "HardProcess:NoSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
      hname6 = "HardProcess:NoSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
      graphics.histos[hname1].Fill(tru_pjjjlvj.M() ,wgt[i])
      graphics.histos[hname2].Fill(tru_pjjjlvj.M() ,wgt[i]-1.)
      graphics.histos[hname3].Fill(tru_pjjj.Pt() ,wgt[i])
      graphics.histos[hname4].Fill(tru_pjjj.Pt() ,wgt[i]-1.)
      graphics.histos[hname5].Fill(tru_plvj.Pt() ,wgt[i])
      graphics.histos[hname6].Fill(tru_plvj.Pt() ,wgt[i]-1.)
   
          
   
   #### best match without selection
   dRmatch = 0.4
   dPhimatch = 1.0
   matches_before_selection = {"mu":-1,"nu":-1,"bL":-1,"qW":-1,"qbarW":-1,"bH":-1}
   drmin = 100
   for j in xrange(len(event.p4_akt4jets)):
      # dr = event.p4_akt4jets[j].DeltaR(tru_bL_prod)
      dr = event.p4_akt4jets[j].DeltaR(tru_bL_decay)
      if(dr<drmin and dr<dRmatch):# and j not in matches_before_selection.values()):
         matches_before_selection["bL"] = j
         drmin = dr
   drmin = 100
   for j in xrange(len(event.p4_akt4jets)):
      dr = event.p4_akt4jets[j].DeltaR(tru_qW)
      if(dr<drmin and dr<dRmatch):# and j not in matches_before_selection.values()):
         matches_before_selection["qW"] = j
         drmin = dr
   drmin = 100
   for j in xrange(len(event.p4_akt4jets)):
      dr = event.p4_akt4jets[j].DeltaR(tru_qbarW)
      if(dr<drmin and dr<dRmatch):# and j not in matches_before_selection.values()):
         matches_before_selection["qbarW"] = j
         drmin = dr
   drmin = 100
   for j in xrange(len(event.p4_akt4jets)):
      # dr = event.p4_akt4jets[j].DeltaR(tru_bH_prod)
      dr = event.p4_akt4jets[j].DeltaR(tru_bH_decay)
      if(dr<drmin and dr<dRmatch):# and j not in matches_before_selection.values()):
         matches_before_selection["bH"] = j
         drmin = dr
   drmin = 100
   for j in xrange(len(event.p4_muons)):
      dr = event.p4_muons[j].DeltaR(tru_mu)
      if(dr<drmin and dr<dRmatch):
         matches_before_selection["mu"] = j
         drmin = dr
   ## the neutrino
   nu1,nu2 = SetPzNu(event.p4_muons[matches_before_selection["mu"]],event.p4_MET[0])
   nu0 = TLorentzVector()
   if(nu1.DeltaR(tru_nu)<nu2.DeltaR(tru_nu)): nu0 = nu1
   else:                                      nu0 = nu2
   if(abs(nu0.DeltaPhi(tru_nu))<dPhimatch): matches_before_selection["nu"] = 1
   ### count matches
   nmatched_before_selection = 0
   for key, index in matches_before_selection.iteritems():
      if(index>=0):  nmatched_before_selection  += 1
   if(nmatched_before_selection==6): nTruMatch_before_selection += 1
   
   if(nmatched_before_selection==6):
      mu = matches_before_selection["mu"]
      j1 = matches_before_selection["qW"]
      j2 = matches_before_selection["qbarW"]
      j3 = matches_before_selection["bH"]
      j4 = matches_before_selection["bL"]
      pv = nu0
      pl  = event.p4_muons[mu]
      pj1 = event.p4_akt4jets[j1]
      pj2 = event.p4_akt4jets[j2]
      pj3 = event.p4_akt4jets[j3]
      pj4 = event.p4_akt4jets[j4]
      mlvj  = (pl+pv+pj4).M()
      mlv   = (pl+pv).M()
      mjj   = (pj1+pj2).M()
      mjjj  = (pj1+pj2+pj3).M()
      pTjjj = (pj1+pj2+pj3).Pt()
      pTlvj = (pl+pv+pj4).Pt()
      mjjjlvj = (pj1+pj2+pj3+pl+pv+pj4).M()
      pTjjjlvj = (pj1+pj2+pj3+pl+pv+pj4).Pt()
      dRlephad = (pl+pv+pj4).DeltaR(pj1+pj2+pj3)
      dRwbhad  = (pj1+pj2).DeltaR(pj3)
      dRwblep  = (pl+pv).DeltaR(pj4)
   
      graphics.histos["Matched:NoSelection:mjjjlvj"].Fill(mjjjlvj)
      graphics.histos["Matched:NoSelection:mjj"].Fill(mjj)
      graphics.histos["Matched:NoSelection:mjj-mW"].Fill(mjj-hardproc.mW)
      graphics.histos["Matched:NoSelection:mjjj"].Fill(mjjj)
      graphics.histos["Matched:NoSelection:mjjj-mt"].Fill(mjjj-hardproc.mt)
      graphics.histos["Matched:NoSelection:mjjj-mjj"].Fill(mjjj-mjj)
      graphics.histos["Matched:NoSelection:mjjj-mjj-(mt-mW)"].Fill(mjjj-mjj-(hardproc.mt-hardproc.mW))
      graphics.histos["Matched:NoSelection:mlvj"].Fill(mlvj)
      graphics.histos["Matched:NoSelection:mlvj-mt"].Fill(mlvj-hardproc.mt)
      graphics.histos["Matched:NoSelection:pTjjjlvj"].Fill(pTjjjlvj)
      graphics.histos["Matched:NoSelection:pTjjj"].Fill(pTjjj)
      graphics.histos["Matched:NoSelection:pTlvj"].Fill(pTlvj)
      graphics.histos["Matched:NoSelection:pTjjj-pTlvj"].Fill(pTjjj-pTlvj)
      graphics.histos["Matched:NoSelection:dRlephad"].Fill(dRlephad)
      graphics.histos["Matched:NoSelection:dRwbhad"].Fill(dRwbhad)
      graphics.histos["Matched:NoSelection:dRwblep"].Fill(dRwblep)
      ### model histograms - "reco" level
      for i in xrange(wgt.size()):
         hname1 = "Matched:NoSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname2 = "Matched:NoSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname3 = "Matched:NoSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname4 = "Matched:NoSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname5 = "Matched:NoSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname6 = "Matched:NoSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         graphics.histos[hname1].Fill(mjjjlvj ,wgt[i])
         graphics.histos[hname2].Fill(mjjjlvj ,wgt[i]-1.)
         graphics.histos[hname3].Fill(pTjjj ,wgt[i])
         graphics.histos[hname4].Fill(pTjjj ,wgt[i]-1.)
         graphics.histos[hname5].Fill(pTlvj ,wgt[i])
         graphics.histos[hname6].Fill(pTlvj ,wgt[i]-1.)



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
   goodmuons = Leptons("muon",event.p4_muons,event.st_muons,event.p4_akt4jets,jets)
   muons = goodmuons.ileptons

   graphics.histos["Muons:Mult"].Fill(len(muons))
   if(len(muons)>0): graphics.histos["Muons:pT1"].Fill(event.p4_muons[muons[0]].Pt())
   if(len(muons)>1): graphics.histos["Muons:pT2"].Fill(event.p4_muons[muons[1]].Pt())


   # define electrons
   goodelectrons = Leptons("electron",event.p4_electrons,event.st_electrons,event.p4_akt4jets,jets)
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
   if(len(bjets)<2):
      FillCutFlow("Bjets.n>1")
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

      #################################
      ibestconf = ttTag.ibestconf #####
      if(ibestconf<0):
         print "cannot find assignment"
         quit()
      #################################

      #### best match with selection
      nmatched = 0
      dRmatch = 0.4
      dPhimatch = 1.0
      matches_after_selection = {"mu":-1,"nu":-1,"bL":-1,"qW":-1,"qbarW":-1,"bH":-1}
      drmatches_after_selection = {"mu":-1,"nu":-1,"bL":-1,"qW":-1,"qbarW":-1,"bH":-1}
      drmin = 100
      for j in jets:
         # dr = event.p4_akt4jets[j].DeltaR(tru_bL_prod)
         dr = event.p4_akt4jets[j].DeltaR(tru_bL_decay)
         if(dr<drmin):# and j not in matches_after_selection.values()):
            if(dr<dRmatch): matches_after_selection["bL"] = j
            drmin = dr
      drmatches_after_selection["bL"] = drmin
      drmin = 100
      for j in jets:
         dr = event.p4_akt4jets[j].DeltaR(tru_qW)
         if(dr<drmin):# and j not in matches_after_selection.values()):
            if(dr<dRmatch): matches_after_selection["qW"] = j
            drmin = dr
      drmatches_after_selection["qW"] = drmin
      drmin = 100
      for j in jets:
         dr = event.p4_akt4jets[j].DeltaR(tru_qbarW)
         if(dr<drmin):# and j not in matches_after_selection.values()):
            if(dr<dRmatch): matches_after_selection["qbarW"] = j
            drmin = dr
      drmatches_after_selection["qbarW"] = drmin
      drmin = 100
      for j in jets:
         # dr = event.p4_akt4jets[j].DeltaR(tru_bH_prod)
         dr = event.p4_akt4jets[j].DeltaR(tru_bH_decay)
         if(dr<drmin):# and j not in matches_after_selection.values()):
            if(dr<dRmatch): matches_after_selection["bH"] = j
            drmin = dr
      drmatches_after_selection["bH"] = drmin
      drmin = 100
      for j in muons:
         dr = event.p4_muons[j].DeltaR(tru_mu)
         if(dr<drmin and dr<dRmatch):
            matches_after_selection["mu"] = j
            drmin = dr
      drmatches_after_selection["mu"] = drmin
      ## the neutrino
      nu1,nu2 = SetPzNu(event.p4_muons[matches_after_selection["mu"]],event.p4_MET[0])
      nu0 = TLorentzVector()
      if(nu1.DeltaR(tru_nu)<nu2.DeltaR(tru_nu)): nu0 = nu1
      else:                                      nu0 = nu2
      dphi = abs(nu0.DeltaPhi(tru_nu))
      if(dphi<dPhimatch): matches_after_selection["nu"] = 1
      drmatches_after_selection["nu"] = dphi
      
      ### count matches_after_selection
      nmatched_after_selection = 0
      for key, index in matches_after_selection.iteritems():
         if(index>=0): nmatched_after_selection  += 1

      graphics.histos["BestMatching:dR:mu"].Fill(drmatches_after_selection["mu"])
      graphics.histos["BestMatching:dR:nu"].Fill(drmatches_after_selection["nu"])
      graphics.histos["BestMatching:dR:bL"].Fill(drmatches_after_selection["bL"])
      graphics.histos["BestMatching:dR:q"].Fill(drmatches_after_selection["qW"])
      graphics.histos["BestMatching:dR:qbar"].Fill(drmatches_after_selection["qbarW"])
      graphics.histos["BestMatching:dR:bH"].Fill(drmatches_after_selection["bH"])      

      if(nmatched_after_selection==6):
         nTruMatch_after_selection += 1
         mu = matches_after_selection["mu"]
         j1 = matches_after_selection["qW"]
         j2 = matches_after_selection["qbarW"]
         j3 = matches_after_selection["bH"]
         j4 = matches_after_selection["bL"]
         pv = nu0
         pl  = event.p4_muons[mu]
         pj1 = event.p4_akt4jets[j1]
         pj2 = event.p4_akt4jets[j2]
         pj3 = event.p4_akt4jets[j3]
         pj4 = event.p4_akt4jets[j4]
         mlvj  = (pl+pv+pj4).M()
         mlv   = (pl+pv).M()
         mjj   = (pj1+pj2).M()
         mjjj  = (pj1+pj2+pj3).M()
         pTjjj = (pj1+pj2+pj3).Pt()
         pTlvj = (pl+pv+pj4).Pt()
         mjjjlvj = (pj1+pj2+pj3+pl+pv+pj4).M()
         pTjjjlvj = (pj1+pj2+pj3+pl+pv+pj4).Pt()
         dRlephad = (pl+pv+pj4).DeltaR(pj1+pj2+pj3)
         dRwbhad  = (pj1+pj2).DeltaR(pj3)
         dRwblep  = (pl+pv).DeltaR(pj4)
         graphics.histos["Matched:WithSelection:mjjjlvj"].Fill(mjjjlvj)
         graphics.histos["Matched:WithSelection:mjj"].Fill(mjj)
         graphics.histos["Matched:WithSelection:mjj-mW"].Fill(mjj-hardproc.mW)
         graphics.histos["Matched:WithSelection:mjjj"].Fill(mjjj)
         graphics.histos["Matched:WithSelection:mjjj-mt"].Fill(mjjj-hardproc.mt)
         graphics.histos["Matched:WithSelection:mjjj-mjj"].Fill(mjjj-mjj)
         graphics.histos["Matched:WithSelection:mjjj-mjj-(mt-mW)"].Fill(mjjj-mjj-(hardproc.mt-hardproc.mW))
         graphics.histos["Matched:WithSelection:mlvj"].Fill(mlvj)
         graphics.histos["Matched:WithSelection:mlvj-mt"].Fill(mlvj-hardproc.mt)
         graphics.histos["Matched:WithSelection:pTjjjlvj"].Fill(pTjjjlvj)
         graphics.histos["Matched:WithSelection:pTjjj"].Fill(pTjjj)
         graphics.histos["Matched:WithSelection:pTlvj"].Fill(pTlvj)
         graphics.histos["Matched:WithSelection:pTjjj-pTlvj"].Fill(pTjjj-pTlvj)
         graphics.histos["Matched:WithSelection:dRlephad"].Fill(dRlephad)
         graphics.histos["Matched:WithSelection:dRwbhad"].Fill(dRwbhad)
         graphics.histos["Matched:WithSelection:dRwblep"].Fill(dRwblep)
         ### model histograms - "reco" level
         for i in xrange(wgt.size()):
            hname1 = "Matched:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname2 = "Matched:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            hname3 = "Matched:WithSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname4 = "Matched:WithSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            hname5 = "Matched:WithSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname6 = "Matched:WithSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            graphics.histos[hname1].Fill(mjjjlvj ,wgt[i])
            graphics.histos[hname2].Fill(mjjjlvj ,wgt[i]-1.)
            graphics.histos[hname3].Fill(pTjjj ,wgt[i])
            graphics.histos[hname4].Fill(pTjjj ,wgt[i]-1.)
            graphics.histos[hname5].Fill(pTlvj ,wgt[i])
            graphics.histos[hname6].Fill(pTlvj ,wgt[i]-1.)
   
   
      #### match to the selected objects
      nv = ttTag.configurations[ibestconf]["nu"]
      j1 = ttTag.configurations[ibestconf]["j1"]
      j2 = ttTag.configurations[ibestconf]["j2"]
      j3 = ttTag.configurations[ibestconf]["j3"]
      j4 = ttTag.configurations[ibestconf]["j4"]
      j3a = ttTag.configurations[ibestconf]["j3a"]
      j4a = ttTag.configurations[ibestconf]["j4a"]
      pv = TLorentzVector()
      if(nv==0): pv = ttTag.p4_nu1
      else:      pv = ttTag.p4_nu2
      pl  = ttTag.p4_lepton
      pj1 = ttTag.jets[j1]
      pj2 = ttTag.jets[j2]
      pj3 = ttTag.jets[j3]
      pj4 = ttTag.jets[j4]
      ptH   = pj1+pj2+pj3
      if(j3a>-1): ptH = ptH+ttTag.jets[j3a]
      ptL   = pl+pv+pj4
      if(j4a>-1): ptL = ptL+ttTag.jets[j4a]
      mlvj  = ptL.M()
      mlv   = (pl+pv).M()
      mjj   = (pj1+pj2).M()
      mjjj  = ptH.M()
      pTjjj = ptH.Pt()
      pTlvj = ptL.Pt()
      mjjjlvj = (ptL+ptH).M()
      pTjjjlvj = (ptL+ptH).Pt()
      dRlephad = ptL.DeltaR(ptH)
      dRwbhad  = (pj1+pj2).DeltaR(pj3)
      dRwblep  = (pl+pv).DeltaR(pj4)
      ### for parton-level matching
      rec_mu = pl
      rec_nu = pv
      rec_j4 = pj4
      rec_j1 = pj1
      rec_j2 = pj2
      rec_j3 = pj3
      ### selected objects rec-tru matching counter
      matching = {"tlep.mu":0, "tlep.nu":0, "tlep.j4":0, "thad.j1":0, "thad.j2":0, "thad.j3":0}
      if(rec_mu.DeltaR(tru_mu)<dRmatch):                                     matching["tlep.mu"] = 1
      if(abs(rec_nu.DeltaPhi(tru_nu))<dPhimatch):                            matching["tlep.nu"] = 1
      # if(rec_nu.DeltaR(tru_nu)<dRmatch):                                   matching["tlep.nu"] = 1
      # if(rec_j4.DeltaR(tru_bL_prod)<dRmatch):                              matching["tlep.j4"] = 1
      if(rec_j4.DeltaR(tru_qW)<dRmatch or rec_j4.DeltaR(tru_qbarW)<dRmatch or rec_j4.DeltaR(tru_bH_decay)<dRmatch or rec_j4.DeltaR(tru_bL_decay)<dRmatch): matching["tlep.j4"] = 1
      if(rec_j1.DeltaR(tru_qW)<dRmatch or rec_j1.DeltaR(tru_qbarW)<dRmatch or rec_j1.DeltaR(tru_bH_decay)<dRmatch or rec_j1.DeltaR(tru_bL_decay)<dRmatch): matching["thad.j1"] = 1
      if(rec_j2.DeltaR(tru_qW)<dRmatch or rec_j2.DeltaR(tru_qbarW)<dRmatch or rec_j2.DeltaR(tru_bH_decay)<dRmatch or rec_j2.DeltaR(tru_bL_decay)<dRmatch): matching["thad.j2"] = 1
      # if(rec_j3.DeltaR(tru_bH_prod)<dRmatch):                              matching["thad.j3"] = 1
      if(rec_j3.DeltaR(tru_qW)<dRmatch or rec_j3.DeltaR(tru_qbarW)<dRmatch or rec_j3.DeltaR(tru_bH_decay)<dRmatch or rec_j3.DeltaR(tru_bL_decay)<dRmatch): matching["thad.j3"] = 1
      for key, flag in matching.iteritems():
         nmatched += flag
      
      # print "min chi2 index =",ibestconf
      # print "obj flags  : %i,%i,%i,%i ; %i,%i" % (matching["thad.j1"],matching["thad.j2"],matching["thad.j3"],matching["tlep.j4"],matching["tlep.mu"],matching["tlep.nu"])
      # print "obj index  : %i,%i,%i,%i" % (j1,j2,j3,j4)
      # print "best index : %i,%i,%i,%i ; %g,%g" % (matches_after_selection["qW"],matches_after_selection["qbarW"],matches_after_selection["bH"],matches_after_selection["bL"],matches_after_selection["mu"],matches_after_selection["nu"])
      # print "best dR    : %g,%g,%g,%g ; %g,%g" % (drmatches_after_selection["qW"],drmatches_after_selection["qbarW"],drmatches_after_selection["bH"],drmatches_after_selection["bL"],drmatches_after_selection["mu"],drmatches_after_selection["nu"])
      # if(nmatched_after_selection==6): print "Should be fully matched"
      # else:                            print "Cannot be fully matched"
      # if(nmatched==6):                 print " --> fully matched"
      # else:                            print " --> NOT matched"
      # print ""

      graphics.histos["Matching:dR:mu"].Fill(rec_mu.DeltaR(tru_mu))
      graphics.histos["Matching:dR:nu"].Fill(rec_nu.DeltaR(tru_nu))
      graphics.histos["Matching:dR:bL"].Fill(rec_j4.DeltaR(tru_bL_decay)) # rec_j4.DeltaR(tru_bL_prod)
      if(rec_j1.DeltaR(tru_qW)<rec_j2.DeltaR(tru_qW)):       graphics.histos["Matching:dR:q"].Fill(rec_j1.DeltaR(tru_qW))
      else:                                                  graphics.histos["Matching:dR:q"].Fill(rec_j2.DeltaR(tru_qW))
      if(rec_j1.DeltaR(tru_qbarW)<rec_j2.DeltaR(tru_qbarW)): graphics.histos["Matching:dR:qbar"].Fill(rec_j1.DeltaR(tru_qbarW))
      else:                                                  graphics.histos["Matching:dR:qbar"].Fill(rec_j2.DeltaR(tru_qbarW))
      graphics.histos["Matching:dR:bH"].Fill(rec_j3.DeltaR(tru_bH_decay)) # rec_j3.DeltaR(tru_bH_prod)
     
      graphics.histos["HardProcess:WithSelection:mjjjlvj"].Fill( tru_pjjjlvj.M() )
      graphics.histos["HardProcess:WithSelection:mjj"].Fill( tru_pjj.M() )
      graphics.histos["HardProcess:WithSelection:mjj-mW"].Fill( tru_pjj.M()-hardproc.mW )
      graphics.histos["HardProcess:WithSelection:mjjj"].Fill( tru_pjjj.M() )
      graphics.histos["HardProcess:WithSelection:mjjj-mt"].Fill( tru_pjjj.M()-hardproc.mt )
      graphics.histos["HardProcess:WithSelection:mjjj-mjj"].Fill( tru_pjjj.M() - tru_pjj.M())
      graphics.histos["HardProcess:WithSelection:mjjj-mjj-(mt-mW)"].Fill( tru_pjjj.M() - tru_pjj.M() - (hardproc.mt-hardproc.mW))
      graphics.histos["HardProcess:WithSelection:mlvj"].Fill( tru_plvj.M() )
      graphics.histos["HardProcess:WithSelection:mlvj-mt"].Fill( tru_plvj.M() - hardproc.mt )
      graphics.histos["HardProcess:WithSelection:pTjjjlvj"].Fill( tru_pjjjlvj.Pt() )
      graphics.histos["HardProcess:WithSelection:pTjjj"].Fill( tru_pjjj.Pt() )
      graphics.histos["HardProcess:WithSelection:pTlvj"].Fill( tru_plvj.Pt() )
      graphics.histos["HardProcess:WithSelection:pTjjj-pTlvj"].Fill( tru_pjjj.Pt() - tru_plvj.Pt() )
      graphics.histos["HardProcess:WithSelection:dRlephad"].Fill( tru_plvj.DeltaR(tru_pjjj) )
      graphics.histos["HardProcess:WithSelection:dRwbhad"].Fill( tru_bH_decay.DeltaR(tru_pjj) ) # tru_bH_prod.DeltaR(tru_pjj)
      graphics.histos["HardProcess:WithSelection:dRwblep"].Fill( tru_bL_decay.DeltaR(tru_plv) ) # tru_bL_prod.DeltaR(tru_plv)
      ### model histograms - "reco" level
      for i in xrange(wgt.size()):
         hname1 = "HardProcess:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname2 = "HardProcess:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname3 = "HardProcess:WithSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname4 = "HardProcess:WithSelection:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname5 = "HardProcess:WithSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname6 = "HardProcess:WithSelection:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         graphics.histos[hname1].Fill(tru_pjjjlvj.M() ,wgt[i])
         graphics.histos[hname2].Fill(tru_pjjjlvj.M() ,wgt[i]-1.)
         graphics.histos[hname3].Fill(tru_pjjj.Pt() ,wgt[i])
         graphics.histos[hname4].Fill(tru_pjjj.Pt() ,wgt[i]-1.)
         graphics.histos[hname5].Fill(tru_plvj.Pt() ,wgt[i])
         graphics.histos[hname6].Fill(tru_plvj.Pt() ,wgt[i]-1.)

      ############################
      # if(nmatched<6): continue ###
      if(nmatched==6): nTruMatch_selected_objects += 1
      ############################

      graphics.histos["All:SelectedObjects:mjjjlvj"].Fill(mjjjlvj)
      graphics.histos["All:SelectedObjects:mjj"].Fill(mjj)
      graphics.histos["All:SelectedObjects:mjj-mW"].Fill(mjj-hardproc.mW)
      graphics.histos["All:SelectedObjects:mjjj"].Fill(mjjj)
      graphics.histos["All:SelectedObjects:mjjj-mt"].Fill(mjjj-hardproc.mt)
      graphics.histos["All:SelectedObjects:mjjj-mjj"].Fill(mjjj-mjj)
      graphics.histos["All:SelectedObjects:mjjj-mjj-(mt-mW)"].Fill(mjjj-mjj-(hardproc.mt-hardproc.mW))
      graphics.histos["All:SelectedObjects:mlvj"].Fill(mlvj)
      graphics.histos["All:SelectedObjects:mlvj-mt"].Fill(mlvj-hardproc.mt)
      graphics.histos["All:SelectedObjects:pTjjjlvj"].Fill(pTjjjlvj)
      graphics.histos["All:SelectedObjects:pTjjj"].Fill(pTjjj)
      graphics.histos["All:SelectedObjects:pTlvj"].Fill(pTlvj)
      graphics.histos["All:SelectedObjects:pTjjj-pTlvj"].Fill(pTjjj-pTlvj)
      graphics.histos["All:SelectedObjects:dRlephad"].Fill(dRlephad)
      graphics.histos["All:SelectedObjects:dRwbhad"].Fill(dRwbhad)
      graphics.histos["All:SelectedObjects:dRwblep"].Fill(dRwblep)
      ### model histograms - "reco" level
      for i in xrange(wgt.size()):
         hname1 = "All:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname2 = "All:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname3 = "All:SelectedObjects:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname4 = "All:SelectedObjects:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         hname5 = "All:SelectedObjects:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname6 = "All:SelectedObjects:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         graphics.histos[hname1].Fill(mjjjlvj ,wgt[i])
         graphics.histos[hname2].Fill(mjjjlvj ,wgt[i]-1.)
         graphics.histos[hname3].Fill(pTjjj ,wgt[i])
         graphics.histos[hname4].Fill(pTjjj ,wgt[i]-1.)
         graphics.histos[hname5].Fill(pTlvj ,wgt[i])
         graphics.histos[hname6].Fill(pTlvj ,wgt[i]-1.)


      if(nmatched==6):
         graphics.histos["Matched:SelectedObjects:mjjjlvj"].Fill(mjjjlvj)
         graphics.histos["Matched:SelectedObjects:mjj"].Fill(mjj)
         graphics.histos["Matched:SelectedObjects:mjj-mW"].Fill(mjj-hardproc.mW)
         graphics.histos["Matched:SelectedObjects:mjjj"].Fill(mjjj)
         graphics.histos["Matched:SelectedObjects:mjjj-mt"].Fill(mjjj-hardproc.mt)
         graphics.histos["Matched:SelectedObjects:mjjj-mjj"].Fill(mjjj-mjj)
         graphics.histos["Matched:SelectedObjects:mjjj-mjj-(mt-mW)"].Fill(mjjj-mjj-(hardproc.mt-hardproc.mW))
         graphics.histos["Matched:SelectedObjects:mlvj"].Fill(mlvj)
         graphics.histos["Matched:SelectedObjects:mlvj-mt"].Fill(mlvj-hardproc.mt)
         graphics.histos["Matched:SelectedObjects:pTjjjlvj"].Fill(pTjjjlvj)
         graphics.histos["Matched:SelectedObjects:pTjjj"].Fill(pTjjj)
         graphics.histos["Matched:SelectedObjects:pTlvj"].Fill(pTlvj)
         graphics.histos["Matched:SelectedObjects:pTjjj-pTlvj"].Fill(pTjjj-pTlvj)
         graphics.histos["Matched:SelectedObjects:dRlephad"].Fill(dRlephad)
         graphics.histos["Matched:SelectedObjects:dRwbhad"].Fill(dRwbhad)
         graphics.histos["Matched:SelectedObjects:dRwblep"].Fill(dRwblep)
         ### model histograms - "reco" level
         for i in xrange(wgt.size()):
            hname1 = "Matched:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname2 = "Matched:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            hname3 = "Matched:SelectedObjects:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname4 = "Matched:SelectedObjects:pTjjj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            hname5 = "Matched:SelectedObjects:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname6 = "Matched:SelectedObjects:pTlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            graphics.histos[hname1].Fill(mjjjlvj ,wgt[i])
            graphics.histos[hname2].Fill(mjjjlvj ,wgt[i]-1.)
            graphics.histos[hname3].Fill(pTjjj ,wgt[i])
            graphics.histos[hname4].Fill(pTjjj ,wgt[i]-1.)
            graphics.histos[hname5].Fill(pTlvj ,wgt[i])
            graphics.histos[hname6].Fill(pTlvj ,wgt[i]-1.)

      graphics.histos["TopTag:mTw"].Fill(mTW)
      graphics.histos["TopTag:mwL"].Fill(mlv)
      graphics.histos["TopTag:mtL"].Fill(mlvj)
      graphics.histos["TopTag:mwH"].Fill(mjj)
      graphics.histos["TopTag:mtH"].Fill(mjjj)
      graphics.histos["TopTag:mtt"].Fill(mjjjlvj)
      graphics.histos["TopTag:pTtLep"].Fill(pTlvj)
      graphics.histos["TopTag:pTtHad"].Fill(pTjjj)
      graphics.histos["TopTag:dRlephad"].Fill(dRlephad)
      
      ### model histograms - "reco" level
      for i in xrange(wgt.size()):
         hname1 = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
         hname2 = "TopTag:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
         graphics.histos[hname1].Fill(mjjjlvj ,wgt[i])
         graphics.histos[hname2].Fill(mjjjlvj ,wgt[i]-1.)
      
      ######## this is process specific ########
      if(ibestconf>=0):
         graphics.histos["HardProcessTops:dRlep"].Fill( (pl+pv+pj4).DeltaR(tru_plvj) )
         graphics.histos["HardProcessTops:dRhad"].Fill( (pj1+pj2+pj3).DeltaR(tru_pjjj) )
         graphics.histos["HardProcessTops:dpTRellep"].Fill(pTlvj/truth["pTlvj"]-1.)
         graphics.histos["HardProcessTops:dpTRelhad"].Fill(pTjjj/truth["pTjjj"]-1.)
         graphics.histos["HardProcessTops:mtt"].Fill( truth["mjjjlvj"] )
         graphics.histos["HardProcessTops:pTtLep"].Fill( truth["pTlvj"] )
         graphics.histos["HardProcessTops:pTtHad"].Fill( truth["pTjjj"] )
         graphics.histos["HardProcessTops:dmRel"].Fill(mjjjlvj/truth["mjjjlvj"]-1.)
         graphics.histos["HardProcessTops:dpTRel:dRtru:lep"].Fill( (pl+pv+pj4).DeltaR(tru_plvj),   pTlvj/truth["pTlvj"]-1.)
         graphics.histos["HardProcessTops:dpTRel:dRtru:had"].Fill( (pj1+pj2+pj3).DeltaR(tru_pjjj), pTjjj/truth["pTjjj"]-1.)
      
         ### model histograms - hard process
         for i in xrange(wgt.size()):
            hname1 = "HardProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
            hname2 = "HardProcessTops:2HDM::mtt:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
            graphics.histos[hname1].Fill( truth["mjjjlvj"] ,wgt[i])
            graphics.histos[hname2].Fill( truth["mjjjlvj"] ,wgt[i]-1.)
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
graphics.plotHist(fname,     "Jets:Mult")
graphics.plotHist(fname,     "Jets:pT1",True)
graphics.plotHist(fname,     "Jets:pT2",True)
graphics.plotHist(fname,     "Jets:pT3",True)
graphics.plotHist(fname,     "Jets:pT4",True)
graphics.plotHist(fname,     "BJets:Mult")
graphics.plotHist(fname,     "BJets:pT1",True)
graphics.plotHist(fname,     "BJets:pT2",True)
graphics.plotHist(fname,     "ETmiss:eT",True)
graphics.plotHist(fname,     "Muons:MWT",False)
graphics.plotHist(fname,     "Jets:dR12")
graphics.plotHist(fname,     "BJets:dR12")
graphics.plotHist(fname,     "TopTag:mwH")
graphics.plotHist(fname,     "TopTag:mTw")
graphics.plotHist(fname,     "TopTag:mwL")
graphics.plotHist(fname,     "TopTag:mtH")
graphics.plotHist(fname,     "TopTag:mtL")
graphics.plotHist(fname,     "TopTag:dRlephad")
graphics.plotHist(fname,     "HardProcessTops:dRhad")
graphics.plotHist(fname,     "HardProcessTops:dRlep")
graphics.plotHist(fname,     "HardProcessTops:dpTRelhad")
graphics.plotHist(fname,     "HardProcessTops:dpTRellep")
graphics.plotHist2(fname,    "TopTag:pTtHad","HardProcessTops:pTtHad")
graphics.plotHist2(fname,    "TopTag:pTtLep","HardProcessTops:pTtLep")
graphics.plotHist2(fname,    "TopTag:mtt","HardProcessTops:mtt")
graphics.plotHist(fname,     "HardProcessTops:dmRel")
graphics.plotHist2D(fname,   "HardProcessTops:dpTRel:dRtru:had",True)
graphics.plotHist2D(fname,   "HardProcessTops:dpTRel:dRtru:lep",True)
graphics.plotHist(fname,     "Matching:dR:mu")
graphics.plotHist(fname,     "Matching:dR:nu")
graphics.plotHist(fname,     "Matching:dR:bL")
graphics.plotHist(fname,     "Matching:dR:q")
graphics.plotHist(fname,     "Matching:dR:qbar")
graphics.plotHist(fname,     "Matching:dR:bH")
graphics.plotHist(fname,     "BestMatching:dR:mu")
graphics.plotHist(fname,     "BestMatching:dR:nu")
graphics.plotHist(fname,     "BestMatching:dR:bL")
graphics.plotHist(fname,     "BestMatching:dR:q")
graphics.plotHist(fname,     "BestMatching:dR:qbar")
graphics.plotHist(fname,     "BestMatching:dR:bH")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjjjlvj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjj-mW",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjjj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjjj-mt",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjjj-mjj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mjjj-mjj-(mt-mW)",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mlvj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:mlvj-mt",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:pTjjjlvj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:pTjjj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:pTlvj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:NoSelection:pTjjj-pTlvj",False,"top products (before selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjjjlvj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjj-mW",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjjj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjjj-mt",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjjj-mjj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mjjj-mjj-(mt-mW)",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mlvj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:mlvj-mt",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:pTjjjlvj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:pTjjj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:pTlvj",False,"top products (after selection)")
graphics.plotHist(fname,     "HardProcess:WithSelection:pTjjj-pTlvj",False,"top products (after selection)")
graphics.plotHist(fname,     "Matched:NoSelection:mjjjlvj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjj-mW",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjjj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjjj-mt",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjjj-mjj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mjjj-mjj-(mt-mW)",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mlvj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:mlvj-mt",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:pTjjjlvj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:pTjjj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:pTlvj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:NoSelection:pTjjj-pTlvj",False,"Reco+matched, before selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjjjlvj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjj-mW",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjjj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjjj-mt",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjjj-mjj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mjjj-mjj-(mt-mW)",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mlvj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:mlvj-mt",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:pTjjjlvj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:pTjjj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:pTlvj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:WithSelection:pTjjj-pTlvj",False,"Reco+matched, after selection")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjjjlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjj-mW",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjjj-mt",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjjj-mjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mjjj-mjj-(mt-mW)",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:mlvj-mt",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:pTjjjlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:pTjjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:pTlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "Matched:SelectedObjects:pTjjj-pTlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjjjlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjj-mW",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjjj-mt",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjjj-mjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mjjj-mjj-(mt-mW)",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:mlvj-mt",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:pTjjjlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:pTjjj",False,"Reco+matched, selected objects")
graphics.plotHist(fname,     "All:SelectedObjects:pTlvj",False,"Reco+matched, selected objects")
graphics.plotHist(fname+")", "All:SelectedObjects:pTjjj-pTlvj",False,"Reco+matched, selected objects")

fname0 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.pdf"
fname1 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.ratio.reco_all.pdf"
fname2 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.ratio.reco_matched.pdf"
fname3 = path+"/Test.TTree.TRUTH1."+name+"."+nameX+"."+str(mX)+"GeV.ratio.hardprocess.pdf"
### model histograms
tanbindices = {}
for i in xrange(len(THDM.parameters)):
   tanb = str(THDM.parameters[i].get("tanb"))
   tanbindices.update({tanb:i})
ihistos = collections.OrderedDict(sorted(tanbindices.items())).values()
ii=0
for i in ihistos:
   name_xx_all = "All:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
   name_ix_all = "All:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
   name_xx_mat = "Matched:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
   name_ix_mat = "Matched:SelectedObjects:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
   name_xx_hps = "HardProcess:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":"+str(i)
   name_ix_hps = "HardProcess:WithSelection:mjjjlvj:"+graphics.ModelName+":"+graphics.ModelMass+":IX:"+str(i)
   name_sm_all = "All:SelectedObjects:mjjjlvj"
   name_sm_mat = "Matched:SelectedObjects:mjjjlvj"
   name_sm_hps = "HardProcess:WithSelection:mjjjlvj"
   tanb   = '%.2f' % THDM.parameters[i].get("tanb")
   sinba  = '%.2f' % THDM.parameters[i].get("sba")
   wX = THDM.parameters[i].get("w"+nameX)/mX*100
   model = "m_{"+nameX+"}="+str(mX)+" GeV, tan#beta="+str(tanb)+", sin(#beta-#alpha)="+str(sinba)
   suff = ""
   if(len(THDM.parameters)>1):
      if(ii==0):                        suff = "("
      elif(ii==len(THDM.parameters)-1): suff = ")"
      else:                             suff = ""
   # graphics.plotHist4(fname0+suff,model,name1,name2,name00,name4)
   graphics.plotRatio(fname1+suff,'Selected (all)',     name_sm_all,name_xx_all,name_ix_all,wX,tanb,sinba,nameX,mX)
   graphics.plotRatio(fname2+suff,'Selected (matched)', name_sm_mat,name_xx_mat,name_ix_mat,wX,tanb,sinba,nameX,mX)
   graphics.plotRatio(fname3+suff,"Hard-process",       name_sm_hps,name_xx_hps,name_ix_hps,wX,tanb,sinba,nameX,mX)
   ii += 1

hfname = path+"/histograms."+name+"."+nameX+"."+str(mX)+"GeV.root"
graphics.writeHistos(hfname)

print "=================================================== cutflow ==================================================="
print "Processed: ",n
print "ngg =",ngg
print "nLepHad = ",nLepHad
print cutflow
print "nTruMatch_before_selection = ",nTruMatch_before_selection
print "nTruMatch_after_selection  = ",nTruMatch_after_selection
print "nTruMatch_selected_objects = ",nTruMatch_selected_objects
print "==============================================================================================================="