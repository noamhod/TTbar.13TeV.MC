#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, gDirectory, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TVirtualPad, TDirectory
import os
import math


class Graphics:
   'Class for ttbar jets selection'

   def __init__(self):
      self.histos = {}
      self.ModelNpoints = 0
      self.ModelMass = ""
      self.ModelName = ""

   def __del__(self):
      class_name = self.__class__.__name__
      # do nothing else


   def setModel(self,n,mass,name):
      self.ModelNpoints = n
      self.ModelMass = mass
      self.ModelName = name
   
   def addHist1(self,name,title,nbins,xmin,xmax,color=ROOT.kBlack,marker=20):
      h = TH1D(name,title,nbins,xmin,xmax)
      h.Sumw2()
      h.SetLineWidth(2)
      h.SetLineColor(color)
      h.SetMarkerColor(color)
      h.SetMarkerStyle(marker)
      h.SetMarkerSize(0.8)
      h.SetBinErrorOption(TH1.kPoisson)
      h.SetDirectory(0)
      self.histos.update({name:h})
   
   def addHist2(self,name,title,nbinsx,xmin,xmax,nbinsy,ymin,ymax):
      h = TH2D(name,title,nbinsx,xmin,xmax,nbinsy,ymin,ymax)
      h.Sumw2()
      h.SetBinErrorOption(TH1.kPoisson)
      h.SetDirectory(0)
      self.histos.update({name:h})
   
   def addHist1N(self,name,title,nbins,xmin,xmax,color1=ROOT.kGray+2,marker1=20,color2=ROOT.kGreen+1,marker2=24):
      for i in xrange(self.ModelNpoints):
         nametmp = name+str(i)
         self.addHist1(nametmp,title,nbins,xmin,xmax,color1,marker1)
   
   
   def plotHist(self,fname,name,logy=False):
      cnv = TCanvas("cnv","",600,600)
      cnv.Draw()
      cnv.cd()
      if(logy): cnv.SetLogy()
      self.histos[name].Draw()
      leg = TLegend(0.5,0.65,0.87,0.9,"","brNDC");
      leg.SetFillStyle(4000); # will be transparent
      leg.SetFillColor(0);
      leg.SetTextFont(42);
      leg.SetBorderSize(0);
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
      leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
      leg.AddEntry(0, "Resolved selection", "");
      leg.AddEntry(self.histos[name],"Reconstructed tops","ple");
      leg.Draw("same")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
   
   def plotHist2(self,fname,name1,name2,logy=False):
      cnv = TCanvas("cnv","",600,600)
      cnv.Draw()
      cnv.cd()
      if(logy): cnv.SetLogy()
      self.histos[name1].SetMinimum(0)
      self.histos[name2].SetMinimum(0)
      if(self.histos[name2].GetMaximum()>self.histos[name1].GetMaximum()): self.histos[name1].SetMaximum(self.histos[name2].GetMaximum()*1.2)
      else:                                                      self.histos[name1].SetMaximum(self.histos[name1].GetMaximum()*1.2)
      self.histos[name1].Draw()
      self.histos[name2].Draw("same")
      leg = TLegend(0.5,0.60,0.87,0.9,"","brNDC");
      leg.SetFillStyle(4000); # will be transparent
      leg.SetFillColor(0);
      leg.SetTextFont(42);
      leg.SetBorderSize(0);
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
      leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
      leg.AddEntry(0, "Resolved selection", "");
      leg.AddEntry(self.histos[name2],"Hard Process tops","ple");
      leg.AddEntry(self.histos[name1],"Reconstructed tops","ple");
      leg.Draw("same")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
   
   def plotHist4(self,fname,model,name1,name2,name3,name4,logy=False):
      cnv = TCanvas("cnv","",600,600)
      cnv.Draw()
      cnv.cd()
      if(logy): cnv.SetLogy()
      self.histos[name1].SetMinimum(0)
      self.histos[name2].SetMinimum(0)
      if(self.histos[name2].GetMaximum()>self.histos[name1].GetMaximum()): self.histos[name1].SetMaximum(self.histos[name2].GetMaximum()*1.2)
      else:                                                      self.histos[name1].SetMaximum(self.histos[name1].GetMaximum()*1.2)
      self.histos[name1].Draw()
      self.histos[name2].Draw("same")
      self.histos[name3].Draw("same")
      self.histos[name4].Draw("same")
      leg = TLegend(0.5,0.50,0.87,0.9,"","brNDC");
      leg.SetFillStyle(4000); # will be transparent
      leg.SetFillColor(0);
      leg.SetTextFont(42);
      leg.SetBorderSize(0);
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
      leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets (resolved)", "");
      leg.AddEntry(0, model, "");
      leg.AddEntry(self.histos[name2],"Hard Process tops 2HDM", "ple");
      leg.AddEntry(self.histos[name4],"Hard Process tops SM",   "ple");
      leg.AddEntry(self.histos[name1],"Reconstructed tops 2HDM","ple");
      leg.AddEntry(self.histos[name3],"Reconstructed tops SM",  "ple");
      leg.Draw("same")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
   
   def plotHist2D(self,fname,name,logz=False):
      gStyle.SetPadRightMargin(0.16)
      cnv = TCanvas("cnv","",800,600)
      cnv.Draw()
      cnv.cd()
      if(logz): cnv.SetLogz()
      self.histos[name].Draw("colz")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
      gStyle.SetPadRightMargin(0.08)

   def plotRatio(self,fname,level,nameSM,nameXX,nameIX,wX,stanb,nameX,mX):
      cnv = TCanvas("cnv","",600,600)
      cnv.Divide(1,2)
      tvp_hists = cnv.cd(1)
      tvp_ratio = cnv.cd(2)
      cnv.Draw()
      tvp_hists.SetPad(0.00, 0.35, 1.00, 1.00)
      tvp_ratio.SetPad(0.00, 0.02, 1.00, 0.35)
      tvp_hists.SetBottomMargin(0.012)
      tvp_ratio.SetBottomMargin(0.20)
      tvp_ratio.SetTopMargin(0.012)
      tvp_hists.SetTicks(1,1)
      tvp_ratio.SetTicks(1,1)	
      
      sXtitle = self.histos[nameXX].GetXaxis().GetTitle()

      self.histos[nameXX].SetMarkerStyle(20)
      self.histos[nameXX].SetMarkerSize(0.9)
      self.histos[nameXX].SetMarkerColor(ROOT.kRed)
      self.histos[nameXX].SetLineColor(ROOT.kRed)
      self.histos[nameXX].SetLineStyle(1)
      self.histos[nameXX].SetLineWidth(2)

      self.histos[nameSM].SetMarkerStyle(24)
      self.histos[nameSM].SetMarkerSize(0.9)
      self.histos[nameSM].SetMarkerColor(ROOT.kBlack)
      self.histos[nameSM].SetLineColor(ROOT.kBlack)
      self.histos[nameSM].SetLineStyle(1)
      self.histos[nameSM].SetLineWidth(2)
      
      hr = self.histos[nameIX].Clone("ratio")
      hr.Sumw2()
      hr.SetTitle(";"+sXtitle+";|SM+#it{"+nameX+"}|^{2}/|SM|^{2}-1 [%]")
      hr.Divide(self.histos[nameIX],self.histos[nameSM],100.,1.) ### to have the interference shape relative to the SM shape in percentage
      hr.SetMarkerStyle(20)
      hr.SetMarkerSize(0.7)
      hr.SetMarkerColor(ROOT.kBlack)
      hr.SetLineColor(ROOT.kBlack)
      hr.SetLineStyle(1)
      hr.SetLineWidth(2)
      xLabelSize = hr.GetXaxis().GetLabelSize()*1.85
      yLabelSize = hr.GetYaxis().GetLabelSize()*1.85
      xTitleSize = hr.GetXaxis().GetTitleSize()*1.85
      yTitleSize = hr.GetYaxis().GetTitleSize()*1.5
      # titleSize  = hr.GetTitleSize()           *1.7
      hr.GetXaxis().SetLabelSize(xLabelSize)
      hr.GetYaxis().SetLabelSize(yLabelSize)
      hr.GetXaxis().SetTitleSize(xTitleSize)
      hr.GetYaxis().SetTitleSize(yTitleSize)
      # hr.SetTitleSize(titleSize)
      hr.GetYaxis().SetTitleOffset(0.55)
      hr.GetXaxis().SetTitleOffset(0.95)
      hr.SetMinimum(-11)
      hr.SetMaximum(+11)
      
      tvp_hists.SetBottomMargin(0)
      tvp_ratio.SetTopMargin(0)
      tvp_ratio.SetBottomMargin(0.20)
      
      leg = TLegend(0.5,0.47,0.87,0.9,"","brNDC")
      leg.SetFillStyle(4000) # will be transparent
      leg.SetFillColor(0)
      leg.SetTextFont(42)
      leg.SetBorderSize(0)
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "")
      leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets (resolved)", "")
      leg.AddEntry(0, level, "")
      leg.AddEntry(self.histos[nameXX],"|SM+#it{"+nameX+"}|^{2} reweighted","ple")
      leg.AddEntry(self.histos[nameSM],"|SM|^{2}","ple")
      leg.AddEntry(0, "tan#beta="+stanb, "")
      leg.AddEntry(0, "sin(#beta-#alpha)=1", "")
      leg.AddEntry(0, "#it{m}_{#it{"+nameX+"}}="+str(mX)+" GeV", "")
      leg.AddEntry(0, "#Gamma_{#it{"+nameX+"}}="+'%.4f' % wX+"%", "")

      tvp_hists.cd()
      ymax = -1
      for b in range(1,self.histos[nameXX].GetNbinsX()+1):
         y = self.histos[nameXX].GetBinContent(b)+self.histos[nameXX].GetBinError(b) 
         if(y>ymax): ymax = y
      self.histos[nameSM].SetMaximum(ymax*1.05)
      self.histos[nameSM].SetMinimum(0.1)
      self.histos[nameXX].SetMaximum(ymax*1.05)
      self.histos[nameXX].SetMinimum(0.1)
      self.histos[nameXX].Draw()
      self.histos[nameSM].Draw("same")
      leg.Draw("same")
      tvp_hists.Update()
      tvp_hists.RedrawAxis()
      
      tvp_ratio.cd()
      tvp_ratio.SetGridy()
      hr.Draw("e1p")
      tvp_ratio.Update()
      tvp_ratio.RedrawAxis()
      
      cnv.Update()
      cnv.SaveAs(fname)
   
   def writeHistos(self,name):
      hfile = TFile(name)
      hfile.cd()
      for h in self.histos.values():
         h.SetDirectory(hfile)
         h.Write()
      hfile.Write()
      hfile.Close()
   
   def bookHistos(self):
      self.addHist1N("TopTag:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":"         ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGray+2,24)
      self.addHist1N("HarProcessTops:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":" ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGreen+1,24)

      self.addHist1N("TopTag:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":IX:"         ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGray+2,20)
      self.addHist1N("HarProcessTops:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":IX:" ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGreen+1,20)
      
      self.addHist1("HarProcessTops:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",       40,350,1350, ROOT.kAzure,20)
      self.addHist1("HarProcessTops:pTlep", ";First hard-process p_{T}(#it{t}_{lep}) [GeV];Events", 40,50,550,   ROOT.kAzure,20)
      self.addHist1("HarProcessTops:pThad", ";Second hard-process p_{T}(#it{t}_{had}) [GeV];Events",40,50,550,   ROOT.kAzure,20)
      
      self.addHist1("Muons:Mult", ";Muon multiplicity;Events",5,0,5)
      self.addHist1("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,30,530)
      self.addHist1("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,30,530)
      self.addHist1("Muons:MWT",  ";MWT(lep) [GeV];Events",50,0,150)
      
      self.addHist1("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
      self.addHist1("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,30,530)
      self.addHist1("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,30,530)
      self.addHist1("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,150)
      
      self.addHist1("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
      self.addHist1("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,30,630)
      
      self.addHist1("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
      self.addHist1("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,30,630)
      self.addHist1("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,30,630)
      
      self.addHist1("ETmiss:eT",     ";#it{E}_{T}^{miss} [GeV];Events",50,0,630)
      
      self.addHist1("ETmiss:dPhiMuons",     ";#Delta#phi(#it{E}_{T}^{miss},Muon);Events",32,0,ROOT.TMath.Pi())
      self.addHist1("ETmiss:dPhiElectrons", ";#Delta#phi(#it{E}_{T}^{miss},Electron);Events",32,0,ROOT.TMath.Pi())
      self.addHist1("ETmiss:dPhiJets",      ";#Delta#phi(#it{E}_{T}^{miss},Jet);Events",32,0,ROOT.TMath.Pi())
      self.addHist1("ETmiss:dPhiBjets",     ";#Delta#phi(#it{E}_{T}^{miss},Bjet);Events",32,0,ROOT.TMath.Pi())
      
      self.addHist1("Muons:dRJets",      ";#DeltaR(Muon,Jet);Events",35,0,7)
      self.addHist1("Muons:dRBjets",     ";#DeltaR(Muon,Bjet);Events",35,0,7)
      
      self.addHist1("Electrons:dRJets",  ";#DeltaR(Electrons,Jet);Events",35,0,7)
      self.addHist1("Electrons:dRBjets", ";#DeltaR(Electrons,Bjet);Events",35,0,7)
      
      self.addHist1("Jets:dRBjets", ";#DeltaR(Jet,Bjet);Events",35,0,7)
      
      self.addHist1("Jets:dR12", ";#DeltaR(Jet1,Jet2);Events",35,0,7)
      self.addHist1("BJets:dR12", ";#DeltaR(Bjet1,Bjet2);Events",35,0,7)
      
      self.addHist1("Jets:mjj",  ";#it{m}(Jet1,Jet2) [GeV];Events",50,0,150)
      
      self.addHist1("Top:mjjb", ";#it{m}(Jet1,Jet2,Bjet) [GeV];Events",50,50,350)
      self.addHist1("Top:mwb",  ";#it{m}(Lepton,Bjet,#it{E}_{T}^{miss}) [GeV];Events",50,0,150)
      
      self.addHist1("TopTag:mwHad",  ";#it{m}(#it{W}_{had}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mTw", ";#it{m}_{T}(#it{W}_{lep}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mLw", ";#it{m}(#it{W}_{lep}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mLw0", ";#it{m}(#it{W}_{lep0}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mLw1", ";#it{m}(#it{W}_{lep1}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mLw2", ";#it{m}(#it{W}_{lep2}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mtHad",  ";#it{m}(#it{t}_{had}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mTt", ";#it{m}_{T}(#it{t}_{lep}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mLt", ";#it{m}(#it{t}_{lep}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mLt0",  ";#it{m}(#it{t}_{lep0}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mLt1",  ";#it{m}(#it{t}_{lep1}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mLt2",  ";#it{m}(#it{t}_{lep2}) [GeV];Events",50,50,350)
      
      self.addHist1("TopTag:dRLw12", ";#DeltaR(#it{W}_{lep1}^{rec},#it{W}_{lep2}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRLt12", ";#DeltaR(#it{t}_{lep1}^{rec},#it{t}_{lep2}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRlep0had", ";#DeltaR(#it{t}_{lep0}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRlep1had", ";#DeltaR(#it{t}_{lep1}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRlep2had", ";#DeltaR(#it{t}_{lep2}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      
      self.addHist1("HarProcessTops:dRlepT", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lepT}^{rec});Events",35,0,7)
      self.addHist1("HarProcessTops:dRlep", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",35,0,7)
      self.addHist1("HarProcessTops:dRlep0", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep0}^{rec});Events",35,0,7)
      self.addHist1("HarProcessTops:dRlep1", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep1}^{rec});Events",35,0,7)
      self.addHist1("HarProcessTops:dRlep2", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep2}^{rec});Events",35,0,7)
      self.addHist1("HarProcessTops:dRhad", ";#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",35,0,7)
      
      self.addHist1("HarProcessTops:dpTRellepT", ";#it{t}_{lepT}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dpTRellep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dpTRellep0", ";#it{t}_{lep0}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dpTRellep1", ";#it{t}_{lep1}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dpTRellep2", ";#it{t}_{lep2}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dpTRelhad", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,5)
      
      self.addHist1("TopTag:pTtTLep", ";#it{p}_{T}(#it{t}_{lepT}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtLep", ";#it{p}_{T}(#it{t}_{lep}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtLep0", ";#it{p}_{T}(#it{t}_{lep0}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtLep1", ";#it{p}_{T}(#it{t}_{lep1}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtLep2", ";#it{p}_{T}(#it{t}_{lep2}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtHad", ";#it{p}_{T}(#it{t}_{had}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:dRlepThad", ";#DeltaR(#it{t}_{lepT}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRlephad", ";#DeltaR(#it{t}_{lep}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:mTtt", ";#it{m}_{T}(#it{t}_{had}, #it{t}_{lepT}) [GeV];Events",40,350,1350)
      self.addHist1("TopTag:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350)
      self.addHist1("TopTag:mtt0", ";#it{m}(#it{t}_{had}, #it{t}_{lep0}) [GeV];Events",40,350,1350)
      self.addHist1("TopTag:mtt1", ";#it{m}(#it{t}_{had}, #it{t}_{lep1}) [GeV];Events",40,350,1350)
      self.addHist1("TopTag:mtt2", ";#it{m}(#it{t}_{had}, #it{t}_{lep2}) [GeV];Events",40,350,1350)
      
      self.addHist1("HarProcessTops:dmRellepT", ";#it{t}_{lepT}: #it{m}_{T}^{rec}(#it{t}_{had}, #it{t}_{lepT})/#it{m}^{tru}(#it{t}_{had}, #it{t}_{lepT})-1;Events",50,-1,5)
      self.addHist1("HarProcessTops:dmRellep", ";#it{t}_{lep}: #it{m}^{rec}(#it{t}_{had}, #it{t}_{lep})/#it{m}^{tru}(#it{t}_{had}, #it{t}_{lep})-1;Events",50,-1,5)
      
      self.addHist2("HarProcessTops:dpTRel:dRtru:had", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",100,0,5, 100,-1,5)
      self.addHist2("HarProcessTops:dpTRel:dRtru:lepT", ";#it{t}_{lepT}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lepT}^{rec});Events",100,0,5, 100,-1,5)
      self.addHist2("HarProcessTops:dpTRel:dRtru:lep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",100,0,5, 100,-1,5)