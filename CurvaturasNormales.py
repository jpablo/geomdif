# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes.pointset import PointSet
from superficie.nodes.line import Line
from superficie.nodes.plane import Plane
from superficie.nodes.curve3d import Curve3D
from superficie.nodes.arrow import Arrow
from superficie.book import chapter, page
from superficie.book.chapter import Chapter
from superficie.book.page import Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import visible_checkbox, slider
from superficie.widgets.visible_checkbox import VisibleCheckBox
from superficie.widgets.slider import Slider
from superficie.plots import ParametricPlot3D
from superficie.viewer.Viewer import Viewer
from superficie.animations import AnimationGroup


def createEllipsoid(a,b,c):

    par_e = lambda u, v: Vec3(a * sin(u) * cos(v), b * sin(u) * sin(v), c * cos(u))
    e = ParametricPlot3D(par_e, (0, pi, 100), (0, 2 * pi, 100))
    e.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
    e.setTransparency(0.5)
    e.setDiffuseColor(_1(40, 200, 120))

    #sep = SoSeparator()
    #sep.addChild(e)

    #return sep
    return e


class Elipsoide1(Page):
    u"""<b>Curvaturas normales</b> en el punto (1,0,0)
      de la elipsoide x^2 + (1/4)y^2 + (1/9)z^2 = 1
    """

    def __init__(self):
        super(Elipsoide1,self).__init__('Elipsoide1')

        self.showAxis(False)

        ellipsoid = createEllipsoid(1.0, 2.0, 3.0)

        self.addChild(ellipsoid)


        normal = Arrow((1,0,0), (2,0,0), 0.05)

        self.addChild(normal)

        normal_plane = Plane(2)
        normal_plane.setOrigin((0,0,1))

        self.addChild(normal_plane)


class Elipsoide2(Page):
    u"""<b>Curvaturas normales</b> en el punto (0,0,3)
      de la elipsoide x^2 + (1/4)y^2 + (1/9)z^2 = 1

      Elipsode3: y=0, x^2=(a^2-b^2)/(a^2-c^2), z^2=c^2(b^2-c^2)/(a^2-c^2)
    """

    def __init__(self):
        super(Elipsoide2,self).__init__('Elipsoide2')

        self.showAxis(False)

        ellipsoid = createEllipsoid(1.0, 2.0, 3.0)

        self.addChild(ellipsoid)


        normal = Arrow((0,0,3), (0,0,4), 0.05)

        self.addChild(normal)

        normal_plane = Plane(1)
        normal_plane.setOrigin((0,1,2))

        self.addChild(normal_plane)


class Cilindro(Page):
    u"""<b>Curvaturas normales</b> en algunos puntos del cilindro
      $x^2 + z^2 = 1$.
    """

    def __init__(self):
        super(Cilindro,self).__init__('Cilindro')

        self.showAxis(False)

        cyl = SoCylinder()
        cyl.radius.setValue(1.0)
        cyl.height.setValue(4.0)
        cyl.parts = SoCylinder.SIDES

        light = SoShapeHints()
#       light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
#       light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
#       light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

        mat = SoMaterial()
        mat.emissiveColor = _1(40, 80, 200)
        mat.diffuseColor = _1(40, 80, 200)
        mat.transparency.setValue(0.5)

        #rot = SoRotationXYZ()
        #rot.axis = SoRotationXYZ.X
        #rot.angle = pi / 2

        #trans = SoTransparencyType()
#       trans.value = SoTransparencyType.DELAYED_BLEND
        #trans.value = SoTransparencyType.SORTED_OBJECT_BLEND
#       trans.value = SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND

        sep = SoSeparator()
        sep.addChild(light)
        #sep.addChild(rot)
        #sep.addChild(trans)
        sep.addChild(mat)
        sep.addChild(cyl)

        self.addChild(sep)

        normal = Arrow((0,0,1), (0,0,2), 0.05)

        self.addChild(normal)

        normal_plane = Plane(1)
        normal_plane.setOrigin((0,1,0))

        self.addChild(normal_plane)




class CurvaturasNormales(Chapter):

    def __init__(self):
        Chapter.__init__(self, name="Ejemplos de Curvaturas Normales")

        figuras = [
            Elipsoide1,
            Elipsoide2,
            Cilindro
        ]

        for f in figuras:
            self.addPage(f())
