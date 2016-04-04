# TTbar.13TeV.MC

Code and Job Option files are in the src/ directory under this directory

All logs, jobs, evnt files and ntuples are available under this directories:
DATADIR=/afs/cern.ch/user/h/hod/data/MC/ttbar
$DATADIR/logs
$DATADIR/jobs
$DATADIR/evnt
$DATADIR/ntup

Initial setup:
* for generating, run `source init.sh` or `source setup.gen.sh`
* for transformation, run `source setup.trf.sh` (in a different shell)
* for analysis, run `source rcInit.sh` or `source setup.ana.sh` (in a different shell)

Each of the steps below should be executed in a different shell


----------------------
To generate EVNT files:
* source setup.gen.sh
* python batch_generate.py -n lep[had]
* bjobs -w
* python check_generate.py -n lep[had]

-----------------------------
To transform to TRUTH0 ntules:
* python batch_transform.py -n lep[had] -f TRUTH0
* bjobs -w
* python check_transform.py -n lep[had] -f TRUTH0

--------------------------------------------------------
To make a simple hard-process tree from the TRUTH0 files:
* python batch_analysis0.py -n lep[had]
* bjobs -w
* python batch_analysis0.py -n lep[had]
* python src/Test.Merged.py -n lep[had]
* A tree with all events and info needed to calculate the weights is available in $DATADIR/ntup/tops.SM.lep[had].merged.root
* A histogram (pdf file) of the ttbar mass at the hard-process level is available in $DATADIR/ntup/Test.TTree.lep[had].pdf

------------------------------------------------
Calculate the weights with the hard-process tree:
* use the 2HDM setup to append the weights
* !!! NEED TO RUN THIS STEP !!!

-------------------------------------------------
To transform to TRUTH1 ntules for "real" analysis (truth jets, MET etc.):
* first have to free up some space: rm -f $DATADIR/ntup/DAOD_TRUTH0.NTUP.*.root
* python batch_transform.py -n lep[had] -f TRUTH1
* bjobs -w
* python check_transform.py -n lep[had] -f TRUTH1

----------------------------------------------------
To run the "real" analysis while reading the weights:
* get the hard-process tree with the appended 2HDM weights
* read this tree as friend while running on the TRUTH1 files
* !!! NEED TO MAKE THIS STEP !!!
