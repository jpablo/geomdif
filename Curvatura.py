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
from superficie.VariousObjects import Sphere, TangentPlane, TangentPlane2
from superficie.util import Vec3, _1

class Elipsoide(Page):
    def __init__(self):
        Page.__init__(self, u"Elipsoide")
        param = lambda u,v: (cos(u)*cos(v), 1.5*cos(v)*sin(u), 2*sin(v))
        elipsoide = ParametricPlot3D(param, (-pi, pi), (-pi/2,pi/2))
        self.addChild(elipsoide)
        def par1(u,v):
            return Vec3(-sin(u)*cos(v), 1.5*cos(u)*cos(v), 0)
        def par2(u,v):
            return Vec3(-cos(u)*sin(v), -1.5*sin(u)*sin(v), 2*cos(v))
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225),visible=True,parent=self)
        Slider(rangep=('u', -pi,pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('v', -pi/2,pi/2,0,20),func=tp.setV,parent=self)

class Cilindro(Page):
    def __init__(self):
        Page.__init__(self, u"Cilindro")
        param = lambda u,t: (cos(u),sin(u),t)
        cilindro = ParametricPlot3D(param, (0, 2*pi), (-1,1))
        self.addChild(cilindro)
        def par1(u,t):
            return Vec3(-sin(u),cos(u),0)
        def par2(u,t):
            return Vec3(0,0,1)
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225),visible=True,parent=self)
        Slider(rangep=('u', 0,2*pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('t', -1,1,0,20),func=tp.setV,parent=self)


class Toro(Page):
    def __init__(self):
        Page.__init__(self, u"Toro")
        a = 1
        b = 0.5

        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        toro = ParametricPlot3D(toroParam1,(0,2*pi,150),(0,2*pi,100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        delta = 0
        p_eli = Sphere((.9571067805, .9571067805, .35+delta),0.02,visible=True)
        p_eli.setColor( _1(194,38,69))
        p_eli.setShininess(1)

        p_par = Sphere ((-0.7071067810, 0.7071067810, 0.5+delta),0.02,visible=True)
        p_par.setColor( _1(240,108,21))
        p_par.setShininess(1)

        p_hyp = Sphere ((0, -0.6464466095, .3535+delta),0.02,visible=True)
        p_hyp.setColor( _1(78,186,69))
        p_hyp.setShininess(1)

        def toro_u(u,v):
            return Vec3(-(1+0.5*cos(v))*sin(u), (1+0.5*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-0.5*sin(v)*cos(u), 0.5*sin(v)*sin(u), 0.5*cos(v))

## plano elíptico

        def eliv(v):
            return Vec3(-1./4*sin(v)*2**(1/2.), -1./4*sin(v)*2**(1/2.), .5*cos(v))
        def eliu(u):
            return Vec3(-(1+1./4*2**(1/2.))*sin(u), (1+1./4*2**(1/2.))*cos(u), 0)

        ptoeli = (pi/4,pi/4)
        plane_eli = TangentPlane(toroParam1,eliu,eliv,ptoeli,_1(252,250,225),visible=True)

## plano parabólico

        def parv(v):
            return Vec3(1./4*sin(v)*2**(1./2),-1./4*sin(v)*2**(1./2),.5*cos(v))
        def paru(u):
            return Vec3(-sin(u), cos(u),0)

        ptopar = (3*pi/4,pi/2)
        plane_par = TangentPlane(toroParam1,paru,parv,ptopar,_1(252,250,225),visible=True)

## plano hyperbólico

        def hypv(v):
            return Vec3(0, .5*sin(v), .5*cos(v))
        def hypu(u):
            return Vec3(-(1-1./4*2**(1/2.))*sin(u), (1-1./4*2**(1/2.))*cos(u), 0)

        ptohyp = (6*pi/4, 3*pi/4)
        plane_hyp = TangentPlane(toroParam1,hypu,hypv,ptohyp,_1(252,250,225),visible=True)


        self.addChild(toro)
        self.addChild(p_eli)
        self.addChild(p_par)
        self.addChild(p_hyp)
        self.addChild(plane_eli)
        self.addChild(plane_par)
        self.addChild(plane_hyp)

figuras = [
    Elipsoide,
    Cilindro,
    Toro
    ]

class Curvatura(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Curvatura")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Curvatura())
    visor.getChapterObject().chapterSpecificIn()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(False)

    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

