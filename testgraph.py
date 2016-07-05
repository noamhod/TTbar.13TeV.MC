#!/usr/bin/python

import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import sys
sys.path.append("/usr/local/Cellar/graphviz/2.38.0/lib/")
sys.path.append("/Users/hod/GitHub/TTbar.13TeV.MC/src")
import graphviz
import uuid
import ROOT
from ROOT import *
import rootstyle
import graphs

ROOT.gROOT.SetBatch(1)
rootstyle.setStyle()


colors = []
def setcolor(st):
   if  (st<20):            colors.append("orange")
   elif(st==21):           colors.append("red")
   elif(st==22):           colors.append("yellow")
   elif(st==23):           colors.append("green")
   elif(st>=30 and st<40): colors.append("cyan")
   elif(st>=40 and st<50): colors.append("violet")
   elif(st>=50 and st<60): colors.append("pink")
   elif(st>=60 and st<70): colors.append("grey")
   else:         colors.append("white")

paticles = [2212,1,2,3,4,5,6,11,12,13,14,15,16,21,22,23,24]

hProd = TH1D("hProd",";;Fraction [%]",3,0,3)
hProd.GetXaxis().SetBinLabel(1,"gg")
hProd.GetXaxis().SetBinLabel(2,"gq")
hProd.GetXaxis().SetBinLabel(3,"qq")

hggFinal = TH1D("hggFinal",";;Fraction [%]",5,0,5)
hggFinal.GetXaxis().SetBinLabel(1,"t#bar{t}")
hggFinal.GetXaxis().SetBinLabel(2,"t#bar{t}+g")
hggFinal.GetXaxis().SetBinLabel(3,"t#bar{t}+gg")
hggFinal.GetXaxis().SetBinLabel(4,"t#bar{t}+gq")
hggFinal.GetXaxis().SetBinLabel(5,"t#bar{t}+qq")

hgqFinal = TH1D("hgqFinal",";;Fraction [%]",5,0,5)
hgqFinal.GetXaxis().SetBinLabel(1,"t#bar{t}")
hgqFinal.GetXaxis().SetBinLabel(2,"t#bar{t}+g")
hgqFinal.GetXaxis().SetBinLabel(3,"t#bar{t}+gg")
hgqFinal.GetXaxis().SetBinLabel(4,"t#bar{t}+gq")
hgqFinal.GetXaxis().SetBinLabel(5,"t#bar{t}+qq")

hqqFinal = TH1D("hqqFinal",";;Fraction [%]",5,0,5)
hqqFinal.GetXaxis().SetBinLabel(1,"t#bar{t}")
hqqFinal.GetXaxis().SetBinLabel(2,"t#bar{t}+g")
hqqFinal.GetXaxis().SetBinLabel(3,"t#bar{t}+gg")
hqqFinal.GetXaxis().SetBinLabel(4,"t#bar{t}+gq")
hqqFinal.GetXaxis().SetBinLabel(5,"t#bar{t}+qq")


for i in xrange(100): #xrange(len(graphs.events)):

   ##################
   maxstatus = 80 ###
   maxdepth = 1e5 ###
   ##################

   label = graphs.events[i][1]["evt"] ## there should always be barcode=1 or 2 for the protons
   hStatuses = TH2D("hStatuses "+label,";status;pdgId",maxstatus,0,maxstatus, 30,0,30)

   G = nx.DiGraph()
   # G = nx.MultiGraph()
   # G = nx.Graph()
   entries = {}
   nlabels = {}
   counters = {21:0, 22:0, 23:0, 1:0}
   depth = 0
 
   bct1 = -1
   bct2 = -1

   for barcode, properties in graphs.events[i].iteritems():

      if(properties["pdgId"]==+6 and (properties["status"]==22 or properties["status"]==23) and len(properties["parentsbc"])>1): bct1 = barcode
      if(properties["pdgId"]==-6 and (properties["status"]==22 or properties["status"]==23) and len(properties["parentsbc"])>1): bct2 = barcode

      # if(abs(properties["pdgId"]) not in paticles): continue
      # if(properties["status"]>maxstatus):           continue
   
      # print "[%i] id=%i, st=%i" % (barcode, properties["pdgId"],properties["status"])
      # print "\t parents:  ",properties["parentsbc"]
      # print "\t children: ",properties["childrenbc"]
   
      if(properties["status"]==1):  counters[1]  += 1
      if(properties["status"]==21): counters[21] += 1
      if(properties["status"]==22): counters[22] += 1
      if(properties["status"]==23): counters[23] += 1
   
      G.add_node(barcode,pdgid=properties["pdgId"],status=properties["status"])
      nlabels.update({barcode:properties["pdgId"]})

      hStatuses.Fill(properties["status"],properties["pdgId"])
   
      for childbc,childid in properties["childrenbc"].iteritems():
         if(childbc not in nlabels.keys()):
            G.add_node(childbc,pdgid=childid,status=graphs.events[i][childbc]["status"])
            nlabels.update({childbc:childid})
         G.add_edge(barcode,childbc)

      for parentbc,parentid in properties["parentsbc"].iteritems():
         if(parentbc not in nlabels.keys()):
            G.add_node(parentbc,pdgid=parentid,status=graphs.events[i][parentbc]["status"])
            nlabels.update({parentbc:parentid})
         G.add_edge(parentbc,barcode)
   
      if(depth>=maxdepth): break
      depth += 1
   
   ### simple analysis - production and sisters
   ng1 = 0
   ng2 = 0
   nq1 = 0
   nq2 = 0
   bcsisters1 = []
   bcsisters2 = []
   for parentbc,parentid in graphs.events[i][bct1]["parentsbc"].iteritems():
      parentstatus = graphs.events[i][parentbc]["status"]
      if(parentid==21):
         if(parentstatus==21 or parentstatus==22):
            ng1 += 1
            for childbc,childid in graphs.events[i][parentbc]["childrenbc"].iteritems():
               if(abs(childid)==6): continue
               if(childbc in bcsisters1): continue
               bcsisters1.append(childbc)
      if(abs(parentid)<6):
         if(parentstatus==21 or parentstatus==22):
            nq1 += 1
            for childbc,childid in graphs.events[i][parentbc]["childrenbc"].iteritems():
               if(abs(childid)==6): continue
               if(childbc in bcsisters1): continue
               bcsisters1.append(childbc)
   for parentbc,parentid in graphs.events[i][bct2]["parentsbc"].iteritems():
      parentstatus = graphs.events[i][parentbc]["status"]
      if(parentid==21):
         if(parentstatus==21 or parentstatus==22):
             ng2 += 1
             for childbc,childid in graphs.events[i][parentbc]["childrenbc"].iteritems():
               if(abs(childid)==6): continue
               if(childbc in bcsisters2): continue
               bcsisters2.append(childbc)
      if(abs(parentid)<6):
         if(parentstatus==21 or parentstatus==22):
            nq2 += 1
            for childbc,childid in graphs.events[i][parentbc]["childrenbc"].iteritems():
               if(abs(childid)==6): continue
               if(childbc in bcsisters2): continue
               bcsisters2.append(childbc)
   ng = 0
   nq = 0
   for bcsister1 in bcsisters1:
      if(graphs.events[i][bcsister1]["pdgId"]==21):    ng += 1
      if(abs(graphs.events[i][bcsister1]["pdgId"])<6): nq += 1
      for bcsister2 in bcsisters2:
         if(bcsister2 in bcsisters1): continue
         if(graphs.events[i][bcsister2]["pdgId"]==21):    ng += 1
         if(abs(graphs.events[i][bcsister2]["pdgId"])<6): nq += 1
   if((ng1+ng2)==4 and (nq1+nq2)==0):   ### gg productuion
      hProd.Fill(0.5)
      if(ng==0 and nq==0): hggFinal.Fill(0.5)
      if(ng==1 and nq==0): hggFinal.Fill(1.5)
      if(ng==2 and nq==0): hggFinal.Fill(2.5)
      if(ng==1 and nq==1): hggFinal.Fill(3.5)
      if(ng==0 and nq==2): hggFinal.Fill(4.5)
   elif((ng1+ng2)==2 and (nq1+nq2)==2): ### gq productuion
      hProd.Fill(1.5)
      if(ng==0 and nq==0): hgqFinal.Fill(0.5)
      if(ng==1 and nq==0): hgqFinal.Fill(1.5)
      if(ng==2 and nq==0): hgqFinal.Fill(2.5)
      if(ng==1 and nq==1): hgqFinal.Fill(3.5)
      if(ng==0 and nq==2): hgqFinal.Fill(4.5)
   elif((nq1+nq2)==4 and (ng1+ng2)==0): ### qq productuion
      hProd.Fill(2.5)
      if(ng==0 and nq==0): hqqFinal.Fill(0.5)
      if(ng==1 and nq==0): hqqFinal.Fill(1.5)
      if(ng==2 and nq==0): hqqFinal.Fill(2.5)
      if(ng==1 and nq==1): hqqFinal.Fill(3.5)
      if(ng==0 and nq==2): hqqFinal.Fill(4.5)
   else: print "error: ng1=%i, ng2=%i, nq1=%i, nq2=%i" % (ng1, ng2, nq1, nq2)

   ### make the flowchart diagram
   pos = nx.nx_agraph.graphviz_layout(G,prog='dot')
   
   ### set the dnodes colors
   for node in G.nodes(data=True):
      if('status' in node[1]): setcolor(int(node[1]['status']))
      else:                    setcolor(0)

   fig, ax = plt.subplots(1, figsize=(15,20))
   plt.suptitle("Event #"+label)

   '''
   'best'         : 0, (only implemented for axes legends)
   'upper right'  : 1,
   'upper left'   : 2,
   'lower left'   : 3,
   'lower right'  : 4,
   'right'        : 5,
   'center left'  : 6,
   'center right' : 7,
   'lower center' : 8,
   'upper center' : 9,
   'center'       : 10,
   '''

   ax.scatter(0,0, c='orange',  marker='o')
   ax.scatter(0,0, c='red',     marker='o')
   ax.scatter(0,0, c='yellow',  marker='o')
   ax.scatter(0,0, c='green',   marker='o')
   ax.scatter(0,0, c='cyan',    marker='o')
   ax.scatter(0,0, c='violet',  marker='o')
   ax.scatter(0,0, c='pink',    marker='o')
   ax.scatter(0,0, c='grey',    marker='o')
   ax.scatter(0,0, c='white',   marker='o')
   leg = ['status<20', 'status=21', 'status=22', 'status=23', '30<status<40', '40<status<50', '50<status<60', '60<status<70', '70<status']
   ax.legend(leg, loc=2, scatterpoints=1, markerscale=2)

   
   if(not os.path.exists("dot")):
      print "please make dir dot/ here"
      quit()
   write_dot(G,'dot/multi.'+label+'.dot')
   nx.draw(G,pos,labels=nlabels,with_labels=True, node_color=colors, node_size=100, font_size=5, arrows=True)
   if(not os.path.exists("pdf")):
      print "please make dir pdf/ here"
      quit()
   plt.savefig("pdf/path."+label+".pdf")
   plt.close()

   print "counters=",counters

   cnv = TCanvas("cnv "+label, "", 500,500)
   hStatuses.Draw("col")
   cnv.SaveAs("pdf/status."+label+".pdf")

cnv = TCanvas("cnv", "", 500,500)
cnv.Draw()
hProd.Scale(100./hProd.GetEntries())
hProd.SetMinimum(0)
hProd.SetMaximum(110)
hProd.Draw("histtext0")
cnv.SaveAs("pdf/multiplicities.pdf(")

cnv = TCanvas("cnv", "", 1200,400)
cnv.Draw()
cnv.Divide(3,1)
cnv.cd(1)
hggFinal.Scale(100./hggFinal.GetEntries())
hggFinal.SetMinimum(0)
hggFinal.SetMaximum(110)
hggFinal.Draw("histtext0")
cnv.cd(2)
hgqFinal.Scale(100./hgqFinal.GetEntries())
hgqFinal.SetMinimum(0)
hgqFinal.SetMaximum(110)
hgqFinal.Draw("histtext0")
cnv.cd(3)
hqqFinal.Scale(100./hqqFinal.GetEntries())
hqqFinal.SetMinimum(0)
hqqFinal.SetMaximum(110)
hqqFinal.Draw("histtext0")
cnv.SaveAs("pdf/multiplicities.pdf)")
