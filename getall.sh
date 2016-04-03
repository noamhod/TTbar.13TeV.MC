scp hod@lxplus.cern.ch:ttbar/*.py .
scp hod@lxplus.cern.ch:ttbar/*.sh .
rm -f rcSetup.sh
scp -r hod@lxplus.cern.ch:ttbar/src .
