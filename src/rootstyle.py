#!/usr/bin/python

import ROOT
from ROOT import gROOT, gStyle

def setStyle():
   gROOT.Reset()
   icol=0;  # WHITE
   font=42; # Helvetica
   tsize=0.05;
   gStyle.SetFrameBorderMode(icol);
   gStyle.SetFrameFillColor(icol);
   gStyle.SetCanvasBorderMode(icol);
   gStyle.SetCanvasColor(icol);
   gStyle.SetPadBorderMode(icol);
   gStyle.SetPadColor(icol);
   gStyle.SetStatColor(icol);
   gStyle.SetPaperSize(20,26);
   gStyle.SetPadTopMargin(0.05);
   gStyle.SetPadRightMargin(0.08);
   gStyle.SetPadBottomMargin(0.15);
   gStyle.SetPadLeftMargin(0.12);
   gStyle.SetTitleXOffset(1.05);
   gStyle.SetTitleYOffset(0.95);
   gStyle.SetTextFont(font);
   gStyle.SetTextSize(tsize);
   gStyle.SetLabelFont(font,"x");
   gStyle.SetTitleFont(font,"x");
   gStyle.SetLabelFont(font,"y");
   gStyle.SetTitleFont(font,"y");
   gStyle.SetLabelFont(font,"z");
   gStyle.SetTitleFont(font,"z");
   gStyle.SetLabelSize(tsize*0.85,"x");
   gStyle.SetTitleSize(tsize*1.10,"x");
   gStyle.SetLabelSize(tsize*0.85,"y");
   gStyle.SetTitleSize(tsize*1.10,"y");
   gStyle.SetLabelSize(tsize*0.85,"z");
   gStyle.SetTitleSize(tsize*1.10,"z");
   gStyle.SetMarkerStyle(20);
   gStyle.SetMarkerSize(0.8);
   gStyle.SetHistLineWidth(2);
   gStyle.SetLineStyleString(2,"[12 12]"); # postscript dashes
   gStyle.SetEndErrorSize(0.);
   # gStyle.SetOptTitle(0);
   gStyle.SetOptStat(0);
   gStyle.SetOptFit(0);
   gStyle.SetPadTickX(1);
   gStyle.SetPadTickY(1);
