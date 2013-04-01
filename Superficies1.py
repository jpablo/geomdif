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
from superficie.equation import createVars


class Plano1(Page):
    u"""
      Una <b>parametrización</b> de los puntos <b>p</b> de una superficie los dota
      de coordenadas y permite utilizar los métodos del cálculo en la superficie.
      <p>
      Salvo el caso en que el plano sea paralelo a uno de los coordenados,
      un plano se ve como techo desde cualquiera de ellos, como lo ilustra la
      interacción, y por lo tanto puede cubrirse con sólo una parametrización.
    """
    def __init__(self):
        "F(x,y) = (x, y, x + y - 6)"
        #u"""l plano x + y + z - 2.5 = 0"""
        Page.__init__(self, u"Plano<br><br>F(x,y) = (x, y, x + y - 6)")

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
    u"""
      Cualquier punto de un paraboloide elíptico en posición canónica pertenece
      a la gráfica de la función diferenciable
      <b>f(x,y)=x<sup>2</sup>/a<sup>2</sup>+y<sup>2</sup>/b<sup>2</sup></b>,
      por eso el paraboloide elíptico también puede cubrirse con sólo una
      parametrización, como lo muestra la interacción, y cada punto se
      identifica con el par <b>(x,y)</b>. La red coordenada en la superficie
      es la imagen de la red coordenada en el plano.
    """
    def __init__(self):
        """F(x,y)=x^2 + y^2 - z = 0"""
        Page.__init__(self, u"Paraboloide Elíptico<br><br>F(x,y)=(x, y, x<sup>2</sup>/a<sup>2</sup> + y<sup>2</sup>/b<sup>2</sup>)")

        z = 0.5
        par = RevolutionPlot3D(lambda r, t: r ** 2 + z, (0, 1), (0, 2 * pi))

        x, y, z2, u, v, cose, sen, t = createVars(['x', 'y', 'z', 'u', 'v', 'cos', 'sen', 't'])

        mesh1 = Plot3D(lambda x, y, h: h * (x ** 2 + y ** 2 + z - .01), (-1, 1), (-1, 1))
        mesh1.addEqn(x**2+y**2 - z2**2 == 1)
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
    u"""
      Un paraboloide hipérbólico en posición canónica también se cubre con sólo
      una parametrización por ser gráfica de una función diferenciable,
      <b>f(x,y)=x<sup>2</sup>-y<sup>2</sup></b>. Localmente, <b>toda superficie
      diferenciable es gráfica de la función altura sobre el plano tangente</b>
      pero difícilmente esa parametrización cubre a toda la superficie.
      <p>
      La interacción muestra cómo se levanta la red coordenada del plano
      <b>XY</b> bajo la parametrización: son dos familias de parábolas.
      También aquí los puntos se identifican con el par <b>(x,y)</b>.
    """
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico<br><br>F(x,y)=(x, y, x<sup>2</sup>-y<sup>2</sup>)")

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
    u"""
      La silla del mono es también una superficie diferenciable que puede
      cubrirse con sólo una vecindad parametrizada, por ser gráfica de la
      función <b>f(x,y)=x<sup>3</sup>-3xy<sup>2</sup></b>, por eso se dice
      que admite un <b>atlas con sólo una carta</b>.
    """
    def __init__(self):
        "x^3 - 3xy^2 - z = 0"
        Page.__init__(self, u"Silla del mono<br><br>F(x,y)=(x, y, x<sup>3</sup> - 3xy<sup>2</sup>)")

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
    u"""
      Otra superficie diferenciable con atlas formado por sólo una carta.
      El interés radica en que su <b>orden de contacto</b> con el plano <b>XY</b>,
      su plano tangente en <b>(0,0,0)</b>, es mayor que <b>2</b>.
      La curvatura gaussiana (ver más adelante) de esta superficie en ese
      punto es cero.
    """
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie cuártica<br><br>F(x,y)=(x,y,x<sup>4</sup>+2x<sup>2</sup>y<sup>2</sup>+y<sup>4</sup>)")

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
    u"""
      Ilustramos medio cono de revolución. En todos los puntos salvo el vértice,
      las rectas tangentes a curvas suaves contenidas en el semicono dan lugar
      a todo un plano. Pero en el vértice, cada generatriz está contenida en su
      recta tangente y por eso el plano tangente no está definido en el vértice.
      El semicono <b>no es una superficie diferenciable</b>.
      <p>
      La interacción muestra cómo se levanta al semicono la red polar,
      que tiene una singularidad en el polo; de hecho en la parametrización
      en coordenadas esféricas dada no se obtiene el vértice.
    """
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Semicono de revolución<br><br>F(&theta;,&rho;)=(&theta;,&rho;,&pi;/4)")

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
    u"""
      La esfera completa no es gráfica de una función diferenciable en tres
      variables, pero sí es la imagen inversa de un valor regular de la función
      <b>G(x,y,z)=x<sup>2</sup>+y<sup>2</sup>+z<sup>2</sup></b>.
      <p>
      Al despejar de <b>x<sup>2</sup>+y<sup>2</sup>+z<sup>2</sup>=1</b>
      una de las variables obtenemos dos raíces, en total seis funciones cuyas
      gráficas son hemisferios sin borde que al cubrir toda la esfera forman un
      atlas para ella como lo muestra la interacción.
      <p>
      Parametrizaciones:
      <ul>
      <li><b>z(x,y) = &radic;(1 - x<sup>2</sup> - y<sup>2</sup>)</b></li>
      <li><b>z(x,y) = - &radic;(1 - x<sup>2</sup> - y<sup>2</sup>)</b></li>
      <li><b>x(y,z) = &radic;(1 - y<sup>2</sup> - z<sup>2</sup>)</b></li>
      <li><b>x(y,z) = - &radic;(1 - y<sup>2</sup> - z<sup>2</sup>)</b></li>
      <li><b>y(z,x) = &radic;(1 - z<sup>2</sup> - x<sup>2</sup>)</b></li>
      <li><b>y(z,x) = - &radic;(1 - z<sup>2</sup> - x<sup>2</sup>)</b></li>
      </ul>
    """
    def __init__(self):
        #u"""x^2 + y^2 + z^2 = 1"""

        super(EsferaCasquetes,self).__init__(u"Otro atlas de la esfera")

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
    u"""
      Cada punto <b>p</b> de la esfera unitaria (salvo el polo norte <b>N=(0,0,1)</b>)
      puede proyectarse en un punto <b>(u,v)</b> en el plano de altura
      <b>z=-1</b> obtenido al cortar ese plano con la recta que une <b>p</b>
      con <b>N</b>.
      <p>
      También podemos proyectar el punto <b>p</b>, salvo el polo sur <b>S=(0,0,-1)</b>,
      desde <b>S</b> a un punto <b>(r,s)</b> en el plano de altura <b>z=1</b>.
      <p>
      Necesitamos dos proyecciones estereográficas para dar coordenadas a todos
      los puntos de la esfera, pero como los cambios de coordenadas son
      difeomorfismos, sigue siendo posible hacer cálculo en la esfera.
      <p>
      La interacción muestra cómo se aplican las dos redes coordenadas de los
      planos en la esfera formando un atlas.
      <p>
      Parametrización usando las proyecciones esterográficas<br>
      <ul>
      <li><b>(x,y,z) &isin; S<sup>2</sup>\{(0,0,1)}</b> corresponde a <b>(u,v) = (x(z-1)/2, y(z-1)/2)</b><br></li>
      <li><b>(x,y,z) &isin; S<sup>2</sup>\{(0,0,-1)}</b> corresponde a <b>(u,v) = (x(z+1)/2, y(z+1)/2)</b><br></li>
      </ul>
    """
    def __init__(self):
        u"""^2 + y^2 = z^2"""
        Page.__init__(self, u"Esfera, parametrización por proyecciones estereográficas")

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

