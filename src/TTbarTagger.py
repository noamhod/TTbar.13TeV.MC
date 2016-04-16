#!/usr/bin/python

import ROOT
from ROOT import std, gROOT, gStyle, TLorentzVector, TMath, TRandom3
import math


class TTbarTagger:
   'Class for ttbar reconstruction'

   def __init__(self,jets,ijets,ibjets,lepton,etmis,EventNumber,mode=1):
      # arguments
      self.mode   = mode # 0: all-hadronic, 1: one-lepton, 2: dilepton
      self.p4_lepton = lepton
      self.p4_etmis  = etmis
      self.jets   = jets
      self.ijets  = ijets
      self.ibjets = ibjets

      # general
      self.mW    = 80.385
      self.wW    = 2.085
      self.ibjet = -1
      self.bjet  = TLorentzVector()
      self.njets = len(ijets)
      self.nbjets = len(ibjets)
      
      # leptonic top
      self.mTw = -1
      self.mTt = -1
      self.p4_WT = TLorentzVector()
      self.p4_tT = TLorentzVector()
      self.p4_Wl1 = TLorentzVector()
      self.p4_Wl2 = TLorentzVector()
      self.p4_Wl  = TLorentzVector()
      self.p4_tl1 = TLorentzVector()
      self.p4_tl2 = TLorentzVector()
      self.p4_tl  = TLorentzVector()
      self.p4_nu1 = TLorentzVector()
      self.p4_nu2 = TLorentzVector()
      self.p4_nu  = TLorentzVector()
      
      # hadronic top1
      self.mw = -1
      self.mt = -1
      self.p4_W = TLorentzVector()
      self.p4_t = TLorentzVector()

      self.rand = TRandom3(EventNumber)

      #######################################
      if(not self.MinimumInput()): return ###
      #######################################

      # order matters below
      self.SetBjet()
      self.SetTopLep()
      self.SetTopHad()
      self.SetTTbar()

   def __del__(self):
      class_name = self.__class__.__name__
      # print class_name, "destroyed"

   def MinimumInput(self):
      if(self.njets<4):  return False
      if(self.nbjets<1): return False
      return True

   def SetBjet(self):
      if(len(self.ibjets)>0): self.ibjet = self.ibjets[0]
      if(len(self.ibjets)>1):
         # associate the semi-leptonic with the b which is closest (dR) to the lepton
         dr1 = self.p4_lepton.DeltaR(self.jets[self.ibjets[0]])
         dr2 = self.p4_lepton.DeltaR(self.jets[self.ibjets[1]])
         if(dr1>dr2):
            self.ibjet = self.ibjets[1]
      self.bjet = self.jets[self.ibjet]

   def SetPzNu(self,wMass):
      mL = self.p4_lepton.M()
      dphi = self.p4_lepton.Phi() - self.p4_etmis.Phi()
      A = (wMass*wMass-mL*mL)/2 + self.p4_etmis.Pt()*self.p4_lepton.Pt()*math.cos(dphi)
      a = math.pow(self.p4_lepton.Pz(),2) - math.pow(self.p4_lepton.E(),2)
      b = 2.*A*self.p4_lepton.Pz()
      c = A*A - math.pow(self.p4_etmis.Pt(),2)*math.pow(self.p4_lepton.E(),2)
      d = b*b-4.*a*c
      nuz1 = 0
      nuz2 = 0
      if(d>0.):
         nuz1 = (-b + math.sqrt(d))/(2.*a)
         nuz2 = (-b - math.sqrt(d))/(2.*a)
      # print "nuz1=",nuz1
      # print "nuz2=",nuz2
      Enu1 = math.sqrt( math.pow(self.p4_etmis.Pt(),2) + math.pow(nuz1,2) )
      Enu2 = math.sqrt( math.pow(self.p4_etmis.Pt(),2) + math.pow(nuz2,2) )
      nu1 = TLorentzVector()
      nu2 = TLorentzVector()
      nu1.SetPxPyPzE(self.p4_etmis.Px(),self.p4_etmis.Py(),nuz1,Enu1)
      nu2.SetPxPyPzE(self.p4_etmis.Px(),self.p4_etmis.Py(),nuz2,Enu2)
      self.p4_nu1 = nu1
      self.p4_nu2 = nu2
      self.p4_Wl1 = self.p4_lepton + self.p4_nu1
      self.p4_Wl2 = self.p4_lepton + self.p4_nu2
      self.p4_tl1 = self.p4_Wl1 + self.bjet
      self.p4_tl2 = self.p4_Wl2 + self.bjet
      if(abs(self.p4_Wl1.M()-self.mW) < abs(self.p4_Wl2.M()-self.mW)): self.p4_nu = nu1
      else:                                                            self.p4_nu = nu2
      self.p4_Wl = self.p4_lepton + self.p4_nu
      self.p4_tl = self.p4_Wl + self.bjet
      if(nuz1==0 and nuz2==0): return False
      return True

   def SetTopLep(self):
      metT = self.p4_etmis.Pt()
      lepT = self.p4_lepton.Pt()
      bT   = self.bjet.Pt()
      ##########################################
      isOK = self.SetPzNu(self.mW)
      if(not isOK):
         nsteps = 1000
         for i in xrange(1,nsteps+1):
            mW = self.rand.BreitWigner(self.mW,self.wW)
            # print "i=%i, mW=%g" % (i,mW)
            if(self.SetPzNu(mW)):
               isOK = True
               break
      if(not isOK): self.SetPzNu(self.mW)
      ##########################################
      self.p4_WT = self.p4_lepton + self.p4_etmis
      self.mTw = math.sqrt((metT+lepT)*(metT+lepT) - (self.p4_WT.Px()*self.p4_WT.Px()) - (self.p4_WT.Py()*self.p4_WT.Py()))
      self.p4_tT = self.p4_WT + self.bjet
      self.mTt = math.sqrt((metT+lepT+bT)*(metT+lepT+bT) - (self.p4_tT.Px()*self.p4_tT.Px()) - (self.p4_tT.Py()*self.p4_tT.Py()))

   def SetTopHad(self):
      # associate those jets with maximum pt of the vectorial sum to the hadronic decay chain
      maxPt = -1
      maxPtIndices = [-1,-1,-1]
      for i in xrange(self.njets):
         if(self.ijets[i]==self.ibjet): continue
         for j in xrange(self.njets):
           if(j<=i):            continue
           if(self.ijets[j]==self.ibjet): continue
           for k in xrange(self.njets):
              if(k==i or k==j):    continue
              if(self.ijets[k]==self.ibjet): continue
              sum = self.jets[self.ijets[i]]+self.jets[self.ijets[j]]+self.jets[self.ijets[k]]
              if(maxPt<0 or maxPt<sum.Pt()):
                 maxPt=sum.Pt()
                 maxPtIndices[0] = self.ijets[i]
                 maxPtIndices[1] = self.ijets[j]
                 maxPtIndices[2] = self.ijets[k]
      self.p4_t = self.jets[maxPtIndices[0]]+self.jets[maxPtIndices[1]]+self.jets[maxPtIndices[2]]
      self.mt = self.p4_t.M()

      # associate those jets that get closest to the W mass with their invariant mass to the W boson
      nmaxPtIndices = len(maxPtIndices)
      wDist = -1
      wMassIndices = [-1,-1]
      for i in xrange(nmaxPtIndices):
         for j in xrange(nmaxPtIndices):
            if(j==i or maxPtIndices[i]>maxPtIndices[j]): continue
            sum = self.jets[maxPtIndices[i]]+self.jets[maxPtIndices[j]]
            if(wDist<0. or wDist>abs(sum.M()-self.mW) ):
              wDist = abs(sum.M()-self.mW)
              wMassIndices[0] = maxPtIndices[i]
              wMassIndices[1] = maxPtIndices[j]
      self.p4_w = self.jets[wMassIndices[0]]+self.jets[wMassIndices[1]]
      self.mw = self.p4_w.M()

   def SetTTbar(self):
      self.p4_tt = self.p4_t + self.p4_tT
      self.mtt = self.p4_tt.M()
