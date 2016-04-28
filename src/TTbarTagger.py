#!/usr/bin/python

import ROOT
from ROOT import std, gROOT, gStyle, TLorentzVector, TMath, TRandom3
import math
import cmath
import numpy as np


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
      self.mtop  = 172.5
      self.wtop  = 1.41
      self.mW    = 80.385
      self.wW    = 2.085
      self.ibjet = -1
      self.bjet  = TLorentzVector()
      self.njets = len(ijets)
      self.nbjets = len(ibjets)
      
      self.configurations = []
      self.chi2all        = []
      self.ibestconf      = -1

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
      self.p4_Wj1 = TLorentzVector()
      self.p4_Wj2 = TLorentzVector()
      self.p4_Bj3 = TLorentzVector()

      self.rand = TRandom3(EventNumber)

      #######################################
      if(not self.MinimumInput()): return ###
      #######################################

      # order matters below
      self.SetPzNu()
      self.ResolvedTagger()

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

   def WmassConstraint(self,wMass):
      mL = self.p4_lepton.M()
      dphi = self.p4_lepton.Phi() - self.p4_etmis.Phi()
      A = (wMass*wMass-mL*mL)/2 + self.p4_etmis.Pt()*self.p4_lepton.Pt()*math.cos(dphi)
      a = math.pow(self.p4_lepton.Pz(),2) - math.pow(self.p4_lepton.E(),2)
      b = 2.*A*self.p4_lepton.Pz()
      c = A*A - math.pow(self.p4_etmis.Pt(),2)*math.pow(self.p4_lepton.E(),2)
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
      if(abs(nuz1)<abs(nuz2)): self.p4_nu = nu1
      else:                    self.p4_nu = nu2
      self.p4_Wl = self.p4_lepton + self.p4_nu
      self.p4_tl = self.p4_Wl + self.bjet
      if(nuz1==0 and nuz2==0): return False
      return True

   def SetPzNu(self,nmaxsteps=1000):
      isOK = self.WmassConstraint(self.mW)
      if(not isOK):
         for i in xrange(1,nmaxsteps+1):
            mW = self.rand.BreitWigner(self.mW,self.wW)
            if(self.WmassConstraint(mW)):
               isOK = True
               break
      if(not isOK): self.WmassConstraint(self.mW)

   def Chi2(self,n,j1,j2,j3,j4,prnt=False):
      pv = TLorentzVector()
      if(n==0): pv = self.p4_nu1
      else:     pv = self.p4_nu2
      pl  = self.p4_lepton
      pj1 = self.jets[j1]
      pj2 = self.jets[j2]
      pj3 = self.jets[j3]
      pj4 = self.jets[j4]
      mjj   = (pj1+pj2).M()
      mjjj  = (pj1+pj2+pj3).M()
      pTjjj = (pj1+pj2+pj3).Pt()
      pTlvj = (pl+pv+pj4).Pt()
      pTtt  = (pj1+pj2+pj3+pl+pv+pj4).Pt()
      mlvj  = (pl+pv+pj4).M()
      dRtt  = (pl+pv+pj4).DeltaR((pj1+pj2+pj3))
      dRwbhad   = (pj1+pj2).DeltaR(pj3)
      dRwblep   = (pl+pv).DeltaR(pj4)
      '''
      mjj-mW:           mean=-1.22914, sigma=4.20931, chi2/NDF=1.62094
      mjjj-mt:          mean=-3.66844, sigma=6.87798, chi2/NDF=1.24702
      mjjj-mjj-(mt-mW): mean=-1.45253, sigma=4.21545, chi2/NDF=0.837826
      mlvj-mt:          mean=-0.617215, sigma=4.30607, chi2/NDF=1.69918
      pTjjj-pTlvj:      mean=-1.42861, sigma=22.3835, chi2/NDF=1.5584
      '''
      chi2_mW   = math.pow((mjj-self.mW-(-1.22914))/4.20931,2)
      chi2_mtH  = math.pow((mjjj-self.mtop-(-3.66844))/6.87798,2)
      chi2_dmWt = math.pow((mjjj-mjj-(self.mtop-self.mW)-(-1.45253))/4.21545,2)
      chi2_mtL  = math.pow((mlvj-self.mtop-(-0.617215))/4.30607,2)
      chi2_dpT  = math.pow((pTjjj-pTlvj-(-1.42861))/22.3835,2)
      chi2arr = [chi2_mW, chi2_dmWt, chi2_mtL, chi2_dpT]
      chi2 = 0
      for i in xrange(len(chi2arr)): chi2 += chi2arr[i]      
      if(prnt):
         print "  mjj=%g, mjjj=%g, mlvj=%g, dpT=%g" % (mjj,mjjj,mlvj,pTjjj-pTlvj)
         print "  chi2_mW=%g, chi2_mtH=%g, chi2_mtL=%g chi2_mWt=%g, chi2_dpT=%g" % (chi2_mW,chi2_mtH,chi2_mtL,chi2_mWt,chi2_dpT)
         return
      self.chi2all.append(chi2)
      self.configurations.append({"nu":n, "j1":j1, "j2":j2, "j3":j3, "j4":j4})

   def JetPermutations(self,n,j1,j2,j3,j4):
      index = [j1,j2,j3,j4]
      for i in xrange(len(index)):
         for j in xrange(len(index)):
            if(j==i): continue
            for k in xrange(len(index)):
               if(k==j or k==i): continue
               for l in xrange(len(index)):
                  if(l==k or l==j or l==i): continue
                  if(index[k] not in self.ibjets and index[l] not in self.ibjets): continue ## j3 or j4 need to be b-tagged
                  self.Chi2(n,index[i],index[j],index[k],index[l])

   def ResolvedTagger(self):
      self.configurations = []
      self.chi2all        = []
      for i1 in xrange(len(self.ijets)):
         for i2 in xrange(len(self.ijets)):
            if(i2<=i1): continue
            for i3 in xrange(len(self.ijets)):
               if(i3<=i2): continue
               for i4 in xrange(len(self.ijets)):
                  if(i4<=i3): continue
                  j1 = self.ijets[i1]
                  j2 = self.ijets[i2]
                  j3 = self.ijets[i3]
                  j4 = self.ijets[i4]
                  if(self.p4_nu1.Pz()==self.p4_nu2.Pz()):
                     self.JetPermutations(0,j1,j2,j3,j4)
                  else:
	                 self.JetPermutations(0,j1,j2,j3,j4)
	                 self.JetPermutations(1,j1,j2,j3,j4)
      #################################################################
      if(len(self.chi2all)>0): self.ibestconf = np.argmin(self.chi2all)
      else:                    self.ibestconf = -1
      #################################################################
      # for c in xrange(len(self.configurations)):
      #    n  = self.configurations[c]["nu"]
      #    j1 = self.configurations[c]["j1"]
      #    j2 = self.configurations[c]["j2"]
      #    j3 = self.configurations[c]["j3"]
      #    j4 = self.configurations[c]["j4"]
      #    pv = TLorentzVector()
      #    if(n==0): pv = self.p4_nu1
      #    else:     pv = self.p4_nu2
      #    pl  = self.p4_lepton
      #    pj1 = self.jets[j1]
      #    pj2 = self.jets[j2]
      #    pj3 = self.jets[j3]
      #    pj4 = self.jets[j4]
      #    mjj   = (pj1+pj2).M()
      #    mjjj  = (pj1+pj2+pj3).M()
      #    pTjjj = (pj1+pj2+pj3).Pt()
      #    pTlvj = (pl+pv+pj4).Pt()
      #    pTtt  = (pj1+pj2+pj3+pl+pv+pj4).Pt()
      #    mlvj  = (pl+pv+pj4).M()
      #    chi2_mW   = math.pow((mjj-self.mW-(-1.65245e+00))/4.42579e+00,2)
      #    chi2_mtH  = math.pow((mjjj-self.mtop-(-3.78031e+00))/7.08922e+00,2)
      #    chi2_dmWt = math.pow((mjjj-mjj-(self.mtop-self.mW)-(-2.11160e+00))/5.25462e+00,2)
      #    chi2_mtL  = math.pow((mlvj-self.mtop-(-1.23194e+00))/4.42772e+00,2)
      #    chi2_dpT  = math.pow((pTjjj-pTlvj-(-3.83318e-01))/1.96484e+01,2)
      #    print "  conf[%i]: %i,%i,%i,%i ; %i -> chi2=%g" % (c,j1,j2,j3,j4,n,self.chi2all[c])
      #    # if(j1==1 and j2==2 and j3==0 and j4==4):
      #    #    print "1,2,0,4: mjj=%g, mjjj=%g, mlvj=%g, dpT=%g" % (mjj,mjjj,mlvj,pTjjj-pTlvj)
      #    #    print "           %g, %g, %g, %g, %g" % (chi2_mW,chi2_mtH,chi2_mtL,chi2_dpT,chi2_dmWt)
      #    # if(j1==1 and j2==2 and j3==4 and j4==0):
      #    #    print "1,2,4,0: mjj=%g, mjjj=%g, mlvj=%g, dpT=%g" % (mjj,mjjj,mlvj,pTjjj-pTlvj)
      #    #    print "           %g, %g, %g, %g, %g" % (chi2_mW,chi2_mtH,chi2_mtL,chi2_dpT,chi2_dmWt)

   def SetTopLep(self):
      metT = self.p4_etmis.Pt()
      lepT = self.p4_lepton.Pt()
      bT   = self.bjet.Pt()
      self.p4_WT = self.p4_lepton + self.p4_etmis
      self.p4_tT = self.p4_WT + self.bjet
      self.mTw = math.sqrt((metT+lepT)*(metT+lepT) - (self.p4_WT.Px()*self.p4_WT.Px()) - (self.p4_WT.Py()*self.p4_WT.Py()))
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
   
      iJ = [wMassIndices[0],wMassIndices[1],-1]
      if((iJ[0]==maxPtIndices[0] and iJ[1]==maxPtIndices[1]) or (iJ[0]==maxPtIndices[1] and iJ[1]==maxPtIndices[0])): iJ[2]=maxPtIndices[2]
      if((iJ[0]==maxPtIndices[0] and iJ[1]==maxPtIndices[2]) or (iJ[0]==maxPtIndices[2] and iJ[1]==maxPtIndices[0])): iJ[2]=maxPtIndices[1]
      if((iJ[0]==maxPtIndices[1] and iJ[1]==maxPtIndices[2]) or (iJ[0]==maxPtIndices[2] and iJ[1]==maxPtIndices[1])): iJ[2]=maxPtIndices[0]
      self.p4_Wj1 = self.jets[iJ[0]]
      self.p4_Wj2 = self.jets[iJ[1]]
      self.p4_Bj3 = self.jets[iJ[2]]

   def SetTTbar(self):
      self.p4_tt = self.p4_t + self.p4_tT
      self.mtt = self.p4_tt.M()
