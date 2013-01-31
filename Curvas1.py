# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, Bundle2, Bundle3, PointSet#, Sphere, Arrow
from superficie.book import Chapter, Page
from superficie.util import Vec3, _1, partial
#from superficie.util import intervalPartition
#from superficie.gui import onOff, CheckBox, Button, SpinBox
from superficie.widgets import VisibleCheckBox, Slider, SpinBox
from superficie.plots import ParametricPlot3D
from superficie.viewer.Viewer import Viewer
from superficie.animations import AnimationGroup

def esfera(col):
    sep = SoSeparator()

#    comp = SoComplexity()
#    comp.value.setValue(1)
#    comp.textureQuality.setValue(0.9)

    esf = SoSphere()
    esf.radius = 2.97

    light = SoShapeHints()
    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
    light.FaceType = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor = col
    mat.diffuseColor = col
    mat.transparency.setValue(0.4)

    trans = SoTransparencyType()
#    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND
    trans.value = SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND
#    trans.value = SoTransparencyType.DELAYED_BLEND

#    sep.addChild(comp)
    sep.addChild(light)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(esf)

    return sep

class Tangente(Page):
    u"""La función tangente establece <b>una biyección</b> <b>entre un segmento abierto y la totalidad de los números reales.</b>
    La gráfica de un periodo es una curva infinitamente diferenciable que admite dos <i>asíntotas</i>:
    una a la izquierda y otra a la derecha. Asíntota de una curva es una recta a la cual la curva se acerca tanto como
    se quiera, sin cortarla y teniendo a la recta como límite de la posición de sus tangentes cuando la norma de $(y,
    tan y)$ tiende a infinito.
    """

    def __init__(self):
        super(Tangente,self).__init__('Tangente')
        self.showAxis(True)
        self.axis_z.setVisible(False)
        npuntos = 100
        delta = .2

        def Tan(t):
            return Vec3(t, tan(t), 0)
        def Derivada(t):
            return Vec3(1, 1 / cos(t) ** 2, 0)

        # Los fragmentos de las curvas
        rango = [
            (-pi, -pi / 2 - delta, npuntos),
            (-pi / 2 + delta, pi / 2 - delta, npuntos),
            (pi / 2 + delta, pi, npuntos)
        ]
        curva1 = Curve3D(Tan, rango, width=2).setBoundingBox((-5, 5), (-5, 5))
        self.addChild(curva1)

        ## Asíntotas
        self.addChild(Line([(-pi / 2, -5, 0), (-pi / 2, 5, 0)], color=(1, .5, .5)))
        self.addChild(Line([(pi / 2, -5, 0), (pi / 2, 5, 0)], color=(1, .5, .5)))

        tangente = curva1.attachField("tangente", Derivada)
        tangente.add_tail(radius = 0.08)
        self.setupAnimations([tangente])

    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))

    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))

    # Dibuja la loxodroma y la esfera

class ValorAbsoluto(Page):
    u"""El valor absoluto es una función continua de su variable pero
    <b>no diferenciable en $0$</b> pues a la  izquierda del origen su gráfica tiene pendiente constante
    $-1$ y a la derecha su pendiente es constante $1$, por eso no puede existir el vector tangente en $(0,0)$."""
    def __init__(self):
        Page.__init__(self, u"Valor absoluto")
        self.showAxis(True)
        self.axis_z.setVisible(False)

        def Abs(t):
            return Vec3(t, abs(t), 0)

        def Derivada(t):
            dt = -1 if t < 0 else 1
            return Vec3(1, dt, 0)

        curva1 = Curve3D(Abs, (-3, 3, 100), width=2)
        curva1.setBoundingBox((-5, 5), (-5, 5))
        self.addChild(curva1)

        tangente = curva1.attachField("tangente", Derivada)
        tangente.add_tail(radius = 0.08)
        self.setupAnimations([tangente])

    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))

    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))

class Cusp(Page):
    u"""Esta curva parametrizada tiene bien definido el vector tangente para cualquier valor del parámetro, pero
    en el punto de corte hay dos vectores tangentes, distinguidos por el parámetro. <b>La traza de la curva no es admisible como $1$-variedad diferenciable</b>.
    """
    def __init__(self):
        Page.__init__(self, u"Curva diferenciable con autointersección")
        self.showAxis(True)
        self.axis_z.setVisible(False)
        def cusp(t): return Vec3(t ** 3 - 4 * t, t ** 2 - 4, 0)
        curva1 = Curve3D(cusp, (-2.5, 2.5, 200), width=2)
        self.addChild(curva1)
        tangente = curva1.attachField("tangente", lambda t: Vec3(-4 + 3 * t ** 2, 2 * t, 0))
        tangente.add_tail(radius = 0.08)
        self.setupAnimations([tangente])

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
        Page.__init__(self, "Alabeada")
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

class Curvas1(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Ejemplos de curvas planas")

        figuras = [
            Tangente,
            ValorAbsoluto,
            Cusp,
            Alabeada,
        ]
        for f in figuras:
            self.addPage(f())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(Curvas1())
    visor.whichChapter = 0
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notasStack.show()
    sys.exit(app.exec_())

