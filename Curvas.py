# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtCore, QtGui
from pivy.coin import *
from pivy.gui.soqt import *
from superficie.VariousObjects import Bundle2, Bundle
from superficie.VariousObjects import Line, GraphicObject, Curve3D, Sphere, Arrow
from superficie.base import Chapter
from superficie.base import Page
from superficie.util import Vec3
from superficie.util import intervalPartition
from superficie.util import connect, connectPartial
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
    def __init__(self):
        Page.__init__(self, u"Hélice Circular")
        tmin = -2 * pi
        tmax = 2 * pi
        npuntos = 200
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)
        self.addChild(cilindro((185. / 255, 46. / 255, 61. / 255), tmax - tmin))
        bpuntos = 100
        bundle = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle.hideAllArrows()
        bundle2 = Bundle(param1hc, param3hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle2.hideAllArrows()


        bundleAnim = Animation(lambda num: bundle[num-1].show(),(4000,1,bpuntos))
        bundleAnim2 = Animation(lambda num: bundle2[num-1].show(),(4000,1,bpuntos))
        self.animaciones = [ Animation(curva.setNumVertices,(4000,1,npuntos)), bundleAnim, bundleAnim2 ]
        Animation.chain(self.animaciones, pause=1000)

        def anima():
            bundle.hideAllArrows()
            bundle2.hideAllArrows()
            self.animaciones[0].start()
        # ============================
        Button("inicio", anima, parent=self)



## ------------------------------- HELICE REFLEJADA ------------------------------- ##

class HeliceReflejada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Reflejada")
        tmin = -2 * pi
        tmax = 2 * pi
        npuntos = 200
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
        puntitos = [[cos(t), sin(t), -t] for t in intervalPartition((tmin, tmax, npuntos))]
        l1 = Line(puntos, (1, 1, 1), 2,parent=self, nvertices=1)
        l2 = Line(puntitos, (128. / 255, 0, 64. / 255), 2,parent=self, nvertices=1)
        curvas = [l1,l2]
        self.addChild(cilindro((7. / 255, 83. / 255, 150. / 255), tmax - tmin))
        bpuntos = 100
        bundle = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle.hideAllArrows()

        def setNumVertices(num):
            for f in curvas:
                f.setNumVertices(num)
        bundleAnim = Animation(lambda num: bundle[num-1].show(),(4000,0,bpuntos))
        self.animaciones = [ Animation(setNumVertices,(4000,0,npuntos)), bundleAnim ]
        Animation.chain(self.animaciones, pause=1000)

        def anima():
            bundle.hideAllArrows()
            for c in curvas:
                c.setNumVertices(1)
            self.animaciones[0].start()
        ## ============================
        Button("inicio", anima, parent=self)

#        return sep

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
        self.setupPlanes()
        ## ============================
        tmin,tmax,npuntos = (-1,1,50)
        altura = -1
        ## ============================
        curva = Curve3D((tmin,tmax,npuntos),lambda t:(t,t**2,t**3), width=3,nvertices=1,parent=self)
        lyz = curva.project(x=altura, color=(0,1,1), width=3, nvertices=1)
        lxz = curva.project(y=altura, color=(1,0,1), width=3, nvertices=1)
        lxy = curva.project(z=altura, color=(1,1,0), width=3, nvertices=1)
        ## ============================
        curvas = [curva, lyz, lxz, lxy]
        ## ============================
        self.animaciones = [ Animation(f.setNumVertices,(4000,0,npuntos)) for f in curvas ]
        Animation.chain(self.animaciones, pause=1000)

        t1 = Arrow(curva[0],lyz[0],escala=.005,escalaVertice=2,extremos=True,parent=self,visible=True)
    
        def trazaCurva(curva2,frame):
            # esto no me gusta mucho, pero solamente así no aparecen
            # artefactos.
            # debe haber algún problema en el código de la flecha
            if frame == 1:
                t1.show()
            elif frame == len(curva):
                t1.hide()
            p2 = curva2[frame-1]
            p1 = curva[frame-1]
            t1.setPoints(p1,p2)
            t1.setLengthFactor(.98)

        for i in range(1,4):
            connectPartial(self.animaciones[i], "frameChanged(int)", trazaCurva, curvas[i])

        ## ============================
        def anima():
            tang.hideAllArrows()
            for c in curvas:
                c.setNumVertices(1)
            self.animaciones[0].start()
        ## ============================
        Button("inicio", anima, parent=self)
        ## ============================
        VisibleCheckBox(u"proyección en el plano x = %d" % altura, lyz, parent=self)
        VisibleCheckBox(u"proyección en el plano y = %d" % altura, lxz, parent=self)
        VisibleCheckBox(u"proyección en el plano z = %d" % altura, lxy, parent=self)
        ## ============================
        c   = lambda t: Vec3(t,t**2,t**3)
        cp  = lambda t: Vec3(1,2*t,3*t**2)
        cpp = lambda t: Vec3(0,2,6*t)
        ## ============================
        tang = Bundle2(curva, cp,  col=(1,.5,.5), factor=.6, parent=self,visible=True)
        ## las vamos a ir mostrando una por una
        tang.hideAllArrows()
        tangAnim = Animation(lambda num: tang[num-1].show(),(4000,0,npuntos))
#        cot  = Bundle2(curva, cpp, col=(1,.5,.5), factor=.2, parent=self)
        self.__anim2 = [self.animaciones[-1],tangAnim]
        Animation.chain(self.__anim2, pause=1000)

        VisibleCheckBox("1a derivada",tang,False,parent=self)
#        VisibleCheckBox("2a derivada",cot, False,parent=self)
        ## ============================
        Slider(
            rangep=('w', .2, .6, .6,  20),
            func=lambda t:(tang.setLengthFactor(t) or cot.setLengthFactor(t)),
            parent=self
        )




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

