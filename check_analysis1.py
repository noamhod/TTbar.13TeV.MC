#!/usr/bin/python

import os
import os.path
import mmap
import subprocess

# Choose the name (lep/had)
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name (lep / had)')
args = parser.parse_args()
name = args.n
print 'name : ',name


data    = "/afs/cern.ch/user/h/hod/data/MC/ttbar"
process = name
njobs   = 50

def logfile(path,proc,jobid,seed):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   f = path+"/ana1."+proc+"."+sjobid+".log"
   return f


def trffile(path,proc,jobid,seed):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   f = path+"/tops.SM.TRUTH1."+proc+"."+sjobid+".root"
   return f


print "Filaed jobs:"
for j in range(1,njobs+1):
   seed  = j
   jobid = j
   logfilename = logfile(data+"/logs",process,jobid,seed)
   jobfilename = logfilename.replace(".log",".sh").replace("log","job")
   bsubcmd = "bsub -q 1nd -o "+logfilename+" "+jobfilename
   if(os.path.isfile(logfilename) and os.access(logfilename, os.R_OK)):
      f = open(logfilename)
      s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
      if(s.find('all OK!')==-1):
         print bsubcmd
      ntupname = trffile(data+"/ntup",process,jobid,seed)
      if(not os.path.isfile(ntupname)):
         print "   ",bsubcmd
