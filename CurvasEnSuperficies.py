# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes import Line, Curve3D, Bundle2, Bundle3, PointSet, SimpleSphere
from superficie.book import Chapter, Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import VisibleCheckBox, Slider, SpinBox
from superficie.plots import ParametricPlot3D
from superficie.viewer.Viewer import Viewer
from superficie.animations import AnimationGroup

class Circulos(Page):
    u"""Note que en el caso del ecuador los vectores de aceleración apuntan al centro de la esfera, pero en el caso del
    paralelo no, por eso el ecuador es una geodésica y un paralelo no lo es.
    """

    def __init__(self, parent=None):
        Page.__init__(self, u"La diferencia entre un Círculo Máximo y un Paralelo")
        self.showAxis(False)

        pmin = 0
        pmax = 2 * pi
        r2 = 3.
        l = -1

        def puntos2(t):
            return Vec3(-cos(t), -sin(t), 0)

        def make_circulo(t):
            return partial(par_esfera, t)

        par_esfera = lambda t, f: Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        par_circulo = lambda f: Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        par_circulo_der = lambda f: Vec3(-cos(f) * sin(t), -sin(t) * sin(f), 0)
        par_circulo_maximo = make_circulo(pi / 2)

        esf = ParametricPlot3D(par_esfera, (0, pi, 100), (0, 2 * pi, 120))
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.3).setDiffuseColor(_1(68, 28, 119)).setSpecularColor(_1(99, 136, 63))
        VisibleCheckBox("esfera", esf, True, parent=self)
        self.addChild(esf)

        cm = Curve3D(par_circulo_maximo, (pmin, pmax, 200), color=_1(255, 255, 255))
        self.addChild(cm)
        aceleracion_cm = cm.attachField("aceleracion", puntos2).show().setLengthFactor(.98).setWidthFactor(.2)

        tini=1.0472
        par_circulo.func_globals['t'] = tini
        #par_circulo_der.func_globals['t'] = tini

        par = Curve3D(par_circulo, (pmin, pmax, 200), color=_1(255, 221, 0))
        self.addChild(par)
        aceleracion_par = par.attachField("aceleracion", par_circulo_der).show().setLengthFactor(1).setWidthFactor(.2)

        circle_2 = SimpleSphere(Vec3(0, 0, cos(tini)), radius=.02)
        circle_2_tr = circle_2.getByName("Translation")

        self.addChild(circle_2)
        self.addChild(SimpleSphere(Vec3(0, 0, 0), radius=.02))

        ## los meridianos
        sep = SoSeparator()
        mer = Curve3D(lambda t: (0, .99 * cos(t), .99 * sin(t)), (pmin, pmax, 100), color=_1(18, 78, 169))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer.root)
        self.addChild(sep)

        # the sphere rotation axis
        self.addChild(Line([(0, 0, -1.2), (0, 0, 1.2)], width=2))

        def test(t):
            par_circulo.func_globals['t'] = t
            par.updatePoints()
            circle_2_tr.translation = (0, 0, cos(t))

        Slider(('t', 0.1, pi-.1, tini, 100), test, duration=4000, parent=self)
        self.setupAnimations([aceleracion_cm, aceleracion_par])

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
        r2 = r - 0.005
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

        ## los meridianos
        sep = SoSeparator()
        mer = Curve3D(lambda t: (0, r2 * cos(t), r2 * sin(t)), (pmin, pmax, 100), color=_1(72, 131, 14))
        for i in range(24):
            sep.addChild(rot(2 * pi / 24))
            sep.addChild(mer.root)

        # highlighted meridians
        r3 = r + 0.005
        mer2 = Curve3D(lambda t: (0, r3 * cos(t), r3 * sin(t)), (pmin, pmax, 100), color=_1(255, 251,0), width=2)
        for i in [-4, -2]:
            sep.addChild(rot(i * 2 * pi / 24))
            sep.addChild(mer2.root)

        self.addChild(sep)

class Toro(Page):
    u"""En un toro hueco hay curvas que rodean tanto al hoyo central como al hueco, la
    que mostramos <b>se cierra sin cortarse</b>. Hay otras que se enredan
    infinitamente sin cortarse y formando un conjunto denso en la superficie del toro.
    """
    def __init__(self):
        super(Toro,self).__init__(u"Curvas tóricas")
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

class CurvasEnSuperficies(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas en superficies")

        figuras = [
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
    visor.book.addChapter(curvas_superficies())
    visor.whichChapter = 0
    visor.chapter.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notesStack.show()
    sys.exit(app.exec_())

