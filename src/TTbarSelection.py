#!/usr/bin/python

import ROOT
from ROOT import std, gROOT, gStyle, TLorentzVector, TMath
import math
import collections

########################
class Jets:
   'Class for ttbar jets selection'

   def __init__(self,jets):
      # arguments
      self.jets = jets

      # helpers
      self.btagged = {}

      # general
      self.ijets  = []
      self.ibjets = []
      self.inonbjets = []
      self.njets = 0
      self.nbjets = 0

      self.SetGoodJets()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def SetGoodJets(self):
      for i in xrange(self.jets.size()):
         if(abs(self.jets[i].Eta())>2.5): continue
         if(self.jets[i].Pt()<25):        continue
         self.ijets.append(i)
      self.njets = len(self.ijets)

   def TagBjets(self,st_bquarks,p4_bquarks):
      for i in self.ijets:
         for j in xrange(p4_bquarks.size()):
            if(st_bquarks[j]!=23):                         continue
            if(self.jets[i].DeltaR(p4_bquarks[j])>0.4): continue
            self.btagged.update({self.jets[i].Pt() : i})
            break
      # sort b-jets
      self.ibjets = collections.OrderedDict(reversed(sorted(self.btagged.items()))).values()
      self.nbjets = len(self.ibjets)
      # get the non-b-tagged jets
      for j in self.ijets:
         if(j not in self.ibjets): self.inonbjets.append(j)


########################
class Leptons:
   'Class for ttbar lepton selection'
   def __init__(self,leptype,p4_leptons,st_leptons,jetsobj):
      # arguments
      self.leptype = leptype
      self.jetsobj = jetsobj
      self.p4_leptons = p4_leptons
      self.st_leptons = st_leptons

      # general
      self.ileptons  = []
      self.nleptons = 0
    
      self.SetGoodLeptons()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def JetOverlap(self,lepton,dRoverlap=0.4):
      for i in self.jetsobj.ijets:
         if(self.jetsobj.jets[i].DeltaR(lepton)<dRoverlap):
            if(self.leptype=="electron"):
   	           if(abs(self.jetsobj.jets[i].Pt()-lepton.Pt())/lepton.Pt()<0.5): return True
            elif(self.leptype=="muon"):
   		       if(abs(self.jetsobj.jets[i].Pt()-lepton.Pt())/lepton.Pt()<0.7): return True
      return False

   def SetGoodLeptons(self):
      for i in xrange(self.p4_leptons.size()):
         if(abs(self.p4_leptons[i].Eta())>2.5):   continue
         if(self.p4_leptons[i].Pt()<30):          continue
         if(self.st_leptons[i]!=1):               continue
         if(self.JetOverlap(self.p4_leptons[i])): continue
         self.ileptons.append(i)


########################
class HardProcessTops:
   'Class for ttbar electron selection'
   def __init__(self,id_tquarks,p4_tquarks,st_tquarks,id_tquarks_parents,p4_tquarks_parents,
                     id_wbosons,p4_wbosons,st_wbosons,id_wbosons_parents,p4_wbosons_parents,id_wbosons_children,p4_wbosons_children):
      # arguments
      self.id_tquarks = id_tquarks
      self.p4_tquarks = p4_tquarks
      self.st_tquarks = st_tquarks
      self.id_tquarks_parents = id_tquarks_parents
      self.p4_tquarks_parents = p4_tquarks_parents
      self.id_wbosons = id_wbosons
      self.p4_wbosons = p4_wbosons
      self.st_wbosons = st_wbosons
      self.id_wbosons_parents = id_wbosons_parents
      self.p4_wbosons_parents = p4_wbosons_parents
      self.id_wbosons_children = id_wbosons_children
      self.p4_wbosons_children = p4_wbosons_children

      vtmp = TLorentzVector()
      self.p4_leptons = []
      self.id_leptons = []

      self.itops    = []
      self.p4_tops  = []
      self.id_tops  = []
      self.topdecay = []
      self.p4_gluons = []

      self.SetHardProcess()
      self.SetTopsDecay(0)
      self.SetTopsDecay(1)

      if(not self.CheckHardProcess()):
         print "Warning: hard process problem in event"
         quit()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def SetHardProcess(self):
      for j in xrange(self.p4_tquarks.size()):
         if(self.st_tquarks[j]!=22): continue
         if(len(self.id_tops)==2):   break
         self.itops.append(j) ## just for book-keeping
         self.id_tops.append(self.id_tquarks[j]) # tops
         self.p4_tops.append(self.p4_tquarks[j]) # tops
         if(self.id_tquarks_parents[j].size()==2):
            if(len(self.p4_gluons)!=2):
               self.p4_gluons.append( self.p4_tquarks_parents[j][0] ) # gluons
               self.p4_gluons.append( self.p4_tquarks_parents[j][1] ) # gluons
            continue
         else:
            print "Error: too few top children: ",self.id_tquarks_parents[j].size()
            quit()
      # print "Found 2 tops:",self.id_tops

   def SetTopsDecay(self,itop):
      p4_w = TLorentzVector()
      id_w = 0
      # print "top id=%i" % (self.id_tops[itop])
      for j in xrange(self.p4_wbosons.size()):
         # print " w id=%i, st=%i" % (self.id_wbosons[j],self.st_wbosons[j])
         for p in xrange(self.id_wbosons_parents[j].size()):
            if(self.id_wbosons_parents[j][p]!=self.id_tops[itop]): continue
            # print "  (%i) parent id=%i" % (itop,self.id_wbosons_parents[j][p])
            id_w = self.id_wbosons[j]
            p4_w = self.p4_wbosons[j]
            break
            ## found the W whose parent is the top in index itop
            ## now have to find out the bottom-most copy of this W
            ## and decide if it decays to leptons or quarks (check it's children)
         if(id_w): break

      # print "trying to match W id=%i fron nW's=%i" % (id_w,self.p4_wbosons.size())
      for k in xrange(self.p4_wbosons.size()): ## loop again on all W's
         if(self.id_wbosons[k]!=id_w):            continue
         # print " test w id=%i, st=%i and dR=%g" % (self.id_wbosons[k],self.st_wbosons[k],p4_w.DeltaR(self.p4_wbosons[k]))
         # if(p4_w.DeltaR(self.p4_wbosons[k])>0.2): continue ## it is another W (same ID)
         for c in xrange(self.id_wbosons_children[k].size()):  ## check children
            # print "  test w child id=%i" % (self.id_wbosons_children[k][c])
            if(id_w==self.id_wbosons_children[k][c]): continue ## it is a copy
            if(abs(self.id_wbosons_children[k][c])<10):
               self.topdecay.append("had") # it is a hadronic W
               break # will exit the loop at the first hadronic decay product
            else:
               self.topdecay.append("lep") # it is a leptonic W
               break # will exit the loop at the first leptonic decay product

      # print " tops id:   ",self.id_tops
      # print " tops type: ",self.topdecay

   def CheckHardProcess(self):
      if(len(self.id_tops)!=2 or len(self.topdecay)!=2): return False
      return True