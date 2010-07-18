# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from superficie.VariousObjects import Sphere
from pivy.coin import *
from math import *
try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.VariousObjects import BasePlane
from superficie.Book import Chapter, Page
from superficie.Plot3D import Plot3D, RevolutionPlot3D
from superficie.util import _1


class Plano(Page):
    def __init__(self):
        "El plano x + 2y + 3z - 4 = 0"
        Page.__init__(self, "Plano")
        plano = Plot3D(lambda x,y: (-x-2*y+4)/3, (-3,3),(-3,3))
        plano.setMeshDiffuseColor(_1(240,170,69))
        self.setupPlanes((-2,2,7))

        p_1 = Sphere((1, 2, -1./3),0.02,visible=True)
        p_1.setColor( _1(116,112,35))
        p_1.setShininess(1)
        
        p_2 = Sphere((2, -2, 2),0.02,visible=True)
        p_2.setColor( _1(214,44,109))
        p_2.setShininess(1)
        
#        pun2_1 = [[-3t/2, sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
#        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)
#        recta2_1

        p_3 = Sphere((-1, 1, 1),0.02,visible=True)
        p_3.setColor( _1(52,171,215))
        p_3.setShininess(1)

        self.addChild(plano)
        self.addChild(p_1)
        self.addChild(p_2)
        self.addChild(p_3)

class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        z = 0.5
        par = RevolutionPlot3D(lambda r,t: r**2+z,(0,1),(0,2*pi))
        par.setAmbientColor(_1(157, 168, 136 ))
        par.setDiffuseColor(_1(157, 168, 136 ))
        par.setSpecularColor(_1(157, 168, 136 ))
        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        p_1 = Sphere((2**(0.5), 3**(0.5), 5),0.02,visible=True)
        p_1.setColor( _1(178, 194, 9))
        p_1.setShininess(1)

        p_2 = Sphere((1, 1, 2),0.02,visible=True)
        p_2.setColor( _1(184, 126, 42))
        p_2.setShininess(1)

        self.addChild(par)
        self.addChild(baseplane)
        self.addChild(p_1)
        self.addChild(p_2)

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

