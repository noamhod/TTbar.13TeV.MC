#!/usr/bin/python

import os
import subprocess
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name (HT0...HT4)')
parser.add_argument('-f', metavar='<number of files>', required=True, help='Number of files')
args = parser.parse_args()
name = args.n
nfiles = args.f
print 'name : ',name
print 'nfiles : ',nfiles

data    = "/afs/cern.ch/user/h/hod/data/MC/ttbar"
process = name
njobs   = int(nfiles)

def jobfile(path,proc,jobid):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   fname = path+"/ana1."+proc+"."+sjobid+".sh"
   lname = fname.replace(".sh",".log").replace("job","log")
   base = os.getcwd()
   f = open(fname,"w")
   f.write("#!/bin/bash\n")
   f.write("echo \"host = $HOSTNAME\"\n")
   f.write("rm -f "+lname+"\n")
   f.write("cd /tmp/hod/\n")
   f.write("export RUCIO_ACCOUNT=hod\n")
   f.write("export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase\n")
   f.write("source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\n")
   f.write('lsetup "rcsetup Base,2.4.5"\n')
   f.write("rc find_packages\n")
   f.write("rc compile\n")
   f.write("cd /tmp/hod/\n")
   f.write("/bin/cp -f /afs/cern.ch/user/h/hod/ttbar/src/Read.xAOD.TRUTH1.Grid.py .\n")
   f.write("python Read.xAOD.TRUTH1.Grid.py -n "+proc+" -i "+sjobid+"\n")
   f.write("/bin/cp -f tops.SM.TRUTH1.root "+data+"/ntup/tops.SM.TRUTH1."+proc+"."+sjobid+".root\n")
   f.write("echo \"host = $HOSTNAME\"\n")
   return fname

p = subprocess.Popen("rm -f "+data+"/jobs/*."+process+"*.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/logs/*."+process+"*.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

for j in range(1,njobs+1):
   seed  = j
   jobid = j
   jobfilename = jobfile(data+"/jobs",process,jobid)
   logfilename = jobfilename.replace("job","log").replace(".sh",".log")
   p = subprocess.Popen("chmod 755 "+jobfilename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   bsubcmd = "bsub -q 1nd -o "+logfilename+" "+jobfilename
   p = subprocess.Popen(bsubcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   print bsubcmd
