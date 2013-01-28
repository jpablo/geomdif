# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, Bundle2, Bundle3, PointSet#, Sphere, Arrow
from superficie.book import Chapter, Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import VisibleCheckBox, Slider, SpinBox
from superficie.plots import ParametricPlot3D
from superficie.viewer.Viewer import Viewer
from superficie.animations import AnimationGroup

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

class Circulos(Page):
    u"""Note que en el caso del ecuador los vectores de aceleración apuntan al centro de la esfera, pero en el caso del
    paralelo no, por eso el ecuador es una geodésica y un paralelo no lo es.
    """

    def __init__(self, parent=None):
        Page.__init__(self, u"Paralelos y Círculos Máximos")
        self.showAxis(False)

        pmin = 0
        pmax = 2 * pi
        r2 = 3.
        l = -1

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
        aceleracion_cm = cm.attachField("aceleracion", puntos2).show().setLengthFactor(1).setWidthFactor(.1)

        tini=1.0472
        par_circulo.func_globals['t'] = tini
        #par_circulo_der.func_globals['t'] = tini

        par = Curve3D(par_circulo, (pmin, pmax, 200), color=_1(255, 221, 0))
        self.addChild(par)
        aceleracion_par = par.attachField("aceleracion", par_circulo_der).show().setLengthFactor(1).setWidthFactor(.1)

        def test(t):
            par_circulo.func_globals['t'] = t
            #par_circulo_der.func_globals['t'] = t
            par.updatePoints()

        Slider(('t', 0.1, pi-.1, tini, 100), test, duration=4000, parent=self)
        self.setupAnimations([aceleracion_cm, aceleracion_par])

def Cylinder(col, length, radius = 0.98):
    sep = SoSeparator()

    cyl = SoCylinder()
    cyl.radius.setValue(radius)
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

class HeliceCircular(Page):
    u"""Las hélices circulares y sus casos límite, la recta y la circunferencia,
    <b>curvas homogéneas</b>: un pedazo de ellas puede acomodarse en cualquier otro lugar de
    la hélice.
    """
    def __init__(self):
        Page.__init__(self, u"Hélice Circular")
        self.showAxis(False)
        tmin = -2 * pi
        tmax = 2 * pi
        npuntos = 300
        self.addChild(Cylinder(_1(185, 46, 61), tmax - tmin, 2))
        ## ============================================
        # 1 implica primer derivada, 2 implica segunda derivada
        def param1hc(t):
            return 2*Vec3(cos(t), sin(t), t/3.0)
        def param2hc(t):
            return 2*Vec3(-sin(t), cos(t), 1/3.0)
        def param3hc(t):
            return 2*Vec3(-cos(t), -sin(t), 0)

        espiral = Curve3D(param1hc, (tmin*1.5, tmax*1.5, npuntos), color=_1(255, 255, 255))
        tangente = espiral.attachField("tangente", param2hc).setLengthFactor(1).setWidthFactor(.6)
        tangente.setRadius( 0.06 )
        tangente.setDiffuseColor( _1(20,240,20) )
        normal = espiral.attachField("normal", param3hc).setLengthFactor(1).setWidthFactor(.6)
        normal.setRadius( 0.06 )
        normal.setDiffuseColor( _1(240,120,20) )
        self.addChild(espiral)
        self.setupAnimations([ AnimationGroup([tangente, normal], (10000,0,len(espiral)-1)) ])

class HeliceReflejada(Page):
    u"""La <b>hélice reflejada</b> no puede llevarse en la hélice anterior
        por un <b>movimiento rígido</b>, es resultado de una reflexión en el
        plano $XY$.
    """
    def __init__(self):
        Page.__init__(self, u"Hélice Cirular Reflejada")
        self.showAxis(False)
        tmin, tmax, npuntos = (-2 * pi, 2 * pi, 200)
        self.addChild(Cylinder(_1(7, 83, 150), tmax - tmin, 2))


        def param1hr(t):
            return 2*Vec3(cos(t), sin(t), -t/3.0)
        def param2hr(t):
            return 2*Vec3(-sin(t), cos(t), -1/3.0)
        def param3hr(t):
            return 2*Vec3(-cos(t), -sin(t), 0)

        espiral = Curve3D(param1hr, (tmin*1.5, tmax*1.5, npuntos), color=_1(255, 255, 255))

        def param1hc_der(t):
            return 2*Vec3(cos(t), sin(t), t/3.0)

        espiral_der = Curve3D(param1hc_der, (tmin*1.5, tmax*1.5, npuntos), color=_1(60, 80, 80))
        tangente = espiral.attachField("tangente", param2hr).setLengthFactor(1).setWidthFactor(.6)
        tangente.setRadius( 0.06 )
        tangente.setDiffuseColor( _1(20,240,20) )
        normal = espiral.attachField("normal", param3hr).setLengthFactor(1).setWidthFactor(.6)
        normal.setRadius( 0.06 )
        normal.setDiffuseColor( _1(240,120,20) )
        self.addChild(espiral)
        self.addChild(espiral_der)

        plano_xy_par = lambda u, v: Vec3(u,v,0)
        plano_xy = ParametricPlot3D(plano_xy_par, (-4,4,20),(-4,4,20))
        plano_xy.setDiffuseColor( _1(200,200,200) )
        plano_xy.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        plano_xy.setTransparency( 0.85 )

        self.addChild( plano_xy )
        self.addChild(Line([(-4, 0, 0), (4, 0, 0)], color=(0.8, 0.8, 0.5)))
        self.addChild(Line([(0, -4, 0), (0, 4, 0)], color=(0.8, 0.8, 0.5)))
        self.setupAnimations([ AnimationGroup([tangente, normal], (10000,0,len(espiral)-1)) ])

def rot(ang):
    """ La rotacion para poder pintar los meridianos """
    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.Z
    rot.angle = ang

    return rot

class Loxi(Page):
    u"""Una loxodroma es una curva en la esfera que forma un <b>ángulo constante</b>
    <b>$alpha$ con los meridianos</b>, es el análogo de una hélice para la esfera.
    En la proyección de Mercator, donde los meridianos se proyectan en rectas paralelas,
    la loxodroma se proyecta en una recta que corta a las anteriores en un ángulo $alpha$.
    """
    def __init__(self, parent=None):
        Page.__init__(self, "Loxodroma")
        self.creaLoxodroma()

    def creaLoxodroma(self):
        tmin = -75
        tmax = 60
        pmin = 0
        pmax = 2 * pi
        r = 3
        r2 = 2.995
        m = tan(pi / 60)
        t0 = pi / 2

        def sigmoide(t):
            return abs(2.0/(1+exp(-(t/15.0)))-1)

        def func(t):
            t = t * sigmoide(t)
            return r * cos(-t) / cosh(m * (-t - t0)), r * sin(-t) / cosh(m * (-t - t0)), r * tanh(m * (-t - t0))

        def cp(t):
            t = t * sigmoide(t)
            den1 = cosh(m * (-t - t0))
            return Vec3(-r * sin(t) / den1 + r * cos(t) * sinh(m * (-t - t0)) * m / den1 ** 2, -r * cos(t) / den1 - r * sin(t) * sinh(m * (-t - t0)) * m / den1 ** 2, -r * (1 - tanh(m * (-t - t0)) ** 2) * m)
        def cpp(t):
            return Vec3(
                    - r * cos(t) / cosh(m * (-t - t0)) - 2 * r * sin(t) * sinh(m * (-t - t0)) * m / cosh(m * (-t - t0)) ** 2 + 2 * r * cos(t) * sinh(m * (-t - t0)) ** 2 * m ** 2 / cosh(m * (-t - t0)) ** 3 - r * cos(t) * m ** 2 / cosh(m * (-t - t0)),
                    r * sin(t) / cosh(m * (-t - t0)) - 2 * r * cos(t) * sinh(m * (-t - t0)) * m / cosh(m * (-t - t0)) ** 2 - 2 * r * sin(t) * sinh(m * (-t - t0)) ** 2 * m ** 2 / cosh(m * (-t - t0)) ** 3 + r * sin(t) * m ** 2 / cosh(m * (-t - t0)),
                    - 2 * r * tanh(m * (-t - t0)) * (1 - tanh(m * (-t - t0)) ** 2) * m ** 2
                    )

        curve = Curve3D(func, (tmin, tmax, 10), color=(1, 1, 0), width=3, nvertices=1, max_distance = .3, max_angle = .2)
        self.addChild(curve)

        tangent = curve.attachField("tangente", cp).setLengthFactor(1).setWidthFactor(.2).show()
        tangent.setRadius(.04)
        tangent.animation.setDuration(30000)

        matHead = SoMaterial()
        matHead.ambientColor = (.33, .22, .27)
        matHead.diffuseColor = (1, 0, 0)
        matHead.specularColor = (.99, .94, .81)
        matHead.shininess = .28
        self.setupAnimations([ AnimationGroup([curve, tangent], (20000,0,len(curve)-1)) ])

        resf = 2.97
        esf = ParametricPlot3D(lambda t, f: (resf * sin(t) * cos(f), resf * sin(t) * sin(f), resf * cos(t)) , (0, pi, 100), (0, 2 * pi, 120))
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor(_1(28, 119, 68))
        self.addChild(esf)
        VisibleCheckBox("esfera", esf, True, parent=self)

        sep = SoSeparator()
        mer = Curve3D(lambda t: (0, r2 * cos(t), r2 * sin(t)), (pmin, pmax, 100), color=_1(72, 131, 14))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer.root)
        self.addChild(sep)

class Toro(Page):
    u"""En un toro hueco hay curvas que rodean tanto al hoyo central como al hueco, la
    que mostramos <b>se cierra sin cortarse</b>. Hay otras que se enredan
    infinitamente sin cortarse y formando un conjunto denso en la superficie del toro.
    """
    def __init__(self):
        super(Toro,self).__init__(u"Toro")
        tmin, tmax, npuntos = (0, 2 * pi, 3000)

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

        curva = Curve3D(curvaToro, (tmin, tmax, npuntos), color=_1(146, 33, 86), width=3, nvertices=1)


        def recalculaCurva(**kargs):
            """a: vueltas horizontales, b: vueltas verticales"""
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

        recalculaCurva.a = 1
        recalculaCurva.b = 1

        sp1 = SpinBox("a", (0, 20, 1), lambda x: recalculaCurva(a=x), parent=self)
        sp2 = SpinBox("b", (0, 20, 1), lambda x: recalculaCurva(b=x), parent=self)

        self.addChild(curva)
        self.addChild(toro)
        curva.animation.setDuration(5000)
        self.setupAnimations([curva])

class Exponencial(Page):
    def __init__(self):
        Page.__init__(self, u"Exponencial")
        self.showAxis(True)
        self.axis_z.setVisible(False)

        def curve(t): return Vec3(exp(t) * cos(t), exp(t) * sin(t), exp(t))
        def derivada(t): return Vec3(exp(t) * cos(t) - exp(t) * sin(t), exp(t) * cos(t) + exp(t) * sin(t), exp(t))
        curva1 = Curve3D(curve, (-pi, 1 * pi, 200), width=2)
        self.addChild(curva1)
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

class curvas_superficies(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas en superficies")

        figuras = [
            HeliceCircular,
            HeliceReflejada,
            Circulos,
            Loxi,
            Toro
        ]
        for f in figuras:
            self.addPage(f())

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(curvas_superficies())
    visor.whichChapter = 0
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notasStack.show()
    sys.exit(app.exec_())

