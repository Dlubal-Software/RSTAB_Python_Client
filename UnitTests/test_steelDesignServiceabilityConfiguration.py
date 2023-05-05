import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import AddOn, NodalSupportType
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.SteelDesign.steelServiceabilityConfiguration import SteelDesignServiceabilityConfigurations

if Model.clientModel is None:
    Model()

def test_SteelDesignServiceabilityConfigurations():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, addOn=AddOn.steel_design_active, status=True)

    Material(1, 'S235')

    Section(1, 'IPE 200')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, 5, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    NodalSupport(1, '1', NodalSupportType.FIXED)

    SteelDesignServiceabilityConfigurations(1, 'Test SLS')
    SteelDesignServiceabilityConfigurations(2, 'SLS2', '1')

    Model.clientModel.service.finish_modification()

    config1 = Model.clientModel.service.get_steel_design_sls_configuration(1)
    config2 = Model.clientModel.service.get_steel_design_sls_configuration(2)

    assert config1.name == "Test SLS"
    assert config2.assigned_to_members == '1'
