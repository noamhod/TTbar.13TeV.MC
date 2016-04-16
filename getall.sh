scp -p hod@lxplus.cern.ch:ttbar/README.md .
scp -p hod@lxplus.cern.ch:ttbar/*.py .
scp -p hod@lxplus.cern.ch:ttbar/*.sh .
rm -f rcSetup.sh
rm -f ._*
scp -pr hod@lxplus.cern.ch:ttbar/src/*.C src/
scp -pr hod@lxplus.cern.ch:ttbar/src/*.py src/
scp -pr hod@lxplus.cern.ch:ttbar/src/*.sh src/
rm -f src/._*
rm -f src/_C.d
rm -f src/_C.so
