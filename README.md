Validation
==========
This Validation package incorporates the new requirement of the SLHC and preseves the regular rel val set up. 
The package as commited to git does the regular rel val


To Make the DQM files for SLHC  

cd to  HcalRecHits/src
In  HcalRecHitsClient.cc, 
 doslhc_  = false; --> to doslhc_  = true;
In HcalRecHitsValidation.cc
 doSLHC_ = conf.getUntrackedParameter<bool>("doSLHC", false); --> false to true


cd HcalDigis/src/
In HcalDigisClient.cc
doslhc_  = false; -->  doslhc_  = true;
In HcalDigisValidation.cc
 doSLHC_ = false; --> doSLHC_ = true;


The rel val scripts for comparison plots are in 
https://github.com/kasmi/Validation/tree/master/CaloTowers/test/macros
use the ones with *SLHC* 
