#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TTree, TLorentzVector, TMath, TVirtualPad, TEventList, TVector2
import os
import math
import subprocess
import collections
import rootstyle
import graphics
from TTbarTagger import TTbarTagger
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name [lep/had]')
parser.add_argument('-r', metavar='<re-hadd ntupe>', required=True, help='Re-hadd ntuple ? [yes/no]')
args = parser.parse_args()
name = args.n
hadd = args.r
print 'name : ',name
print 're-hadd : ',hadd

ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()

path = "/afs/cern.ch/user/h/hod/data/MC/ttbar/ntup"
fmerged = path+"/tops.SM.TRUTH1."+name+".merged.root"
if(hadd=="yes"):
   p = subprocess.Popen("rm -f  "+path+"/tops.SM.TRUTH1."+name+".merged.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   p = subprocess.Popen("hadd  "+fmerged+"  "+path+"/tops.SM.TRUTH1."+name+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   print out


gROOT.LoadMacro( "src/Loader.C+" )

tfile = TFile(path+"/tops.SM.TRUTH1."+name+".merged.root","READ")
tree = tfile.Get("SM")

def MWT(pLep,pMET):
   mwt = math.sqrt(2*(pLep.Pt()*pMET.Pt() - pLep.Px()*pMET.Px() - pLep.Py()*pMET.Py()))
   return mwt

# def LeptonicMT(lep,bjet,etmis):
#    metT = etmis.Pt()
#    lepT = lep.Pt()
#    bT   = bjet.Pt()
#    WT = lep+etmis
#    mTw = math.sqrt((metT+lepT)*(metT+lepT) - (WT.Px()*WT.Px()) - (WT.Py()*WT.Py()))
#    topT = WT + bjet
#    mTt = math.sqrt((metT+lepT+bT)*(metT+lepT+bT) - (topT.Px()*topT.Px()) - (topT.Py()*topT.Py()))
#    lepb = bjet + lep
#    mlb = lepb.M() 
#    return (mTw,mTt,mlb)
# 
# 
# def HadronicMT(jets,ijets,ibjet=-1):
#    njets  = len(ijets)
# 
#    # have to have at least 3 jets...
#    if(njets<3): return (-1,-1)
#    
#    # associate those jets with maximum pt of the vectorial sum to the hadronic decay chain
#    maxPt = -1
#    maxPtIndices = [-1,-1,-1]
#    for i in xrange(njets):
#      if(ijets[i]==ibjet): continue
#      for j in xrange(njets):
#        if(j<=i):            continue
#        if(ijets[j]==ibjet): continue
#        for k in xrange(njets):
#           if(k==i or k==j):    continue
#           if(ijets[k]==ibjet): continue
#           sum = jets[ijets[i]]+jets[ijets[j]]+jets[ijets[k]]
#           if(maxPt<0 or maxPt<sum.Pt()):
#              maxPt=sum.Pt()
#              maxPtIndices[0] = ijets[i]
#              maxPtIndices[1] = ijets[j]
#              maxPtIndices[2] = ijets[k]
# 
#    mtop = ( jets[maxPtIndices[0]]+jets[maxPtIndices[1]]+jets[maxPtIndices[2]] ).M()
# 
#    # associate those jets that get closest to the W mass with their invariant mass to the W boson
#    nmaxPtIndices = len(maxPtIndices)
#    mW = 80.385
#    wDist = -1
#    wMassIndices = [-1,-1]
#    for i in xrange(nmaxPtIndices):
#       for j in xrange(nmaxPtIndices):
#          if(j==i or maxPtIndices[i]>maxPtIndices[j]): continue
#          sum = jets[maxPtIndices[i]]+jets[maxPtIndices[j]]
#          if(wDist<0. or wDist>abs(sum.M()-80.385) ):
#             wDist = abs(sum.M()-mW)
#             wMassIndices[0] = maxPtIndices[i]
#             wMassIndices[1] = maxPtIndices[j]
# 
#    mw = ( jets[wMassIndices[0]]+jets[wMassIndices[1]] ).M()
#  
#    return (mw, mtop)

   

def JetOverlap(obj,jets,ijets,objtype,dRoverlap=0.4):
   for i in ijets:
      if(jets[i].DeltaR(obj)<dRoverlap):
         if(objtype=="electron"):
	        if(abs(jets[i].Pt()-obj.Pt())/obj.Pt()<0.3): return True
         elif(objtype=="muon"):
		    if(abs(jets[i].Pt()-obj.Pt())/obj.Pt()<0.5): return True
         else: return True
   return False

# histos = {}
# def addHist(name,title,nbins,xmin,xmax,color=ROOT.kBlack,marker=20):
#    h = TH1D(name,title,nbins,xmin,xmax)
#    h.Sumw2()
#    h.SetLineWidth(2)
#    h.SetLineColor(color)
#    h.SetMarkerColor(color)
#    h.SetMarkerStyle(marker)
#    h.SetMarkerSize(0.8)
#    h.SetBinErrorOption(TH1.kPoisson)
#    histos.update({name:h})
# 
# addHist("Muons:Mult", ";Muon multiplicity;Events",5,0,5)
# addHist("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,30,530)
# addHist("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,30,530)
# addHist("Muons:MWT",  ";MWT (Muon) [GeV];Events",50,0,630)
# 
# addHist("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
# addHist("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,30,530)
# addHist("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,30,530)
# addHist("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,630)
# 
# addHist("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
# addHist("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,30,630)
# addHist("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,30,630)
# addHist("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,30,630)
# addHist("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,30,630)
# 
# addHist("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
# addHist("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,30,630)
# addHist("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,30,630)
# addHist("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,30,630)
# addHist("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,30,630)
# 
# addHist("ETmiss:eT",     ";#it{E}_{T}^{miss} [GeV];Events",50,0,630)
# 
# addHist("ETmiss:dPhiMuons",     ";#Delta#phi(#it{E}_{T}^{miss},Muon);Events",32,0,ROOT.TMath.Pi())
# addHist("ETmiss:dPhiElectrons", ";#Delta#phi(#it{E}_{T}^{miss},Electron);Events",32,0,ROOT.TMath.Pi())
# addHist("ETmiss:dPhiJets",      ";#Delta#phi(#it{E}_{T}^{miss},Jet);Events",32,0,ROOT.TMath.Pi())
# addHist("ETmiss:dPhiBjets",     ";#Delta#phi(#it{E}_{T}^{miss},B-jet);Events",32,0,ROOT.TMath.Pi())
# 
# addHist("Muons:dRJets",      ";#DeltaR(Muon,Jet);Events",50,0,7)
# addHist("Muons:dRBjets",     ";#DeltaR(Muon,B-jet);Events",50,0,7)
# 
# addHist("Electrons:dRJets",  ";#DeltaR(Electrons,Jet);Events",50,0,7)
# addHist("Electrons:dRBjets", ";#DeltaR(Electrons,B-jet);Events",50,0,7)
# 
# addHist("Jets:dRBjets", ";#DeltaR(Jet,B-jet);Events",50,0,7)
# 
# addHist("Jets:dR12", ";#DeltaR(Jet1,Jet2);Events",50,0,7)
# addHist("BJets:dR12", ";#DeltaR(B-jet1,B-jet2);Events",50,0,7)
# 
# addHist("Jets:mjj",  ";#it{m}(Jet1,Jet2);Events",50,0,150)
# 
# addHist("Top:mjjb", ";#it{m}(Jet1,Jet2,Bjet);Events",50,50,350)
# addHist("Top:mwb",  ";#it{m}(Lepton,Bjet,#it{E}_{T}^{miss});Events",50,0,150)
# 
# addHist("TopTag:mTw", ";#it{m}_{T}(#it{W});Events",50,0,150)
# addHist("TopTag:mTt", ";#it{m}_{T}(#it{t}-lep);Events",50,50,350)
# addHist("TopTag:mw",  ";#it{m}(#it{W});Events",50,0,150)
# addHist("TopTag:mt",  ";#it{m}(#it{t}-had);Events",50,50,350)
# addHist("TopTag:mtt", ";#it{m}(#it{t}-had);Events",80,350,1000)



n=1
for event in tree:

   jets = []
   bflags = []
   btagged = {}
   for i in xrange(event.p4_akt4jets.size()):
      if(abs(event.p4_akt4jets[i].Eta())>2.5): continue
      if(event.p4_akt4jets[i].Pt()<25):        continue
      jets.append(i)
      graphics.histos["ETmiss:dPhiJets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[i].Phi()-event.p4_MET[0].Phi()))  )
      bflags.append(False)
      for j in xrange(event.p4_bquarks.size()):
         if(event.st_bquarks[j]!=23): continue
         dRb = event.p4_akt4jets[i].DeltaR(event.p4_bquarks[j])
         if(dRb<0.4):
            bflags[len(bflags)-1] = True
            btagged.update({event.p4_akt4jets[i].Pt() : i})
            graphics.histos["ETmiss:dPhiBjets"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_akt4jets[i].Phi()-event.p4_MET[0].Phi())) )
            break

      # isbtagged = False
      # if(event.id_bquarks_children[j].size()==0): continue
      # for k in xrange(event.id_bquarks_children[j].size()):
      #    if(event.id_bquarks_children[j][k]==21):                  continue
      #    if(event.id_bquarks_children[j][k]==event.id_bquarks[j]): continue
      #    dRb = event.p4_akt4jets[i].DeltaR(event.p4_bquarks_children[j][k])
      #    # print "b-decay["+str(k)+"] id = "+str(event.id_bquarks_children[j][k])+" -> dR="+str(dRb)
      #    if(dRb<0.4):
      #       isbtagged = True
      #       btagged.append(i)
      #       break
      # if(isbtagged): break

      # isbtagged = False
      # for j in xrange(event.p4_tquarks.size()):
      # if(event.id_tquarks_children[j].size()==0): continue
      # for k in xrange(event.id_tquarks_children[j].size()):
      #    if(abs(event.id_tquarks_children[j][k])!=5): continue
      #    dRb = event.p4_akt4jets[i].DeltaR(event.p4_tquarks_children[j][k])
      #    print "jet["+str(i)+"]: b["+str(j)+"] from t-decay["+str(k)+"] id = "+str(event.id_tquarks_children[j][k])+" -> dR="+str(dRb)
      #    if(dRb<1.0):
      #       isbtagged = True
      #       btagged.append(i)
      #       break
      # if(isbtagged): break

   muons = []
   for i in xrange(event.p4_muons.size()):
      if(abs(event.p4_muons[i].Eta())>2.5): continue
      if(event.p4_muons[i].Pt()<30):        continue
      if(event.st_muons[i]!=1):             continue
      if(JetOverlap(event.p4_muons[i],event.p4_akt4jets,jets,"muon")): continue
      muons.append(i)
      graphics.histos["ETmiss:dPhiMuons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_muons[i].Phi()-event.p4_MET[0].Phi())) )
   graphics.histos["Muons:Mult"].Fill(len(muons))
   if(len(muons)>0): graphics.histos["Muons:pT1"].Fill(event.p4_muons[muons[0]].Pt())
   if(len(muons)>1): graphics.histos["Muons:pT2"].Fill(event.p4_muons[muons[1]].Pt())

   electrons = []
   for i in xrange(event.p4_electrons.size()):
      if(abs(event.p4_electrons[i].Eta())>2.5): continue
      if(event.p4_electrons[i].Pt()<30):        continue
      if(event.st_electrons[i]!=1):             continue
      if(JetOverlap(event.p4_electrons[i],event.p4_akt4jets,jets,"electron")): continue
      electrons.append(i)
      graphics.histos["ETmiss:dPhiElectrons"].Fill( abs(TVector2.Phi_mpi_pi(event.p4_electrons[i].Phi()-event.p4_MET[0].Phi())) )
   graphics.histos["Electrons:Mult"].Fill(len(electrons))
   if(len(electrons)>0): graphics.histos["Electrons:pT1"].Fill(event.p4_electrons[electrons[0]].Pt())
   if(len(electrons)>1): graphics.histos["Electrons:pT2"].Fill(event.p4_electrons[electrons[1]].Pt())



   graphics.histos["Jets:Mult"].Fill(len(jets))
   if(len(jets)>0): graphics.histos["Jets:pT1"].Fill(event.p4_akt4jets[jets[0]].Pt())
   if(len(jets)>1): graphics.histos["Jets:pT2"].Fill(event.p4_akt4jets[jets[1]].Pt())
   if(len(jets)>2): graphics.histos["Jets:pT3"].Fill(event.p4_akt4jets[jets[2]].Pt())
   if(len(jets)>3): graphics.histos["Jets:pT4"].Fill(event.p4_akt4jets[jets[3]].Pt())

   btagged_ptsorted = collections.OrderedDict(reversed(sorted(btagged.items()))).values()
   graphics.histos["BJets:Mult"].Fill(len(btagged_ptsorted))
   if(len(btagged_ptsorted)>0): graphics.histos["BJets:pT1"].Fill(event.p4_akt4jets[btagged_ptsorted[0]].Pt())
   if(len(btagged_ptsorted)>1): graphics.histos["BJets:pT2"].Fill(event.p4_akt4jets[btagged_ptsorted[1]].Pt())
   if(len(btagged_ptsorted)>2): graphics.histos["BJets:pT3"].Fill(event.p4_akt4jets[btagged_ptsorted[2]].Pt())
   if(len(btagged_ptsorted)>3): graphics.histos["BJets:pT4"].Fill(event.p4_akt4jets[btagged_ptsorted[3]].Pt())

   graphics.histos["ETmiss:eT"].Fill(event.p4_MET[0].Pt())

   if(len(muons)>0 and len(electrons)==0): graphics.histos["Muons:MWT"].Fill(MWT(event.p4_muons[muons[0]],event.p4_MET[0]))
   if(len(electrons)>0 and len(muons)==0): graphics.histos["Electrons:MWT"].Fill(MWT(event.p4_electrons[electrons[0]],event.p4_MET[0]))
   
   non_btagged = []
   for j in jets:
     if(j in btagged_ptsorted): continue
     non_btagged.append(j)

   for j in jets:
     for i in muons:     graphics.histos["Muons:dRJets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
     for i in electrons: graphics.histos["Electrons:dRJets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   for j in btagged_ptsorted:
      for i in muons:     graphics.histos["Muons:dRBjets"].Fill(event.p4_muons[i].DeltaR(event.p4_akt4jets[j]))
      for i in electrons: graphics.histos["Electrons:dRBjets"].Fill(event.p4_electrons[i].DeltaR(event.p4_akt4jets[j]))
   for j in non_btagged:
      for i in btagged_ptsorted:
         graphics.histos["Jets:dRBjets"].Fill(event.p4_akt4jets[j].DeltaR(event.p4_akt4jets[i]))
   
   if(len(non_btagged)>1):      graphics.histos["Jets:dR12"].Fill(event.p4_akt4jets[non_btagged[0]].DeltaR(event.p4_akt4jets[non_btagged[1]]))
   if(len(btagged_ptsorted)>1): graphics.histos["BJets:dR12"].Fill(event.p4_akt4jets[btagged_ptsorted[0]].DeltaR(event.p4_akt4jets[btagged_ptsorted[1]]))

   # if(len(non_btagged)>1): graphics.histos["Jets:mjj"].Fill( (event.p4_akt4jets[non_btagged[0]]+event.p4_akt4jets[non_btagged[1]]).M() )
   # if(len(non_btagged)>1 and len(btagged_ptsorted)>1 and ((len(muons)>0 and len(electrons)==0) or (len(muons)==0 and len(electrons)>0)) ):
   #    j1  = event.p4_akt4jets[non_btagged[0]]
   #    j2  = event.p4_akt4jets[non_btagged[1]]
   #    b1  = event.p4_akt4jets[btagged_ptsorted[0]]
   #    b2  = event.p4_akt4jets[btagged_ptsorted[1]]
   #    lep = TLorentzVector()
   #    if(len(muons)>0 and len(electrons)==0): lep = event.p4_muons[0]
   #    if(len(muons)==0 and len(electrons)>0): lep = event.p4_electrons[0]
   #    mt   = -1
   #    mTt  = -1
   #    mTw  = -1
   #    mlb  = -1
   #    if( lep.DeltaR(b1)<lep.DeltaR(b2) ):
   #       mt = (j1+j2+b2).M()
   #       mTw, mTt, mlb = LeptonicMT(lep,b1,event.p4_MET[0]) # MWT((lep+b1),event.p4_MET[0])
   #    elif( lep.DeltaR(b2)<=lep.DeltaR(b1) ):
   #       mt = (j1+j2+b1).M()
   #       mTw, mTt, mlb = LeptonicMT(lep,b2,event.p4_MET[0]) # MWT((lep+b2),event.p4_MET[0])
   #    if(mt>0):  graphics.histos["Top:mjjb"].Fill(mt)
   #    if(mTt>0): graphics.histos["Top:mwb"].Fill(mTt)


   if(len(jets)>3 and len(btagged_ptsorted)>0 and ((len(muons)>0 and len(electrons)==0) or (len(muons)==0 and len(electrons)>0)) ):
      etmis = event.p4_MET[0]
      lep   = TLorentzVector()
      if(len(muons)>0 and len(electrons)==0): lep = event.p4_muons[0]
      if(len(muons)==0 and len(electrons)>0): lep = event.p4_electrons[0]

      # ibjet = btagged_ptsorted[0]
      # bjet  = event.p4_akt4jets[ibjet]
      # if(len(btagged_ptsorted)>1):
      #    dr1 = lep.DeltaR(event.p4_akt4jets[btagged_ptsorted[0]])
      #    dr2 = lep.DeltaR(event.p4_akt4jets[btagged_ptsorted[1]])
      #    if(dr1>dr2):
      #       ibjet = btagged_ptsorted[1]
      #       bjet  = event.p4_akt4jets[ibjet]
      # mTw, mTt, mlb = LeptonicMT(lep,bjet,etmis)
      # mw, mt        = HadronicMT(event.p4_akt4jets,jets,ibjet)

      ttTag = TTbarTagger(event.p4_akt4jets,jets,btagged_ptsorted,lep,etmis,1)
      if(not ttTag.MinimumInput()): continue
      graphics.histos["TopTag:mTw"].Fill(ttTag.mTw)
      graphics.histos["TopTag:mTt"].Fill(ttTag.mTt)
      graphics.histos["TopTag:mw"].Fill(ttTag.mw)
      graphics.histos["TopTag:mt"].Fill(ttTag.mt)
      graphics.histos["TopTag:mtt"].Fill(ttTag.mtt)

   ### end of events loop
   if(n%10000==0): print "processed |SM+X|^2 generated ",n
   n+=1


# def plot(fname,name,logy=False):
#    cnv = TCanvas("cnv","",600,600)
#    cnv.Draw()
#    cnv.cd()
#    if(logy): cnv.SetLogy()
#    histos[name].Draw()
#    cnv.Update()
#    cnv.RedrawAxis()
#    cnv.SaveAs(fname)

fname = path+"/Test.TTree.TRUTH1."+name+".pdf"

graphics.plotHist(fname+"(", "Muons:Mult")
graphics.plotHist(fname,     "Muons:pT1",True)
graphics.plotHist(fname,     "Muons:pT2",True)
graphics.plotHist(fname,     "Electrons:Mult")
graphics.plotHist(fname,     "Electrons:pT1",True)
graphics.plotHist(fname,     "Electrons:pT2",True)
graphics.plotHist(fname,     "Jets:Mult")
graphics.plotHist(fname,     "Jets:pT1",True)
graphics.plotHist(fname,     "Jets:pT2",True)
graphics.plotHist(fname,     "Jets:pT3",True)
graphics.plotHist(fname,     "Jets:pT4",True)
graphics.plotHist(fname,     "BJets:Mult")
graphics.plotHist(fname,     "BJets:pT1",True)
graphics.plotHist(fname,     "BJets:pT2",True)
graphics.plotHist(fname,     "BJets:pT3",True)
graphics.plotHist(fname,     "BJets:pT4",True)
graphics.plotHist(fname,     "ETmiss:eT",True)
graphics.plotHist(fname,     "Muons:MWT",True)
graphics.plotHist(fname,     "Electrons:MWT",True)
graphics.plotHist(fname,     "ETmiss:dPhiMuons")  
graphics.plotHist(fname,     "ETmiss:dPhiElectrons")
graphics.plotHist(fname,     "ETmiss:dPhiJets")
graphics.plotHist(fname,     "ETmiss:dPhiBjets")  
graphics.plotHist(fname,     "Muons:dRJets")  
graphics.plotHist(fname,     "Muons:dRBjets")
graphics.plotHist(fname,     "Electrons:dRJets")
graphics.plotHist(fname,     "Jets:dRBjets")
graphics.plotHist(fname,     "Jets:dR12")
graphics.plotHist(fname,     "BJets:dR12")
# graphics.plotHist(fname,     "Jets:mjj")
# graphics.plotHist(fname,     "Top:mjjb")
# graphics.plotHist(fname+")", "Top:mwb")
graphics.plotHist(fname,     "TopTag:mTw")
graphics.plotHist(fname,     "TopTag:mTt")
graphics.plotHist(fname,     "TopTag:mw")
graphics.plotHist(fname,     "TopTag:mt")
graphics.plotHist(fname+")", "TopTag:mtt")

