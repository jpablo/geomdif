# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtCore, QtGui
from pivy.coin import *

try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False


from superficie.VariousObjects import Bundle2, Bundle, Bundle3
from superficie.VariousObjects import Line, GraphicObject, Curve3D, Sphere, Arrow
from superficie.base import Chapter
from superficie.base import Page
from superficie.util import Vec3
from superficie.util import intervalPartition
from superficie.util import connect, connectPartial
from superficie.Animation import Animation
from superficie.gui import onOff, CheckBox, Slider, Button, VisibleCheckBox, SpinBox
from superficie.gui import DoubleSpinBox
from superficie.Plot3D import ParametricPlot3D

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

#    comp = SoComplexity()
#    comp.value.setValue(1)
#    comp.textureQuality.setValue(0.9)

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

#    sep.addChild(comp)
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
        tmax =  2 * pi
        npuntos = 200
        self.addChild(cilindro((185. / 255, 46. / 255, 61. / 255), tmax - tmin))
        ## ============================================
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)
        bpuntos = 100
        bundle = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle.hideAllArrows()
        bundle2 = Bundle(param1hc, param3hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle2.hideAllArrows()

        self.setupAnimations([curva,bundle,bundle2])



## ------------------------------- HELICE REFLEJADA ------------------------------- ##

class HeliceReflejada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Reflejada")
        tmin,tmax,npuntos = (-2 * pi,2 * pi,200)
        self.addChild(cilindro((7. / 255, 83. / 255, 150. / 255), tmax - tmin))
        
        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
        puntitos = [[cos(t), sin(t), -t] for t in intervalPartition((tmin, tmax, npuntos))]
        l1 = Line(puntos, (1, 1, 1), 2,parent=self, nvertices=1)
        l2 = Line(puntitos, (128. / 255, 0, 64. / 255), 2,parent=self, nvertices=1)

        bpuntos = 100
        bundle  = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle2 = Bundle(param1hc, param3hc, (tmin, tmax, bpuntos), (116. / 255, 0, 63. / 255), 1.5,visible=True,parent=self)
        bundle.hideAllArrows()
        bundle2.hideAllArrows()

        self.setupAnimations([l1,l2,bundle,bundle2])



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
        tmin = -40 * pi
        tmax =  40 * pi
        pmin = 0
        pmax = 2 * pi
        r = 3
        r2 = 2.995
        m = tan(pi / 60)
        t0 = pi / 2

        func = lambda t: ( r * cos(-t) / cosh(m * (-t-t0)), r * sin(-t) / cosh(m * (-t-t0)), r * tanh(m * (-t-t0)) )

        curva = Curve3D((tmin,tmax,250),func, color=(1,1,0),width=3,nvertices=1,parent=self)

        def cp(t):
            den1 = cosh(m*(-t-t0))
            return Vec3(-r*sin(t)/den1+r*cos(t)*sinh(m*(-t-t0))*m/den1**2, -r*cos(t)/den1-r*sin(t)*sinh(m*(-t-t0))*m/den1**2, -r*(1-tanh(m*(-t-t0))**2)*m)
        def cpp(t):
            return Vec3(
                -r*cos(t)/cosh(m*(-t-t0))-2*r*sin(t)*sinh(m*(-t-t0))*m/cosh(m*(-t-t0))**2+2*r*cos(t)*sinh(m*(-t-t0))**2*m**2/cosh(m*(-t-t0))**3-r*cos(t)*m**2/cosh(m*(-t-t0)),
                r*sin(t)/cosh(m*(-t-t0))-2*r*cos(t)*sinh(m*(-t-t0))*m/cosh(m*(-t-t0))**2-2*r*sin(t)*sinh(m*(-t-t0))**2*m**2/cosh(m*(-t-t0))**3+r*sin(t)*m**2/cosh(m*(-t-t0)),
                -2*r*tanh(m*(-t-t0))*(1-tanh(m*(-t-t0))**2)*m**2
            )

        tang = Bundle2(curva, cp, (1,1,1),factor=.6, parent=self,visible=False)
        tang2 = Bundle3(curva, cp, factor=.6, parent=self,visible=False)
        tang2.setTransparencyType(8)
        tang2.setTransparency(0.6)

        cot  = Bundle2(curva, cpp, (1,1,1),factor=1, parent=self,visible=False)

        matHead = SoMaterial()
        matHead.ambientColor  = (.33, .22, .27)
        matHead.diffuseColor  = (1,0,0)
        matHead.specularColor = (.99, .94, .81)
        matHead.shininess = .28
        tang.setHeadMaterial(matHead)


        def tipoTrans(i):
            tang2.setTransparencyType(i)
            print i
        def tipoTrans2(i):
            cot.setTransparencyType(i)
            print i
#        SpinBox("# flechas", (1,len(tang),1), tang2.setNumVisibleArrows, parent=self)
#        SpinBox("trans. type", (0,9,8), tipoTrans, parent=self)
#        DoubleSpinBox("t.val ", (0,1,.94), tang2.material.transparency.setValue, parent=self)

#        SpinBox("# flechas", (1,len(cot),1), cot.setNumVisibleArrows, parent=self)
#        SpinBox("trans. type", (0,9,8), tipoTrans2, parent=self)
#        DoubleSpinBox("t.val ", (0,1,.94), cot.material.transparency.setValue, parent=self)


        self.addChild(tang)
        self.addChild(curva)

        self.setupAnimations([curva])
        
        VisibleCheckBox("vectores tangentes", tang, False, parent=self)
        VisibleCheckBox("haz tangente", tang2, False, parent=self)
        VisibleCheckBox("haz cotangente", cot, False, parent=self)

        resf = 2.99
        esf = ParametricPlot3D(lambda t,f: (resf*sin(t)*cos(f),resf*sin(t)*sin(f),resf*cos(t)) , (0,pi,100),(0,2*pi,120),visible=True)
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor((28. / 255, 119. / 255, 68. / 255))
        self.addChild(esf)
        VisibleCheckBox("esfera", esf, True, parent=self)

        sep = SoSeparator()
        mer = Curve3D((pmin,pmax,200),lambda t: (0, r2 * cos(t), r2 * sin(t)), color=(72. / 255, 131. / 255, 14. / 255))
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
        c   = lambda t: Vec3(t,t**2,t**3)
        cp  = lambda t: Vec3(1,2*t,3*t**2)
        cpp = lambda t: Vec3(0,2,6*t)
        ## ============================
        tmin,tmax,npuntos = (-1,1,50)
        altura = -1
        ## ============================
        curva = Curve3D((tmin,tmax,npuntos),lambda t:(t,t**2,t**3), width=3,nvertices=1,parent=self)
        lyz = curva.project(x=altura, color=(0,1,1), width=3, nvertices=1)
        lxz = curva.project(y=altura, color=(1,0,1), width=3, nvertices=1)
        lxy = curva.project(z=altura, color=(1,1,0), width=3, nvertices=1)

        tang = Bundle2(curva, cp,  col=(1,.5,.5), factor=.6, parent=self,visible=True)
        tang.hideAllArrows()
        cot  = Bundle2(curva, cpp, col=(1,.5,.5), factor=.2, parent=self, visible=True)
        cot.hideAllArrows()

        ## ============================
        curvas = [curva, lyz, lxz, lxy]
        ## ============================
        self.setupAnimations(curvas + [tang,cot])

        t1 = Arrow(curva[0],lyz[0],escala=.005,escalaVertice=2,extremos=True,parent=self,visible=False)
    
        connect(self.animations[1],"stateChanged(QTimeLine::State)", lambda state: t1.show() if state==2 else None)
        connect(self.animations[3],"stateChanged(QTimeLine::State)", lambda state: t1.hide() if state==0 else None)

        def trazaCurva(curva2,frame):
            p2 = curva2[frame-1]
            p1 = curva[frame-1]
            t1.setPoints(p1,p2)
            t1.setLengthFactor(.98)

        for i in range(1,4):
            connectPartial(self.animations[i], "frameChanged(int)", trazaCurva, curvas[i])


#        VisibleCheckBox("1a derivada",tang,False,parent=self)
#        VisibleCheckBox("2a derivada",cot, False,parent=self)
        ## ============================
#        Slider(
#            rangep=('w', .2, .6, .6,  20),
#            func=lambda t:(tang.setLengthFactor(t) or cot.setLengthFactor(t)),
#            parent=self
#        )


## -------------------------------TORO------------------------------- ##


class Toro(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Toro")
        tmin,tmax,npuntos = (0,40*pi,3000)

        a = 1
        b = 0.5
        c = .505
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))
        def toroParam2(u,v):
            return ((a+c*cos(v))*cos(u),(a+c*cos(v))*sin(u),c*sin(v))
        def curvaPlana(t):
            return (t,t)
        def curvaToro(t):
            return toroParam2(*curvaPlana(t))

        toro = ParametricPlot3D(toroParam1,(0,2*pi,150),(0,2*pi,100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        curva = Curve3D((tmin,tmax,npuntos), curvaToro, color=(146./255, 33./255, 86/255.), width=3,nvertices=1,parent=self)


        def recalculaCurva(**kargs):
            "a: vueltas horizontales, b: vueltas verticales"
            keys = kargs.keys()
            if "a" in keys:
                recalculaCurva.a = kargs["a"]
            if "b" in keys:
                recalculaCurva.b = kargs["b"]

            def curvaPlana(t):
                return (recalculaCurva.a*t,recalculaCurva.b*t)
            def curvaToro(t):
                return toroParam2(*curvaPlana(t))
            
            curva.updatePoints(curvaToro)

#        self.animation2 = Animation(recalculaCurva2,(10000,1,20))
#        Button("Curvas2", self.animation2.start, parent=self)

        recalculaCurva.a = 1
        recalculaCurva.b = 1

        sp1 = DoubleSpinBox("a", (0,20,1), lambda x: recalculaCurva(a=x), parent=self)
        sp2 = DoubleSpinBox("b", (0,20,1), lambda x: recalculaCurva(b=x), parent=self)
        sp1.setSingleStep(.005)
        sp2.setSingleStep(.005)


        self.addChild(toro)
        curva.animation.setDuration(5000)
        self.setupAnimations([curva])



## ------------------------------------------------------------------------ ##
figuras = [Loxi, HeliceCircular, HeliceReflejada, Alabeada, Toro]


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
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(Curvas())
    visor.getChapterObject().chapterSpecificIn()
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
#    SoQt.mainLoop()
    sys.exit(app.exec_())

