#!/usr/bin/python

import os
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
nevts   = 10000

def jobfile(path,proc,jobid,seed):
   sjobid = str(jobid)
   if(j<10): sjobid = "0"+sjobid
   fname = path+"/gen."+proc+"."+sjobid+".sh"
   lname = fname.replace(".sh",".log").replace("job","log")
   base = os.getcwd()
   sseed = str(seed)
   snevts = str(nevts)
   firstevent = str(nevts*(j-1)+1)
   runnumber = ""
   if  (proc=="inc"): runnumber = "999990"
   elif(proc=="lep"): runnumber = "999991"
   elif(proc=="had"): runnumber = "999992"
   elif(proc=="el"):  runnumber = "999993"
   elif(proc=="mu"):  runnumber = "999994"
   procname = ""
   if  (proc=="inc"): procname = "Inc"
   elif(proc=="lep"): procname = "Lep"
   elif(proc=="had"): procname = "Had"
   elif(proc=="el"):  procname = "Electrons"
   elif(proc=="mu"):  procname = "Muons"
   f = open(fname,"w")
   f.write("#!/bin/bash\n")
   f.write("echo \"host = $HOSTNAME\"\n")
   f.write("rm -f "+lname+"\n")
   f.write("/bin/cp -f  "+base+"/src/*  /tmp/hod/\n")
   f.write("cd /tmp/hod/\n")
   f.write("ls -lrt\n")
   f.write("export RUCIO_ACCOUNT=hod\n")
   f.write("export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase\n")
   f.write("source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh\n")
   f.write('lsetup "asetup 19.2.5.1,here"\n')
   f.write("cmt co -r MadGraphControl-00-05-33 Generators/MadGraphControl\n")
   f.write("cd Generators/MadGraphControl/cmt\n")
   f.write("make clean; make\n")
   f.write("cd /tmp/hod/\n")
   f.write("Generate_tf.py --ecmEnergy=13000. --maxEvents="+snevts+" --firstEvent="+firstevent+" --runNumber="+runnumber+" --randomSeed="+sseed+" --outputEVNTFile=EVNT.root --jobConfig=MC15."+runnumber+".MadGraphPythia8EvtGen_A14NNPDF23_ttbar_"+procname+".py\n")
   f.write("/bin/cp -f log.generate "+data+"/evnt/log.generate."+proc+"."+sjobid+"\n")
   f.write("/bin/cp -f EVNT.root "+data+"/evnt/EVNT."+proc+"."+sjobid+".root\n")
   f.write("echo \"host = $HOSTNAME\"\n")
   return fname

p = subprocess.Popen("rm -f "+data+"/jobs/*."+process+"*.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/logs/*."+process+"*.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/evnt/log.generate."+process+".*", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
p = subprocess.Popen("rm -f "+data+"/evnt/EVNT."+process+".*.root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

#log.generate.had.44
for j in range(1,njobs+1):
   seed  = j
   jobid = j
   jobfilename = jobfile(data+"/jobs",process,jobid,seed)
   logfilename = jobfilename.replace("job","log").replace(".sh",".log")
   p = subprocess.Popen("chmod 755 "+jobfilename, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   bsubcmd = "bsub -q 1nd -o "+logfilename+" "+jobfilename
   p = subprocess.Popen(bsubcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p.communicate()
   print bsubcmd
