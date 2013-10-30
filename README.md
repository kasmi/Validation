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


++++++ Inventory of what I changed ++++++++

--- HcalRecHits
----------------
HcalRecHits/src

HcalRecHitsClient.cc and HcalRecHitsValidation.cc

HcalRecHits/interface

HcalRecHitsClient.h and HcalRecHitsValidation.h 

--- HcalDigis
--------------
HcalDigis/src

HcalDigisClient.cc and HcalDigisValidation.cc

HcalDigis/interface

HcalDigisValidation.h and HcalDigisClient.h


--- CaloTowers
--------------
CaloTowers/test/macros
+++++
Copy these files:

rootlogon.C and RelValMacro.C

Add these files:

RunRVMacros_SLHC.csh

InputRelVal_Medium_SLHC.txt

CaloTowers/test/macros/html_indices
++++++
Add these filese 

RelVal_HcalDigis_SLHC.html 

RelVal_RecHits_SLHC.html


