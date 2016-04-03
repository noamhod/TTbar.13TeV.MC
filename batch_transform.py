#!/usr/bin/python

import os
import subprocess
import argparse
parser = argparse.ArgumentParser(description='Read xAOD')
parser.add_argument('-n', metavar='<process name>', required=True, help='The process name (lep / had)')
parser.add_argument('-f', metavar='<process format>', required=True, help='The process format (TRUTH0 / TRUTH1)')
args = parser.parse_args()
name = args.n
frmt = args.f
print 'name : ',name
print 'frmt : ',frmt

data    = "/afs/cern.ch/user/h/hod/data/MC/ttbar"
process = name
format  = frmt
njobs   = 50

def jobfile(path,proc,jobid):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   fname = path+"/trf."+proc+"."+sjobid+".sh"
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
   f.write('lsetup "asetup 20.1.X.Y-VAL,rel_1,AtlasDerivation,gcc48,here --nightliesarea=/afs/cern.ch/atlas/software/builds/nightlies"\n')
   f.write("Reco_tf.py --inputEVNTFile "+data+"/evnt/EVNT."+proc+"."+sjobid+".root  --outputDAODFile NTUP.root --reductionConf "+format+"\n")
   f.write("/bin/cp -f DAOD_"+format+".NTUP.root "+data+"/ntup/DAOD_"+format+".NTUP."+proc+"."+sjobid+".root\n")
   f.write("echo \"host = $HOSTNAME\"\n")
   return fname

p = subprocess.Popen("rm -f "+data+"/jobs/*."+process+"*.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/logs/*."+process+"*.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/ntup/DAOD_"+format+".NTUP."+process+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
