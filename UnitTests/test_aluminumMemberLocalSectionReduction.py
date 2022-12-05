import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import AluminumMemberLocalSectionReductionType, FastenerDefinitionType, MultipleOffsetDefinitionType
from RSTAB.initModel import Model
from RSTAB.TypesForAluminumDesign.aluminumMemberLocalSectionReduction import AluminumMemberLocalSectionReduction
from RSTAB.initModel import AddOn, SetAddonStatus


if Model.clientModel is None:
    Model()


def test_AluminumMemberLocalSectionReduction():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.aluminum_design_active, True)

    AluminumMemberLocalSectionReduction(1, "", "",
        [
            [AluminumMemberLocalSectionReductionType.REDUCTION_COMPONENT_TYPE_DESIGN_PARAMETERS, 1, False, FastenerDefinitionType.DEFINITION_TYPE_ABSOLUTE, 0.2, 0, MultipleOffsetDefinitionType.OFFSET_DEFINITION_TYPE_ABSOLUTE, 0.0]
        ],
        "")

    AluminumMemberLocalSectionReduction(2, "", "",
        [
            [AluminumMemberLocalSectionReductionType.REDUCTION_COMPONENT_TYPE_DESIGN_PARAMETERS, 1.2, True, FastenerDefinitionType.DEFINITION_TYPE_ABSOLUTE, 0.1, 2, MultipleOffsetDefinitionType.OFFSET_DEFINITION_TYPE_ABSOLUTE, 2],
            [AluminumMemberLocalSectionReductionType.REDUCTION_COMPONENT_TYPE_DESIGN_PARAMETERS, 2.0, True, FastenerDefinitionType.DEFINITION_TYPE_RELATIVE, 0.20, 3, MultipleOffsetDefinitionType.OFFSET_DEFINITION_TYPE_RELATIVE, 0.1]
        ],
        "")

    AluminumMemberLocalSectionReduction(3, "", "",
        [
            [AluminumMemberLocalSectionReductionType.REDUCTION_COMPONENT_TYPE_DESIGN_PARAMETERS, 1.5, False, FastenerDefinitionType.DEFINITION_TYPE_RELATIVE, 0.15, 0, MultipleOffsetDefinitionType.OFFSET_DEFINITION_TYPE_ABSOLUTE, 0.0],
            [AluminumMemberLocalSectionReductionType.REDUCTION_COMPONENT_TYPE_DESIGN_PARAMETERS, 1.8, True, FastenerDefinitionType.DEFINITION_TYPE_RELATIVE, 0.25, 4, MultipleOffsetDefinitionType.OFFSET_DEFINITION_TYPE_ABSOLUTE, 0.3]
        ], ""
        )

    Model.clientModel.service.finish_modification()

    smlr_1 = Model.clientModel.service.get_aluminum_member_local_section_reduction(1)
    assert smlr_1.components[0][0].row['position'] == 1
    assert smlr_1.components[0][0].row['multiple'] == False
    assert smlr_1.components[0][0].row['fastener_definition_type'] == 'DEFINITION_TYPE_ABSOLUTE'
    assert smlr_1.components[0][0].row['reduction_area'] == 0.2

    smlr_2 = Model.clientModel.service.get_aluminum_member_local_section_reduction(2)
    assert smlr_2.components[0][0].row['position'] == 1.2
    assert smlr_2.components[0][0].row['multiple'] == True
    assert smlr_2.components[0][1].row['fastener_definition_type'] == 'DEFINITION_TYPE_RELATIVE'
    assert smlr_2.components[0][1].row['reduction_area_factor'] == 0.20
    assert smlr_2.components[0][0].row['multiple_offset'] == 2

    smlr_3 = Model.clientModel.service.get_aluminum_member_local_section_reduction(3)
    assert smlr_3.components[0][1].row['position'] == 1.8
    assert smlr_3.components[0][0].row['multiple'] == False
    assert smlr_3.components[0][1].row['multiple'] == True
    assert smlr_3.components[0][1].row['multiple_offset_definition_type'] == 'OFFSET_DEFINITION_TYPE_ABSOLUTE'
    assert smlr_3.components[0][1].row['multiple_offset'] == 0.3
