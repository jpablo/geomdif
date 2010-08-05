# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.VariousObjects import Bundle2, Bundle, Bundle3
from superficie.VariousObjects import Line, GraphicObject, Curve3D, Sphere, Arrow, Cylinder
from superficie.Book import Chapter
from superficie.Book import Page
from superficie.util import Vec3, _1, partial
from superficie.util import intervalPartition
from superficie.util import connect, connectPartial
from superficie.Animation import Animation, AnimationCurve, Animatable
from superficie.gui import onOff, CheckBox, Slider, Button, VisibleCheckBox, SpinBox
from superficie.gui import DoubleSpinBox
from superficie.Plot3D import ParametricPlot3D
from superficie.Viewer import Viewer

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
    light.FaceType = SoShapeHints.UNKNOWN_FACE_TYPE

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




class HeliceCircular(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular")
        tmin = -2 * pi
        tmax = 2 * pi
        npuntos = 200
        self.addChild(Cylinder(_1(185, 46, 61), tmax - tmin, 2))
        ## ============================================
        # 1 implica primer derivada, 2 implica segunda derivada
        def param1hc(t):
            return 2*Vec3(cos(t), sin(t), t/3.0)
        def param2hc(t):
            return 2*Vec3(-sin(t), cos(t), 1/3.0)
        def param3hc(t):
            return 2*Vec3(-cos(t), -sin(t), 0)
        
        espiral = Curve3D(param1hc, (tmin*1.5, tmax*1.5, npuntos), color=_1(255, 255, 255), parent=self)
        tangente = espiral.setField("tangente", param2hc).setLengthFactor(1).setWidthFactor(.6)
        normal = espiral.setField("normal", param3hc).setLengthFactor(1).setWidthFactor(.6)
        self.setupAnimations([tangente, normal])
        ## ============================================
#        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
#        curva = Line(puntos, (1, 1, 1), 2, parent=self, nvertices=1)
#        bpuntos = 100
#        bundle = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5, visible=True, parent=self)
#        bundle.hideAllArrows()
#        bundle2 = Bundle(param1hc, param3hc, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5, visible=True, parent=self)
#        bundle2.hideAllArrows()
#
#        mathead = SoMaterial()
#        mathead.ambientColor = _1(120, 237, 119)
#        mathead.diffuseColor = _1(217, 237, 119)
#        mathead.specularColor = _1(184, 237, 119)
#        mathead.shininess = .28
#        bundle.setHeadMaterial(mathead)
#
#        mattube = SoMaterial()
#        mattube.ambientColor = _1(213, 227, 232)
#        mattube.diffuseColor = _1(213, 227, 232)
#        mattube.specularColor = _1(213, 227, 232)
#        mattube.shininess = .28
#        bundle2.setMaterial(mattube)
#
#        matHead = SoMaterial()
#        matHead.ambientColor = _1(0, 96, 193)
#        matHead.diffuseColor = _1(0, 96, 193)
#        matHead.specularColor = _1(0, 96, 193)
#        matHead.shininess = .28
#        bundle2.setHeadMaterial(matHead)
#
#        self.setupAnimations([curva, bundle, bundle2])



## ------------------------------- HELICE REFLEJADA ------------------------------- ##

class HeliceReflejada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Reflejada")
        tmin, tmax, npuntos = (-2 * pi, 2 * pi, 200)
        self.addChild(Cylinder(_1(7, 83, 150), tmax - tmin, 2))


        def param1hr(t):
            return 2*Vec3(cos(t), sin(t), -t/3.0)
        def param2hr(t):
            return 2*Vec3(-sin(t), cos(t), -1/3.0)
        def param3hr(t):
            return 2*Vec3(-cos(t), -sin(t), 0)

        espiral = Curve3D(param1hr, (tmin*1.5, tmax*1.5, npuntos), color=_1(255, 255, 255), parent=self)
        tangente = espiral.setField("tangente", param2hr).setLengthFactor(1).setWidthFactor(.6)
        normal = espiral.setField("normal", param3hr).setLengthFactor(1).setWidthFactor(.6)
        self.setupAnimations([tangente, normal])
        ## ============================================
        
#        puntos = [[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
#        puntitos = [[cos(t), sin(t), -t] for t in intervalPartition((tmin, tmax, npuntos))]
#        l1 = Line(puntos, (1, 1, 1), 2, parent=self, nvertices=1)
#        l2 = Line(puntitos, _1(128, 0, 64), 2, parent=self, nvertices=1)
#
#        bpuntos = 100
#        bundle = Bundle(param1hr, param2hr, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5, visible=True, parent=self)
#        bundle2 = Bundle(param1hr, param3hr, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5, visible=True, parent=self)
#        bundle.hideAllArrows()
#        bundle2.hideAllArrows()
#
#        mathead = SoMaterial()
#        mathead.ambientColor = _1(184, 237, 119)
#        mathead.diffuseColor = _1(184, 237, 119)
#        mathead.specularColor = _1(184, 237, 119)
#        mathead.shininess = .28
#        bundle.setHeadMaterial(mathead)
#
#
#        matHead = SoMaterial()
#        matHead.ambientColor = _1(116, 0, 63)
#        matHead.diffuseColor = _1(116, 0, 63)
#        matHead.specularColor = _1(116, 0, 63)
#        matHead.shininess = .28
#        bundle2.setHeadMaterial(matHead)
#
#        mattube = SoMaterial()
#        mattube.ambientColor = _1(213, 227, 232)
#        mattube.diffuseColor = _1(213, 227, 232)
#        mattube.specularColor = _1(213, 227, 232)
#        mattube.shininess = .28
#        bundle2.setMaterial(mattube)
#
#        self.setupAnimations([l1, l2, bundle, bundle2])



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
        tmax = 40 * pi
        pmin = 0
        pmax = 2 * pi
        r = 3
        r2 = 2.995
        m = tan(pi / 60)
        t0 = pi / 2

        func = lambda t: (r * cos(-t) / cosh(m * (-t - t0)), r * sin(-t) / cosh(m * (-t - t0)), r * tanh(m * (-t - t0)))

        curva = Curve3D(func, (tmin, tmax, 250), color=(1, 1, 0), width=3, nvertices=1, parent=self)

        def cp(t):
            den1 = cosh(m * (-t - t0))
            return Vec3(-r * sin(t) / den1 + r * cos(t) * sinh(m * (-t - t0)) * m / den1 ** 2, -r * cos(t) / den1 - r * sin(t) * sinh(m * (-t - t0)) * m / den1 ** 2, -r * (1 - tanh(m * (-t - t0)) ** 2) * m)
        def cpp(t):
            return Vec3(
                - r * cos(t) / cosh(m * (-t - t0)) - 2 * r * sin(t) * sinh(m * (-t - t0)) * m / cosh(m * (-t - t0)) ** 2 + 2 * r * cos(t) * sinh(m * (-t - t0)) ** 2 * m ** 2 / cosh(m * (-t - t0)) ** 3 - r * cos(t) * m ** 2 / cosh(m * (-t - t0)),
                r * sin(t) / cosh(m * (-t - t0)) - 2 * r * cos(t) * sinh(m * (-t - t0)) * m / cosh(m * (-t - t0)) ** 2 - 2 * r * sin(t) * sinh(m * (-t - t0)) ** 2 * m ** 2 / cosh(m * (-t - t0)) ** 3 + r * sin(t) * m ** 2 / cosh(m * (-t - t0)),
                - 2 * r * tanh(m * (-t - t0)) * (1 - tanh(m * (-t - t0)) ** 2) * m ** 2
            )

        tang = Bundle2(curva, cp, (1, 1, 1), factor=.6, parent=self, visible=False)
        tang2 = Bundle3(curva, cp, factor=.6, parent=self, visible=False)
        tang2.setTransparencyType(8)
        tang2.setTransparency(0.6)

        cot = Bundle2(curva, cpp, (1, 1, 1), factor=1, parent=self, visible=False)

        matHead = SoMaterial()
        matHead.ambientColor = (.33, .22, .27)
        matHead.diffuseColor = (1, 0, 0)
        matHead.specularColor = (.99, .94, .81)
        matHead.shininess = .28
        tang.setHeadMaterial(matHead)

        mattube = SoMaterial()
        mattube.ambientColor = _1(213, 227, 232)
        mattube.diffuseColor = _1(213, 227, 232)
        mattube.specularColor = _1(213, 227, 232)
        mattube.shininess = .28
        cot.setMaterial(mattube)


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
        #VisibleCheckBox("superficie tangente", tang2, False, parent=self)
        VisibleCheckBox(u"vectores de aceleración", cot, False, parent=self)

        resf = 2.99
        esf = ParametricPlot3D(lambda t, f: (resf * sin(t) * cos(f), resf * sin(t) * sin(f), resf * cos(t)) , (0, pi, 100), (0, 2 * pi, 120), visible=True)
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor(_1(28, 119, 68))
        self.addChild(esf)
        VisibleCheckBox("esfera", esf, True, parent=self)

        sep = SoSeparator()
        mer = Curve3D(lambda t: (0, r2 * cos(t), r2 * sin(t)), (pmin, pmax, 200), color=_1(72, 131, 14))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer)
        self.addChild(sep)

## ----------------------CIRCULOS MAXIMOS Y PARALELOS---------------------- ##
class Circulos(Page):
    def __init__(self, parent=None):
        Page.__init__(self, u"Paralelos y Círculos Máximos")

        pmin = 0
        pmax = 2 * pi
        resf = 1
        r2 = 3.
        l = -1
        npuntos = 200

        def puntos(t):
            return Vec3(-r2 * sin(t), r2 * cos(t), 0)
        def puntos2(t):
            return Vec3(-cos(t), -sin(t), 0)
        def puntitos(t):
            f = acos(l / r2)
            return Vec3(-r2 * sin(f) * sin(t), r2 * sin(f) * cos(t), l)
        def puntitos2(t):
            f = acos(l / r2)
            return Vec3(-r2 * sin(f) * cos(t), -r2 * sin(f) * sin(t), l)

        def make_circulo(t):
            return partial(par_esfera, t)
            
        par_esfera = lambda t, f: Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        par_circulo = lambda f: Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        par_circulo_der = lambda f: Vec3(-cos(f) * sin(t), -sin(t) * sin(f), 0) 
        par_circulo_maximo = make_circulo(pi / 2)
        
        esf = ParametricPlot3D(par_esfera, (0, pi, 100), (0, 2 * pi, 120))
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor(_1(68, 28, 119))
        VisibleCheckBox("esfera", esf, True, parent=self)
        self.addChild(esf)

        cm = Curve3D(par_circulo_maximo, (pmin, pmax, 200), color=_1(255, 255, 255))
        self.addChild(cm)
        aceleracion_cm = cm.setField("aceleracion", puntos2).show().setLengthFactor(1).setWidthFactor(.2)
        
        
        tini=1.0472
        par_circulo.func_globals['t'] = tini
        #par_circulo_der.func_globals['t'] = tini
        
        par = Curve3D(par_circulo, (pmin, pmax, 200), color=_1(255, 221, 0), parent=self)
        aceleracion_par = par.setField("aceleracion", par_circulo_der).show().setLengthFactor(1).setWidthFactor(.2)
        
        def test(t):
            par_circulo.func_globals['t'] = t
            #par_circulo_der.func_globals['t'] = t
            par.updatePoints()
            
        Slider(('t', 0.1, pi-.1, tini, 100), test, duration=4000, parent=self)
#        
#        tangcm = Bundle2(cm, puntos, (1, 1, 1), factor=.6, parent=self, visible=False) #@UnusedVariable
#        tangpa = Bundle2(par, puntitos, (1, 1, 1), factor=.6, parent=self, visible=False)
#        tangpa.setTransparencyType(8)
#        tangpa.setTransparency(0.6)
#
#        cotcm = Bundle2(cm, puntos2, (1, 1, 1), factor=.6, parent=self, visible=False)
#        cotpa = Bundle2(par, puntitos2, (1, 1, 1), factor=.6, parent=self, visible=False)
#
#        mattube = SoMaterial()
#        mattube.ambientColor = _1(43, 141, 69)
#        mattube.diffuseColor = _1(43, 141, 69)
#        mattube.specularColor = _1(43, 141, 69)
#        mattube.shininess = .28
#        cotcm.setMaterial(mattube)

#        VisibleCheckBox(u"vectores tangentes del círculo máximo", tangcm, False, parent=self)
#        VisibleCheckBox(u"vectores tangentes del círculo paralelo", tangpa, False, parent=self)
#        VisibleCheckBox(u"vectores de aceleración del círculo máximo", cotcm, False, parent=self)
#        VisibleCheckBox(u"vectores de aceleración del círculo paralelo", cotpa, False, parent=self)
        
        self.setupAnimations([aceleracion_cm, aceleracion_par])

## -------------------------ALABEADA--------------------------------------- ##

class Alabeada(Page):
    def __init__(self):
        Page.__init__(self, "Alabeada")
        self.setupPlanes()
        ## ============================
        c = lambda t: Vec3(t, t ** 2, t ** 3)
        cp = lambda t: Vec3(1, 2 * t, 3 * t ** 2)
        cpp = lambda t: Vec3(0, 2, 6 * t)
        ## ============================
        altura = -1
        ## ============================
        curva = Curve3D(lambda t:(t, t ** 2, t ** 3), (-1, 1, 50), width=3, nvertices=1, parent=self)
        lyz = curva.project(x=altura, color=(0, 1, 1), width=3, nvertices=1)
        lxz = curva.project(y=altura, color=(1, 0, 1), width=3, nvertices=1)
        lxy = curva.project(z=altura, color=(1, 1, 0), width=3, nvertices=1)

        tangente = curva.setField("tangente", cp).hide().setLengthFactor(.1).setWidthFactor(.1)
        normal = curva.setField("normal", cpp).hide().setLengthFactor(.1).setWidthFactor(.1)

#        tang = Bundle2(curva, cp, col=(1, .5, .5), factor=.3, parent=self, visible=True)
#        tang.hideAllArrows()
#        cot = Bundle2(curva, cpp, col=(1, .5, .5), factor=.1, parent=self, visible=True)
#        cot.hideAllArrows()

#        mattube = SoMaterial()
#        mattube.ambientColor = _1(206, 205, 202)
#        mattube.diffuseColor = _1(206, 205, 202)
#        mattube.specularColor = _1(206, 205, 202)
#        mattube.shininess = .28
#        tang.setMaterial(mattube)
#
#        mathead = SoMaterial()
#        mathead.ambientColor = _1(3, 107, 170)
#        mathead.diffuseColor = _1(3, 107, 170)
#        mathead.specularColor = _1(3, 107, 170)
#        mathead.shininess = .28
#        cot.setHeadMaterial(mathead)
#
#        mattube = SoMaterial()
#        mattube.ambientColor = _1(213, 227, 232)
#        mattube.diffuseColor = _1(213, 227, 232)
#        mattube.specularColor = _1(213, 227, 232)
#        mattube.shininess = .28
#        cot.setMaterial(mattube)

        curvas = [curva, lyz, lxz, lxy]
        self.setupAnimations(curvas)

        t1 = Arrow(curva[0], lyz[0], escala=.005, escalaVertice=2, extremos=True, parent=self, visible=False)
        t1.AmbientColor = _1(213, 227, 232)
        t1.DiffuseColor = _1(213, 227, 232)
        t1.SpecularColor = _1(213, 227, 232)
        t1.Shininess = .28

        lyz.animation.onStart(t1.show)
        
        lxy.animation.onFinished(
                ).wait(1000
                ).execute(t1.hide
                ).execute(tangente.show
                ).afterThis(tangente.animation
                ).execute(normal.show
                ).afterThis(normal.animation)
        

        def trazaCurva(curva2, frame):
            p2 = curva2[frame - 1]
            p1 = curva[frame - 1]
            t1.setPoints(p1, p2)
            #t1.setLengthFactor(.98)

        for c in curvas[1:]:
            c.animation.addFunction(partial(trazaCurva, c))


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
        tmin, tmax, npuntos = (0, 40 * pi, 3000)

        a = 1
        b = 0.5
        c = .505
        def toroParam1(u, v):
            return ((a + b * cos(v)) * cos(u), (a + b * cos(v)) * sin(u), b * sin(v))
        def toroParam2(u, v):
            return ((a + c * cos(v)) * cos(u), (a + c * cos(v)) * sin(u), c * sin(v))
        def curvaPlana(t):
            return (t, t)
        def curvaToro(t):
            return toroParam2(*curvaPlana(t))

        toro = ParametricPlot3D(toroParam1, (0, 2 * pi, 150), (0, 2 * pi, 100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        curva = Curve3D(curvaToro, (tmin, tmax, npuntos), color=_1(146, 33, 86), width=3, nvertices=1, parent=self)


        def recalculaCurva(**kargs):
            "a: vueltas horizontales, b: vueltas verticales"
            keys = kargs.keys()
            if "a" in keys:
                recalculaCurva.a = kargs["a"]
            if "b" in keys:
                recalculaCurva.b = kargs["b"]

            def curvaPlana(t):
                return (recalculaCurva.a * t, recalculaCurva.b * t)
            def curvaToro(t):
                return toroParam2(*curvaPlana(t))
            
            curva.updatePoints(curvaToro)

#        self.animation2 = Animation(recalculaCurva2,(10000,1,20))
#        Button("Curvas2", self.animation2.start, parent=self)

        recalculaCurva.a = 1
        recalculaCurva.b = 1

        sp1 = SpinBox("a", (0, 20, 1), lambda x: recalculaCurva(a=x), parent=self)
        sp2 = SpinBox("b", (0, 20, 1), lambda x: recalculaCurva(b=x), parent=self)
#        sp1.setSingleStep(.005)
#        sp2.setSingleStep(.005)


        self.addChild(toro)
        curva.animation.setDuration(5000)
        self.setupAnimations([curva])



## ------------------------------------------------------------------------ ##
## CUADRO 1. La gráfica de la función tangente: $alpha(y)= (y, tan y)$ para $y\in (-pi, pi)$.
 
class Tangente(Page):
    def __init__(self):
        Page.__init__(self, u"Tangente")
        self.showAxis(True)
        npuntos = 100
        delta = .2
        def Tan(t):
            return Vec3(t, tan(t), 0)
        #=======================================================================
        # Los fragmentos de las curvas
        #=======================================================================
        #TODO: Permitir que el rango sea una lista de segmentos
        rango = [
                (-pi, -pi / 2 - delta, npuntos),
                (-pi / 2 + delta, pi / 2 - delta, npuntos),
                (pi / 2 + delta, pi, npuntos)
        ]
        curva1 = Curve3D(Tan, rango, parent=self, width=2)
        #=======================================================================
        ## Asíntotas
        #=======================================================================
        Line([(-pi / 2, -5, 0), (-pi / 2, 5, 0)], visible=True, parent=self, color=(1, .5, .5))
        Line([(pi / 2, -5, 0), (pi / 2, 5, 0)], visible=True, parent=self, color=(1, .5, .5))
        
        curva1.setBoundingBox((-5, 5), (-5, 5))

        def Derivada(t):
            return Vec3(1, 1 / cos(t) ** 2, 0)         

        tangente = curva1.setField("tangente", Derivada)
        self.setupAnimations([tangente])
        
    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))
        
    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))
        
        
class ValorAbsoluto(Page):
    def __init__(self):
        Page.__init__(self, u"Valor absoluto")
        self.showAxis(True)
        
        def Abs(t):
            return Vec3(t, abs(t), 0)
        
        curva1 = Curve3D(Abs, (-3, 3, 100), parent=self, width=2)
        curva1.setBoundingBox((-5, 5), (-5, 5))

        def Derivada(t):
            if t < 0:
                dt = -1
            elif t > 0:
                dt = 1
            return Vec3(1, dt, 0)
        
        curva1.derivative = Derivada
        curva1.tangent_vector.show()
        self.setupAnimations([curva1.tangent_vector])
        
    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))
        
    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))


class Cusp(Page):
    def __init__(self):
        Page.__init__(self, u"Autointersección")
        self.showAxis(True)
        
        def cusp(t):
            return Vec3(t ** 3 - 4 * t, t ** 2 - 4, 0)
        
        curva1 = Curve3D(cusp, (-2.5, 2.5, 200), parent=self, width=2)
        curva1.derivative = lambda t: Vec3(-4 + 3 * t ** 2, 2 * t, 0)
        curva1.tangent_vector.show()
                
        self.setupAnimations([curva1.tangent_vector])
        
    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))
        
    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))
        
class Exponencial(Page):
    def __init__(self):
        Page.__init__(self, u"Exponencial")
        self.showAxis(True)
        
        def curve(t): return Vec3(exp(t) * cos(t), exp(t) * sin(t), exp(t))
        def derivada(t): return Vec3(exp(t) * cos(t) - exp(t) * sin(t), exp(t) * cos(t) + exp(t) * sin(t), exp(t))
        curva1 = Curve3D(curve, (-pi, 1 * pi, 200), parent=self, width=2)
        curva1.derivative = derivada
        curva1.tangent_vector.show()
        self.setupAnimations([curva1.tangent_vector])
        
    def pre(self):
        c = Viewer.Instance().camera
        c.position = (0, 0, 10)
        c.pointAt(Vec3(0, 0, 0))
        
    def post(self):
        c = Viewer.Instance().camera
        c.position = (7, 7, 7)
        c.pointAt(Vec3(0, 0, 0), Vec3(0, 0, 1))
        
# ------------------------------------------------------------------------ ##
figuras = [Tangente, ValorAbsoluto, Cusp, Alabeada, Circulos, HeliceCircular, HeliceReflejada, Loxi, Toro]
#---------------------------------------------------------- 
#figuras = [HeliceCircular, HeliceReflejada]

class Curvas1(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas I")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
#        print "chapterSpecificIn"
        pass
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)

## ------------------------------------------------------------------------ ##




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(Curvas1())
    visor.whichChapter = 0
#    visor.chapter.chapterSpecificIn()
    ## ============================
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())

