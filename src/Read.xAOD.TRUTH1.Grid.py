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

Q = array( 'f', [ 0 ] )
PDGID1 = array( 'i', [ 0 ] )
PDGID2 = array( 'i', [ 0 ] )

p4_me = ROOT.vector(TLorentzVector)()
id_me = ROOT.vector(int)()
st_me = ROOT.vector(int)()
bc_me = ROOT.vector(int)()
MEcode = array( 'i', [ 0 ] )

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


tree.Branch("Q",Q,"Q/I")
tree.Branch("PDGID1",PDGID1,"PDGID1/I")
tree.Branch("PDGID2",PDGID2,"PDGID2/I")

tree.Branch("p4_me",p4_me)
tree.Branch("id_me",id_me)
tree.Branch("st_me",st_me)
tree.Branch("bc_me",bc_me)
tree.Branch("MEcode",MEcode,"MEcode/I")

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



def ClearVectors():
   ### ME participants
   p4_me.clear()
   id_me.clear()
   st_me.clear()
   bc_me.clear()
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

#####################
makegraph = False ###
#####################
if(makegraph):
   fgraphs = open('graphs.py','w')
   fgraphs.write("#!/usr/bin/python\n")
   fgraphs.write("events = [\n")
   fgraphs.close()

ngg = 0
ngq = 0
nqq = 0
ntt = 0
nttg = 0
nttgg = 0
nttqq = 0
nttxx = 0
npassed = 0
print( "Number of input events: %s" % t.GetEntries() )
for entry in xrange(t.GetEntries()):
   t.GetEntry(entry)
   ClearVectors()

   ### for the graph
   evt = "%i" % t.EventInfo.eventNumber()
   entries = {}

   ### for the ME
   meindices = {"tops":[-1,-1], "parents1":[-1,-1], "parents2":[-1,-1], "sisters1":[], "sisters2":[]}

   ### PDF info
   pdfinfo = t.TruthEvents[0].pdfInfo()
   Q[0]      = pdfinfo.Q
   PDGID1[0] = pdfinfo.pdgId1
   PDGID2[0] = pdfinfo.pdgId2


   for i in xrange(t.TruthParticles.size()):
      p = t.TruthParticles.at(i)

      if(makegraph):
         ##### graph
         childrenbc = {}
         parentsbc  = {}
         if(p.hasDecayVtx()):
           decayvtx = p.decayVtx()
           for j in xrange(decayvtx.nOutgoingParticles()):
              child = decayvtx.outgoingParticle(j)
              if(not child): continue
              childrenbc.update({child.barcode():child.pdgId()})
         if(p.hasProdVtx()):
               prodvtx = p.prodVtx()
               for j in xrange(prodvtx.nIncomingParticles()):
                  parent = prodvtx.incomingParticle(j)
                  if(not parent): continue
                  parentsbc.update({parent.barcode():parent.pdgId()})
         if(p.barcode() not in entries.keys()): entries.update({p.barcode():{"evt":evt, "pdgId":p.pdgId(), "status":p.status(), "childrenbc":childrenbc, "parentsbc":parentsbc}})
         #############

      ### for ME
      if(abs(p.pdgId())==6 and (p.status()==22 or p.status()==23) and (meindices["tops"][0]<0 or meindices["tops"][1]<0)):
         if(p.hasProdVtx()):
            prodvtx = p.prodVtx()
            if(prodvtx.nIncomingParticles()==2):
               iTop = -1
               sTop = ""
               if(meindices["tops"][0]<0): iTop = 0
               else:                       iTop = 1
               sTop = str(iTop+1)
               meindices["tops"][iTop] = p.index()
               parent1 = prodvtx.incomingParticle(0)
               parent2 = prodvtx.incomingParticle(1)
               if(parent1):
                  meindices["parents"+sTop][0] = parent1.index()
                  if(parent1.hasDecayVtx()):
                    decayvtx = parent1.decayVtx()
                    for j in xrange(decayvtx.nOutgoingParticles()):
                       child = decayvtx.outgoingParticle(j)
                       if(not child):             continue
                       if(abs(child.pdgId())==6): continue
                       if(child.index() not in meindices["sisters"+sTop]): meindices["sisters"+sTop].append(child.index())
               if(parent2):
                  meindices["parents"+sTop][1] = parent2.index()
                  if(parent2.hasDecayVtx()):
                    decayvtx = parent2.decayVtx()
                    for j in xrange(decayvtx.nOutgoingParticles()):
                       child = decayvtx.outgoingParticle(j)
                       if(not child):             continue
                       if(abs(child.pdgId())==6): continue
                       if(child.index() not in meindices["sisters"+sTop]): meindices["sisters"+sTop].append(child.index())
            else:
               print "Top parents number is not 2: ", prodvtx.nIncomingParticles()
               quit()
            if(meindices["parents"+sTop][0]<0 or meindices["parents"+sTop][1]<0):
               print "Parent indices are invalid: (%i, %i)" % (meindices["parents"+sTop][0], meindices["parents"+sTop][1])
               quit()

      
      # if(i<20):
      #    print "[%i] id=%i, st=%i, bc=%i" % (i,p.pdgId(),p.status(),p.barcode())
      #    if(p.hasProdVtx()):
      #       prodvtx = p.prodVtx()
      #       for j in xrange(prodvtx.nIncomingParticles()):
      #          parent = prodvtx.incomingParticle(j)
      #          if(not parent): continue
      #          print "  parent id=%i, bc=%i" % (parent.pdgId(),parent.barcode())
      #    if(p.hasDecayVtx()):
      #       decayvtx = p.decayVtx()
      #       for j in xrange(decayvtx.nOutgoingParticles()):
      #          child = decayvtx.outgoingParticle(j)
      #          if(not child): continue
      #          print "    child id=%i, bc=%i" % (child.pdgId(),child.barcode())

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

   if(makegraph):
      fgraphs = open('graphs.py','a')
      fgraphs.write(str(entries)+",\n")
      fgraphs.close()


   ### ME stuff
   t1 = meindices["tops"][0]
   t2 = meindices["tops"][1]
   p1a = meindices["parents1"][0]
   p1b = meindices["parents1"][1]
   p2a = meindices["parents2"][0]
   p2b = meindices["parents2"][1]
   s1a = -1
   if(len(meindices["sisters1"])>0): s1a = meindices["sisters1"][0]
   s1b = -1
   if(len(meindices["sisters1"])>1): s1b = meindices["sisters1"][1]
   s2a = -1
   if(len(meindices["sisters2"])>0): s2a = meindices["sisters2"][0]
   s2b = -1
   if(len(meindices["sisters2"])>1): s2b = meindices["sisters2"][1]
   # print "\nEvent "+evt+" ->", meindices
   if(t1>=0 and t2>=0 and p1a>=0 and p1b>=0 and p2a>=0 and p2b>=0):
      # print "top1: id=%i, st=%i, bc=%i -> par1id=%i, par2id=%i" % (t.TruthParticles[t1].pdgId(), t.TruthParticles[t1].status(), t.TruthParticles[t1].barcode(), t.TruthParticles[p1a].pdgId(), t.TruthParticles[p1b].pdgId())
      # for i in meindices["sisters1"]:
      #    print "sister1 index=%i: id=%i, status=%i" % (i, t.TruthParticles[i].pdgId(),t.TruthParticles[i].status())
      # print "top2: id=%i, st=%i, bc=%i -> par1id=%i, par2id=%i" % (t.TruthParticles.at(t2).pdgId(), t.TruthParticles.at(t2).status(), t.TruthParticles.at(t2).barcode(), t.TruthParticles[p2a].pdgId(), t.TruthParticles.at(p2b).pdgId())
      # for i in meindices["sisters2"]:
      #    print "sister2 index=%i: id=%i, status=%i" % (i, t.TruthParticles[i].pdgId(),t.TruthParticles[i].status())

      isGG = True
      ### check that the top parents are gluons
      if(t.TruthParticles[p1a].pdgId()!=21 or t.TruthParticles[p1b].pdgId()!=21):
         # print "Not a gg production: idmother1=%i, idmother2=%i" % (t.TruthParticles[p1a].pdgId(),t.TruthParticles[p1b].pdgId())
         if(abs(t.TruthParticles[p1a].pdgId())<6   and t.TruthParticles[p1b].pdgId()==21):
            ngq += 1
            MEcode[0] = -1
         elif(abs(t.TruthParticles[p1b].pdgId())<6 and t.TruthParticles[p1a].pdgId()==21):
            ngq += 1
            MEcode[0] = -1
         else:
            nqq += 1
            MEcode[0] = -2
         isGG = False
      else:
         ngg += 1

      ### check that the tops parents are the same
      if(isGG and ((p2a!=p1a and p2a!=p1b) or (p2b!=p1a and p2b!=p1b))):
         print "ERROR: tops parents (gluons) are not the same (p1a=%i, p1b=%i, p2a=%i, p2b=%i)" % (p1a,p1b,p2a,p2b)
         isGG = False
      ### check that the tops sisters are the same
      if(isGG and ((s2a!=s1a and s2a!=s1b) or (s2b!=s1a and s2b!=s1b))):
         print "ERROR: tops sisters are not the same (s1a=%i, s1b=%i, s2a=%i, s2b=%i)" % (s1a,s1b,s2a,s2b)
         isGG = False

      ### fill the ME vectors anyhow (regardless of the production state)
      finalMEindices = [p1a,p1b,t1,t2]
      if(s1a>=0): finalMEindices.append(s1a)
      if(s1b>=0): finalMEindices.append(s1b)
      for k in finalMEindices:
         p = t.TruthParticles[k]
         v = TLorentzVector()
         v.SetPxPyPzE(p.px()/1000.,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
         p4_me.push_back(v)
         id_me.push_back(p.pdgId())
         st_me.push_back(p.status())
         bc_me.push_back(p.barcode())

      if(isGG):
         if(s1a<0  and s1b<0):
            MEcode[0] = 0 ### no extra partons
            ntt += 1
         elif(s1a>=0 and s1b<0):
            MEcode[0] = 1 ### one extra gluon
            nttg += 1
         else:
            id1 = t.TruthParticles[s1a].pdgId()
            id2 = t.TruthParticles[s1b].pdgId()
            if(id1==21 and id2==21):
               MEcode[0] = 2 ### extra gg
               nttgg += 1
            else:
               if(abs(id1)==abs(id2)): nttqq += 1
               else:                   nttxx += 1
               if  (abs(id1)==2 and abs(id2)==2): MEcode[0] = 3 ### extra uu
               elif(abs(id1)==1 and abs(id2)==1): MEcode[0] = 4 ### extra dd
               elif(abs(id1)==3 and abs(id2)==3): MEcode[0] = 5 ### extra ss
               elif(abs(id1)==4 and abs(id2)==4): MEcode[0] = 6 ### extra cc
               elif(abs(id1)==5 and abs(id2)==5): MEcode[0] = 7 ### extra bb
               else: 
                  print "ERROR: unknown parton final state (id1=%i id2=%i)" % (id1,id2)  
   else:
      print "ERROR: cannot find ME (t1=%i t2=%i p1a=%i p1b=%i p2a=%i p2b=%i)" % (t1,t2,p1a,p1b,p2a,p2b)

   q = 0
   for j in xrange(p4_me.size()):
      if(j<2): continue
      q += math.sqrt(p4_me[j].M()*p4_me[j].M() + p4_me[j].Pt()*p4_me[j].Pt())
   q = q/2.
   if(abs(pdfinfo.Q-q)/pdfinfo.Q>0.05):
      print ">0.05 relative difference: Q=%g, q=%g" % (pdfinfo.Q, q)

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
   if(name=="HT0"):
      geneff[0] = 0.489
   if(name=="HT1"):
      geneff[0] = 0.0344
   if(name=="HT2"):
      geneff[0] = 0.0114
   if(name=="HT3"):
      geneff[0] = 0.00968
   if(name=="HT4"):
      geneff[0] = 0.00368

   ###############
   tree.Fill() ###
   ###############

   if(entry%1000==0):
      print("Processing run %i, event %i, entry %i" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber(), entry+1) )
      print("nmuons=%i, nelectrons=%i, njets=%i, MET=%g") % (p4_muons.size(),p4_electrons.size(),p4_akt4jets.size(),p4_MET[0].E())
      print("ngg=%i, ngq=%i, nqq=%i") % (ngg,ngq,nqq)
      print("ntt=%i, nttg=%i, nttgg=%i, nttqq=%i, nttxx=%i") % (ntt,nttg,nttgg,nttqq,nttxx)

   pass # end loop over entries

if(makegraph):
   fgraphs = open('graphs.py','a')
   fgraphs.write("]\n")
   fgraphs.close()

ClearVectors() # cleanup
print "nPassed = ",npassed
tree.GetCurrentFile().Write()
tree.GetCurrentFile().Close()
print "all OK!"
