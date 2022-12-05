import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import AddOn, TimberServiceClassServiceClass
from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.TypesForTimberDesign.timberServiceClass import TimberServiceClass

if Model.clientModel is None:
    Model()

def test_timberServiceClass():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.timber_design_active, True)

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 10, 0, 0)
    Material(1, 'KLH (20 mm) | KLH')
    Section(1, 'R_M1 0.2/0.5', 1)
    Member(1, 1, 2, 0, 1, 1)
    Member(2, 2, 3, 0, 1, 1)

    TimberServiceClass(members='1 2', service_class=TimberServiceClassServiceClass.TIMBER_SERVICE_CLASS_TYPE_2)

    Model.clientModel.service.finish_modification()

    tsc1 = Model.clientModel.service.get_timber_service_class(1)

    assert tsc1.member == '1 2'
    assert tsc1.service_class == TimberServiceClassServiceClass.TIMBER_SERVICE_CLASS_TYPE_2.name
