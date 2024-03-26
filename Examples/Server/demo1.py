### Before running this file connect RSTABServer
### change directory in terminal where RSTAB9Server.exe located then run below command in terminal with your login and license details
'''
.\RSTAB9Server.exe --email=jane.doe@gmail.com --password=125 --license=000005-25 --start-soap-server=8081 --soap-number-of-model-server-ports=10
'''


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)

sys.path.append(os.path.dirname(PROJECT_ROOT))

from RSTAB.enums import NodalSupportType, NodalLoadDirection, ActionCategoryType, AddOn
from RSTAB.initModel import CalculateSelectedCases, Model, SetAddonStatus, Calculate_all
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.Results.resultTables import ResultTables, ConvertResultsToListOfDct
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.TypesForSteelDesign.steelEffectiveLengths import SteelEffectiveLengths
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.Loads.nodalLoad import NodalLoad

if __name__ == '__main__':
    l = float(input('Length of the cantilever in m: '))
    f = float(input('Force in kN: '))

    Model(True, "Demo1") # crete new model called Demo1
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active)
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')
    Section(1, 'IPE 200')
    Node(1, 0.0, 0.0, 0.0)
    Node(2, l, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    NodalSupport(1, '1', NodalSupportType.FIXED)
    SteelEffectiveLengths()
    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    StaticAnalysisSettings.SecondOrderPDelta(2, "SecondOrder")
    StaticAnalysisSettings.LargeDeformation(3, "LargeDeformation")
    LoadCasesAndCombinations()
    LoadCase.StaticAnalysis(1, 'Self-Weight',analysis_settings_no=1,self_weight=[True, 0.0, 0.0, 1.0])
    LoadCase.StaticAnalysis(2, 'Variable',analysis_settings_no=1,action_category=ActionCategoryType.ACTION_CATEGORY_IMPOSED_LOADS_CATEGORY_B_OFFICE_AREAS_QI_B)

    NodalLoad(1, 1, '2', NodalLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, f*1000)
    Model.clientModel.service.finish_modification()

    Calculate_all()
    result = ConvertResultsToListOfDct(Model.clientModel.service.get_results_for_steel_design_overview_errors_and_warnings())
    print(result)
