import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import NodalSupportType, AddOn, ActionCategoryType, ActionType
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.node import Node
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RSTAB.LoadCasesAndCombinations.action import Action

if Model.clientModel is None:
    Model()

def test_action():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, addOn = AddOn.structure_stability_active, status = True)

    Node(1, 0.0, 0.0, 0.0)
    Node(2, 5, 0.0, 0.0)
    NodalSupport(1, '1', NodalSupportType.FIXED)

    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    LoadCasesAndCombinations({
                    "current_standard_for_combination_wizard": 6207,
                    "activate_combination_wizard_and_classification": True,
                    "activate_combination_wizard": True,
                    "result_combinations_active": False,
                    "result_combinations_parentheses_active": False,
                    "result_combinations_consider_sub_results": False,
                    "combination_name_according_to_action_category": False
                 },
                 model= Model)

    LoadCase(1, 'Self-Weight', [True, 0.0, 0.0,1.0])

    Action(1, ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, ActionType.ACTING_DIFFERENTLY, [[1,1]])

    Model.clientModel.service.finish_modification()

    action = Model.clientModel.service.get_action(1)
    assert action.action_category == ActionCategoryType.ACTION_CATEGORY_PERMANENT_G.name
    assert action.action_type == ActionType.ACTING_DIFFERENTLY.name
