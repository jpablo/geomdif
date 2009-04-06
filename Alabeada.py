# -*- coding: utf-8 -*-
import sys
from pivy.coin import *
from pivy.gui.soqt import *
from PyQt4 import QtCore, QtGui
from math import *
from superficie.VariousObjects import Sphere, Tube, Line, Bundle, Base, Page
from superficie.util import intervalPartition, wrap, Vec3, conectaParcial,  \
    genIntervalPartition, partial, conecta
from superficie.gui import onOff, CheckBox, Slider
from superficie.animation import Timer


class Alabeada(Page):
    def __init__(self,parent = None):
        Page.__init__(self, parent, "Alabeada")
        self.addChild(alabeada())


class alabeada(Base):
    def __init__(self, parent=None):
        Base.__init__(self, "Alabeada")
        ## ============================
        c   = lambda t: Vec3(t,t**2,t**3)
        cp  = lambda t: Vec3(1,2*t,3*t**2)
        cpp = lambda t: Vec3(0,2,6*t)
        ## ============================
        tmin = -1
        tmax = 1
        puntos = intervalPartition([tmin,tmax,50], c)
        xy = [(p[0],p[1],tmin**3)  for p in puntos]
        yz = [(tmin,p[1],p[2])     for p in puntos]
        xz = [(p[0],tmin**2,p[2])  for p in puntos]
        ## ============================
        curva = Line(puntos, width=3, nvertices = 1)
        self.addChild(curva)
        ## ============================
        lxy = Line(xy,(1,1,0), nvertices=1)
        lyz = Line(yz,(0,1,1), nvertices=1)
        lxz = Line(xz,(1,0,1), nvertices=1)
        ## ============================
        def setNumVertices(n):
            for f in [curva, lxy, lyz, lxz]:
                f.setNumVertices(n)
            self.parent.viewAll()
        ## ============================
        timeline = QtCore.QTimeLine(2000)
        timeline.setCurveShape(timeline.LinearCurve)
        timeline.setFrameRange(0, 50)
        conecta(timeline, QtCore.SIGNAL("frameChanged(int)"), setNumVertices)
        self.addWidget(CheckBox(self, timeline.start, lambda:setNumVertices(1), "inicio"))
        self.addWidgetChild(onOff(lxy, u"proyección en el plano xy"))
        self.addWidgetChild(onOff(lyz, u"proyección en el plano yz"))
        self.addWidgetChild(onOff(lxz, u"proyección en el plano xz"))
        ## ============================
        tang = Bundle(c, cp,  (tmin, tmax, 50), (1,.5,.5), .6)
        cot  = Bundle(c, cpp, (tmin, tmax, 50), (1,.5,.5), .2)
        self.addWidgetChild(onOff(tang, "1a derivada", False))
        self.addWidgetChild(onOff(cot,  "2a derivada", False))
        ## ============================
        self.addWidget(Slider(rangep=('w', .2, 1, 1,  20),
            func=lambda t:(tang.setLengthFactor(t) or cot.setLengthFactor(t))))




if __name__ == "__main__":
    from superficie.util import main
    from superficie.Viewer import Viewer

    app = main()
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter()
    ## ============================
    visor.addPageChild(Alabeada())
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
#    visor.trackCameraPosition(True)
    SoQt.mainLoop()
