#!/usr/bin/env python

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
ROOT.gROOT.Macro( '$ROOTCOREDIR/scripts/load_packages.C' )
if(not ROOT.xAOD.Init().isSuccess()): print "Failed xAOD.Init()" # Initialize the xAOD infrastructure

from ROOT import std, gROOT, TFile, TTree, TLorentzVector
tfile = "tops.SM.root" 
tfile = TFile(tfile,"RECREATE")
tree = TTree("SM","SM")
pdgid = std.vector(int)()
p4    = ROOT.vector(TLorentzVector)()
RunNumber = array( 'i', [ 0 ] )
EventNumber = array( 'i', [ 0 ] )
tree.Branch("id",pdgid) 
tree.Branch("p4",p4)
tree.Branch("RunNumber",RunNumber,"RunNumber/I")
tree.Branch("EventNumber",EventNumber,"EventNumber/I")


# Set up the input files:
xaodpath = "$HOME/data/MC/ttbar/ntup/"
fullpath = ROOT.gSystem.ExpandPathName(xaodpath)
fileName = fullpath+"/DAOD_TRUTH1.NTUP."+name+"."+jobid+".root"
treeName = "CollectionTree" # default when making transient tree anyway
f = ROOT.TFile.Open(fileName)
t = ROOT.xAOD.MakeTransientTree(f, treeName) # Make the "transient tree"


def GetRecord(p):
   print "["+str(i)+"]  id="+str(p.pdgId())+"  status="+str(p.status())+"  pxpypze=("+str(p.px())+","+str(p.py())+","+str(p.pz())+","+str(p.e())+")"
   if(p.hasProdVtx()):
      prodvtx = p.prodVtx()
      nIncoming = prodvtx.nIncomingParticles()
      if(nIncoming>0): print "   parents:"
      for j in xrange(0,nIncoming):
         parent = prodvtx.incomingParticle(j)
         if(not parent): continue
         print "      ["+str(parent.index())+"]  id="+str(parent.pdgId())+"  status="+str(parent.status())+"  pxpypze=("+str(parent.px())+","+str(parent.py())+","+str(parent.pz())+","+str(parent.e())+")"
   if(p.hasDecayVtx()):
      decayvtx = p.decayVtx()
      nOutgoing = decayvtx.nOutgoingParticles()
      if(nOutgoing>0): print "   children:"
      for j in xrange(0,nOutgoing):
         child = decayvtx.outgoingParticle(j)
         if(not child): continue
         print "      ["+str(child.index())+"]  id="+str(child.pdgId())+"  status="+str(child.status())+"  pxpypze=("+str(child.px())+","+str(child.py())+","+str(child.pz())+","+str(child.e())+")"

def ClearParticles():
   pdgid.clear()
   p4.clear()

def AddParticle(p,indices):
   v = TLorentzVector()
   v.SetPxPyPzE(p.px()/1000,p.py()/1000.,p.pz()/1000.,p.e()/1000.)
   pdgid.push_back(p.pdgId())
   p4.push_back(v)
   indices.append(p.index())
   #print "added pdgId="+str(p.pdgId())+" of index="+str(p.index())

def AddWithParents(p,indices):
   if(p.hasProdVtx()):
      prodvtx = p.prodVtx()
      nIncoming = prodvtx.nIncomingParticles()
      for j in xrange(0,nIncoming):
         parent = prodvtx.incomingParticle(j)
         if(not parent):                continue
         if(parent.index() in indices): continue
         AddParticle(parent,indices)
      AddParticle(p,indices)

print( "Number of input events: %s" % t.GetEntries() )
nPairs = 0
for entry in xrange( 0,t.GetEntries()):
   t.GetEntry( entry )
   nplus  = 0 
   nminus = 0
   npairs = 0
   ClearParticles()
   indices = []
   # loop over truth particles collection
   for i in xrange(t.TruthParticles.size()):
      p = t.TruthParticles.at(i)
      if(p.pdgId()==+6):
         nplus+=1
         AddWithParents(p,indices)
      if(p.pdgId()==-6):
         nminus+=1
         AddWithParents(p,indices)
      if(abs(p.pdgId())==6 or abs(p.pdgId())==5): GetRecord(p)
      #if(nplus==1 and nminus==1): break
      pass # end for loop over truth particles collection
   atLeast1pair = False
   if(nplus>=1 and nminus>=1): atLeast1pair = True
   if(atLeast1pair): nPairs+=1
   print ""
   if(entry%1000==0): print( "Processing run #%i, event #%i  :  found pairs %i out of %i processed" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber() ,nPairs, entry+1) )
   RunNumber[0] = t.EventInfo.runNumber()
   EventNumber[0] = t.EventInfo.eventNumber()
   tree.Fill()
   pass # end loop over entries
print "Found "+str(nPairs)+" ttbar pairs"
tree.GetCurrentFile().Write() 
tree.GetCurrentFile().Close()
print "all OK!"
