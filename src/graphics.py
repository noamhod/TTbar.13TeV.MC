#!/usr/bin/python
import ROOT
from ROOT import std, gROOT, gStyle, gPad, gDirectory, TCanvas, TH1, TH1D, TH2D, TLegend, TLine, TFile, TVirtualPad, TDirectory
import os
import math


class Graphics:
   'Class for ttbar jets selection'

   def __init__(self,legtxt1,legtxt2=""):
      self.legtxt1 = legtxt1
      self.legtxt2 = legtxt2
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
   
   
   def plotHist(self,fname,name,logy=False,legtxt=""):
      cnv = TCanvas(name,"",600,600)
      cnv.Draw()
      cnv.cd()
      if(logy): cnv.SetLogy()
      self.histos[name].Draw()
      leg = TLegend(0.5,0.70,0.87,0.9,"","brNDC");
      leg.SetFillStyle(4000); # will be transparent
      leg.SetFillColor(0);
      leg.SetTextFont(42);
      leg.SetBorderSize(0);
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
      # leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
      leg.AddEntry(0, "#it{gg}#rightarrow#it{t}#bar{#it{t}}#rightarrow"+self.legtxt1, "");
      # leg.AddEntry(0, "Resolved selection", "");
      if(self.legtxt2!=""): leg.AddEntry(0, self.legtxt2, "");
      if(legtxt==""): leg.AddEntry(self.histos[name],"Reconstructed tops","ple");
      else:           leg.AddEntry(self.histos[name],legtxt,"ple");
      leg.Draw("same")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
   
   def plotHist2(self,fname,name1,name2,logy=False):
      cnv = TCanvas(name1,"",600,600)
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
      cnv = TCanvas(name1,"",600,600)
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
      cnv = TCanvas(name,"",800,600)
      cnv.Draw()
      cnv.cd()
      if(logz): cnv.SetLogz()
      self.histos[name].Draw("colz")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
      gStyle.SetPadRightMargin(0.08)

   def plotRatio(self,fname,level,nameSM,nameXX,nameIX,wX,stanb,ssinba,nameX,mX):
      cnv = TCanvas(nameXX,"",600,600)
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
      self.histos[nameXX].SetMarkerSize(0.6)
      self.histos[nameXX].SetMarkerColor(ROOT.kRed)
      self.histos[nameXX].SetLineColor(ROOT.kRed)
      self.histos[nameXX].SetLineStyle(1)
      self.histos[nameXX].SetLineWidth(2)

      self.histos[nameSM].SetMarkerStyle(24)
      self.histos[nameSM].SetMarkerSize(0.6)
      self.histos[nameSM].SetMarkerColor(ROOT.kBlack)
      self.histos[nameSM].SetLineColor(ROOT.kBlack)
      self.histos[nameSM].SetLineStyle(1)
      self.histos[nameSM].SetLineWidth(2)
      
      hr = self.histos[nameIX].Clone("ratio")
      hr.Sumw2()
      hr.SetTitle(";"+sXtitle+";|SM+#it{"+nameX+"}|^{2}/|SM|^{2}-1 [%]")
      hr.Divide(self.histos[nameIX],self.histos[nameSM],100.,1.) ### to have the interference shape relative to the SM shape in percentage
      hr.SetMarkerStyle(20)
      hr.SetMarkerSize(0.6)
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
      leg.AddEntry(0, "sin(#beta-#alpha)="+ssinba, "")
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

   def plotHistNorm2(self,fname,name1,name2,logy=False):
      cnv = TCanvas(name1,"",600,600)
      cnv.Draw()
      cnv.cd()
      if(logy): cnv.SetLogy()
      self.histos[name1].SetMinimum(0)
      self.histos[name2].SetMinimum(0)
      int1 = self.histos[name1].Integral()
      max1 = self.histos[name1].GetMaximum()
      int2 = self.histos[name2].Integral()
      max2 = self.histos[name2].GetMaximum()
      if(max2/int2>max1/int1):
         self.histos[name2].DrawNormalized()
         self.histos[name1].DrawNormalized("same")
      else:
         self.histos[name1].DrawNormalized()
         self.histos[name2].DrawNormalized("same")
      leg = TLegend(0.5,0.60,0.87,0.9,"","brNDC");
      leg.SetFillStyle(4000); # will be transparent
      leg.SetFillColor(0);
      leg.SetTextFont(42);
      leg.SetBorderSize(0);
      leg.AddEntry(0, "MadGraph+Pythia8 (OTF)", "");
      leg.AddEntry(0, "#it{pp}#rightarrow#it{t}#bar{#it{t}}#rightarrow#mu+jets", "");
      leg.AddEntry(0, "Resolved selection", "");
      leg.AddEntry(self.histos[name1],"gg production","ple");
      leg.AddEntry(self.histos[name2],"q#bar{q} production","ple");
      leg.Draw("same")
      cnv.Update()
      cnv.RedrawAxis()
      cnv.SaveAs(fname)
   
   def writeHistos(self,name):
      hfile = TFile(name,"RECREATE")
      hfile.cd()
      for h in self.histos.values():
         h.SetDirectory(hfile)
         h.Write()
      hfile.Write()
      hfile.Close()
   
   def bookHistos(self):
      self.addHist1N("TopTag:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":"         ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGray+2,24)
      self.addHist1N("HardProcessTops:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":" ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGreen+1,24)

      self.addHist1N("TopTag:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":IX:"         ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGray+2,20)
      self.addHist1N("HardProcessTops:2HDM::mtt:"+self.ModelName+":"+self.ModelMass+":IX:" ,";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350,ROOT.kGreen+1,20)
      
      self.addHist1("HardProcessTops:mtt", ";#it{m}(#it{t}_{had}#it{t}_{lep}) [GeV];Events", 40,350,1350, ROOT.kAzure,20)
      self.addHist1("HardProcessTops:pTtLep", ";p_{T}(#it{t}_{lep}) [GeV];Events", 40,50,550,  ROOT.kAzure,20)
      self.addHist1("HardProcessTops:pTtHad", ";p_{T}(#it{t}_{had}) [GeV];Events",40,50,550,   ROOT.kAzure,20)
      
      self.addHist1("Muons:Mult", ";Muon multiplicity;Events",5,0,5)
      self.addHist1("Muons:pT1",  ";Leading muon p_{T} [GeV];Events",50,0,500)
      self.addHist1("Muons:pT2",  ";Subeading muon p_{T} [GeV];Events",50,0,500)
      self.addHist1("Muons:MWT",  ";MWT(lep) [GeV];Events",50,0,150)
      
      self.addHist1("Electrons:Mult", ";Electron multiplicity;Events",5,0,5)
      self.addHist1("Electrons:pT1",  ";Leading electron p_{T} [GeV];Events",50,0,500)
      self.addHist1("Electrons:pT2",  ";Subeading electron p_{T} [GeV];Events",50,0,500)
      self.addHist1("Electrons:MWT",  ";MWT (Electron) [GeV];Events",50,0,150)
      
      self.addHist1("Jets:Mult", ";Jet multiplicity;Events",15,0,15)
      self.addHist1("Jets:pT1",  ";First jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:pT2",  ";Second jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:pT3",  ";Third jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:pT4",  ";Forth jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:pT5",  ";Fifth jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:pT6",  ";Sixth jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("Jets:m1",  ";First jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:m2",  ";Second jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:m3",  ";Third jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:m4",  ";Forth jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:m5",  ";Fifth jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:m6",  ";Sixth jet mass [GeV];Events",50,0,200)
      self.addHist1("Jets:ht",  ";Jets #it{H}_{T} [GeV];Events",100,0,1500)
      
      self.addHist1("BJets:Mult", ";B Jet multiplicity;Events",5,0,5)
      self.addHist1("BJets:pT1",  ";First B jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("BJets:pT2",  ";Second B jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("BJets:pT3",  ";Third B jet p_{T} [GeV];Events",50,0,600)
      self.addHist1("BJets:pT4",  ";Forth B jet p_{T} [GeV];Events",50,0,600)
      
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
      
      self.addHist1("TopTag:mwH",  ";#it{m}(#it{W}_{had}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mTw", ";#it{m}_{T}(#it{W}_{lep}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mwL", ";#it{m}(#it{W}_{lep}) [GeV];Events",50,0,150)
      self.addHist1("TopTag:mtH",  ";#it{m}(#it{t}_{had}) [GeV];Events",50,50,350)
      self.addHist1("TopTag:mtL", ";#it{m}(#it{t}_{lep}) [GeV];Events",50,50,350)
      
      self.addHist1("HardProcessTops:dRlep", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});Events",35,0,7)
      self.addHist1("HardProcessTops:dRhad", ";#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});Events",35,0,7)
      
      self.addHist1("HardProcessTops:dpTRellep", ";#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,+2)
      self.addHist1("HardProcessTops:dpTRelhad", ";#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",50,-1,+2)
      
      self.addHist1("TopTag:pTtTLep", ";#it{p}_{T}(#it{t}_{lepT}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtLep", ";#it{p}_{T}(#it{t}_{lep}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:pTtHad", ";#it{p}_{T}(#it{t}_{had}) [GeV];Events",40,50,550)
      self.addHist1("TopTag:dRlepThad", ";#DeltaR(#it{t}_{lepT}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:dRlephad", ";#DeltaR(#it{t}_{lep}^{rec},#it{t}_{had}^{rec});Events",35,0,7)
      self.addHist1("TopTag:mtt", ";#it{m}(#it{t}_{had}, #it{t}_{lep}) [GeV];Events",40,350,1350)
      
      self.addHist1("HardProcessTops:dmRel", ";#it{t}_{lep}: #it{m}^{rec}(#it{t}_{had}, #it{t}_{lep})/#it{m}^{tru}(#it{t}_{had}, #it{t}_{lep})-1;Events",50,-2,+2)
      
      self.addHist2("HardProcessTops:dpTRel:dRtru:had", ";#DeltaR(#it{t}_{had}^{tru},#it{t}_{had}^{rec});#it{t}_{had}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",100,0,5, 100,-1,+2)
      self.addHist2("HardProcessTops:dpTRel:dRtru:lep", ";#DeltaR(#it{t}_{lep}^{tru},#it{t}_{lep}^{rec});#it{t}_{lep}: #it{p}_{T}^{rec}/#it{p}_{T}^{tru}-1;Events",100,0,5, 100,-1,+2)

      self.addHist1("Matching:dR:mu", ";#DeltaR(lep_{tru},lep_{rec}^{selected});Events",35,0,7)
      self.addHist1("Matching:dR:nu", ";#DeltaR(#nu_{tru},#nu_{rec}^{selected});Events",35,0,7)
      self.addHist1("Matching:dR:bL",  ";#DeltaR(bL_{tru},b_{rec}^{selected});Events",35,0,7)
      self.addHist1("Matching:dR:q", ";#DeltaR(q_{tru},j_{rec}^{selected});Events",35,0,7)
      self.addHist1("Matching:dR:qbar", ";#DeltaR(#bar{q}_{tru},j_{rec}^{selected});Events",35,0,7)
      self.addHist1("Matching:dR:bH", ";#DeltaR(bH_{tru},b_{rec}^{selected});Events",35,0,7)
      self.addHist1("BestMatching:dR:mu", ";#DeltaR(lep_{tru},lep_{rec}^{best});Events",35,0,7)
      self.addHist1("BestMatching:dR:nu", ";#DeltaR(#nu_{tru},#nu_{rec}^{best});Events",32,0,ROOT.TMath.Pi())
      self.addHist1("BestMatching:dR:bL",  ";#DeltaR(bL_{tru},b_{rec}^{best});Events",35,0,7)
      self.addHist1("BestMatching:dR:q", ";#DeltaR(q_{tru},j_{rec}^{best});Events",35,0,7)
      self.addHist1("BestMatching:dR:qbar", ";#DeltaR(#bar{q}_{tru},j_{rec}^{best});Events",35,0,7)
      self.addHist1("BestMatching:dR:bH", ";#DeltaR(bH_{tru},b_{rec}^{best});Events",35,0,7)

      self.addHist1N("Matched:NoSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350,ROOT.kRed,24)
      self.addHist1N("Matched:NoSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,  ROOT.kRed,24)
      self.addHist1N("Matched:NoSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,  ROOT.kRed,24)
      self.addHist1N("Matched:NoSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350,ROOT.kRed,24)
      self.addHist1N("Matched:NoSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,  ROOT.kRed,24)
      self.addHist1N("Matched:NoSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,  ROOT.kRed,24)
      self.addHist1("Matched:NoSelection:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5, ROOT.kGray+2,20)
      self.addHist1("Matched:NoSelection:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5, ROOT.kGray+2,20)

      self.addHist1N("Matched:WithSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("Matched:WithSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:WithSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:WithSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("Matched:WithSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:WithSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1("Matched:WithSelection:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5, ROOT.kSpring-6,20)
      self.addHist1("Matched:WithSelection:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5, ROOT.kSpring-6,20)

      self.addHist1N("Matched:SelectedObjects:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("Matched:SelectedObjects:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:SelectedObjects:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:SelectedObjects:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("Matched:SelectedObjects:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("Matched:SelectedObjects:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1("Matched:SelectedObjects:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350)
      self.addHist1("Matched:SelectedObjects:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120)
      self.addHist1("Matched:SelectedObjects:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50)
      self.addHist1("Matched:SelectedObjects:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220)
      self.addHist1("Matched:SelectedObjects:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50)
      self.addHist1("Matched:SelectedObjects:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130)
      self.addHist1("Matched:SelectedObjects:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50)
      self.addHist1("Matched:SelectedObjects:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220)
      self.addHist1("Matched:SelectedObjects:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50)
      self.addHist1("Matched:SelectedObjects:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250)
      self.addHist1("Matched:SelectedObjects:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500)
      self.addHist1("Matched:SelectedObjects:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500)
      self.addHist1("Matched:SelectedObjects:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120)
      self.addHist1("Matched:SelectedObjects:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2)
      self.addHist1("Matched:SelectedObjects:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5)
      self.addHist1("Matched:SelectedObjects:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5)

      self.addHist1N("All:SelectedObjects:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("All:SelectedObjects:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("All:SelectedObjects:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("All:SelectedObjects:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("All:SelectedObjects:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("All:SelectedObjects:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1("All:SelectedObjects:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350)
      self.addHist1("All:SelectedObjects:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120)
      self.addHist1("All:SelectedObjects:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50)
      self.addHist1("All:SelectedObjects:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220)
      self.addHist1("All:SelectedObjects:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50)
      self.addHist1("All:SelectedObjects:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130)
      self.addHist1("All:SelectedObjects:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50)
      self.addHist1("All:SelectedObjects:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220)
      self.addHist1("All:SelectedObjects:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50)
      self.addHist1("All:SelectedObjects:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250)
      self.addHist1("All:SelectedObjects:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500)
      self.addHist1("All:SelectedObjects:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500)
      self.addHist1("All:SelectedObjects:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120)
      self.addHist1("All:SelectedObjects:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2)
      self.addHist1("All:SelectedObjects:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5)
      self.addHist1("All:SelectedObjects:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5)


      self.addHist1N("HardProcess:NoSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("HardProcess:NoSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:NoSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:NoSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("HardProcess:NoSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:NoSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1("HardProcess:NoSelection:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5, ROOT.kOrange+7,20)
      self.addHist1("HardProcess:NoSelection:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5, ROOT.kOrange+7,20)

      self.addHist1N("HardProcess:WithSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("HardProcess:WithSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:WithSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:WithSelection:mjjjlvj:"+self.ModelName+":"+self.ModelMass+":IX:", ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kRed,24)
      self.addHist1N("HardProcess:WithSelection:pTjjj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1N("HardProcess:WithSelection:pTlvj:"  +self.ModelName+":"+self.ModelMass+":IX:", ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500,   ROOT.kRed,24)
      self.addHist1("HardProcess:WithSelection:mjjjlvj",          ";#it{m}_{jjjlvj} [GeV];Events",100,350,1350, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjj",              ";#it{m}_{jj} [GeV];Events",100,50,120, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjj-mW",           ";#it{m}_{jj}-#it{m}_{#it{W}} [GeV];Events",100,-50,+50, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjjj",             ";#it{m}_{jjj} [GeV];Events",100,120,220, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjjj-mt",          ";#it{m}_{jjj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjjj-mjj",         ";#it{m}_{jjj}-#it{m}_{jj} [GeV];Events",100,30,130, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mjjj-mjj-(mt-mW)", ";#it{m}_{jjj}-#it{m}_{jj}-(#it{m}_{#it{t}}-#it{m}_{#it{W}}) [GeV];Events",100,-50,+50, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mlvj",             ";#it{m}_{lvj} [GeV];Events",100,120,220, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:mlvj-mt",          ";#it{m}_{lvj}-#it{m}_{#it{t}} [GeV];Events",100,-50,+50, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:pTjjjlvj",         ";#it{p}_{T}^{jjjlvj} [GeV];Events",100,0,250, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:pTjjj",            ";#it{p}_{T}^{jjj} [GeV];Events",100,0,500, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:pTlvj",            ";#it{p}_{T}^{lvj} [GeV];Events",100,0,500, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:pTjjj-pTlvj",      ";#it{p}_{T}^{jjj}-#it{p}_{T}^{lvj} [GeV];Events",100,-120,+120, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:dRlephad",         ";#DeltaR(jjj,lvj);Events",100,1,5.2, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:dRwbhad",          ";#DeltaR(jj,b_{had}^{notag});Events",100,0,5, ROOT.kAzure,20)
      self.addHist1("HardProcess:WithSelection:dRwblep",          ";#DeltaR(lv,b_{lep}^{notag});Events",100,0,5, ROOT.kAzure,20)


      self.addHist1("HardProcess:qq:mtt",";#it{m}_{t#bar{t}} [GeV];Events",100,350,1350, ROOT.kAzure,20)
      self.addHist1("HardProcess:qq:pTt",";#it{p}_{T}^{t} [GeV];Events",100,0,500, ROOT.kAzure,20)
      self.addHist1("HardProcess:qq:pTtbar",";#it{p}_{T}^{#bar{t}} [GeV];Events",100,0,500, ROOT.kAzure,20)
      self.addHist1("HardProcess:qq:etat",";#eta_{t};Events",100,-5,+5, ROOT.kAzure,20)
      self.addHist1("HardProcess:qq:etatbar",";#eta_{#bar{t}};Events",100,-5,+5, ROOT.kAzure,20)
      self.addHist1("HardProcess:qq:x",      ";#it{x};Events",100,0,+1, ROOT.kAzure,20)

      self.addHist1("HardProcess:gg:mtt",";#it{m}_{t#bar{t}} [GeV];Events",100,350,1350, ROOT.kBlack,20)
      self.addHist1("HardProcess:gg:pTt",";#it{p}_{T}^{t} [GeV];Events",100,0,500, ROOT.kBlack,20)
      self.addHist1("HardProcess:gg:pTtbar",";#it{p}_{T}^{#bar{t}} [GeV];Events",100,0,500, ROOT.kBlack,20)
      self.addHist1("HardProcess:gg:etat",";#eta_{t};Events",100,-5,+5, ROOT.kBlack,20)
      self.addHist1("HardProcess:gg:etatbar",";#eta_{#bar{t}};Events",100,-5,+5, ROOT.kBlack,20)
      self.addHist1("HardProcess:gg:x",      ";#it{x};Events",100,0,+1, ROOT.kBlack,20)
      
