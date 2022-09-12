import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import *
from RSTAB.initModel import Model
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.line import Line
from RSTAB.BasicObjects.surface import Surface
from RSTAB.BasicObjects.thickness import Thickness
from RSTAB.TypesForLines.lineSupport import LineSupport
from RSTAB.TypesForLines.lineHinge import LineHinge
from RSTAB.TypesForLines.lineWeldedJoint import LineWeldedJoint
from RSTAB.TypesForLines.lineMeshRefinements import LineMeshRefinements


if Model.clientModel is None:
    Model()

def test_typesForLines():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')
    Thickness(1, 'Thick', 1, 0.35)

    Node(1, 0, 0, 0)
    Node(2, 5, 0, 0)
    Node(3, 5, 5, 0)
    Node(4, 0, 5, 0)
    Node(5,2.5,2.5,-2.5)

    Line(1, '1 2')
    Line(2, '2 3')
    Line(3, '3 4')
    Line(4, '4 1')

    Line(5, '1 3')
    Line(6, '1 5')
    Line(7, '5 3')

    Surface(1, '1,2,5')
    Surface(2, '3,4,5')
    Surface(3, '5-7')

    LineSupport(1,'1', LineSupportType.HINGED)
    LineSupport(2,'2', LineSupportType.FREE)

    slab = LineHinge.slabWallConnection
    LineHinge(1,'2/5', params=slab)

    LineWeldedJoint(1,'5','1 2', LineWeldedJointType.BUTT_JOINT, WeldType.WELD_SINGLE_V, 0.005)

    params = LineMeshRefinements.TypeSpecificParams
    LineMeshRefinements(1,'3', LineMeshRefinementsType.TYPE_LENGTH, 2, '', params)

    LineMeshRefinements.TargetFELength(2, '4', 0.05)
    LineMeshRefinements.NumberFiniteElements(3,'5',15)
    LineMeshRefinements.Gradually(4,'6',4)

    Model.clientModel.service.finish_modification()

    ls = Model.clientModel.service.get_line_support(1)
    assert ls.rotational_restraint['x'] == 0
    assert ls.rotational_restraint['y'] == 0
    assert ls.rotational_restraint['z'] == 0
    assert ls.spring['x'] > 10e100
    assert ls.spring['y'] > 10e100
    assert ls.spring['z'] > 10e100

    ls = Model.clientModel.service.get_line_support(2)
    assert ls.rotational_restraint['x'] == 0
    assert ls.rotational_restraint['y'] == 0
    assert ls.rotational_restraint['z'] == 0
    assert ls.spring['x'] == 10000
    assert ls.spring['y'] == 0
    assert ls.spring['z'] == 0

    lwj = Model.clientModel.service.get_line_welded_joint(1)
    assert lwj.joint_type == 'BUTT_JOINT'
    assert lwj.weld_type == 'WELD_SINGLE_V'
    assert round(lwj.weld_size_a1, 3) == 0.005

    lmr = Model.clientModel.service.get_line_mesh_refinement(1)
    assert lmr.type == 'TYPE_LENGTH'
    assert lmr.lines == '3'
    assert lmr.number_of_layers == 2

    lmr = Model.clientModel.service.get_line_mesh_refinement(3)
    assert lmr.type == 'TYPE_ELEMENTS'
    assert lmr.elements_finite_elements == 15

    lmr = Model.clientModel.service.get_line_mesh_refinement(4)
    assert lmr.type == 'TYPE_GRADUAL'
    assert lmr.gradual_rows == 4
