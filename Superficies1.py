# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pivy.coin import *
from math import *

from superficie.nodes import BasePlane, Curve3D
from superficie.book import Chapter, Page
from superficie.plots import ParametricPlot3D, Plot3D, RevolutionPlot3D
from superficie.widgets import Slider
from superficie.util import _1, connect, Vec3, main
from superficie.animations import Animation


class Plano1(Page):
    u"""La superficie más sencilla es un plano, que es infinitamente reglada; salvo para los
    planos paralelos a uno coordenado, un plano se ve como techo desde cualquiera de los
    planos coordenados: desde el plano $XY$ porque $z = - x – y - 6$, o desde el plano $YZ$
    porque $x = - y – z - 6$, o desde el plano $ZX$ porque $y = - x – z - 6$. Un plano admite
             un atlas con sólo una vecindad parametrizada que lo cubre totalmente.
    """
    def __init__(self):
        u"""l plano x + y + z - 2.5 = 0"""
        Page.__init__(self, "Plano")

        plane = lambda x, y: -x - y
        p1 = lambda x, y, t1: (x, y, (1 - t1) * (-x - y) - 2 * t1)
        p2 = lambda x, y, t2: (x, (1 - t2) * y - 2 * t2, -x - y)
        p3 = lambda x, y, t3: ((1 - t3) * x - 2 * t3, y, -x - y)

        r = (-1, 1, 15)
        plano = Plot3D(plane, (-1, 1), (-1, 1))
        plano.setTransparencyType(8)
        plano1 = ParametricPlot3D(p1, r, r)
        plano2 = ParametricPlot3D(p2, r, r)
        plano3 = ParametricPlot3D(p3, r, r)
        planos = [plano1, plano2, plano3]
        for p in planos:
            p.linesVisible = True
            p.meshVisible = False
        plano1.setMeshDiffuseColor((1, 0, 0))
        plano2.setMeshDiffuseColor((0, 1, 0))
        plano3.setMeshDiffuseColor((0, 1, 1))
        plano.diffuseColor = _1(29, 214, 216)
        plano.transparency = 0.5
        plano.setAmbientColor(_1(29, 214 , 216))
        self.setupPlanes((-2, 2, 7))

        self.addChildren([plano, plano1, plano2, plano3])

        ## no controls
        for i, plano in enumerate(planos):
            plano.parameters['t%d' % (i + 1)].hide()

        self.setupAnimations([plano.parameters['t%d' % (i + 1)].asAnimation() for i, plano in enumerate(planos)])


class ParaboloideEliptico(Page):
    u"""Cualquier punto de un paraboloide elíptico, aunque no sea de revolución, corresponde a
              un solo punto del plano $XZ$ porque esa superficie es la gráfica de la función
              diferenciable $F: \R^2 \rightarrow \R$ dada por $F(x,z) = x^2 + z^2$. Esta superficie
              también admite un atlas con sólo una vecindad parametrizada que la cubre
              completamente
    """
    def __init__(self):
        """x^2 + y^2 - z = 0"""
        Page.__init__(self, u"Paraboloide Elíptico")

        z = 0.5
        par = RevolutionPlot3D(lambda r, t: r ** 2 + z, (0, 1), (0, 2 * pi))
        mesh1 = Plot3D(lambda x, y, h: h * (x ** 2 + y ** 2 + z - .01), (-1, 1), (-1, 1))
        mesh1.addFunction(lambda x, y, h: h * (x ** 2 + y ** 2 + z + .01))
        mesh1.setLinesVisible(True)
        mesh1.setMeshVisible(False)
        mesh1.setBoundingBox(zrange=(-1, 1.5))
        par.setAmbientColor(_1(145, 61, 74))
        par.setDiffuseColor(_1(145, 61, 74))
        par.setSpecularColor(_1(145, 61, 74))
        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2, 2, 7))

        self.addChild(par)
        self.addChild(mesh1)
        self.addChild(baseplane)

class ParaboloideHiperbolico(Page):
    u"""Cualquier punto de un paraboloide hiperbólico, que es una superficie doblemente
     reglada, corresponde a un solo punto del plano $XY$ porque esa superficie es la gráfica
              de la función diferenciable $F: \R^2 \rightarrow \R$ dada por $F(x,y) = x^2 - y^2$. Esta
              superficie también admite un atlas con sólo una vecindad parametrizada que la cubre
              completamente.
    """
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        z = 1.5
        parab = Plot3D(lambda x, y: x ** 2 - y ** 2 + z, (-1, 1), (-1, 1))
        parab1 = Plot3D(lambda x, y, h: h * (x ** 2 - y ** 2 + z), (-1, 1), (-1, 1)) #@UndefinedVariable
        parab1.setLinesVisible(True)
        parab1.setMeshVisible(False)
        parab.setAmbientColor(_1(145, 61 , 74))
        parab.setDiffuseColor(_1(127, 119, 20))
        parab.setSpecularColor(_1(145, 61 , 74))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2, 2, 7))

        self.addChild(parab)
        self.addChild(parab1)
        self.addChild(baseplane)

class LasilladelMono(Page):
    u"""La silla del mono también es gráfica de la función diferenciable $F: \R^2 \rightarrow \R$
               dada por $F(x,y) = x^3-3xy^2$. Ésta es otra superficie que admite un atlas con sólo una
               vecindad parametrizada que la cubre completamente.
    """
    def __init__(self):
        "x^3 - 3xy^2 - z = 0"
        Page.__init__(self, u"La silla del mono")

        silla = Plot3D(lambda x, y: x ** 3 - 3 * x * y ** 2 + 2.5, (-1, 1), (-1, 1))
        silla.setAmbientColor(_1(151, 139, 125))
        silla.setDiffuseColor(_1(151, 139, 125))
        silla.setSpecularColor(_1(151, 139, 125))
#        silla.setShininess(1)
#        plano.setScaleFactor((1,1,.6))

        def cVec(pto):
            "pto: Vec3"
            return pto * 1.1
        silla.addVectorField(cVec)

#        def setXscale(t):
#            scale.scaleFactor = (1,1,t)
#        Slider(
#            rangep=('z', .2, 1, 1,  20),
#            func=setXscale,
#            parent=self
#        )
#

        silla1 = Plot3D(lambda x, y, h: h * (x ** 3 - 3 * x * y ** 2 + 2.5), (-1, 1), (-1, 1)) #@UndefinedVariable
#        silla1.setScaleFactor((1,1,.6))
        silla1.setLinesVisible(True)
        silla1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2, 2, 7))

        self.addChild(silla)
        self.addChild(silla1)
        self.addChild(baseplane)

class Superficiecuartica(Page):
    u"""Esta superficie es gráfica de la función diferenciable $F: R^2 \rightarrow R$ dada por
                  $F(x,y) = x^4+2x^2y^2 + y^4 $. Por eso esta superficie también admite un atlas con
                  sólo una vecindad parametrizada que la cubre completamente.
    """
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cuártica")

#        cuart = Plot3D(lambda x,y: x**4 + 2*x**2*y**2 + y**4 + 1, (-1,1),(-1,1))
        cuart = RevolutionPlot3D(lambda r, t: r ** 4 + 1, (0, 1), (0, 2 * pi))
#        cuart.setScaleFactor((1,1,.6))

        mesh1 = Plot3D(lambda x, y, h: h * (x ** 4 + 2 * x ** 2 * y ** 2 + y ** 4 + 1), (-1, 1), (-1, 1))
        mesh1.setLinesVisible(True)
        mesh1.setMeshVisible(False)
        mesh1.setBoundingBox(zrange=(-1, 2))

#        cuart.setAmbientColor(_1(168,211,8))
        cuart.setDiffuseColor(_1(168, 211, 8))
        cuart.setSpecularColor(_1(168, 211, 8))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2, 2, 7))

        self.addChild(cuart)
        self.addChild(mesh1)
        self.addChild(baseplane)

class Conoderevolucion(Page):
    u"""El cono completo no es la gráfica de una función diferenciable de dos variables, y
                 como todas las  generatrices pasan por el vértice, en ese punto es imposible
                 bien-aproximar el cono por un plano; no existe el plano tangente en ese punto.
    """
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Cono de Revolución")

        cono = RevolutionPlot3D(lambda r, t: r + 1, (0, 1), (0, 2 * pi))
        cono1 = RevolutionPlot3D(lambda r, t, h: h * (r + 1), (0.05, 1), (0, 2 * pi)) #@UndefinedVariable
        cono1.setLinesVisible(True)
        cono1.setMeshVisible(False)
        cono.setDiffuseColor(_1(149, 24, 82))
        cono.setSpecularColor(_1(149, 24, 82))


        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2, 2, 7))
        self.addChild(cono)
        self.addChild(cono1)
        self.addChild(baseplane)

class EsferaCasquetes(Page):
    u"""La esfera completa no es la gráfica de una función diferenciable de dos variables, pero sí
              es la imagen inversa de un valor regular de una función diferenciable
              $G: \R^3 \rightarrow \R$. Un atlas de la esfera requiere al menos dos vecindades
               parametrizadas para cubrirla toda; estos seis casquetes forman un atlas de la esfera
    """
    def __init__(self):
        u"""^2 + y^2 = z^2"""

        super(EsferaCasquetes,self).__init__(u"Atlas de la esfera")

        r = .998
        esf = ParametricPlot3D(lambda t, f: (r * sin(t) * cos(f), r * sin(t) * sin(f), r * cos(t)), (0, pi, 70), (0, 2 * pi, 70))
        esf.setDiffuseColor(_1(99, 136, 63))
        esf.setSpecularColor(_1(99, 136, 63))

        pars = [
            lambda u,v, t1: (u, v, 1.5-t1*(1.5-sqrt(1 - u**2 - v**2))),
            lambda u,v, t2: (u, v, -1-t2*(-1+sqrt(1 - u**2 - v**2))),
            lambda u,v, t3: (u, 1.5-t3*(1.5-sqrt(1 - u**2 - v**2)),v),
            lambda u,v, t4: (u, -1.5-t4*(-1.5+sqrt(1 - u**2 - v**2)),v),
            lambda u,v, t5: (1.5-t5*(1.5-sqrt(1 - u**2 - v**2)),u,v),
            lambda u,v, t6, : (-1.5-t6*(-1.5+sqrt(1 - u**2 - v**2)),u,v)
        ]

        d = .7
        colores = [(0,0,1),(0,0,1),(0,1,0),(0,1,0),(1,0,0),(1,0,0)]
        planos = [ParametricPlot3D(par, (-d, d, 40), (-d, d, 40)).setLinesVisible(True).setMeshVisible(False).setMeshDiffuseColor(colores[i]) for i,par in enumerate(pars)]

        baseplane = BasePlane()
        baseplane.setHeight(-1.005)
        baseplane.setRange((-2,2, 7))
        self.addChild(esf)
        for p in planos:
            self.addChild(p)
        self.addChild(baseplane)

        ## no queremos los controles
        for i,plano in enumerate(planos):
            plano.parameters['t%d' % (i+1)].hide()

        anims = [plano.parameters['t%d' % (i+1)].asAnimation() for i,plano in enumerate(planos)]
        self.setupAnimations(anims)

class Esfera(Page):
    u"""Estas dos proyecciones esterográficas muestran que es posible cubrir a la esfera con dos vecindades parametrizadas.
     Ellas bastan para formar un atlas para la esfera.
    """
    def __init__(self):
        u"""^2 + y^2 = z^2"""
        Page.__init__(self, u"Esfera <br> (Proyección estereográfica)")

        r = .998
        esf = ParametricPlot3D(lambda t, f: (r * sin(t) * cos(f), r * sin(t) * sin(f), r * cos(t)), (0, pi, 70), (0, 2 * pi, 70))
#        esf.setAmbientColor(_1(99,136,63))
        esf.setDiffuseColor(_1(99, 136, 63))
        esf.setSpecularColor(_1(99, 136, 63))


        def proyZm1(u, v, t1):
            """proy desde el polo norte al plano z=-1"""
            den = u ** 2 + v ** 2 + 4
            x = u - t1 * (u - 4 * u / den)
            y = v - t1 * (v - 4 * v / den)
            z = -1 - t1 * (-2 + 8 / den)
            return (x, y, z)

        def proyZ1(u, v, t2):
            """proy desde el polo sur al plano z=1"""
            den = u ** 2 + v ** 2 + 4
            x = u - t2 * (u - 4 * u / den)
            y = v - t2 * (v - 4 * v / den)
            z = 1 - t2 * (2 - 8 / den)
            return (x, y, z)

        stereo = ParametricPlot3D(proyZm1, (-3, 3, 70), (-3, 3, 70))
        stereo.setLinesVisible(True)
        stereo.setMeshVisible(False)
        stereo.setMeshDiffuseColor(_1(117, 55, 79))

        stereo2 = ParametricPlot3D(proyZ1, (-3, 3, 70), (-3, 3, 70))
        stereo2.setLinesVisible(True)
        stereo2.setMeshVisible(False)
        stereo2.setMeshDiffuseColor(_1(80, 87, 193))
        stereo2.setTransparency(0.5)
        stereo2.setTransparencyType(8)


        baseplane = BasePlane()
        baseplane.setHeight(-1.005)
        baseplane.setRange((-4, 4, 7))
        self.addChild(esf)
        self.addChild(stereo2)
        self.addChild(stereo)
        self.addChild(baseplane)

        params = [stereo,stereo2]

        ## no queremos los controles
        for i,p in enumerate(params):
            p.parameters['t%d' % (i+1)].hide()

        anims = [p.parameters['t%d' % (i+1)].asAnimation() for i,p in enumerate(params)]
        self.setupAnimations(anims)

class Superficies1(Chapter):
    def __init__(self):
        super(Superficies1,self).__init__("Superficies y sus parametrizaciones")

        figuras = [
            Plano1,
            ParaboloideEliptico,
            ParaboloideHiperbolico,
            LasilladelMono,
            Superficiecuartica,
            Conoderevolucion,
            Esfera,
            EsferaCasquetes
        ]

        for f in figuras:
            self.addPage(f())


if __name__ == "__main__":
    visor = main(Superficies1)

