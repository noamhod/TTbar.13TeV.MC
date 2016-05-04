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
            # if(st_bquarks[j]!=23):                    continue
            if(st_bquarks[j]<60):                       continue
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
   def __init__(self,leptype,p4_leptons,st_leptons,p4_jets,ijets):
      # arguments
      self.leptype = leptype
      self.p4_leptons = p4_leptons
      self.st_leptons = st_leptons
      self.p4_jets = p4_jets
      self.ijets   = ijets

      # general
      self.ileptons  = []
      self.nleptons = 0
    
      self.SetGoodLeptons()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def JetOverlap(self,lepton):
      for i in self.ijets:
         if(self.leptype=="electron"):
            if(self.p4_jets[i].DeltaR(lepton)<0.2): return True
         elif(self.leptype=="muon"):
            if(self.p4_jets[i].DeltaR(lepton)<(0.04 + 10/lepton.Pt())): return True
            # if(self.p4_jets[i].DeltaR(lepton)<0.2): return True
         else:
            print "unsupported lepton: "+self.leptype+" -> quitting!"
            quit()
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
   def __init__(self,id_tquarks,p4_tquarks,st_tquarks,bc_tquarks,
                     id_tquarks_parents,p4_tquarks_parents,bc_tquarks_parents,
                     id_tquarks_children,p4_tquarks_children,bc_tquarks_children,
                     id_wbosons,p4_wbosons,st_wbosons,bc_wbosons,
                     id_wbosons_parents,p4_wbosons_parents,bc_wbosons_parents,
                     id_wbosons_children,p4_wbosons_children,bc_wbosons_children,
                     id_bquarks,p4_bquarks,st_bquarks,bc_bquarks,
                     id_bquarks_parents,p4_bquarks_parents,bc_bquarks_parents,
                     id_bquarks_children,p4_bquarks_children,bc_bquarks_children):
      # arguments
      self.id_tquarks = id_tquarks
      self.p4_tquarks = p4_tquarks
      self.st_tquarks = st_tquarks
      self.bc_tquarks = bc_tquarks
      self.id_tquarks_children = id_tquarks_children
      self.p4_tquarks_children = p4_tquarks_children
      self.bc_tquarks_children = bc_tquarks_children
      self.id_tquarks_parents = id_tquarks_parents
      self.p4_tquarks_parents = p4_tquarks_parents
      self.bc_tquarks_parents = bc_tquarks_parents
      self.id_wbosons = id_wbosons
      self.p4_wbosons = p4_wbosons
      self.st_wbosons = st_wbosons
      self.bc_wbosons = bc_wbosons
      self.id_wbosons_parents = id_wbosons_parents
      self.p4_wbosons_parents = p4_wbosons_parents
      self.bc_wbosons_parents = bc_wbosons_parents
      self.id_wbosons_children = id_wbosons_children
      self.p4_wbosons_children = p4_wbosons_children
      self.bc_wbosons_children = bc_wbosons_children
      self.id_bquarks = id_bquarks
      self.p4_bquarks = p4_bquarks
      self.st_bquarks = st_bquarks
      self.bc_bquarks = bc_bquarks
      self.id_bquarks_children = id_bquarks_children
      self.p4_bquarks_children = p4_bquarks_children
      self.bc_bquarks_children = bc_bquarks_children
      self.id_bquarks_parents = id_bquarks_parents
      self.p4_bquarks_parents = p4_bquarks_parents
      self.bc_bquarks_parents = bc_bquarks_parents

      self.mW = 80.385
      self.mt = 172.5

      vtmp = TLorentzVector()
      self.p4_products = {}
      self.id_products = {}
      self.p4_gluons   = {}
      self.b     = TLorentzVector()
      self.nu    = TLorentzVector()
      self.l     = TLorentzVector()
      self.qW    = TLorentzVector()
      self.qbarW = TLorentzVector()
      self.qB    = TLorentzVector()

      self.idb     = 0
      self.idnu    = 0
      self.idl     = 0
      self.idqW    = 0
      self.idqbarW = 0
      self.idqB    = 0

      self.itops    = []
      self.p4_tops  = []
      self.id_tops  = []
      self.topdecay = []

      self.barcode2index_t = {}
      self.barcode2index_w = {}
      self.barcode2index_b = {}
      self.diagrams = {}
      self.InitDiagrams()

      self.SetHardProcess()
      self.SetTopsDecay(0)
      self.SetTopsDecay(1)
      self.SetPartons(0)
      self.SetPartons(1)

      if(not self.CheckHardProcess()):
         print "Warning: hard process problem in event"
         quit()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def PrintHardProcess(self):
      print "--- t-quarks:"
      for j in xrange(self.p4_tquarks.size()):
         print " t[%i] id=%i, st=%i, bc=%g" % (j, self.id_tquarks[j], self.st_tquarks[j], self.bc_tquarks[j])
         for p in xrange(self.id_tquarks_parents[j].size()):
            print "   t.p[%i] id=%i, bc=%i" % (p, self.id_tquarks_parents[j][p], self.bc_tquarks_parents[j][p])
         for c in xrange(self.id_tquarks_children[j].size()):
            print "   t.c[%i] id=%i, bc=%i" % (c, self.id_tquarks_children[j][c], self.bc_tquarks_children[j][c])
      print "--- W-bosons:"
      for j in xrange(self.p4_wbosons.size()):
         print " w[%i] id=%i, st=%i, bc=%g" % (j, self.id_wbosons[j], self.st_wbosons[j], self.bc_wbosons[j])
         for p in xrange(self.id_wbosons_parents[j].size()):
            print "   w.p[%i] id=%i, bc=%i" % (p, self.id_wbosons_parents[j][p], self.bc_wbosons_parents[j][p])
         for c in xrange(self.id_wbosons_children[j].size()):
            print "   w.c[%i] id=%i, bc=%i" % (c, self.id_wbosons_children[j][c], self.bc_wbosons_children[j][c])
      print "--- b-quarks:"
      for j in xrange(self.p4_bquarks.size()):
         print " b[%i] id=%i, st=%i, bc=%g" % (j, self.id_bquarks[j], self.st_bquarks[j], self.bc_bquarks[j])
         for p in xrange(self.id_bquarks_parents[j].size()):
            print "   b.p[%i] id=%i, bc=%i" % (p, self.id_bquarks_parents[j][p], self.bc_bquarks_parents[j][p])
         for c in xrange(self.id_bquarks_children[j].size()):
            print "   b.c[%i] id=%i, bc=%i" % (c, self.id_bquarks_children[j][c], self.bc_bquarks_children[j][c])


   def InitDiagrams(self):
      for j in xrange(self.p4_tquarks.size()):
         self.barcode2index_t.update({self.bc_tquarks[j]:j})
      for j in xrange(self.p4_wbosons.size()):
         self.barcode2index_w.update({self.bc_wbosons[j]:j})
      for j in xrange(self.p4_bquarks.size()):
         self.barcode2index_b.update({self.bc_bquarks[j]:j})
   
      for j in xrange(self.p4_tquarks.size()):
         if(self.st_tquarks[j]==22 and len(self.diagrams)<2):
            topname = ""
            if(self.id_tquarks[j]>0): topname = "t"
            else:                     topname = "tbar"
            diagram = {"t-production":-1, "t-radiation":-1, "t-decay":-1, "W-production":-1, "W-decay":-1, "b-production":-1, "b-radiation":-1, "b-decay":-1}
            self.diagrams.update({topname:diagram})
            self.SetDiagram(j,topname)

   def SetDiagram(self,index,topname):
      self.diagrams[topname]["t-production"] = index
      barcode = self.bc_tquarks[index]
      while(self.id_tquarks_children[index].size()==1 or (self.id_tquarks_children[index].size()==2 and (abs(self.id_tquarks_children[index][0])==6 or abs(self.id_tquarks_children[index][0])==21))):
         barcode = self.bc_tquarks_children[index][0]
         if(self.id_tquarks_children[index].size()==2):
            self.diagrams[topname]["t-radiation"] = index
            if(abs(self.id_tquarks_children[index][0])==6):   barcode = self.bc_tquarks_children[index][0]
            elif(abs(self.id_tquarks_children[index][1])==6): barcode = self.bc_tquarks_children[index][1]
            else:
               print "problem in t-decay, quiting"
               quit()
         index = self.barcode2index_t[barcode]
      self.diagrams[topname]["t-decay"] = index

      if(abs(self.id_tquarks_children[index][0])==24 and abs(self.id_tquarks_children[index][1])==5):
         w_prod_barcode = self.bc_tquarks_children[index][0]
         b_prod_barcode = self.bc_tquarks_children[index][1]
      elif(abs(self.id_tquarks_children[index][1])==24 and abs(self.id_tquarks_children[index][0])==5):
         w_prod_barcode = self.bc_tquarks_children[index][1]
         b_prod_barcode = self.bc_tquarks_children[index][0]
      else:
         print "problem in W/b-production, quiting"
         quit()
      self.diagrams[topname]["W-production"] = self.barcode2index_w[w_prod_barcode]
      self.diagrams[topname]["b-production"] = self.barcode2index_b[b_prod_barcode]


      index = self.barcode2index_w[w_prod_barcode]
      while(self.id_wbosons_children[index].size()==1):
         barcode = self.bc_wbosons_children[index][0]
         index = self.barcode2index_w[barcode]
      self.diagrams[topname]["W-decay"] = index
  
      index = self.barcode2index_b[b_prod_barcode]
      while((self.id_bquarks_children[index].size()==1 and abs(self.id_bquarks_children[index][0])==5) or (self.id_bquarks_children[index].size()==2 and (abs(self.id_bquarks_children[index][0])==5 or abs(self.id_bquarks_children[index][0])==21))):
         barcode = self.bc_bquarks_children[index][0]
         if(self.id_bquarks_children[index].size()==2):
            self.diagrams[topname]["b-radiation"] = index
            if(abs(self.id_bquarks_children[index][0])==5):   barcode = self.bc_bquarks_children[index][0]
            elif(abs(self.id_bquarks_children[index][1])==5): barcode = self.bc_bquarks_children[index][1]
            else: 
               print "problem in b-decay, quiting"
               quit()
         index = self.barcode2index_b[barcode]
      self.diagrams[topname]["b-decay"] = index


   def SetHardProcess(self):
      for j in xrange(self.p4_tquarks.size()):
         if(self.st_tquarks[j]!=22): continue
         if(len(self.id_tops)==2):   break
         self.itops.append(j) ## book-keeping
         self.id_tops.append(self.id_tquarks[j]) # tops
         self.p4_tops.append(self.p4_tquarks[j]) # tops
         if(self.id_tquarks_parents[j].size()==2):
            tmp = []
            t = len(self.p4_gluons)
            self.p4_gluons.update({t:tmp})
            self.p4_gluons[t].append( self.p4_tquarks_parents[j][0] ) # gluons
            self.p4_gluons[t].append( self.p4_tquarks_parents[j][1] ) # gluons
         else:
            print "Error: too few top children: ",self.id_tquarks_parents[j].size()
            quit()

      for t in xrange(len(self.itops)):
         itop = self.itops[t]
         for j in xrange(self.p4_tquarks.size()):
            if(self.st_tquarks[j]==22):                    continue # not a decaying top
            if(self.id_tquarks[j]!=self.id_tquarks[itop]): continue # not the same top
            if(self.id_tquarks_children[j].size()!=2):     continue # doesn't have 2 children
            p4_tmp = []
            id_tmp = []
            self.p4_products.update({t:p4_tmp})
            self.id_products.update({t:id_tmp})
            self.p4_products[t].append( self.p4_tquarks_children[j][0] ) # b's and W's
            self.id_products[t].append( self.id_tquarks_children[j][0] ) # b's and W's
            self.p4_products[t].append( self.p4_tquarks_children[j][1] ) # b's and W's
            self.id_products[t].append( self.id_tquarks_children[j][1] ) # b's and W's
         # print "products: ",self.id_products[t]

   def SetTopsDecay(self,itop):
      p4_w = TLorentzVector()
      id_w = 0
      for j in xrange(self.p4_wbosons.size()):
         for p in xrange(self.id_wbosons_parents[j].size()):
            if(self.id_wbosons_parents[j][p]!=self.id_tops[itop]): continue
            id_w = self.id_wbosons[j]
            p4_w = self.p4_wbosons[j]
            break
            ## found the W whose parent is the top in index itop
            ## now have to find out the bottom-most copy of this W
            ## and decide if it decays to leptons or quarks (check it's children)
         if(id_w): break

      wasappended = False
      for k in xrange(self.p4_wbosons.size()): ## loop again on all W's
         if(self.id_wbosons[k]!=id_w): continue
         for c in xrange(self.id_wbosons_children[k].size()):  ## check children
            if(id_w==self.id_wbosons_children[k][c]): continue ## it is a copy
            self.p4_products[itop].append( self.p4_wbosons_children[k][c] ) # leptons and quarks
            self.id_products[itop].append( self.id_wbosons_children[k][c] ) # leptons and quarks
            if(abs(self.id_wbosons_children[k][c])<10   and not wasappended):
               self.topdecay.append("had") # it is a hadronic W
               wasappended = True
            elif(abs(self.id_wbosons_children[k][c])>10 and not wasappended):
               self.topdecay.append("lep") # it is a leptonic W
               wasappended = True
      # print "products for id="+str(self.id_tops[itop])+"["+str(itop)+"]: ",self.id_products[itop]

   def SetPartons(self,itop):
      for i in xrange(len(self.id_products[itop])):
         pdgid = self.id_products[itop][i]
         if(self.topdecay[itop]=="lep"):
            if(abs(pdgid)==5):                                       
               self.b   = self.p4_products[itop][i]
               self.idb = pdgid
               # print "id b=",self.id_products[itop][i]
            if(abs(pdgid)>10 and abs(pdgid)<20 and abs(pdgid)%2!=0):
               self.l   = self.p4_products[itop][i]
               self.idl = pdgid
               # print "id l=",self.id_products[itop][i]
            if(abs(pdgid)>10 and abs(pdgid)<20 and abs(pdgid)%2==0):
               self.nu   = self.p4_products[itop][i]
               self.idnu = pdgid
               # print "id nu=",self.id_products[itop][i]
         if(self.topdecay[itop]=="had"):
            if(abs(pdgid)==5):
               self.qB   = self.p4_products[itop][i]
               self.idqB = pdgid
               # print "id qB=",self.id_products[itop][i]
            if(abs(pdgid)<5 and pdgid>0):
               self.qW   = self.p4_products[itop][i]
               self.idqW = pdgid
               # print "id qW=",self.id_products[itop][i]
            if(abs(pdgid)<5 and pdgid<0):
               self.qbarW   = self.p4_products[itop][i]
               self.idqbarW = pdgid
               # print "id qbarW=",self.id_products[itop][i]
      # print "products for id="+str(self.id_tops[itop])+"["+str(itop)+"], "+self.topdecay[itop]+" -> ",self.id_products[itop]

   def CheckHardProcess(self):
      if(len(self.id_tops)!=2 or len(self.topdecay)!=2):
         print "len(self.id_tops)=%i, len(self.topdecay)=%i" % (len(self.id_tops), len(self.topdecay))
         return False
      return True