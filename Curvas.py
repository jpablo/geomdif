# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtCore, QtGui
from pivy.coin import *
from pivy.gui.soqt import *
from superficie.VariousObjects import Bundle
from superficie.VariousObjects import Line, GraphicObject
from superficie.base import Chapter
from superficie.base import Page
from superficie.util import Vec3
from superficie.util import intervalPartition
from superficie.util import connect
from superficie.Animation import Animation
from superficie.gui import onOff, CheckBox, Slider, Button, VisibleCheckBox

## ---------------------------------- CILINDRO ----------------------------------- ##

def cilindro(col, length):
    sep = SoSeparator()

    cyl = SoCylinder()
    cyl.radius.setValue(0.98)
    cyl.height.setValue(length)
    cyl.parts = SoCylinder.SIDES

    light = SoShapeHints()
#    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
#    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
#    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor = col
    mat.diffuseColor = col
    mat.transparency.setValue(0.5)

    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.X
    rot.angle = pi / 2

    trans = SoTransparencyType()
#    trans.value = SoTransparencyType.DELAYED_BLEND
    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND
#    trans.value = SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND

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
#    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND
    trans.value = SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND
#    trans.value = SoTransparencyType.DELAYED_BLEND

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



class HeliceCircular(Page):
    def __init__(self, parent=None):
        Page.__init__(self, u"Hélice Circular")
        self.addChild(self.helicecircular())

    # Dibuja la helice y el cilindro
    def helicecircular(self):
        tmin = -2 * pi
        tmax = 2 * pi
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, 200))]

        haz1hc = Bundle(param1hc, param2hc, (tmin, tmax, 50), (128. / 255, 1, 0), 1.5)
        sep = SoSeparator()

        sep.addChild(Line(puntos, (.8, .8, .8), 2))
        sep.addChild(cilindro((1, 0, 0.5), tmax - tmin))
        sep.addChild(haz1hc.root)
        return sep

## ------------------------------- HELICE REFLEJADA ------------------------------- ##

class HeliceReflejada(Page):
    def __init__(self, parent=None):
        Page.__init__(self, u"Hélice Reflejada")
        self.addChild(self.helicereflejada())

    # Dibuja las helices y el cilindro
    def helicereflejada(self):
        tmin = -2 * pi
        tmax = 2 * pi
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, 200))]

        puntitos = [[cos(t), sin(t), -t] for t in intervalPartition((tmin, tmax, 200))]
        haz2hc = Bundle(param1hc, param2hc, (tmin, tmax, 50), (116. / 255, 0, 63. / 255), 1.5)
        sep = SoSeparator()

        sep.addChild(Line(puntos, (1, 1, 1), 2))
        sep.addChild(Line(puntitos, (128. / 255, 0, 64. / 255), 2))
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

class Loxi(Page):
    def __init__(self, parent=None):
        Page.__init__(self, "Loxodroma")
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
        sep.addChild(Line(puntos2, (1, 1, 0), 3))
        sep.addChild(esfera((28. / 255, 119. / 255, 68. / 255)))
        mer = Line(puntitos2, (72. / 255, 131. / 255, 14. / 255))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer)
        self.addChild(sep)

## ------------------------------------------------------------------------ ##

class Alabeada(Page):
    def __init__(self):
        Page.__init__(self, "Alabeada")
        ## ============================
        c   = lambda t: Vec3(t,t**2,t**3)
        cp  = lambda t: Vec3(1,2*t,3*t**2)
        cpp = lambda t: Vec3(0,2,6*t)
        ## ============================
        tmin = -1
        tmax = 1
        npuntos = 50
        puntos = intervalPartition((tmin,tmax,npuntos), c)
        xy = [(p[0],p[1],0) for p in puntos]
        yz = [(0,p[1],p[2]) for p in puntos]
        xz = [(p[0],0,p[2]) for p in puntos]
        ## ============================
        curva = Line(puntos, width=3, nvertices = 1, parent=self)
        ## ============================
        self.lxy = Line(xy,(1,1,0), nvertices=1, parent=self)
        self.lyz = Line(yz,(0,1,1), nvertices=1, parent=self)
        self.lxz = Line(xz,(1,0,1), nvertices=1, parent=self)
        ## ============================
        self.animaciones = [ Animation(f.setNumVertices,(2000,0,npuntos)) for f in [curva, self.lxy, self.lyz, self.lxz] ]
        Animation.chain(self.animaciones, pause=1000)
        ## ============================
        Button("inicio", self.animaciones[0].start, parent=self)
        ## ============================
        VisibleCheckBox(self.lxy, u"proyección en el plano xy")
        VisibleCheckBox(self.lyz, u"proyección en el plano yz")
        VisibleCheckBox(self.lxz, u"proyección en el plano xz")
        ## ============================

        tang = Bundle(c, cp,  (tmin, tmax, npuntos), (1,.5,.5), .6)
        cot  = Bundle(c, cpp, (tmin, tmax, npuntos), (1,.5,.5), .2)
        self.addWidgetChild(onOff(tang, "1a derivada", False))
        self.addWidgetChild(onOff(cot,  "2a derivada", False))
        ## ============================
        self.addWidget(Slider(rangep=('w', .2, 1, 1,  20),
            func=lambda t:(tang.setLengthFactor(t) or cot.setLengthFactor(t))))




## ------------------------------------------------------------------------ ##
figuras = [Loxi, HeliceCircular, HeliceReflejada, Alabeada]


class Curvas(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Curvas")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)

## ------------------------------------------------------------------------ ##




if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
#    app = main(sys.argv)
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
#    visor.setColorLightOn(False)
#    visor.setWhiteLightOn(True)
    visor.addChapter(Curvas())
    visor.getChapterObject().chapterSpecificIn()
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
#    SoQt.mainLoop()
    sys.exit(app.exec_())

