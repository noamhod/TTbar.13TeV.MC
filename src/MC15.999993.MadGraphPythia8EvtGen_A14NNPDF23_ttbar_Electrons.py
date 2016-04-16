from MadGraphControl.MadGraphUtils import *

nevents=10000
mode=0


### DSID lists (extensions can include systematics samples)
test=[999993]


fcard = open('proc_card_mg5.dat','w')
if runArgs.runNumber in test:
    fcard.write("""
    import model sm
    define l+ = e+
    define l- = e-
    define p = g u c d s u~ c~ d~ s~
    define j = g u c d s u~ c~ d~ s~
    generate    g g > t t~, ( t > b w+, w+ > l+ vl), ( t~ > b~ w-, w- > j j)    @1
    add process g g > t t~, ( t > b w+, w+ > j j),   ( t~ > b~ w-, w- > l- vl~) @2
    add process g g > t t~, ( t > b w+, w+ > l+ vl), ( t~ > b~ w-, w- > l- vl~) @3
    output -f""")
    fcard.close()

else: 
    raise RuntimeError("runNumber %i not recognised in these jobOptions."%runArgs.runNumber)



beamEnergy=-999
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.
else: 
    raise RuntimeError("No center of mass energy found.")


extras = { 'lhe_version':'2.0', 
           'cut_decays':'F',
           'MT':'172.5',
           'pdlabel':"'nn23lo1'",
           'use_syst':"False"}
    
runName='run_01'     


process_dir = new_process()
build_run_card(run_card_old=get_default_runcard(proc_dir=process_dir),run_card_new='run_card.dat',
               nevts=nevents,rand_seed=runArgs.randomSeed,beamEnergy=beamEnergy,extras=extras)

    
print_cards()

generate(run_card_loc='run_card.dat',param_card_loc=None,mode=mode,proc_dir=process_dir,run_name=runName)
arrange_output(run_name=runName,proc_dir=process_dir,outputDS=runName+'._00001.events.tar.gz',lhe_version=3,saveProcDir=True)  

   

#### Shower 
evgenConfig.description = 'MadGraph_ttbar'
evgenConfig.keywords+=['ttbar','jets']
evgenConfig.inputfilecheck = runName
runArgs.inputGeneratorFile=runName+'._00001.events.tar.gz'

include("MC15JobOptions/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")
include("MC15JobOptions/Pythia8_MadGraph.py")
