#!/usr/bin/env python
import os
import math
from array import array
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>',  required=True, help='The process name')
parser.add_argument('-i', metavar='<process jobid>', required=True, help='The process job id')
args = parser.parse_args()
name  = args.n
jobid = args.i
print 'name  : ',name
print 'jobid : ',jobid

# Set up ROOT and RootCore:
import ROOT
from ROOT import std, gROOT, TFile, TTree, TLorentzVector
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
if(not ROOT.xAOD.Init().isSuccess()): print "Failed xAOD.Init()" # Initialize the xAOD infrastructure

# Set up the input files:
xaodpath = "$HOME/data/MC/ttbar/ntup/"
fullpath = ROOT.gSystem.ExpandPathName(xaodpath)
fileName = fullpath+"/DAOD_TRUTH1.NTUP."+name+"."+jobid+".root"
if(not os.path.isfile(fileName)):
   print "ERROR, file "+fileName+" does not exist"
   quit()
treeName = "CollectionTree" # default when making transient tree anyway
f = ROOT.TFile.Open(fileName)
t = ROOT.xAOD.MakeTransientTree(f,treeName) # Make the "transient tree"

#ROOT.xAOD.TFileAccessTracer.enableDataSubmission(False)

tfile = "tops.SM.TRUTH1.root"
tfile = TFile(tfile,"RECREATE")
tree = TTree("SM","SM")

p4_muons     = ROOT.vector(TLorentzVector)()
id_muons     = ROOT.vector(int)()
st_muons     = ROOT.vector(int)()
p4_electrons = ROOT.vector(TLorentzVector)()
id_electrons = ROOT.vector(int)()
st_electrons = ROOT.vector(int)()
p4_bquarks   = ROOT.vector(TLorentzVector)()
id_bquarks   = ROOT.vector(int)()
st_bquarks   = ROOT.vector(int)()
p4_akt4jets  = ROOT.vector(TLorentzVector)()
p4_akt4dRb   = ROOT.vector(float)()
p4_MET       = ROOT.vector(TLorentzVector)()

RunNumber = array( 'i', [ 0 ] )
EventNumber = array( 'i', [ 0 ] )

tree.Branch("p4_muons",p4_muons)
tree.Branch("id_muons",id_muons)
tree.Branch("st_muons",st_muons)
tree.Branch("p4_electrons",p4_electrons)
tree.Branch("id_electrons",id_electrons)
tree.Branch("st_electrons",st_electrons)
tree.Branch("p4_bquarks",p4_bquarks)
tree.Branch("id_bquarks",id_bquarks)
tree.Branch("st_bquarks",st_bquarks)
tree.Branch("p4_akt4jets",p4_akt4jets)
tree.Branch("p4_akt4dRb",p4_akt4dRb)
tree.Branch("p4_MET",p4_MET)
tree.Branch("RunNumber",RunNumber,"RunNumber/I")
tree.Branch("EventNumber",EventNumber,"EventNumber/I")


def ClearVectors():
   p4_muons.clear()
   id_muons.clear()
   st_muons.clear()
   p4_electrons.clear()
   id_electrons.clear()
   st_electrons.clear()
   p4_bquarks.clear()
   id_bquarks.clear()
   st_bquarks.clear()
   p4_akt4jets.clear()
   p4_akt4dRb.clear()
   p4_MET.clear()


npassed = 0
print( "Number of input events: %s" % t.GetEntries() )
for entry in xrange(t.GetEntries()):
   t.GetEntry(entry)
   ClearVectors()

   for i in xrange(t.TruthParticles.size()):
      p = t.TruthParticles.at(i)
      if(abs(p.pdgId())==5):
         v = TLorentzVector()
         v.SetPxPyPzE(p.px()/1000,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
         p4_bquarks.push_back(v)
         id_bquarks.push_back(p.pdgId())
         st_bquarks.push_back(p.status())
   for i in xrange(t.TruthMuons.size()):
      p = t.TruthMuons.at(i)
      #if(p.status()!=1 or abs(p.eta())>2.5 or p.pt()/1000.<30.): continue
      v = TLorentzVector()
      v.SetPxPyPzE(p.px()/1000,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
      p4_muons.push_back(v)
      id_muons.push_back(p.pdgId())
      st_muons.push_back(p.status())
      pass # end for loop over truth particles collection
   for i in xrange(t.TruthElectrons.size()):
      p = t.TruthElectrons.at(i)
      #if(p.status()!=1 or abs(p.eta())>2.5 or p.pt()/1000.<30.): continue
      v = TLorentzVector()
      v.SetPxPyPzE(p.px()/1000,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
      p4_electrons.push_back(v)
      id_electrons.push_back(p.pdgId())
      st_electrons.push_back(p.status())
      pass # end for loop over truth particles collection
   for i in xrange(t.AntiKt4TruthJets.size()):
      p = t.AntiKt4TruthJets.at(i)
      ### dRb = ROOT.xAOD.TruthLabelDeltaR_B("TruthLabelDeltaR_B")
      ### if(dRb.isAvailable(p)): p4_akt4dRb.push_back(dRb(p))
      ### else:                   p4_akt4dRb.push_back(1000.)
      #if(abs(p.eta())>2.5 or p.pt()/1000.<25.): continue
      v = TLorentzVector()
      v.SetPtEtaPhiM(p.pt()/1000,p.eta()/1000.,p.phi()/1000.,p.m()/1000.)
      p4_akt4jets.push_back(v)
      pass # end for loop over truth particles collection

   MET    = t.MET_Truth["NonInt"].met()/1000
   METphi = t.MET_Truth["NonInt"].phi()
   METx   = MET*math.cos(METphi)
   METy   = MET*math.sin(METphi)
   v.SetPtEtaPhiE(MET,0.,METphi,MET)
   p4_MET.push_back(v)

   RunNumber[0] = t.EventInfo.runNumber()
   EventNumber[0] = t.EventInfo.eventNumber()

   '''
   MWT = 0
   if(p4_muons.size()==1):     MWT = math.sqrt(2*(p4_muons[0].Pt()*MET     - p4_muons[0].Px()*METx     - p4_muons[0].Py()*METy))
   if(p4_electrons.size()==1): MWT = math.sqrt(2*(p4_electrons[0].Pt()*MET - p4_electrons[0].Px()*METx - p4_electrons[0].Py()*METy))

   if(p4_muons.size()==1 or p4_electrons.size()==1): continue
   if(p4_akt4jets.size()>=4):                        continue
   if(p4_MET[0].E()>20.):                            continue
   if(MET+MWT<60.):                                  continue
   npassed = npassed+1
   '''

   tree.Fill()

   if(entry%1000==0):
      print("Processing run %i, event %i, entry %i" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber(), entry+1) )
      print("nmuons=%i, nelectrons=%i, njets=%i, MET=%g") % (p4_muons.size(),p4_electrons.size(),p4_akt4jets.size(),p4_MET[0].E())

   pass # end loop over entries
ClearVectors() # cleanup
print "nPassed = ",npassed
tree.GetCurrentFile().Write()
tree.GetCurrentFile().Close()
print "all OK!"
