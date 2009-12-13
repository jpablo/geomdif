# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pivy.coin import *
from math import *
try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.base import Chapter, Page, BasePlane
from superficie.Plot3D import Plot3D, RevolutionPlot3D,ParametricPlot3D, RevolutionParametricPlot3D
from superficie.gui import Slider, SpinBox
from superficie.VariousObjects import Sphere
from superficie.util import Vec3, _1


class Plano(Page):
    def __init__(self):
        "El plano x + y + z - 2.5 = 0"
        Page.__init__(self, "Plano")
        plano = Plot3D(lambda x,y: -x-y, (-1,1),(-1,1))
        self.setupPlanes((-2,2,7))
        self.addChild(plano)


class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        z = 0.5
        par = RevolutionPlot3D(lambda r,t: r**2+z,(0,1),(0,2*pi))
        par.setAmbientColor(_1(145, 61 , 74 ))
        par.setDiffuseColor(_1(145, 61 , 74 ))
        par.setSpecularColor(_1(145, 61 , 74 ))
        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        self.addChild(par)
        self.addChild(baseplane)

class ParaboloideHiperbolico(Page):
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        z = 1.5
        parab = Plot3D(lambda x,y: x**2 - y**2+z, (-1,1),(-1,1))
        parab.setAmbientColor(_1(145, 61 , 74 ))
        parab.setDiffuseColor(_1(127,119,20))
        parab.setSpecularColor(_1(145, 61 , 74 ))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        self.addChild(parab)
        self.addChild(baseplane)


class Superficiecuartica(Page):
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cuártica")

        cuart = RevolutionPlot3D(lambda r,t: r**4 + 1,(0,1),(0,2*pi))
        cuart.setDiffuseColor(_1(168,211,8))
        cuart.setSpecularColor(_1(168,211,8))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))
        self.addChild(cuart)
        self.addChild(baseplane)


figuras = [
    Plano,
    ParaboloideEliptico,
    ParaboloideHiperbolico,
    Superficiecuartica
    ]

class Superficies2(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Superficies II")
        for f in figuras:
            self.addPage(f())
        self.whichPage = 0

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies2())
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

