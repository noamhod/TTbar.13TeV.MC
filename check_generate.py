#!/usr/bin/python

import os
import os.path
import mmap
import subprocess

# Choose the name (lep/had)
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name')
args = parser.parse_args()
name = args.n
print 'name : ',name


data    = "/afs/cern.ch/user/h/hod/data/MC/ttbar"
process = name
njobs   = 50

def logfile(path,proc,jobid):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   fname = path+"/gen."+proc+"."+sjobid+".log"
   return fname

def genfiles(path,proc,jobid):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   f1 = path+"/log.generate."+process+"."+sjobid
   f2 = path+"/EVNT."+process+"."+sjobid+".root"
   return (f1, f2)

print "Filaed jobs:"
for j in range(1,njobs+1):
   jobid = j
   logfilename = logfile(data+"/logs",process,jobid)
   jobfilename = logfilename.replace(".log",".sh").replace("log","job")
   bsubcmd = "bsub -q 1nd -o "+logfilename+" "+jobfilename
   #print "CHECKING ",bsubcmd
   if(os.path.isfile(logfilename) and os.access(logfilename, os.R_OK)):
      f = open(logfilename)
      s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
      if(s.find('trf exit code 0')==-1):
         print bsubcmd
      genlog, genevnt = genfiles(data+"/evnt",process,jobid)
      if(not os.path.isfile(genlog) or not os.path.isfile(genlog)):
         print "   ",bsubcmd
