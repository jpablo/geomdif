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

from superficie.base import Chapter, Page, BasePlane
from superficie.Plot3D import Plot3D, RevolutionPlot3D,ParametricPlot3D, RevolutionParametricPlot3D
from superficie.gui import Slider, SpinBox
from superficie.VariousObjects import Sphere
from superficie.util import Vec3

class Plano1(Page):
    def __init__(self):
        "El plano x + y + z - 2.5 = 0"
        Page.__init__(self, "Plano")

        plano = Plot3D(lambda x,y: -x-y, (-1,1),(-1,1))
        plano1 = ParametricPlot3D(lambda x,y: (x,y,h1*(-x-y) + (1-h1)*(-2)), (-.5,.5),(-.5,.5))
        plano2 = ParametricPlot3D(lambda x,z: (x,h2*(-x-z) + (1-h2)*(-2),z), (-.5,.5),(-.5,.5))
        plano3 = ParametricPlot3D(lambda y,z: (h3*(-y-z) + (1-h3)*(-2),y,z), (-.5,.5),(-.5,.5))
        for p in [plano1,plano2,plano3]:
            p.setLinesVisible(True)
            p.setMeshVisible(False)
#        plano1.setDiffuseColor((1,0,0))
        plano2.setMeshDiffuseColor((0,1,0))
        plano3.setMeshDiffuseColor((0,0,1))
        plano.setDiffuseColor((252. / 255, 144. / 255 , 0. / 255 ))
        self.setupPlanes((-2,2,7))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(plano2)
        self.addChild(plano3)


class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        z = 0.5
        par = RevolutionPlot3D(lambda r,t: r**2+z,(0,1),(0,2*pi))
        par1 = RevolutionPlot3D(lambda r,t: h*(r**2 +z),(0,1),(0,2*pi))
        par1.setLinesVisible(True)
        par1.setMeshVisible(False)
        par.setDiffuseColor((145. / 255, 61. / 255 , 74. / 255 ))
        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        self.addChild(par)
        self.addChild(par1)
        self.addChild(baseplane)

class ParaboloideHiperbolico(Page):
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        z = 1.5
        parab = Plot3D(lambda x,y: x**2 - y**2+z, (-1,1),(-1,1))
        parab1 = Plot3D(lambda x,y: h*(x**2 - y**2+z), (-1,1),(-1,1))
        parab1.setLinesVisible(True)
        parab1.setMeshVisible(False)
        parab.setDiffuseColor((127./255,119./255,20./255))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        self.addChild(parab)
        self.addChild(parab1)
        self.addChild(baseplane)

class LasilladelMono(Page):
    def __init__(self):
        "x^3 - 3xy^2 - z = 0"
        Page.__init__(self, u"La silla del mono")

        silla = Plot3D(lambda x,y: x**3 - 3*x*y**2 +2.5, (-1,1),(-1,1))
        silla.setDiffuseColor((151./255,139./255,125./255))
        silla.setEmissiveColor((151./255,139./255,125./255))
        silla.setAmbientColor((151./255,139./255,125./255))
#        silla.setShininess(1)
#        plano.setScaleFactor((1,1,.6))

        def cVec(pto):
            "pto: Vec3"
            return pto*1.1
        silla.addVectorField(cVec)

#        def setXscale(t):
#            scale.scaleFactor = (1,1,t)
#        Slider(
#            rangep=('z', .2, 1, 1,  20),
#            func=setXscale,
#            parent=self
#        )
#


        silla1 = Plot3D(lambda x,y: h*(x**3 - 3*x*y**2 + 2.5), (-1,1),(-1,1))
#        silla1.setScaleFactor((1,1,.6))
        silla1.setLinesVisible(True)
        silla1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))

        self.addChild(silla)
        self.addChild(silla1)
        self.addChild(baseplane)

class Superficiecuartica(Page):
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cuártica")

#        cuart = Plot3D(lambda x,y: x**4 + 2*x**2*y**2 + y**4 + 1, (-1,1),(-1,1))
        cuart = RevolutionPlot3D(lambda r,t: r**4 + 1,(0,1),(0,2*pi))
#        cuart.setScaleFactor((1,1,.6))
        cuart1 = RevolutionPlot3D(lambda r,t: h*(r**4 + 1),(0,1),(0,2*pi))
        cuart1.setLinesVisible(True)
        cuart1.setMeshVisible(False)
        cuart.setDiffuseColor((149./255,24./255,82./255))
        cuart.setAmbientColor((149./255,24./255,82./255))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))
        self.addChild(cuart)
        self.addChild(cuart1)
        self.addChild(baseplane)

class Conoderevolucion(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Cono de Revolución")

        cono = RevolutionPlot3D(lambda r,t: r + 1,(0,1),(0,2*pi))
        cono1 = RevolutionPlot3D(lambda r,t: h*(r + 1),(0,1),(0,2*pi))
        cono1.setLinesVisible(True)
        cono1.setMeshVisible(False)
        cono.setDiffuseColor((161./255,244./255,92./255))
        cono.setAmbientColor((161./255,244./255,92./255))
        cono.setEmissiveColor((161./255,244./255,92./255))


        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))
        self.addChild(cono)
        self.addChild(cono1)
        self.addChild(baseplane)

class Esfera(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Esfera")

        r = .998
        esf = ParametricPlot3D(lambda t,f: (r*sin(t)*cos(f),r*sin(t)*sin(f),r*cos(t)) , (0,pi,70),(0,2*pi,70))

        esf.setDiffuseColor((216./255,217./255,211./255))
        esf.setAmbientColor((216./255,217./255,211./255))
#        esf.setEmissiveColor((216./255,217./255,211./255))
        
        def proyK(x,y):
            den = x**2+y**2+1-2*k+k**2
            return ((-2*x*(k-1))/den, (-2*y*(k-1))/den, 1 + 2*(k-1)*(1-k)/den)

        def proyZm1(u,v):
            "proy desde el polo norte al plano z=-1"
            den = u**2+v**2+4
            x = u - t*(u-4*u/den)
            y = v - t*(v-4*v/den)
            z = -1 -t*(-2+8/den)
            return (x,y,z)

        def proyZ1(u,v):
            "proy desde el polo sur al plano z=1"
            den = u**2+v**2+4
            x = u - t*(u-4*u/den)
            y = v - t*(v-4*v/den)
            z = 1 -t*(2-8/den)
            return (x,y,z)

        def proyC(r,t):
            return (2*r / (r**2+1), t, (r**2-1) / (r**2+1))
        def proyCz0(r,t):
            return (r, t, 0)

        stereo = ParametricPlot3D(proyZm1, (-3,3,70),(-3,3,70))
        stereo.setLinesVisible(True)
        stereo.setMeshVisible(False)
        stereo.setMeshDiffuseColor((248./255,45./255,50./255))
        stereo2 = ParametricPlot3D(proyZ1, (-3,3,70),(-3,3,70))
        stereo2.setLinesVisible(True)
        stereo2.setMeshVisible(False)
        stereo2.setMeshDiffuseColor((2./255,96./255,200./255))

        baseplane = BasePlane()
        baseplane.setHeight(-1.005)
        baseplane.setRange((-4,4,7))
        self.addChild(esf)
        self.addChild(stereo2)
        self.addChild(stereo)
        self.addChild(baseplane)

class Helicoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Helicoide")

        helic1 = ParametricPlot3D(lambda u,v: (sinh(v)*cos(u),sinh(v)*sin(u),u), (-pi,pi,60),(-2,2))
        helic1.setVerticesPerColumn(2)

        helic1.setDiffuseColor((202./255,78./255,70./255))
        helic1.setAmbientColor((202./255,78./255,70./255))

        ## Esto no funciona por la forma en que se toma la lista de puntos
#        quad.mesh.verticesPerRow = 15

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = helic1.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )
        self.addChild(helic1)

class Catenoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Catenoide")

        cat = ParametricPlot3D(lambda u,v: (cosh(v)*cos(u),cosh(v)*sin(u),v),(0,2*pi,60),(-1,1))
        cat.setVerticesPerColumn(2)

        cat.setDiffuseColor((4./255,73./255,143./255))
        cat.setAmbientColor((4./255,73./255,143./255))

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = cat.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )

        self.addChild(cat)


figuras = [
    Plano1,
    ParaboloideEliptico,
    ParaboloideHiperbolico,
    LasilladelMono,
    Superficiecuartica,
    Conoderevolucion,
    Esfera,
    Helicoide,
    Catenoide,
    ]

class Superficies1(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Superficies I")
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

