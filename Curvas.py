# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from PyQt4 import QtCore
from pivy.coin import *
from pivy.gui.soqt import *
from superficie.VariousObjects import Bundle
from superficie.VariousObjects import Line
from superficie.base import Chapter
from superficie.base import PageContainer
from superficie.util import Vec3
from superficie.util import intervalPartition
from superficie.util import conecta
from superficie.gui import onOff, CheckBox, Slider

## ---------------------------------- CILINDRO ----------------------------------- ##

def cilindro(col, length):
    sep = SoSeparator()

    cyl = SoCylinder()
    cyl.radius.setValue(0.98)
    cyl.height.setValue(length)
    cyl.parts = SoCylinder.SIDES

    light = SoShapeHints()
    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor = col
    mat.diffuseColor = col
    mat.transparency.setValue(0.5)

    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.X
    rot.angle = pi / 2

    trans = SoTransparencyType()
    trans.value = SoTransparencyType.DELAYED_BLEND

    sep.addChild(light)
    sep.addChild(rot)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(cyl)

    return sep

## ---------------------------------- ESFERA--------------------------------- ##

def esfera(col):
    sep = SoSeparator()

    comp = SoComplexity()
    comp.value.setValue(1)
    comp.textureQuality.setValue(0.9)

    esf = SoSphere()
    esf.radius = 2.97

    light = SoShapeHints()
    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor = col
    mat.diffuseColor = col
    mat.transparency.setValue(0.4)

    trans = SoTransparencyType()
    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND

    sep.addChild(comp)
    sep.addChild(light)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(esf)

    return sep
## ------------------------------- HELICE CIRCULAR ------------------------------- ##


# 1 implica primer derivada, 2 implica segunda derivada
def param1hc(t):
    return Vec3(cos(t), sin(t), t)
def param2hc(t):
    return Vec3(-sin(t), cos(t), 1)
def param3hc(t):
    return Vec3(-cos(t), -sin(t), 0)



class HeliceCircular(PageContainer):
    def __init__(self, parent=None):
        PageContainer.__init__(self, u"Hélice Circular")
        self.addChild(self.helicecircular())

    # Dibuja la helice y el cilindro
    def helicecircular(self):
        tmin = -2 * pi
        tmax = 2 * pi
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, 200))]

        haz1hc = Bundle(param1hc, param2hc, (tmin, tmax, 50), (128. / 255, 1, 0), 1.5)
        sep = SoSeparator()

        sep.addChild(Line(puntos, (.8, .8, .8), 2).root)
        sep.addChild(cilindro((1, 0, 0.5), tmax - tmin))
        sep.addChild(haz1hc.root)
        return sep

## ------------------------------- HELICE REFLEJADA ------------------------------- ##

class HeliceReflejada(PageContainer):
    def __init__(self, parent=None):
        PageContainer.__init__(self, u"Hélice Reflejada")
        self.addChild(self.helicereflejada())

    # Dibuja las helices y el cilindro
    def helicereflejada(self):
        tmin = -2 * pi
        tmax = 2 * pi
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, 200))]

        puntitos = [[cos(t), sin(t), -t] for t in intervalPartition((tmin, tmax, 200))]
        haz2hc = Bundle(param1hc, param2hc, (tmin, tmax, 50), (116. / 255, 0, 63. / 255), 1.5)
        sep = SoSeparator()

        sep.addChild(Line(puntos, (1, 1, 1), 2).root)
        sep.addChild(Line(puntitos, (128. / 255, 0, 64. / 255), 2).root)
        sep.addChild(cilindro((7. / 255, 83. / 255, 150. / 255), tmax - tmin))
        sep.addChild(haz2hc.root)

        return sep

## -------------------------------LOXODROMA------------------------------- ##


# La rotacion para poder pintar los meridianos
def rot(ang):
    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.Z
    rot.angle = ang

    return rot

# Dibuja la loxodroma y la esfera

class Loxi(PageContainer):
    def __init__(self, parent=None):
        PageContainer.__init__(self, "Loxodroma")
        self.creaLoxodroma()

    def creaLoxodroma(self):
        tmin = -50 * pi
        tmax = 50 * pi
        pmin = 0
        pmax = 2 * pi
        r = 3
        m = tan(pi / 60)
        t0 = pi / 2

        puntos2 = [[r * cos(t) / cosh(m * (t-t0)), r * sin(t) / cosh(m * (t-t0)), r * tanh(m * (t-t0))] for t in intervalPartition((tmin, tmax, 2000))]
        puntitos2 = [[0, r * cos(t), r * sin(t)] for t in intervalPartition((pmin, pmax, 200))]

        sep = SoSeparator()
        sep.addChild(Line(puntos2, (1, 1, 0), 3).root)
        sep.addChild(esfera((28. / 255, 119. / 255, 68. / 255)))
        mer = Line(puntitos2, (72. / 255, 131. / 255, 14. / 255))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer.root)
        self.addChild(sep)

## ------------------------------------------------------------------------ ##

class Alabeada(PageContainer):
    def __init__(self, parent=None):
        PageContainer.__init__(self, "Alabeada")
        ## ============================
        c   = lambda t: Vec3(t,t**2,t**3)
        cp  = lambda t: Vec3(1,2*t,3*t**2)
        cpp = lambda t: Vec3(0,2,6*t)
        ## ============================
        tmin = -1
        tmax = 1
        npuntos = 50
        puntos = intervalPartition((tmin,tmax,npuntos), c)
        xy = [(p[0],p[1],0)  for p in puntos]
        yz = [(0,p[1],p[2])     for p in puntos]
        xz = [(p[0],0,p[2])  for p in puntos]
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
        timeline.setFrameRange(0, npuntos)
        conecta(timeline, QtCore.SIGNAL("frameChanged(int)"), setNumVertices)
        ## ============================
        cb = CheckBox(self, timeline.start, lambda:setNumVertices(1), "inicio")
        self.addWidget(cb)
        self.addWidgetChild(onOff(lxy, u"proyección en el plano xy"))
        self.addWidgetChild(onOff(lyz, u"proyección en el plano yz"))
        self.addWidgetChild(onOff(lxz, u"proyección en el plano xz"))
        ## ============================
        tang = Bundle(c, cp,  (tmin, tmax, npuntos), (1,.5,.5), .6)
        cot  = Bundle(c, cpp, (tmin, tmax, npuntos), (1,.5,.5), .2)
        self.addWidgetChild(onOff(tang, "1a derivada", False))
        self.addWidgetChild(onOff(cot,  "2a derivada", False))
        ## ============================
        self.addWidget(Slider(rangep=('w', .2, 1, 1,  20),
            func=lambda t:(tang.setLengthFactor(t) or cot.setLengthFactor(t))))




## ------------------------------------------------------------------------ ##

class Curvas(Chapter):
    def __init__(self, parent=None):
        Chapter.__init__(self, parent=parent, name="Curvas")
        self.addPage(Loxi())
        self.addPage(HeliceCircular())
        self.addPage(HeliceReflejada())
        self.addPage(Alabeada())


## ------------------------------------------------------------------------ ##




if __name__ == "__main__":
    from superficie.util import main
    from superficie.Viewer import Viewer
    print 1
    app = main()
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter()
    ## ============================    
    for f, n in figuras:
        visor.addPage()
        fig = f()
        fig.getGui = lambda: QtGui.QLabel("<center><h1>%s</h1></center>" % n)
        visor.addChild(fig)
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    SoQt.mainLoop()
