# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, PointSet
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
    u"""
      La función tangente establece un <b>difeomorfismo</b> entre un segmento
      abierto y la totalidad de los números reales. La gráfica de un periodo
      es una curva infinitamente diferenciable que admite dos asíntotas:
      una a la izquierda y otra a la derecha. Una <b>asíntota</b> de una curva es
      una recta a la cual la curva se acerca tanto como se quiera, sin
      cortarla y teniendo a la recta como límite de la posición de sus
      tangentes cuando la norma de <b>(x, tan x)</b> tiende a infinito.
    """

    def __init__(self):
        PlanePage.__init__(self, u'Gráfica de la tangente<br>&alpha;(x)=(x,tan x)')
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
    u"""
      El valor absoluto es una función continua, pero no es diferenciable
      en <b>0</b> pues a la izquierda del origen su gráfica tiene pendiente
      constante <b>–1</b> y a la derecha tiene pendiente constante <b>+1</b>,
      por eso no existe el vector tangente en <b>(0,0)</b>.
    """

    def __init__(self):
        PlanePage.__init__(self, u"Gráfica del valor absoluto<br>&alpha;(x)=(x, |x|)")

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
    u"""
      <p>
      Esta curva parametrizada tiene bien definido el vector tangente para
      cualquier valor del parámetro. Sin embargo, en el punto de corte hay dos
      vectores tangentes distinguidos por el parámetro, de modo que la traza
      de la curva no es admisible como <b>1-variedad diferenciable</b>.
      <p>
      La interacción muestra cómo cambia la magnitud del vector tangente
      porque la curva no se recorre con velocidad constante.
      Cuando la velocidad tiene <b>norma constante 1</b> se dice que el
      parámetro es la <b>longitud de arco</b>.
    """

    def __init__(self):
        PlanePage.__init__(self, u"Curva diferenciable con autointersección<br>&alpha;(t)=(t<sup>3</sup>-4t, t<sup>2</sup>-4)")

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
