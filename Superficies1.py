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
from superficie.Plot3D import Plot3D, RevolutionPlot3D,ParametricPlot3D
from superficie.gui import Slider, SpinBox

class Plano1(Page):
    def __init__(self):
        "El plano x + y + z - 2.5 = 0"
        Page.__init__(self, "Plano")

        plano = Plot3D(lambda x,y: 2.5-x-y, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(2.5-x-y), (-1,1),(-1,1))
        plano1.drawStyle.style = SoDrawStyle.LINES
        plano1.setDiffuseColor((1,0,0))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)


class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        par = RevolutionPlot3D(lambda r,t: r**2 +1,(0,1),(0,2*pi))
        par1 = RevolutionPlot3D(lambda r,t: h*(r**2 +1),(0,1),(0,2*pi))
        par1.drawStyle.style = SoDrawStyle.LINES
        par1.setDiffuseColor((1,0,0))
        disco = RevolutionPlot3D(lambda r,t: 0 ,(0,2),(0,2*pi))
        self.addChild(par)
        self.addChild(par1)
        self.addChild(disco)

class ParaboloideHiperbolico(Page):
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        plano = Plot3D(lambda x,y: x**2 - y**2+1, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(x**2 - y**2+1), (-1,1),(-1,1))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)

class LasilladelMono(Page):
    def __init__(self):
        "x^3 - 3xy^2 - z = 0"
        Page.__init__(self, u"La silla del mono")

        plano = Plot3D(lambda x,y: x**3 - 3*x*y**2 +2.5, (-1,1),(-1,1))
        plano.setScaleFactor((1,1,.6))

#        def setXscale(t):
#            scale.scaleFactor = (1,1,t)
#        Slider(
#            rangep=('z', .2, 1, 1,  20),
#            func=setXscale,
#            parent=self
#        )
#


        plano1 = Plot3D(lambda x,y: h*(x**3 - 3*x*y**2 + 2.5), (-1,1),(-1,1))
        plano1.setScaleFactor((1,1,.6))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)

class Superficiecuartica(Page):
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cuártica")

#        plano = Plot3D(lambda x,y: x**4 + 2*x**2*y**2 + y**4 + 1, (-1,1),(-1,1))
        plano = RevolutionPlot3D(lambda r,t: r**4 + 1,(0,1),(0,2*pi))
#        plano.setScaleFactor((1,1,.6))
        plano1 = RevolutionPlot3D(lambda r,t: h*(r**4 + 1),(0,1),(0,2*pi))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)

class Conoderevolucion(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Cono de Revolución")

        plano = RevolutionPlot3D(lambda r,t: r + 1,(0,1),(0,2*pi))
        plano1 = RevolutionPlot3D(lambda r,t: h*(r + 1),(0,1),(0,2*pi))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(cuadrado)

class Esfera(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Esfera")

        plano = ParametricPlot3D(lambda t,f: (sin(t)*cos(f),sin(t)*sin(f),cos(t) + 1.5) , (0,pi),(0,2*pi))
        cuadrado = Plot3D(lambda x,y: 0, (-2,2),(-2,2))
        self.addChild(plano)
        self.addChild(cuadrado)

class Helicoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Helicoide")

        plano1 = ParametricPlot3D(lambda u,v: (sinh(v)*cos(u),sinh(v)*sin(u),u), (-pi,pi,60),(-2,2))
        plano1.setVerticesPerColumn(2)

        ## Esto no funciona por la forma en que se toma la lista de puntos
#        quad.mesh.verticesPerRow = 15

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = plano1.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )
        self.addChild(plano1)

class Catenoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Catenoide")

        plano = ParametricPlot3D(lambda u,v: (cosh(v)*cos(u),cosh(v)*sin(u),v),(0,2*pi,60),(-1,1))
        plano.setVerticesPerColumn(2)

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = plano.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )

        self.addChild(plano)


figuras = [
    Plano1,
    ParaboloideEliptico,
    ParaboloideHiperbolico,
    LasilladelMono,
    Superficiecuartica,
    Conoderevolucion,
    Esfera,
    Helicoide,
    Catenoide
    ]

class Superficies1(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Superficies")
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

