# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, Bundle2, Bundle3, PointSet
from superficie.book import Chapter, Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import VisibleCheckBox, Slider, SpinBox
from superficie.plots import ParametricPlot3D
from superficie.animations import AnimationGroup


class PlanePage(Page):
    def __init__(self, name):
        Page.__init__(self, name)
        self.camera_position = (0, 0, 13)
        self.camera_point_at = [SbVec3f(0, 0, 0), SbVec3f(0, 1, 0)]
        self.showAxis(True)
        self.axis_z.setVisible(False)


class Tangente(PlanePage):
    u"""La función tangente establece <b>una biyección</b> <b>entre un segmento abierto y la totalidad de los \
    números reales.</b>
    La gráfica de un periodo es una curva infinitamente diferenciable que admite dos <i>asíntotas</i>:
    una a la izquierda y otra a la derecha. Asíntota de una curva es una recta a la cual la curva se acerca tanto como
    se quiera, sin cortarla y teniendo a la recta como límite de la posición de sus tangentes cuando la norma de $(y,
    tan y)$ tiende a infinito.
    """

    def __init__(self):
        PlanePage.__init__(self, 'Tangente')
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
        tangente.add_tail(radius=0.08)
        self.setupAnimations([tangente])


class ValorAbsoluto(PlanePage):
    u"""El valor absoluto es una función continua de su variable pero
    <b>no diferenciable en $0$</b> pues a la  izquierda del origen su gráfica tiene pendiente constante
    $-1$ y a la derecha su pendiente es constante $1$, por eso no puede existir el vector tangente en $(0,0)$."""

    def __init__(self):
        PlanePage.__init__(self, u"Valor absoluto")

        def Abs(t):
            return Vec3(t, abs(t), 0)

        def Derivada(t):
            dt = -1 if t < 0 else 1
            return Vec3(1, dt, 0)

        curva1 = Curve3D(Abs, (-3, 3, 100), width=2)
        curva1.setBoundingBox((-5, 5), (-5, 5))
        self.addChild(curva1)

        tangente = curva1.attachField("tangente", Derivada)
        tangente.add_tail(radius=0.08)
        self.setupAnimations([tangente])


class Cusp(PlanePage):
    u"""Esta curva parametrizada tiene bien definido el vector tangente para cualquier valor del parámetro, pero
    en el punto de corte hay dos vectores tangentes, distinguidos por el parámetro. <b>La traza de la curva no es
    admisible como $1$-variedad diferenciable</b>.
    """

    def __init__(self):
        PlanePage.__init__(self, u"Curva diferenciable con autointersección")

        def cusp(t):
            return Vec3(t ** 3 - 4 * t, t ** 2 - 4, 0)
        curve1 = Curve3D(cusp, (-2.5, 2.5, 200), width=2)
        self.addChild(curve1)
        tangent = curve1.attachField("tangente", lambda t: Vec3(-4 + 3 * t ** 2, 2 * t, 0))
        tangent.add_tail(radius=0.08)
        self.setupAnimations([tangent])


class Curvas1(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas planas")

        pages = [
            Tangente,
            ValorAbsoluto,
            Cusp
        ]
        for f in pages:
            self.addPage(f())

if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.book.addChapter(Curvas1())
    visor.whichChapter = 0
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notesStack.show()
    sys.exit(app.exec_())
