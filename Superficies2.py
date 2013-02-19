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

from superficie.nodes import Sphere, BasePlane, Line, Curve3D
from superficie.book import Chapter, Page
from superficie.plots import Plot3D, RevolutionPlot3D
from superficie.util import _1, Vec3, intervalPartition

class ParaboloideHiperbolico(Page):
    u"""Para el paraboloide hiperbólico, el plano tangente en cada punto corta a la superficie
               en dos rectas y hay parte de la superficie en cada uno de los semiespacios definidos
               por él. Hay curvas en la superficie cuyos vectores de aceleración apuntan a lados distintos
              del plano tangente.
    """
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




figuras = [
    ParaboloideHiperbolico,
    ]

class Superficies2(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Plano tangente")
        for f in figuras:
            self.addPage(f())
        self.whichPage = 0

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
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

