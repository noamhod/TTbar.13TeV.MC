#!/usr/bin/python

import os
import subprocess

data    = "/afs/cern.ch/user/h/hod/data/MC/ttbar"
process = "lep"
njobs   = 50

def jobfile(path,proc,jobid):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   fname = path+"/ana."+proc+"."+sjobid+".sh"
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
   f.write('lsetup "rcsetup Base,2.4.4"\n')
   f.write("rc find_packages\n")
   f.write("rc compile\n")
   f.write("/bin/cp -f /afs/cern.ch/user/h/hod/ttbar/src/Read.xAOD.py .\n")
   f.write("python Read.xAOD.py -n "+proc+" -i "+sjobid+"\n")
   f.write("/bin/cp -f tops.SM.root "+data+"/ntup/tops.SM."+proc+"."+sjobid+".root\n")
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
