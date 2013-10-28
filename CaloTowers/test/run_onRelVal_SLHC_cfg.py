import os
import FWCore.ParameterSet.Config as cms

process = cms.Process("hcalval")
process.load('Configuration.Geometry.GeometryExtended2019Reco_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

# I added this hoping it will resolve hcaldigis
#process.load('Configuration/StandardSequences/DigiToRaw_cff')
#process.load('Configuration/StandardSequences/RawToDigi_cff')


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'DES19_62_V7::All', '')

#process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.load("DQMServices.Core.DQM_cfg")
process.DQM.collectorHost = ''

process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound') )

#######################################################################
# TWO-file approach, as both RAW  (for HCAL re-reco)    and
#                               RECO (for unchanged ECAL)  are required 
#######################################################################
process.source = cms.Source("PoolSource",
noEventSort = cms.untracked.bool(True),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),   
    #--- full set of GEN-SIM-RECO RelVal files ----------------------------
#    fileNames = cms.untracked.vstring('file:QCD_30_35_cfi_py_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_L1Reco_RECO.root'
    fileNames = cms.untracked.vstring(
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/2E14980A-A61C-E311-83B6-003048D37424.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/36DE2547-A01C-E311-8720-003048946FAE.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/58CBA062-A01C-E311-A2D5-003048FEAF50.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/7ECFDEFF-9F1C-E311-960F-D8D385FF4A94.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/B8683B34-A01C-E311-81D5-003048CF68C6.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/C2CABE3A-AA1C-E311-81A7-0025901D6286.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/E03DE07E-A91C-E311-A742-BCAEC518FF40.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/EC9AF207-A01C-E311-8B1E-003048D373EC.root',
       '/store/relval/CMSSW_6_2_0_SLHC1/RelValTTbar_14TeV/GEN-SIM-RECO/DES19_62_V7_UPG2019-v1/00000/FA3D38D9-BE1C-E311-8B5C-003048FEB916.root'
    ),
    #--- full set of GEN-SIM-DIGI-RAW(-HLTDEBUG) RelVal files -------------
    secondaryFileNames = cms.untracked.vstring(
     ),  
    inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
)


process.load("DQMServices.Components.MEtoEDMConverter_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.FEVT = cms.OutputModule("PoolOutputModule",
     outputCommands = cms.untracked.vstring('drop *', 'keep *_MEtoEDMConverter_*_*'),
     fileName = cms.untracked.string("HcalValHarvestingEDM.root")
)


process.hcalDigiAnalyzer = cms.EDAnalyzer("HcalDigisValidation",
    outputFile		      = cms.untracked.string('HcalDigisValidationRelVal.root'),
    digiLabel		      = cms.InputTag("simHcalDigis"),
    zside		      = cms.untracked.string('*'),
    mode		      = cms.untracked.string('multi'),

    hcalselector	      = cms.untracked.string('all'),
    mc			      = cms.untracked.string('yes') # 'yes' for MC
)   

process.hcalTowerAnalyzer = cms.EDAnalyzer("CaloTowersValidation",
    outputFile               = cms.untracked.string('CaloTowersValidationRelVal.root'),
    CaloTowerCollectionLabel = cms.untracked.InputTag('towerMaker'),

    hcalselector             = cms.untracked.string('all'),
    mc                       = cms.untracked.string('no'),
    useAllHistos             = cms.untracked.bool(False)                         
)

process.hcalNoiseRates = cms.EDAnalyzer('NoiseRates',
    outputFile   = cms.untracked.string('NoiseRatesRelVal.root'),
    rbxCollName  = cms.untracked.InputTag('hcalnoise'),

    minRBXEnergy = cms.untracked.double(20.0),
    minHitEnergy = cms.untracked.double(1.5),
    useAllHistos = cms.untracked.bool(False)                         
)


#--- NB: CHANGED for SLHC/Upgrade
process.hcalRecoAnalyzer = cms.EDAnalyzer("HcalRecHitsValidation",
    outputFile                = cms.untracked.string('HcalRecHitValidationRelVal.root'),
    HBHERecHitCollectionLabel = cms.untracked.InputTag("hbheUpgradeReco"),
    HFRecHitCollectionLabel   = cms.untracked.InputTag("hfUpgradeReco"),
    HORecHitCollectionLabel   = cms.untracked.InputTag("horeco"),
    eventype                  = cms.untracked.string('multi'),
    ecalselector              = cms.untracked.string('yes'),
    hcalselector              = cms.untracked.string('all'),
    mc                        = cms.untracked.string('no') 
)



process.load('Configuration/StandardSequences/EDMtoMEAtRunEnd_cff')
process.dqmSaver.referenceHandling = cms.untracked.string('all')

cmssw_version = os.environ.get('CMSSW_VERSION','CMSSW_X_Y_Z')
Workflow = '/HcalValidation/'+'Harvesting/'+str(cmssw_version)
process.dqmSaver.workflow = Workflow

process.calotowersClient = cms.EDAnalyzer("CaloTowersClient", 
     outputFile = cms.untracked.string('CaloTowersHarvestingME.root'),
     DQMDirName = cms.string("/") # root directory
)

process.noiseratesClient = cms.EDAnalyzer("NoiseRatesClient", 
     outputFile = cms.untracked.string('NoiseRatesHarvestingME.root'),
     DQMDirName = cms.string("/") # root directory
)

process.hcalrechitsClient = cms.EDAnalyzer("HcalRecHitsClient", 
     outputFile = cms.untracked.string('HcalRecHitsHarvestingME.root'),
     DQMDirName = cms.string("/") # root directory
)


process.hcaldigisClient = cms.EDAnalyzer("HcalDigisClient",
     outputFile	= cms.untracked.string('HcalDigisHarvestingME.root'),
     DQMDirName	= cms.string("/") # root directory
)   


#process.hcalDigis.InputLabel = 'rawDataCollector' # MC
#---------------------------------------------------- Job PATH 
process.p2 = cms.Path( 
process.hcalTowerAnalyzer * 
process.hcalNoiseRates * 
process.hcalRecoAnalyzer *
process.hcalDigiAnalyzer * 
process.calotowersClient * 
process.noiseratesClient *
process.hcalrechitsClient * 
process.hcaldigisClient * 
process.dqmSaver)


#--- Customization for SLHC

from SLHCUpgradeSimulations.Configuration.HCalCustoms import customise_HcalPhase1
process=customise_HcalPhase1(process)

