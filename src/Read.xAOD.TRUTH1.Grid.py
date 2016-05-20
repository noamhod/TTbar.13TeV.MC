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
ROOT.gROOT.SetBatch(1)
from ROOT import std, gROOT, TFile, TTree, TLorentzVector
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
if(not ROOT.xAOD.Init().isSuccess()): print "Failed xAOD.Init()" # Initialize the xAOD infrastructure


sample = ""
if  (name=="HT0"): sample = "user.cyoung.TRUTH1.13TeV.407200.MGPy8EG_A14N_ttbarNp012p_1of5.8May16.eXX1_EXT0"
elif(name=="HT1"): sample = "user.cyoung.TRUTH1.13TeV.407201.MGPy8EG_A14N_ttbarNp012p_2of5.9May16.eXX1_EXT0"
elif(name=="HT2"): sample = "user.cyoung.TRUTH1.13TeV.407202.MGPy8EG_A14N_ttbarNp012p_3of5.9May16.eXX1_EXT0"
elif(name=="HT3"): sample = "user.cyoung.TRUTH1.13TeV.407203.MGPy8EG_A14N_ttbarNp012p_4of5.9May16.eXX1_EXT0"
elif(name=="HT4"): sample = "user.cyoung.TRUTH1.13TeV.407204.MGPy8EG_A14N_ttbarNp012p_5of5.9May16.eXX1_EXT0"
else:
   print "unknown sample bin:",name
   quit()

home = ROOT.gSystem.ExpandPathName("$HOME")
base = home+"/data/MC/ttbar/ntup/MGPy8EG_A14N_ttbarNp012p"
sampledir = base+"/"+sample
files = os.listdir(sampledir)
print "in direcrtory",sampledir
print "N files =",len(files)

# Set up the input files:
job = int(jobid)-1
print "jobid=",jobid
print "job=",job
print "len(files)=",len(files)
print files
fileName = sampledir+"/"+files[int(job)]
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
bc_muons     = ROOT.vector(int)()
p4_electrons = ROOT.vector(TLorentzVector)()
id_electrons = ROOT.vector(int)()
st_electrons = ROOT.vector(int)()
bc_electrons = ROOT.vector(int)()

p4_bquarks   = ROOT.vector(TLorentzVector)()
id_bquarks   = ROOT.vector(int)()
st_bquarks   = ROOT.vector(int)()
bc_bquarks   = ROOT.vector(int)()
p4_bquarks_parents  = ROOT.vector(ROOT.vector(TLorentzVector))()
id_bquarks_parents  = ROOT.vector(ROOT.vector(int))()
bc_bquarks_parents  = ROOT.vector(ROOT.vector(int))()
p4_bquarks_children = ROOT.vector(ROOT.vector(TLorentzVector))()
id_bquarks_children = ROOT.vector(ROOT.vector(int))()
bc_bquarks_children = ROOT.vector(ROOT.vector(int))()

p4_tquarks = ROOT.vector(TLorentzVector)()
id_tquarks = ROOT.vector(int)()
st_tquarks = ROOT.vector(int)()
bc_tquarks = ROOT.vector(int)()
p4_tquarks_parents  = ROOT.vector(ROOT.vector(TLorentzVector))()
id_tquarks_parents  = ROOT.vector(ROOT.vector(int))()
bc_tquarks_parents  = ROOT.vector(ROOT.vector(int))()
p4_tquarks_children = ROOT.vector(ROOT.vector(TLorentzVector))()
id_tquarks_children = ROOT.vector(ROOT.vector(int))()
bc_tquarks_children = ROOT.vector(ROOT.vector(int))()

p4_wbosons = ROOT.vector(TLorentzVector)()
id_wbosons = ROOT.vector(int)()
st_wbosons = ROOT.vector(int)()
bc_wbosons = ROOT.vector(int)()
p4_wbosons_parents  = ROOT.vector(ROOT.vector(TLorentzVector))()
id_wbosons_parents  = ROOT.vector(ROOT.vector(int))()
bc_wbosons_parents  = ROOT.vector(ROOT.vector(int))()
p4_wbosons_children = ROOT.vector(ROOT.vector(TLorentzVector))()
id_wbosons_children = ROOT.vector(ROOT.vector(int))()
bc_wbosons_children = ROOT.vector(ROOT.vector(int))()

p4_akt4jets  = ROOT.vector(TLorentzVector)()
p4_MET       = ROOT.vector(TLorentzVector)()

RunNumber     = array( 'i', [ 0 ] )
EventNumber   = array( 'i', [ 0 ] )
MCEventWeight = array( 'f', [ 0 ] )
geneff        = array( 'f', [ 0 ] )
sigma         = array( 'f', [ 0 ] )

tree.Branch("p4_bquarks",p4_bquarks)
tree.Branch("id_bquarks",id_bquarks)
tree.Branch("st_bquarks",st_bquarks)
tree.Branch("bc_bquarks",bc_bquarks)
tree.Branch("p4_bquarks_parents",p4_bquarks_parents)
tree.Branch("id_bquarks_parents",id_bquarks_parents)
tree.Branch("bc_bquarks_parents",bc_bquarks_parents)
tree.Branch("p4_bquarks_children",p4_bquarks_children)
tree.Branch("id_bquarks_children",id_bquarks_children)
tree.Branch("bc_bquarks_children",bc_bquarks_children)

tree.Branch("p4_tquarks",p4_tquarks)
tree.Branch("id_tquarks",id_tquarks)
tree.Branch("st_tquarks",st_tquarks)
tree.Branch("bc_tquarks",bc_tquarks)
tree.Branch("p4_tquarks_parents",p4_tquarks_parents)
tree.Branch("id_tquarks_parents",id_tquarks_parents)
tree.Branch("bc_tquarks_parents",bc_tquarks_parents)
tree.Branch("p4_tquarks_children",p4_tquarks_children)
tree.Branch("id_tquarks_children",id_tquarks_children)
tree.Branch("bc_tquarks_children",bc_tquarks_children)

tree.Branch("p4_wbosons",p4_wbosons)
tree.Branch("id_wbosons",id_wbosons)
tree.Branch("st_wbosons",st_wbosons)
tree.Branch("bc_wbosons",bc_wbosons)
tree.Branch("p4_wbosons_parents",p4_wbosons_parents)
tree.Branch("id_wbosons_parents",id_wbosons_parents)
tree.Branch("bc_wbosons_parents",bc_wbosons_parents)
tree.Branch("p4_wbosons_children",p4_wbosons_children)
tree.Branch("id_wbosons_children",id_wbosons_children)
tree.Branch("bc_wbosons_children",bc_wbosons_children)

tree.Branch("p4_muons",p4_muons)
tree.Branch("id_muons",id_muons)
tree.Branch("st_muons",st_muons)
tree.Branch("bc_muons",bc_muons)

tree.Branch("p4_electrons",p4_electrons)
tree.Branch("id_electrons",id_electrons)
tree.Branch("st_electrons",st_electrons)
tree.Branch("bc_electrons",bc_electrons)

tree.Branch("p4_akt4jets",p4_akt4jets)

tree.Branch("p4_MET",p4_MET)

tree.Branch("RunNumber",RunNumber,"RunNumber/I")
tree.Branch("EventNumber",EventNumber,"EventNumber/I")
tree.Branch("MCEventWeight",MCEventWeight,"MCEventWeight/F")
tree.Branch("geneff",geneff,"geneff/F")
tree.Branch("sigma",sigma,"sigma/F")


def ClearVectors():
   ### b-quarks
   p4_bquarks.clear()
   id_bquarks.clear()
   st_bquarks.clear()
   bc_bquarks.clear()
   for i in xrange(p4_bquarks_parents.size()):
      p4_bquarks_parents[i].clear()
      id_bquarks_parents[i].clear()
      bc_bquarks_parents[i].clear()
   p4_bquarks_parents.clear()
   id_bquarks_parents.clear()
   bc_bquarks_parents.clear()
   for i in xrange(p4_bquarks_children.size()):
      p4_bquarks_children[i].clear()
      id_bquarks_children[i].clear()
      bc_bquarks_children[i].clear()
   p4_bquarks_children.clear()
   id_bquarks_children.clear()
   bc_bquarks_children.clear()
   ### t-quarks
   p4_tquarks.clear()
   id_tquarks.clear()
   st_tquarks.clear()
   bc_tquarks.clear()
   for i in xrange(p4_tquarks_parents.size()):
      p4_tquarks_parents[i].clear()
      id_tquarks_parents[i].clear()
      bc_tquarks_parents[i].clear()
   p4_tquarks_parents.clear()
   id_tquarks_parents.clear()
   bc_tquarks_parents.clear()
   for i in xrange(p4_tquarks_children.size()):
      p4_tquarks_children[i].clear()
      id_tquarks_children[i].clear()
      bc_tquarks_children[i].clear()
   p4_tquarks_children.clear()
   id_tquarks_children.clear()
   bc_tquarks_children.clear()
   ### W-bosons
   p4_wbosons.clear()
   id_wbosons.clear()
   st_wbosons.clear()
   bc_wbosons.clear()
   for i in xrange(p4_wbosons_parents.size()):
      p4_wbosons_parents[i].clear()
      id_wbosons_parents[i].clear()
      bc_wbosons_parents[i].clear()
   p4_wbosons_parents.clear()
   id_wbosons_parents.clear()
   bc_wbosons_parents.clear()
   for i in xrange(p4_wbosons_children.size()):
      p4_wbosons_children[i].clear()
      id_wbosons_children[i].clear()
      bc_wbosons_children[i].clear()
   p4_wbosons_children.clear()
   id_wbosons_children.clear()
   bc_wbosons_children.clear()

   ### met
   p4_MET.clear()
   ### muons
   p4_muons.clear()
   id_muons.clear()
   st_muons.clear()
   bc_muons.clear()
   ### electrons
   p4_electrons.clear()
   id_electrons.clear()
   st_electrons.clear()
   bc_electrons.clear()
   ### jets
   p4_akt4jets.clear()


p4_tmp = ROOT.vector(TLorentzVector)()
id_tmp = ROOT.vector(int)()
bc_tmp = ROOT.vector(int)()

npassed = 0
print( "Number of input events: %s" % t.GetEntries() )
for entry in xrange(t.GetEntries()):
   t.GetEntry(entry)
   ClearVectors()

   for i in xrange(t.TruthParticles.size()):
      p = t.TruthParticles.at(i)
      ### get b-quarks with parents and children
      if(abs(p.pdgId())==5):
         v = TLorentzVector()
         v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
         p4_bquarks.push_back(v)
         id_bquarks.push_back(p.pdgId())
         st_bquarks.push_back(p.status())
         bc_bquarks.push_back(p.barcode())
         p4_bquarks_parents.push_back(p4_tmp)
         id_bquarks_parents.push_back(id_tmp)
         bc_bquarks_parents.push_back(bc_tmp)
         p4_bquarks_children.push_back(p4_tmp)
         id_bquarks_children.push_back(id_tmp)
         bc_bquarks_children.push_back(bc_tmp)
         if(p.hasProdVtx()):
            prodvtx = p.prodVtx()
            for j in xrange(prodvtx.nIncomingParticles()):
               parent = prodvtx.incomingParticle(j)
               if(not parent): continue
               v.SetPxPyPzE(parent.px()/1000.,parent.py()/1000.,parent.pz()/1000.,parent.e()/1000.)
               p4_bquarks_parents[p4_bquarks_parents.size()-1].push_back(v)
               id_bquarks_parents[id_bquarks_parents.size()-1].push_back(parent.pdgId())
               bc_bquarks_parents[bc_bquarks_parents.size()-1].push_back(parent.barcode())
         if(p.hasDecayVtx()):
            decayvtx = p.decayVtx()
            for j in xrange(decayvtx.nOutgoingParticles()):
               child = decayvtx.outgoingParticle(j)
               if(not child): continue
               v.SetPxPyPzE(child.px()/1000.,child.py()/1000.,child.pz()/1000.,child.e()/1000.)
               p4_bquarks_children[p4_bquarks_children.size()-1].push_back(v)
               id_bquarks_children[id_bquarks_children.size()-1].push_back(child.pdgId())
               bc_bquarks_children[bc_bquarks_children.size()-1].push_back(child.barcode())
      ### get t-quarks with parents and children
      if(abs(p.pdgId())==6):
         v = TLorentzVector()
         v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
         p4_tquarks.push_back(v)
         id_tquarks.push_back(p.pdgId())
         st_tquarks.push_back(p.status())
         bc_tquarks.push_back(p.barcode())
         p4_tquarks_parents.push_back(p4_tmp)
         id_tquarks_parents.push_back(id_tmp)
         bc_tquarks_parents.push_back(bc_tmp)
         p4_tquarks_children.push_back(p4_tmp)
         id_tquarks_children.push_back(id_tmp)
         bc_tquarks_children.push_back(bc_tmp)
         if(p.hasProdVtx()):
            prodvtx = p.prodVtx()
            for j in xrange(prodvtx.nIncomingParticles()):
               parent = prodvtx.incomingParticle(j)
               if(not parent): continue
               v.SetPxPyPzE(parent.px()/1000.,parent.py()/1000.,parent.pz()/1000.,parent.e()/1000.)
               p4_tquarks_parents[p4_tquarks_parents.size()-1].push_back(v)
               id_tquarks_parents[id_tquarks_parents.size()-1].push_back(parent.pdgId())
               bc_tquarks_parents[bc_tquarks_parents.size()-1].push_back(parent.barcode())
         if(p.hasDecayVtx()):
            decayvtx = p.decayVtx()
            for j in xrange(decayvtx.nOutgoingParticles()):
               child = decayvtx.outgoingParticle(j)
               if(not child): continue
               v.SetPxPyPzE(child.px()/1000.,child.py()/1000.,child.pz()/1000.,child.e()/1000.)
               p4_tquarks_children[p4_tquarks_children.size()-1].push_back(v)
               id_tquarks_children[id_tquarks_children.size()-1].push_back(child.pdgId())
               bc_tquarks_children[bc_tquarks_children.size()-1].push_back(child.barcode())
      ### get W-bosons with parents and children
      if(abs(p.pdgId())==24):
         v = TLorentzVector()
         v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
         p4_wbosons.push_back(v)
         id_wbosons.push_back(p.pdgId())
         st_wbosons.push_back(p.status())
         bc_wbosons.push_back(p.barcode())
         p4_wbosons_parents.push_back(p4_tmp)
         id_wbosons_parents.push_back(id_tmp)
         bc_wbosons_parents.push_back(bc_tmp)
         p4_wbosons_children.push_back(p4_tmp)
         id_wbosons_children.push_back(id_tmp)
         bc_wbosons_children.push_back(bc_tmp)
         if(p.hasProdVtx()):
            prodvtx = p.prodVtx()
            for j in xrange(prodvtx.nIncomingParticles()):
               parent = prodvtx.incomingParticle(j)
               if(not parent): continue
               v.SetPxPyPzE(parent.px()/1000.,parent.py()/1000.,parent.pz()/1000.,parent.e()/1000.)
               p4_wbosons_parents[p4_wbosons_parents.size()-1].push_back(v)
               id_wbosons_parents[id_wbosons_parents.size()-1].push_back(parent.pdgId())
               bc_wbosons_parents[bc_wbosons_parents.size()-1].push_back(parent.barcode())
         if(p.hasDecayVtx()):
            decayvtx = p.decayVtx()
            for j in xrange(decayvtx.nOutgoingParticles()):
               child = decayvtx.outgoingParticle(j)
               if(not child): continue
               v.SetPxPyPzE(child.px()/1000.,child.py()/1000.,child.pz()/1000.,child.e()/1000.)
               p4_wbosons_children[p4_wbosons_children.size()-1].push_back(v)
               id_wbosons_children[id_wbosons_children.size()-1].push_back(child.pdgId())
               bc_wbosons_children[bc_wbosons_children.size()-1].push_back(child.barcode())

   ### "reconstructed" objects
   for i in xrange(t.TruthMuons.size()):
      p = t.TruthMuons.at(i)
      v = TLorentzVector()
      v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
      p4_muons.push_back(v)
      id_muons.push_back(p.pdgId())
      st_muons.push_back(p.status())
      pass # end for loop over truth particles collection
   for i in xrange(t.TruthElectrons.size()):
      p = t.TruthElectrons.at(i)
      v = TLorentzVector()
      v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
      p4_electrons.push_back(v)
      id_electrons.push_back(p.pdgId())
      st_electrons.push_back(p.status())
      pass # end for loop over truth particles collection
   for i in xrange(t.AntiKt4TruthJets.size()):
      p = t.AntiKt4TruthJets.at(i)
      v = TLorentzVector()
      #v.SetPtEtaPhiM(p.pt()/1000.,p.eta(),p.phi(),p.m()/1000.)
      v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
      p4_akt4jets.push_back(v)
      pass # end for loop over truth particles collection
   MET    = t.MET_Truth["NonInt"].met()/1000.
   METphi = t.MET_Truth["NonInt"].phi()
   METx   = MET*math.cos(METphi)
   METy   = MET*math.sin(METphi)
   v.SetPtEtaPhiM(MET,0.,METphi,0.)
   p4_MET.push_back(v)

   ### Event info
   RunNumber[0]   = t.EventInfo.runNumber()
   EventNumber[0] = t.EventInfo.eventNumber()
   MCEventWeight[0] = t.EventInfo.mcEventWeight()

   geneff[0] = 1.
   sigma[0]  = 0.
   if(name=="HT0"):
      geneff[0] = 0.489
      sigma[0]  = 400000  # N=10e6, L=25fb-1
   if(name=="HT1"):
      geneff[0] = 0.0344
      sigma[0]  = 27777.8 # N=5e6, L=180fb-1
   if(name=="HT2"):
      geneff[0] = 0.0114
      sigma[0]  = 6666.7  # N=5e6, L=750fb-1
   if(name=="HT3"):
      geneff[0] = 0.00968
      sigma[0]  = 7272.7  # N=8e6, L=1100fb-1
   if(name=="HT4"):
      geneff[0] = 0.00368
      sigma[0]  = 333.3   # N=1e6, L=3000fb-1

   ###############
   tree.Fill() ###
   ###############

   if(entry%1000==0):
      print("Processing run %i, event %i, entry %i" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber(), entry+1) )
      print("nmuons=%i, nelectrons=%i, njets=%i, MET=%g") % (p4_muons.size(),p4_electrons.size(),p4_akt4jets.size(),p4_MET[0].E())

   pass # end loop over entries
ClearVectors() # cleanup
print "nPassed = ",npassed
tree.GetCurrentFile().Write()
tree.GetCurrentFile().Close()
print "all OK!"
