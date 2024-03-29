import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.initModel import Model, SetAddonStatus
from RSTAB.enums import AddOn
from RSTAB.dataTypes import inf
from RSTAB.TypesForMembers.memberRotationalRestraint import MemberRotationalRestraint
from RSTAB.TypesForMembers.memberShearPanel import MemberShearPanel
from RSTAB.TypesForMembers.memberSupport import MemberSupport

if Model.clientModel is None:
    Model()

def test_memberSupport():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.aluminum_design_active)
    SetAddonStatus(Model.clientModel, AddOn.timber_design_active)
    SetAddonStatus(Model.clientModel, AddOn.steel_design_active)

    MemberSupport(1, spring_translation_x=3000)

    MemberShearPanel.TrapezodialSheeting()
    MemberRotationalRestraint.Continuous()

    MemberSupport(3)

    Model.clientModel.service.finish_modification()

    memberSupport1 = Model.clientModel.service.get_member_support(1)
    assert memberSupport1.spring_translation_x == 3000

    memberSupport3 = Model.clientModel.service.get_member_support(3)
    assert memberSupport3.spring_translation_z == inf
