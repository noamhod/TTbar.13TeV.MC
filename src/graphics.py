#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TVirtualPad
import os
import math

histos = {}

def addHist1(name,title,nbins,xmin,xmax,color=ROOT.kBlack,marker=20):
   h = TH1D(name,title,nbins,xmin,xmax)
   h.Sumw2()
   h.SetLineWidth(2)
   h.SetLineColor(color)
   h.SetMarkerColor(color)
   h.SetMarkerStyle(marker)
   h.SetMarkerSize(0.8)
   h.SetBinErrorOption(TH1.kPoisson)
   histos.update({name:h})

def addHist2(name,title,nbinsx,xmin,xmax,nbinsy,ymin,ymax):
   h = TH2D(name,title,nbinsx,xmin,xmax,nbinsy,ymin,ymax)
   h.Sumw2()
   h.SetBinErrorOption(TH1.kPoisson)
   histos.update({name:h})
   

def plotHist(fname,name,logy=False):
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   if(logy): cnv.SetLogy()
   histos[name].Draw()
   leg = TLegend(0.5,0.65,0.87,0.9,"","brNDC");
   leg.SetFillStyle(4000); # will be transparent
   leg.SetFillColor(0);
   leg.SetTextFont(42);
   leg.SetBorderSize(0);
   leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
   leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
   leg.AddEntry(0, "Resolved selection", "");
   leg.AddEntry(histos[name],"Reconstructed tops","ple");
   leg.Draw("same")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

def plotHist2(fname,name1,name2,logy=False):
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   if(logy): cnv.SetLogy()
   histos[name1].SetMinimum(0)
   histos[name2].SetMinimum(0)
   if(histos[name2].GetMaximum()>histos[name1].GetMaximum()): histos[name1].SetMaximum(histos[name2].GetMaximum()*1.2)
   else:                                                      histos[name1].SetMaximum(histos[name1].GetMaximum()*1.2)
   histos[name1].Draw()
   histos[name2].Draw("same")
   leg = TLegend(0.5,0.60,0.87,0.9,"","brNDC");
   leg.SetFillStyle(4000); # will be transparent
   leg.SetFillColor(0);
   leg.SetTextFont(42);
   leg.SetBorderSize(0);
   leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
   leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
   leg.AddEntry(0, "Resolved selection", "");
   leg.AddEntry(histos[name2],"Hard Process tops","ple");
   leg.AddEntry(histos[name1],"Reconstructed tops","ple");
   leg.Draw("same")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)


def plotHist2D(fname,name,logz=False):
   gStyle.SetPadRightMargin(0.16)
   cnv = TCanvas("cnv","",800,600)
   cnv.Draw()
   cnv.cd()
   if(logz): cnv.SetLogz()
   histos[name].Draw("colz")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)
   gStyle.SetPadRightMargin(0.08)


addHist1("HarProcessTops:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350, ROOT.kAzure-9, 24)
addHist1("HarProcessTops:pTlep", ";First hard-process p_{T}(#it{t}_{lep}) [GeV];Events",40,50,550, ROOT.kAzure-9, 24)
addHist1("HarProcessTops:pThad", ";Second hard-process p_{T}(#it{t}_{had}) [GeV];Events",40,50,550, ROOT.kAzure-9, 24)

addHist1("Muons:Mult", ";Muon multiplicity;Events",5,0,5)
addHist1("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,30,530)
addHist1("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,30,530)
addHist1("Muons:MWT",  ";MWT(lep) [GeV];Events",50,0,150)

addHist1("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
addHist1("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,30,530)
addHist1("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,30,530)
addHist1("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,150)

addHist1("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
addHist1("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,30,630)
addHist1("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,30,630)
addHist1("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,30,630)
addHist1("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,30,630)

addHist1("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
addHist1("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,30,630)
addHist1("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,30,630)
addHist1("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,30,630)
addHist1("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,30,630)

addHist1("ETmiss:eT",     ";#it{E}_{T}^{miss} [GeV];Events",50,0,630)

addHist1("ETmiss:dPhiMuons",     ";#Delta#phi(#it{E}_{T}^{miss},Muon);Events",32,0,ROOT.TMath.Pi())
addHist1("ETmiss:dPhiElectrons", ";#Delta#phi(#it{E}_{T}^{miss},Electron);Events",32,0,ROOT.TMath.Pi())
addHist1("ETmiss:dPhiJets",      ";#Delta#phi(#it{E}_{T}^{miss},Jet);Events",32,0,ROOT.TMath.Pi())
addHist1("ETmiss:dPhiBjets",     ";#Delta#phi(#it{E}_{T}^{miss},Bjet);Events",32,0,ROOT.TMath.Pi())

addHist1("Muons:dRJets",      ";#DeltaR(Muon,Jet);Events",35,0,7)
addHist1("Muons:dRBjets",     ";#DeltaR(Muon,Bjet);Events",35,0,7)

addHist1("Electrons:dRJets",  ";#DeltaR(Electrons,Jet);Events",35,0,7)
addHist1("Electrons:dRBjets", ";#DeltaR(Electrons,Bjet);Events",35,0,7)

addHist1("Jets:dRBjets", ";#DeltaR(Jet,Bjet);Events",35,0,7)

addHist1("Jets:dR12", ";#DeltaR(Jet1,Jet2);Events",35,0,7)
addHist1("BJets:dR12", ";#DeltaR(Bjet1,Bjet2);Events",35,0,7)

addHist1("Jets:mjj",  ";#it{m}(Jet1,Jet2) [GeV];Events",50,0,150)

addHist1("Top:mjjb", ";#it{m}(Jet1,Jet2,Bjet) [GeV];Events",50,50,350)
addHist1("Top:mwb",  ";#it{m}(Lepton,Bjet,#it{E}_{T}^{miss}) [GeV];Events",50,0,150)

addHist1("TopTag:mwHad",  ";#it{m}(#it{W}_{had}) [GeV];Events",50,0,150)
addHist1("TopTag:mTw", ";#it{m}_{T}(#it{W}_{lep}) [GeV];Events",50,0,150)
addHist1("TopTag:mLw", ";#it{m}(#it{W}_{lep}) [GeV];Events",50,0,150)
addHist1("TopTag:mLw0", ";#it{m}(#it{W}_{lep0}) [GeV];Events",50,0,150)
addHist1("TopTag:mLw1", ";#it{m}(#it{W}_{lep1}) [GeV];Events",50,0,150)
addHist1("TopTag:mLw2", ";#it{m}(#it{W}_{lep2}) [GeV];Events",50,0,150)
addHist1("TopTag:mtHad",  ";#it{m}(#it{t}_{had}) [GeV];Events",50,50,350)
addHist1("TopTag:mTt", ";#it{m}_{T}(#it{t}_{lep}) [GeV];Events",50,50,350)
addHist1("TopTag:mLt", ";#it{m}(#it{t}_{lep}) [GeV];Events",50,50,350)
addHist1("TopTag:mLt0",  ";#it{m}(#it{t}_{lep0}) [GeV];Events",50,50,350)
addHist1("TopTag:mLt1",  ";#it{m}(#it{t}_{lep1}) [GeV];Events",50,50,350)
addHist1("TopTag:mLt2",  ";#it{m}(#it{t}_{lep2}) [GeV];Events",50,50,350)

addHist1("TopTag:dRLw12", ";#DeltaR(#it{W}_{lep1}^{rec},#it{W}_{lep2}^{rec});Events",35,0,7)
addHist1("TopTag:dRLt12", ";#DeltaR(#it{t}_{lep1}^{rec},#it{t}_{lep2}^{rec});Events",35,0,7)
addHist1("TopTag:dRlep0had", ";#DeltaR(#it{t}_{lep0}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
addHist1("TopTag:dRlep1had", ";#DeltaR(#it{t}_{lep1}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
addHist1("TopTag:dRlep2had", ";#DeltaR(#it{t}_{lep2}^{rec},#it{t}_{had}^{rec});Events",35,0,7)

addHist1("HarProcessTops:dRlepT", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lepT}^{rec});Events",35,0,7)
addHist1("HarProcessTops:dRlep", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",35,0,7)
addHist1("HarProcessTops:dRlep0", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep0}^{rec});Events",35,0,7)
addHist1("HarProcessTops:dRlep1", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep1}^{rec});Events",35,0,7)
addHist1("HarProcessTops:dRlep2", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep2}^{rec});Events",35,0,7)
addHist1("HarProcessTops:dRhad", ";#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",35,0,7)

addHist1("HarProcessTops:dpTRellepT", ";#it{t}_{lepT}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
addHist1("HarProcessTops:dpTRellep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
addHist1("HarProcessTops:dpTRellep0", ";#it{t}_{lep0}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
addHist1("HarProcessTops:dpTRellep1", ";#it{t}_{lep1}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
addHist1("HarProcessTops:dpTRellep2", ";#it{t}_{lep2}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
addHist1("HarProcessTops:dpTRelhad", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)

addHist1("TopTag:pTtTLep", ";#it{p}_{T}(#it{t}_{lepT}) [GeV];Events",40,50,550)
addHist1("TopTag:pTtLep", ";#it{p}_{T}(#it{t}_{lep}) [GeV];Events",40,50,550)
addHist1("TopTag:pTtLep0", ";#it{p}_{T}(#it{t}_{lep0}) [GeV];Events",40,50,550)
addHist1("TopTag:pTtLep1", ";#it{p}_{T}(#it{t}_{lep1}) [GeV];Events",40,50,550)
addHist1("TopTag:pTtLep2", ";#it{p}_{T}(#it{t}_{lep2}) [GeV];Events",40,50,550)
addHist1("TopTag:pTtHad", ";#it{p}_{T}(#it{t}_{had}) [GeV];Events",40,50,550)
addHist1("TopTag:dRlepThad", ";#DeltaR(#it{t}_{lepT}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
addHist1("TopTag:dRlephad", ";#DeltaR(#it{t}_{lep}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
addHist1("TopTag:mTtt", ";#it{m}_{T}(#it{t}_{had}, #it{t}_{lepT}) [GeV];Events",40,350,1350)
addHist1("TopTag:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350)
addHist1("TopTag:mtt0", ";#it{m}(#it{t}_{had}, #it{t}_{lep0}) [GeV];Events",40,350,1350)
addHist1("TopTag:mtt1", ";#it{m}(#it{t}_{had}, #it{t}_{lep1}) [GeV];Events",40,350,1350)
addHist1("TopTag:mtt2", ";#it{m}(#it{t}_{had}, #it{t}_{lep2}) [GeV];Events",40,350,1350)

addHist1("HarProcessTops:dmRellepT", ";#it{t}_{lepT}: #it{m}_{T}^{rec}(#it{t}_{had}, #it{t}_{lepT})/#it{m}^{tru}(#it{t}_{had}, #it{t}_{lepT})-1;Events",50,-1,5)
addHist1("HarProcessTops:dmRellep", ";#it{t}_{lep}: #it{m}^{rec}(#it{t}_{had}, #it{t}_{lep})/#it{m}^{tru}(#it{t}_{had}, #it{t}_{lep})-1;Events",50,-1,5)

addHist2("HarProcessTops:dpTRel:dRtru:had", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",100,0,5, 100,-1,5)
addHist2("HarProcessTops:dpTRel:dRtru:lepT", ";#it{t}_{lepT}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lepT}^{rec});Events",100,0,5, 100,-1,5)
addHist2("HarProcessTops:dpTRel:dRtru:lep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",100,0,5, 100,-1,5)
