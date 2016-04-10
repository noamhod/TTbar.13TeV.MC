#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TVirtualPad
import os
import math

histos = {}

def addHist(name,title,nbins,xmin,xmax,color=ROOT.kBlack,marker=20):
   h = TH1D(name,title,nbins,xmin,xmax)
   h.Sumw2()
   h.SetLineWidth(2)
   h.SetLineColor(color)
   h.SetMarkerColor(color)
   h.SetMarkerStyle(marker)
   h.SetMarkerSize(0.8)
   h.SetBinErrorOption(TH1.kPoisson)
   histos.update({name:h})

def plotHist(fname,name,logy=False):
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   if(logy): cnv.SetLogy()
   histos[name].Draw()
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

def plotHist2(fname,name1,name2,logy=False):
   cnv = TCanvas("cnv","",600,600)
   cnv.Draw()
   cnv.cd()
   if(logy): cnv.SetLogy()
   if(histos[name1].GetMaximum()>histos[name2].GetMaximum()):
      histos[name1].SetMinimum(0)
      histos[name1].Draw()
      histos[name2].Draw("same")
   else:
      histos[name2].SetMinimum(0)
      histos[name2].Draw()
      histos[name1].Draw("same")
   leg = TLegend(0.5,0.4,0.87,0.9,"","brNDC");
   leg.SetFillStyle(4000); # will be transparent
   leg.SetFillColor(0);
   leg.SetTextFont(42);
   leg.SetBorderSize(0);
   leg.AddEntry(0, "MadGraph+Pythia8 OTF", "");
   leg.AddEntry(0, "#it{gg}#rightarrow#it{t}_{lep}#it{t}_{had/lep}", "");
   leg.AddEntry(histos[name1],"Hard Process top","ple");
   leg.AddEntry(histos[name2],"Reconstructed tops","ple");
   leg.Draw("same")
   cnv.Update()
   cnv.RedrawAxis()
   cnv.SaveAs(fname)

addHist("HarProcessTops:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350, ROOT.kAzure-9, 24)
addHist("HarProcessTops:pTlep", ";First hard-process p_{T}(#it{t}_{lep}) [GeV];Events",40,50,550, ROOT.kAzure-9, 24)
addHist("HarProcessTops:pThad", ";Second hard-process p_{T}(#it{t}_{had}) [GeV];Events",40,50,550, ROOT.kAzure-9, 24)

addHist("Muons:Mult", ";Muon multiplicity;Events",5,0,5)
addHist("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,30,530)
addHist("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,30,530)
addHist("Muons:MWT",  ";MWT (Muon) [GeV];Events",50,0,150)

addHist("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
addHist("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,30,530)
addHist("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,30,530)
addHist("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,150)

addHist("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
addHist("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,30,630)
addHist("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,30,630)

addHist("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
addHist("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,30,630)
addHist("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,30,630)

addHist("ETmiss:eT",     ";#it{E}_{T}^{miss} [GeV];Events",50,0,630)

addHist("ETmiss:dPhiMuons",     ";#Delta#phi(#it{E}_{T}^{miss},Muon);Events",32,0,ROOT.TMath.Pi())
addHist("ETmiss:dPhiElectrons", ";#Delta#phi(#it{E}_{T}^{miss},Electron);Events",32,0,ROOT.TMath.Pi())
addHist("ETmiss:dPhiJets",      ";#Delta#phi(#it{E}_{T}^{miss},Jet);Events",32,0,ROOT.TMath.Pi())
addHist("ETmiss:dPhiBjets",     ";#Delta#phi(#it{E}_{T}^{miss},Bjet);Events",32,0,ROOT.TMath.Pi())

addHist("Muons:dRJets",      ";#DeltaR(Muon,Jet);Events",35,0,7)
addHist("Muons:dRBjets",     ";#DeltaR(Muon,Bjet);Events",35,0,7)

addHist("Electrons:dRJets",  ";#DeltaR(Electrons,Jet);Events",35,0,7)
addHist("Electrons:dRBjets", ";#DeltaR(Electrons,Bjet);Events",35,0,7)

addHist("Jets:dRBjets", ";#DeltaR(Jet,Bjet);Events",35,0,7)

addHist("Jets:dR12", ";#DeltaR(Jet1,Jet2);Events",35,0,7)
addHist("BJets:dR12", ";#DeltaR(Bjet1,Bjet2);Events",35,0,7)

addHist("Jets:mjj",  ";#it{m}(Jet1,Jet2) [GeV];Events",50,0,150)

addHist("Top:mjjb", ";#it{m}(Jet1,Jet2,Bjet) [GeV];Events",50,50,350)
addHist("Top:mwb",  ";#it{m}(Lepton,Bjet,#it{E}_{T}^{miss}) [GeV];Events",50,0,150)

addHist("TopTag:mTw", ";#it{m}_{T}(#it{W}) [GeV];Events",50,0,150)
addHist("TopTag:mTt", ";#it{m}_{T}(#it{t}_{lep}) [GeV];Events",50,50,350)
addHist("TopTag:mw",  ";#it{m}(#it{W}) [GeV];Events",50,0,150)
addHist("TopTag:mt",  ";#it{m}(#it{t}_{had}) [GeV];Events",50,50,350)

addHist("HarProcessTops:dRlep", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",35,0,7)
addHist("HarProcessTops:dRhad", ";#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",35,0,7)

addHist("HarProcessTops:dpTRellep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-5,5)
addHist("HarProcessTops:dpTRelhad", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-5,5)

addHist("TopTag:pTtLep", ";#it{p}_{T}(#it{t}_{lep}) [GeV];Events",40,50,550)
addHist("TopTag:pTtHad", ";#it{p}_{T}(#it{t}_{had}) [GeV];Events",40,50,550)
addHist("TopTag:dRlephad", ";#DeltaR(#it{t}_{lep}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
addHist("TopTag:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350)
