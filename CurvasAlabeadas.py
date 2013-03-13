# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, Bundle2, Bundle3, PointSet, SimpleSphere
from superficie.book import Chapter, Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import VisibleCheckBox, Slider, SpinBox
from superficie.plots import ParametricPlot3D
from superficie.viewer.Viewer import Viewer
from superficie.animations import AnimationGroup


def Cylinder(col, length, radius = 0.98):
    sep = SoSeparator()

    cyl = SoCylinder()
    cyl.radius.setValue(radius)
    cyl.height.setValue(length)
    cyl.parts = SoCylinder.SIDES

    light = SoShapeHints()
#    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
#    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
#    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor = col
    mat.diffuseColor = col
    mat.transparency.setValue(0.5)

    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.X
    rot.angle = pi / 2

    trans = SoTransparencyType()
#    trans.value = SoTransparencyType.DELAYED_BLEND
    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND
#    trans.value = SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND

    sep.addChild(light)
    sep.addChild(rot)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(cyl)

    return sep

class HeliceCircular(Page):
    #u"""Las hélices circulares y sus casos límite, la recta y la circunferencia,
    #<b>curvas homogéneas</b>: un pedazo de ellas puede acomodarse en cualquier otro lugar de
    #la hélice.
    #"""
    def __init__(self):
        Page.__init__(self, u"Hélice circular, curvatura y torsión")
        self.camera_position = (10, -10, 10)
        self.showAxis(False)
        tmin = -2 * pi
        tmax = 2 * pi
        npuntos = 300
        self.addChild(Cylinder(_1(185, 46, 61), tmax - tmin, 2))
        ## ============================================
        # 1 implica primer derivada, 2 implica segunda derivada
        def param1hc(t):
            return 2*Vec3(cos(t), sin(t), t/3.0)
        def param2hc(t):
            return 2*Vec3(-sin(t), cos(t), 1/3.0)
        def param3hc(t):
            return 2*Vec3(-cos(t), -sin(t), 0)

        espiral = Curve3D(param1hc, (tmin*1.5, tmax*1.5, npuntos), color=_1(255, 255, 255))
        tangente = espiral.attachField("tangente", param2hc).setLengthFactor(1).setWidthFactor(.6)
        tangente.setRadius( 0.06 )
        tangente.setDiffuseColor( _1(20,240,20) )
        normal = espiral.attachField("normal", param3hc).setLengthFactor(1).setWidthFactor(.6)
        normal.setRadius( 0.06 )
        normal.setDiffuseColor( _1(240,120,20) )
        self.addChild(espiral)
        self.setupAnimations([ AnimationGroup([tangente, normal], (10000,0,len(espiral)-1)) ])

class HeliceReflejada(Page):
    u"""La <b>hélice reflejada</b> no puede llevarse en la hélice anterior
        por un <b>movimiento rígido</b>, es resultado de una reflexión en el
        plano $XY$.
    """
    def __init__(self):
        Page.__init__(self, u"Hélice circular reflejada")
        self.camera_position = (10, -10, 10)
        self.showAxis(False)
        tmin, tmax, npuntos = (-2 * pi, 2 * pi, 200)
        self.addChild(Cylinder(_1(7, 83, 150), tmax - tmin, 2))


        def param1hr(t):
            return 2*Vec3(cos(t), sin(t), -t/3.0)
        def param2hr(t):
            return 2*Vec3(-sin(t), cos(t), -1/3.0)
        def param3hr(t):
            return 2*Vec3(-cos(t), -sin(t), 0)

        espiral = Curve3D(param1hr, (tmin*1.5, tmax*1.5, npuntos), color=_1(240, 10, 120))

        def param1hc_der(t):
            return 2*Vec3(cos(t), sin(t), t/3.0)

        espiral_der = Curve3D(param1hc_der, (tmin*1.5, tmax*1.5, npuntos), color=_1(20, 240, 240))
        tangente = espiral.attachField("tangente", param2hr).setLengthFactor(1).setWidthFactor(.6)
        tangente.setRadius( 0.06 )
        tangente.setDiffuseColor( _1(20,240,20) )
        normal = espiral.attachField("normal", param3hr).setLengthFactor(1).setWidthFactor(.6)
        normal.setRadius( 0.06 )
        normal.setDiffuseColor( _1(240,120,20) )
        self.addChild(espiral)
        self.addChild(espiral_der)

        plano_xy_par = lambda u, v: Vec3(u,v,0)
        plano_xy = ParametricPlot3D(plano_xy_par, (-4,4,20),(-4,4,20))
        plano_xy.setDiffuseColor( _1(200,200,200) )
        plano_xy.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        plano_xy.setTransparency( 0.85 )

        self.addChild( plano_xy )
        self.addChild(Line([(-4, 0, 0), (4, 0, 0)], color=(0.8, 0.8, 0.5)))
        self.addChild(Line([(0, -4, 0), (0, 4, 0)], color=(0.8, 0.8, 0.5)))
        self.setupAnimations([ AnimationGroup([tangente, normal], (10000,0,len(espiral)-1)) ])

class Exponencial(Page):
    def __init__(self):
        Page.__init__(self, u"Exponencial")
        self.showAxis(True)
        self.axis_z.setVisible(False)

        def curve(t): return Vec3(exp(t) * cos(t), exp(t) * sin(t), exp(t))
        def derivada(t): return Vec3(exp(t) * cos(t) - exp(t) * sin(t), exp(t) * cos(t) + exp(t) * sin(t), exp(t))
        curva1 = Curve3D(curve, (-pi, 1 * pi, 200), width=2)
        self.addChild(curva1)
        curva1.derivative = derivada
        curva1.tangent_vector.show()
        self.setupAnimations([curva1.tangent_vector])

    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))

    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))

class Alabeada(Page):
    u"""
    Una curva parametrizada diferenciable es <b>regular</b> si en cada punto tiene bien definida su recta tangente:
    el vector tangente es no nulo en todos los puntos de su dominio.
    <br>
    La <b>Alabeada</b> tiene como proyección en el plano $XY$ una parábola, en el
    plano ZX una cúbica, y en el plano $YZ$ la curva $y^3=z^2$ que tiene una singularidad en
    $(0,0)$ porque la tangente en ese punto no está bien definida.
    """
    def __init__(self):
        Page.__init__(self, u"Curva cúbica alabeada")
        self.camera_position = (5, 5, 5)
        self.camera_viewAll = True
        self.setupPlanes()
        c = lambda t: Vec3(t, t ** 2, t ** 3)
        altura = -1
        curva = Curve3D(c, (-1, 1, 100), width=5, nvertices=1)
        lyz = curva.project(x=altura, color=(0, 1, 1), width=3, nvertices=1)
        lxz = curva.project(y=altura, color=(1, 0, 1), width=3, nvertices=1)
        lxy = curva.project(z=altura, color=(1, 1, 0), width=3, nvertices=1)
        curvas = [curva, lxy, lxz, lyz]
        self.showAxis(False)
        self.addChildren(curvas)
        self.setupAnimations([ AnimationGroup(curvas, (5000,0,len(curva)-1)) ])

class CurvasAlabeadas(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas alabeadas")

        figuras = [
            #Exponencial,
            Alabeada,
            HeliceCircular,
            HeliceReflejada
        ]
        for f in figuras:
            self.addPage(f())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.book.addChapter(curvas_superficies())
    visor.whichChapter = 0
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notesStack.show()
    sys.exit(app.exec_())

