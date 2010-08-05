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

from superficie.Book import Chapter, Page
from superficie.Plot3D import Plot3D, ParametricPlot3D
from superficie.gui import Slider
from superficie.VariousObjects import Sphere, TangentPlane, TangentPlane2
from superficie.util import Vec3, _1

class Elipsoide(Page):
    def __init__(self):
        Page.__init__(self, u"Elipsoide")
        param = lambda u,v: (cos(u)*cos(v), 1.5*cos(v)*sin(u), 2*sin(v))
        elipsoide = ParametricPlot3D(param, (-pi, pi), (-pi/2,pi/2))
        col = _1(84,129,121)
        elipsoide.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)
        self.addChild(elipsoide)
        par1 = lambda u,v: Vec3(-sin(u)*cos(v), 1.5*cos(u)*cos(v), 0)
        par2 = lambda u,v: Vec3(-cos(u)*sin(v), -1.5*sin(u)*sin(v), 2*cos(v))
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225),visible=True,parent=self)
        Slider(rangep=('u', -pi,pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('v', -pi/2,pi/2,0,20),func=tp.setV,parent=self)

class Cilindro(Page):
    def __init__(self):
        Page.__init__(self, u"Cilindro")
        param = lambda u,t: Vec3(cos(u),sin(u),t)
        cilindro = ParametricPlot3D(param, (0, 2*pi), (-1,1))
        col = _1(177,89,77)
        cilindro.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)
        self.addChild(cilindro)
        def par1(u,t): return Vec3(-sin(u),cos(u),0)
        def par2(u,t): return Vec3(0,0,1)
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225),visible=True,parent=self)
        tp.localOriginSphere.hide()
        tp.localYAxis.setColor(col).setWidth(2).show()
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

#        delta = 0
#        p_eli = Sphere((.9571067805, .9571067805, .35+delta),0.02,visible=True)
#        p_eli.setColor( _1(194,38,69))
#        p_eli.setShininess(1)
#
#        p_par = Sphere ((-0.7071067810, 0.7071067810, 0.5+delta),0.02,visible=True)
#        p_par.setColor( _1(240,108,21))
#        p_par.setShininess(1)
#
#        p_hyp = Sphere ((0, -0.6464466095, .3535+delta),0.02,visible=True)
#        p_hyp.setColor( _1(78,186,69))
#        p_hyp.setShininess(1)

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))

## plano elíptico

        def eliv(v,t):
            return Vec3(-1./4*sin(v)*2**(1/2.), -1./4*sin(v)*2**(1/2.), .5*cos(v))
        def eliu(t,u):
            return Vec3(-(1+1./4*2**(1/2.))*sin(u), (1+1./4*2**(1/2.))*cos(u), 0)

        ptoeli = (pi/4,pi/4)
        plane_eli = TangentPlane2(toroParam1,toro_u,toro_v,ptoeli,_1(252,250,225),visible=True)

## plano parabólico

        def parv(v,t):
            return Vec3(1./4*sin(v)*2**(1./2),-1./4*sin(v)*2**(1./2),.5*cos(v))
        def paru(t,u):
            return Vec3(-sin(u), cos(u),0)

        ptopar = (3*pi/4,pi/2)
        plane_par = TangentPlane2(toroParam1,toro_u,toro_v,ptopar,_1(252,250,225),visible=True)

## plano hyperbólico

        def hypv(v,t):
            return Vec3(0, .5*sin(v), .5*cos(v))
        def hypu(u,t):
            return Vec3(-(1-1./4*2**(1/2.))*sin(u), (1-1./4*2**(1/2.))*cos(u), 0)

        ptohyp = (6*pi/4, 3*pi/4)
        plane_hyp = TangentPlane2(toroParam1,toro_u,toro_v,ptohyp,_1(252,250,225),visible=True)

        self.addChild(toro)
#        self.addChild(p_eli)
#        self.addChild(p_par)
#        self.addChild(p_hyp)
        self.addChild(plane_eli)
        self.addChild(plane_par)
        self.addChild(plane_hyp)

figuras = [
    Elipsoide,
    Cilindro,
    Toro
    ]

class Superficies3(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Superficies III")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies3())
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

