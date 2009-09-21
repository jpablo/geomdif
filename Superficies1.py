# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic
from pivy.coin import *
from math import *
try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.base import Chapter, Page
from superficie.Plot3D import Plot3D, RevolutionPlot3D

class Plano1(Page):
    def __init__(self):
        "El plano x + y + z – 6 = 0"
        Page.__init__(self, "Plano")

        plano = Plot3D(lambda x,y: 2.5-x-y, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(2.5-x-y), (-1,1),(-1,1))
        cuadrado = Plot3D(lambda x,y: 0, (-1,1),(-1,1))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)


class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + z^2 – y = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        par = RevolutionPlot3D(lambda r,t: r**2 +1,(0,1),(0,2*pi))
        par1 = RevolutionPlot3D(lambda r,t: h*(r**2 +1),(0,1),(0,2*pi))
        disco = RevolutionPlot3D(lambda r,t: 0 ,(0,1),(0,2*pi))
        self.addChild(par)
        self.addChild(par1)
        self.addChild(disco)

class ParaboloideHiperbolico(Page):
    def __init__(self):
        "x^2 - z^2 – y = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        plano = Plot3D(lambda x,y: x**2 - y**2+1, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(x**2 - y**2+1), (-1,1),(-1,1))
        cuadrado = Plot3D(lambda x,y: 0, (-1,1),(-1,1))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)


figuras = [Plano1, ParaboloideEliptico, ParaboloideHiperbolico]

class Superficies1(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Curvas")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies1())
    visor.getChapterObject().chapterSpecificIn()
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

