# -*- coding: utf-8 -*-
from math import pi, sin, cos, tan, sqrt
from PyQt4 import QtGui
from pivy.coin import SoTransparencyType
from superficie.util import Vec3, _1, partial
from superficie.nodes import Curve3D, Line, Arrow, BasePlane, Plane, Sphere
from superficie.animations import AnimationGroup, Animation
from superficie.plots import ParametricPlot3D, Plot3D
from superficie.widgets import VisibleCheckBox, Slider
from superficie.book import Chapter, Page


class Plano1(Page):
    u"""
      Si en una superficie asignamos a cada punto un vector tangente de forma
      diferenciable (es lo que se llama un <b>campo de vectores tangentes</b>),
      la topología de la superficie puede forzar la aparición de <b>singularidades</b>,
      puntos donde el vector tangente esté obligado a anularse.
      <p>
      La interacción muestra un campo tangente en el plano sin singularidades
      donde los vectores tangentes son todos paralelos a un mismo vector y
      corren sobre sus <b>trayectorias</b>.
      <p>
      Campo de vectores tangentes:<br>
      <b>(x,y) &rarr; (1,0)</b>
    """
    ## meridianos
    def __init__(self):
        Page.__init__(self, u"Campo sin singularidades en el plano<br><br>(x,y) &rarr; (1,0)")

        par_plano = lambda u, v: Vec3(u,v,0)

        def plano_u(u,v):
            return Vec3(1,0,0)

        def plano_v(u,v):
            return Vec3(0,1,0)

        parab = ParametricPlot3D(par_plano, (-1,1,20),(-1,1,20))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return lambda t: par_plano(t,c)

        def make_tang(c):
            return lambda t: plano_u(t,c)

        tangentes = []
        ncurves = 30
        steps = 70

        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2 - 1
            curva = Curve3D(make_curva(ct),(-1,1,steps), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (6000, 0, steps-1))
        self.setupAnimations([a1])


class Esfera1(Page):
    u"""
      Dice un teorema famoso: <b>“La esfera no se puede peinar”</b>, es decir,
      todo campo tangente en la esfera tiene al menos una singularidad.
      <p>
      En esta interacción, los vectores son tangentes a círculos resultado de
      cortar la esfera con planos del haz que contienen a una misma recta
      tangente a la esfera, y sus normas decrecen al acercarse al punto de
      tangencia que es una <b>singularidad de índice 2</b>, pues los vectores
      tangentes anclados en puntos de un círculo que rodee la singularidad,
      si se dibujan con un mismo origen, le dan dos vueltas a ese origen.
      <p>
      Campo de vectores tangentes:<br>
      <b>(s,t) &rarr; (-4st, 2(1 + s<sup>2</sup> + t<sup>2</sup>) - 4t<sup>2</sup>, 4t) / (1 + s<sup>2</sup> + t<sup>2</sup>)<sup>2</sup></b>
    """
    def __init__(self):
        Page.__init__(self, u"Campo en la esfera con sólo una singularidad")

        def make_circulo(t):
            return partial(par_esfera, t)

        par_esfera = lambda t, f: 0.99*Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        esf = ParametricPlot3D(par_esfera, (0, pi, 100), (0, 2 * pi, 120))
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor(_1(68, 28, 119))
        VisibleCheckBox("esfera", esf, True, parent=self)
        self.addChild(esf)

        def par_curva(c,t):
            t = tan(t/(4*pi))
            den = c**2+t**2+1
            return Vec3(2*c / den, 2*t / den, (c**2+t**2-1) / den)


        def par_tang(c,t):
            t = tan(t/(4*pi))
            den = (c**2+t**2+1)**2
            return Vec3(-2*c*(2*t) / den, (2*(c**2+t**2+1)-4*t**2) / den, 4*t / den)

        def make_curva(c):
            return partial(par_curva,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(-10,11):
            ct = tan(c/(2*pi))
            curva = Curve3D(make_curva(ct),(-20,20,80), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(1).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (10000, 0, 79))
        self.setupAnimations([a1])


class Esfera2(Page):
    u"""
      Otro teorema famoso (debido a Poincaré) dice: <b>“En una superficie
      compacta, la suma de los índices de un campo con singularidades aisladas
      es igual a la característica de Euler"</b>.
      <p>
      El campo en esta interacción tiene dos singularidades aisladas,
      cada una con índice <b>1</b>, y la característica de Euler de la esfera
      es <b>2</b>.
      Las normas de los vectores deben decrecer al acercarse a una singularidad
      para que el campo sea diferenciable.
      <p>
      Campo de vectores tangentes:<br>
      <b>(u,v) &rarr; (-sen u sen v, sen u cos v, 0)</b>
    """
    ## paralelos
    def __init__(self):
        Page.__init__(self, u"Campo en la esfera con dos singularidades")

        par_esfera = lambda u, v: Vec3(sin(u) * cos(v), sin(u) * sin(v), cos(u))

        def esfera_u(u, v):
            return Vec3(cos(u) * cos(v), cos(u) * sin(v), -sin(u))

        def esfera_v(u, v):
            return Vec3(-sin(u) * sin(v), cos(v) * sin(u), 0)


        parab = ParametricPlot3D(par_esfera, (0, 2, 150), (0, 2 * pi, 100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_esfera, c)

        def make_tang(c):
            return partial(esfera_v, c)

        tangentes = []
        curves = []
        ncurves = 70
        for c in range(0, ncurves + 1):
            ## -1 < ct < 1
            ct = c / float(ncurves) * pi
            curve = Curve3D(make_curva(ct), (0, 2 * pi, 100), width=1)
            tangent = curve.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1).show()
            tangentes.append(tangent)
            curves.append(curve)
        self.addChildren(curves)
        self.setupAnimations([AnimationGroup(tangentes, (6000, 0, 99))])


class Esfera3(Page):
    u"""
      El campo anterior tenía como trayectorias los paralelos de la esfera,
      en este caso las trayectorias son meridianos y la norma de los vectores
      tangentes debe tender a cero al acercarse a uno de los polos que son las
      singularidades, cada una de índice <b>1</b>.
      <p>
      Campo de vectores tangentes:<br>
      <b>(u,v) &rarr; (-cos u sen u cos v, -cos u sen u sen v, 1 - cos<sup>2</sup>u)</b>
    """
    ## meridianos
    def __init__(self):
        Page.__init__(self, u"Otro campo en la esfera con dos singularidades")

        par_esfera = lambda u, v: Vec3(sin(u) * cos(v), sin(u) * sin(v), cos(u))

        def esfera_u(u,v):
            return Vec3(-cos(u)*cos(v)*sin(u), -cos(u)*sin(u)*sin(v), 1-cos(u)**2)

        parab = ParametricPlot3D(par_esfera, (0,pi,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return lambda t: par_esfera(t,c)

        def make_tang(c):
            return lambda t: esfera_u(t,c)

        tangentes = []
        curves = []
        ncurves = 70
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curve = Curve3D(make_curva(ct),(-(pi-.02),-.02,100), width=1)
            tangent = curve.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1).show()
            tangentes.append(tangent)
            curves.append(curve)
        self.addChildren(curves)
        self.setupAnimations([AnimationGroup(tangentes, (6000, 0, 99))])


class ParaboloideHiperbolico(Page):
    u"""
      Este campo tangente en el paraboloide hiperbólico no tiene singularidades,
      las trayectorias son parábolas.
      <p>
      Parabolide hiperbólico:<br>
      <b>z = x<sup>2</sup> - y<sup>2</sup></b>
      <p>
      Campo de vectores tangentes:<br>
      <b>(x,y) &rarr; (0, 1, -2y)</b>
    """
    def __init__(self):
        Page.__init__(self, u"Campo en el paraboloide hiperbólico sin singularidades<br><br>(x,y) &rarr; (0, 1, -2y)")

        par_parab = lambda x, y: Vec3(x,y,x ** 2 - y ** 2)
        par_tang = lambda x,y: Vec3(0,1,-2*y)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_parab,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(0,21):
            ## -1 < ct < 1
            ct = 2*c/20.0-1
            curva = Curve3D(make_curva(ct),(-1,1,50), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.3).setWidthFactor(.075)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])


class ParaboloideHiperbolicoReglado(Page):
    u"""
      El paraboloide hiperbólico contiene dos familias de rectas;
      el campo en esta interacción tiene como trayectorias las recta de una
      familia y no tiene singularidades.
      <p>
      Parabolide hiperbólico:<br>
      <b>z = xy</b>
      <p>
      Campo de vectores tangentes:<br>
      <b>(x,y) &rarr; (0, 1, x)</b>
    """
    def __init__(self):
        Page.__init__(self, u"Otro campo en el paraboloide hiperbólico sin singularidades<br><br>(x,y) &rarr; (0, 1, x)")

        par_parab = lambda x, y: Vec3(x,y,x*y)
        par_tang = lambda x,y: Vec3(0,1,x)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_parab,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(0,21):
            ## -1 < ct < 1
            ct = 2*c/20.0-1
            curva = Curve3D(make_curva(ct),(-1,1,50), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])


class ParaboloideHiperbolicoCortes(Page):
    u"""
      El paraboloide hiperbólico también puede verse formado por las curvas
      que resultan al cortarlo con planos a altura <b>k</b>, con <b>k</b>
      corriendo sobre todos los números reales: son hipérbolas excepto cuando
      <b>k = 0</b>, donde se obtienen las dos rectas que pasan por el
      <b>punto silla</b>.
      <p>
      El campo en esta interacción tiene esas curvas como
      trayectorias y en consecuencia, para cumplir con la diferenciabilidad
      hay una singularidad en el punto silla. ¿Cuál es su índice?
      <p>
      Parabolide hiperbólico:<br>
      <b>z = xy</b>
      <p>
      Campo de vectores tangentes:<br>
      <b>(x,y) &rarr; (0, 1, -k/x<sup>2</sup>)</b>
    """
    def __init__(self):
        Page.__init__(self, u"Campo en el paraboloide hiperbólico con una singularidad<br><br>(x,y) &rarr; (0, 1, -k/x<sup>2</sup>)")

        par_parab = lambda x, y: Vec3(x,y,x*y)
        par_tang = lambda x,y: Vec3(0,1,x)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            #return partial(par_parab,c)
            return lambda x : Vec3( x, c/x, c*1.01 )

        def make_curva_negy(c):
            #return partial(par_parab,c)
            return lambda x : Vec3( x, -c/x, -c*0.99 )

        def make_tang(c):
            #return partial(par_tang,c)
            return lambda x : Vec3( x, -c/(x**2), 0.0 ) / ( sqrt( x**2 + c**2/(x**4) ) )

        def make_tang_negy(c):
            #return partial(par_tang,c)
            return lambda x : Vec3( x, c/(x**2), 0.0 ) / ( sqrt( x**2 + c**2/(x**4) ) )

        tangentes = []

        for c in range(1,10):
            ## 0 < ct < 1
            ct = c/10.0
            curva = Curve3D(make_curva(ct),(ct,1.0,50), width=1.5)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)

            curva = Curve3D(make_curva_negy(ct),(ct,1.0,50), width=1.5)
            curva.attachField("tangente_negy", make_tang_negy(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente_negy'].show()
            tangentes.append(curva.fields['tangente_negy'])
            self.addChild(curva)

            #ct = -1.0 + c/10.0
            curva = Curve3D(make_curva(ct),(-ct, -1.0, 50), width=1.5)
            curva.attachField("tangente2", make_tang(-ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente2'].show()
            tangentes.append(curva.fields['tangente2'])
            self.addChild(curva)

            curva = Curve3D(make_curva_negy(ct),(-ct, -1.0, 50), width=1.5)
            curva.attachField("tangente_negy2", make_tang_negy(-ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente_negy2'].show()
            tangentes.append(curva.fields['tangente_negy2'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (5000, 0, 49))
        self.setupAnimations([a1])

        self.addChild(Line([(-1, 0, 0.01), (1, 0, 0.01)], color=(1, 1, 1)).setWidth(1.5))
        self.addChild(Line([(0, -1, 0.01), (0, 1, 0.01)], color=(1, 1, 1)).setWidth(1.5))


class ToroMeridianos(Page):
    u"""
      El toro puede generarse rotando un círculo en torno a una recta en el
      mismo plano y que no corte al círculo.
      La interacción muestra los vectores tangentes a todos esos círculos y
      que forman un campo en el toro sin singularidades.
      <p>
      Campo de vectores tangentes:<br>
      <b>(u,v) &rarr; (-b sen v cos u, -b sen v sen u, b cos v)</b>
    """
    def __init__(self):
        Page.__init__(self, u"Campo en el toro sin singularidades")
        a = 1
        b = 0.5
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))


        parab = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)


        def make_curva(c):
            return partial(toroParam1,c)

        def make_tang(c):
            return partial(toro_v,c)

        tangentes = []
        ncurves = 70
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0,2*pi,100), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])


class ToroParalelos(Page):
    u"""
      El campo anterior tuvo como trayectorias los meridianos del toro.
      Esta interacción muestra un campo sin singularidades cuyos vectores
      tangentes son los paralelos del toro.
      <p>
      Campo de vectores tangentes:<br>
      <b>(u,v) &rarr; ((a + b cos v) cos u,(a + b cos v) sen u, b sen v )</b>
    """
    def __init__(self):
        Page.__init__(self, u"Otro campo en el toro sin singularidades")
        a = 1
        b = 0.5
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))


        parab = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)


        def make_curva(c):
            return lambda t: toroParam1(t,c)

        def make_tang(c):
            return lambda t: toro_u(t,c)

        tangentes = []
        ncurves = 50
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0,2*pi,100), width=1)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            self.addChild(curva)


        def animaTangentes(n):
            for tang in tangentes:
                tang.animateArrow(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])


class ToroVerticalMorseTest(Page):
    def __init__(self):
        Page.__init__(self, u"Campo de Morse sobre el toro")
        a = 2.0
        b = 1.0
        g = -1.25
        # T(u,v)
        def toroParam1(u,v):
            return (b*sin(u),(a+b*cos(u))*cos(v),(a+b*cos(u))*sin(v))

        def toroNormal(u,v):
            coef = b * ( a + b * cos(u) )
            return Vec3( coef * sin(u), coef * cos(u) * cos(v), coef * cos(u) * sin(v) )

        def toroMorse(u,v):
            #coef = -b * ( a + b * cos(u) )
            coef2 = -g * cos(u) * sin(v)
            return Vec3( coef2 * sin(u), coef2 * cos(u) * cos(v), g + coef2 * cos(u) * sin(v) )

        paratoro = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        paratoro.setTransparency(0.25)
        paratoro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        paratoro.setDiffuseColor(_1(68, 28, 119))
        self.addChild(paratoro)


        def make_curva(c):
            return lambda t: toroParam1(c,t)

        def make_curva2(c):
            return lambda t: toroParam1(c,-t)

        def make_tang(c):
            return lambda t: toroMorse(c,t)

        def make_tang2(c):
            return lambda t: toroMorse(c,-t)

        tangentes = []
        tangentes2 = []
        ncurves = 12
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            #curva = Curve3D(make_curva(ct),(-pi/2,pi/2,100), width=0.5)
            curva = Curve3D(make_curva(ct),(pi/2,3*pi/2,100), width=0.5)
            curva.attachField("tangente", make_tang(ct)).setLengthFactor(1).setWidthFactor(.5)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])
            ###
            ct2 = c/float(ncurves) * 2*pi
            #curva2 = Curve3D(make_curva2(ct2),(pi/2,3*pi/2,100), width=0.5)
            curva2 = Curve3D(make_curva2(ct2),(-pi/2,pi/2,100), width=0.5)
            curva2.attachField("tangente", make_tang2(ct2)).setLengthFactor(1).setWidthFactor(.5)
            curva2.fields['tangente'].show()
            tangentes2.append(curva2.fields['tangente'])
            self.addChild(curva)
            self.addChild(curva2)


        def animaTangentes(n):
            for tang in tangentes+tangentes2:
                tang.animateArrow(int(n))

        a1 = Animation(animaTangentes, (6000, 0, 99), times=1)
        self.setupAnimations([a1])

        Slider(rangep=('u', 0,99,0,100),func=animaTangentes, parent=self)



class AnimatedArrow(Arrow):

    def __init__(self, base_fun, end_fun, s=1000):
        super(AnimatedArrow, self).__init__(base_fun(0), end_fun(0))
        self.base_function = base_fun
        self.end_function = end_fun
        self.steps = s
        self.animation = Animation(self.animateArrow, (1000, 0, self.steps-1))

    def animateArrow(self, t):
        self.setPoints(self.base_function(t), self.end_function(t))


a = 2.0 #R
b = 1.0 #r
g = -1.0

class ToroVerticalMorseConstr(Page):
    u"""
      En un punto dado del toro (colocado verticalmente sobre el piso),
      el vector del <b>campo de Morse</b> se obtiene proyectando en el plano
      tangente al punto el campo gravitacional constante <b>(0,0,-g)</b>.
      Una gota de agua que escurra desde un punto cercano al punto más alto
      seguiría la trayectoria mostrada en la interacción.
    """
    def __init__(self):
        Page.__init__(self, u"Construcción de un vector del campo de Morse sobre el toro")

        def coreTorusAt(p):
            dyz = sqrt( p[1]**2 + p[2]**2 )
            return Vec3( 0.0, a*p[1]/dyz, a*p[2]/dyz )

        def unitNormalToTorusAt(p):
            core = coreTorusAt(p)
            p_core = p - core
            dp_core = p_core.length()
            return p_core / dp_core

        def projAtTorus(p):
            core = coreTorusAt(p)
            p_core = p - core
            factor = 1.005*b / p_core.length() #un poco más de 1 para que se vea mejor...
            return core + factor * p_core

        def valMorseFieldAt(p):
            n = unitNormalToTorusAt(p)
            gdotn = -g*n[2]
            return Vec3( gdotn*n[0], gdotn*n[1], g + gdotn*n[2] )

        def nextPoint(p,dt):
            return projAtTorus( p + dt*valMorseFieldAt(p) )

        class CurveVectorField:
            def __init__(self, c):
                self.curve = c

            def basePoint(self, t):
                return self.curve[int(t)]

            def endPoint(self, t):
                return self.curve[int(t)] + valMorseFieldAt( self.curve[int(t)] )

        class CurveNormalField:
            def __init__(self, c):
                self.curve = c

            def basePoint(self, t):
                return self.curve[int(t)]

            def endPoint(self, t):
                return self.curve[int(t)] + unitNormalToTorusAt( self.curve[int(t)] )

        class CurveGravityField:
            def __init__(self, c):
                self.curve = c

            def basePoint(self, t):
                return self.curve[int(t)]

            def endPoint(self, t):
                return self.curve[int(t)] + Vec3( 0, 0, g )

        curves = []
        vectorial_fields_curves = []
        vectorial_fields_curves_bk = []

        dtheta = pi/10.0
        nrot = -4
        points_down_curve = []
        points_up_curve = []
        q = Vec3( b*cos(nrot*dtheta), a+b*sin(nrot*dtheta), 0.0 )
        # calculo empezando enmedio del toro
        for n in range(0,100):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_down_curve.append(p)
            points_up_curve.append( Vec3( p[0], p[1], -p[2] ) )
            q = nextPoint(p, 0.05)

        #Tangent Plane
        p = projAtTorus(q)
        p[2] = -p[2]
        v = valMorseFieldAt(p)
        u = v.cross( unitNormalToTorusAt(p) )
        tangent_plane = Plane( _1(200,200,200), p, v+p, u+p )

        points_down_curve.reverse() # recorrer de arriba a enmedio
        points_down_curve.pop() # quitar los puntos de enmedio, repetidos en las listas
        points_down_curve.extend( points_up_curve ) # unir listas
        points_down_curve.reverse()

        curve = Line(points_down_curve, width=2.5)
        curves.append( curve )

        cvf = CurveVectorField(curve)
        vectorial_fields_curves_bk.append(cvf)

        arrow = AnimatedArrow( cvf.basePoint, cvf.endPoint )
        arrow.setDiffuseColor(_1(220,40,200))
        arrow.setWidthFactor( 0.48 )
        arrow.add_tail( 0.025 )

        vectorial_fields_curves.append( arrow )


        cnf = CurveNormalField(curve)
        vectorial_fields_curves_bk.append(cnf)

        arrown = AnimatedArrow( cnf.basePoint, cnf.endPoint )
        arrown.setDiffuseColor(_1(220,240,20))
        arrown.setWidthFactor( 0.4 )
        #arrown.add_tail( 0.025 )

        vectorial_fields_curves.append( arrown )

        cgf = CurveGravityField(curve)
        vectorial_fields_curves_bk.append(cgf)

        arrowg = AnimatedArrow( cgf.basePoint, cgf.endPoint )
        arrowg.setDiffuseColor(_1(10,240,20))
        arrowg.setWidthFactor( 0.4 )
        #arrowg.add_tail( 0.025 )

        vectorial_fields_curves.append( arrowg )

        self.addChildren( curves )
        self.addChildren( vectorial_fields_curves )
        self.addChild( tangent_plane )


        def setSyncParam(t):
            for i in range(0, len(vectorial_fields_curves)):
                #curve = curves[i]
                if t < len( curves[0].getPoints() ):
                    vec_field = vectorial_fields_curves[i]
                    vec_field.animateArrow(t)

            q = (curves[0])[int(t)]
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            u = v.cross( unitNormalToTorusAt(p) )
            tangent_plane.setPoints( p, v+p, u+p )

        Slider(rangep=('t', 0,198,1,199), func=setSyncParam, duration=8000, parent=self)


        # T(u,v)
        def toroParam1(u,v):
            return (b*sin(u),(a+b*cos(u))*cos(v),(a+b*cos(u))*sin(v))

        def toroParam(u,v):
            return Vec3(b*sin(u),(a+b*cos(u))*cos(v),(a+b*cos(u))*sin(v))

        paratoro = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        paratoro.setTransparency(0.25)
        paratoro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        paratoro.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        paratoro.setDiffuseColor(_1(68, 28, 119))
        self.addChild(paratoro)


class ToroVerticalMorse(Page):
    u"""
      El campo de Morse en el toro vertical tiene cuatro singularidades:
      la del punto más alto se llama <b>fuente</b>, la del punto más bajo se
      llama <b>sumidero</b> y las dos en el círculo central se llaman
      <b>puntos silla</b>. Calcule el índice en cada singularidad,
      sume los índices (fíjese en el sentido de los giros) y confirme que se
      cumple el Teorema de Poincaré.
      <p>
      Toro:<br>
      <b>x<sup>2</sup> + (y - R)<sup>2</sup> = r<sup>2</sup></b> rotada en
      torno al eje <b>X</b>
      <p>
      Campo de vectores tangentes:<br>
      <b>p &rarr; G + (G&bull;N(p))N(p)</b>, donde <b>G = (0,0,-g)</b> y
      <b>N(p)</b> es el vector normal unitario en el punto <b>p</b> del toro.
    """
    def __init__(self):
        Page.__init__(self, u"Campo de Morse sobre el toro")

        def coreTorusAt(p):
            dyz = sqrt( p[1]**2 + p[2]**2 )
            return Vec3( 0.0, a*p[1]/dyz, a*p[2]/dyz )

        def unitNormalToTorusAt(p):
            core = coreTorusAt(p)
            p_core = p - core
            dp_core = p_core.length()
            return p_core / dp_core

        def projAtTorus(p):
            core = coreTorusAt(p)
            p_core = p - core
            factor = 1.01*b / p_core.length() #un poco más de 1 para que se vea mejor...
            return core + factor * p_core

        def valMorseFieldAt(p):
            n = unitNormalToTorusAt(p)
            gdotn = -g*n[2]
            return Vec3( gdotn*n[0], gdotn*n[1], g + gdotn*n[2] )

        def nextPoint(p,dt):
            return projAtTorus( p + dt*valMorseFieldAt(p) )

        class CurveVectorField:
            def __init__(self, c):
                self.curve = c

            def basePoint(self, t):
                return self.curve[int(t)]

            def endPoint(self, t):
                return self.curve[int(t)] + valMorseFieldAt( self.curve[int(t)] )

        curves = []
        vectorial_fields_curves = []
        vectorial_fields_curves_bk = []

        dtheta = 2.0*pi/20.0
        for nrot in range(0,20):
            points_down_curve = []
            points_up_curve = []
            q = Vec3( b*cos(nrot*dtheta), a+b*sin(nrot*dtheta), 0.0 )
            # calculo empezando enmedio del toro
            for n in range(0,100):
                p = projAtTorus(q)
                v = valMorseFieldAt(p)
                if v.length() < 0.01:
                    break
                points_down_curve.append(p)
                points_up_curve.append( Vec3( p[0], p[1], -p[2] ) )
                q = nextPoint(p, 0.05)

            points_down_curve.reverse() # recorrer de arriba a enmedio
            points_down_curve.pop() # quitar los puntos de enmedio, repetidos en las listas
            points_down_curve.extend( points_up_curve ) # unir listas
            points_down_curve.reverse()

            curve = Line(points_down_curve, width=2.5)
            curves.append( curve )

            cvf = CurveVectorField(curve)
            vectorial_fields_curves_bk.append(cvf)

            arrow = AnimatedArrow( cvf.basePoint, cvf.endPoint )
            arrow.setDiffuseColor(_1(220,40,20))
            arrow.setWidthFactor( 0.25 )
            arrow.add_tail( 0.025 )

            vectorial_fields_curves.append( arrow )


            # la otra mitad del toro... reflejando por el eje Z
            points_reflected_curve = []
            for p in points_down_curve:
                points_reflected_curve.append( Vec3( -p[0], -p[1], p[2] ) )

            curveR = Line(points_reflected_curve, width=2.5)
            curves.append( curveR )

            cvf = CurveVectorField(curveR)
            vectorial_fields_curves_bk.append(cvf)

            arrow = AnimatedArrow( cvf.basePoint, cvf.endPoint )
            arrow.setDiffuseColor(_1(220,40,20))
            arrow.setWidthFactor( 0.25 )
            arrow.add_tail( 0.025 )

            vectorial_fields_curves.append( arrow )

        # paralelos hasta arriba
        points_curve1 = []
        q = Vec3( 0.25, 0.0, a+b )
        for n in range(0,100):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_curve1.append(p)
            q = nextPoint(p, 0.05)

        curve1 = Line(points_curve1, width=2.5)
        curves.append( curve1 )

        cvf = CurveVectorField(curve1)
        vectorial_fields_curves_bk.append(cvf)

        arrow = AnimatedArrow( cvf.basePoint, cvf.endPoint )
        arrow.setDiffuseColor(_1(220,40,20))
        arrow.setWidthFactor( 0.25 )
        arrow.add_tail( 0.025 )

        vectorial_fields_curves.append( arrow )

        points_curve2 = []
        q = Vec3( -0.25, 0.0, a+b )
        for n in range(0,100):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_curve2.append(p)
            q = nextPoint(p, 0.05)

        curve2 = Line(points_curve2, width=2.5)
        curves.append( curve2 )

        cvf = CurveVectorField(curve2)
        vectorial_fields_curves_bk.append(cvf)

        arrow = AnimatedArrow( cvf.basePoint, cvf.endPoint )
        arrow.setDiffuseColor(_1(220,40,20))
        arrow.setWidthFactor( 0.25 )
        arrow.add_tail( 0.025 )

        vectorial_fields_curves.append( arrow )


        self.addChildren( curves )
        self.addChildren( vectorial_fields_curves )


        def setSyncParam(t):
            for i in range(0, len(vectorial_fields_curves)):
                curve = curves[i]
                if t < len( curve.getPoints() ):
                    vec_field = vectorial_fields_curves[i]
                    #vec_field.animateArrow(int(t))
                    vec_field.animateArrow(t)

        Slider(rangep=('t', 0,198,1,199), func=setSyncParam, duration=16000, parent=self)


        # T(u,v)
        def toroParam1(u,v):
            return (b*sin(u),(a+b*cos(u))*cos(v),(a+b*cos(u))*sin(v))

        def toroParam(u,v):
            return Vec3(b*sin(u),(a+b*cos(u))*cos(v),(a+b*cos(u))*sin(v))

        paratoro = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        paratoro.setTransparency(0.25)
        paratoro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        paratoro.setDiffuseColor(_1(68, 28, 119))
        self.addChild(paratoro)

        critic1 = Sphere( center=Vec3(0,0,a+b), radius=0.075, color=_1(240,10,20) )
        critic2 = Sphere( center=Vec3(0,0,a-b), radius=0.075, color=_1(240,10,20) )
        critic3 = Sphere( center=Vec3(0,0,-a+b), radius=0.075, color=_1(240,10,20) )
        critic4 = Sphere( center=Vec3(0,0,-a-b), radius=0.075, color=_1(240,10,20) )

        self.addChild(critic1)
        self.addChild(critic2)
        self.addChild(critic3)
        self.addChild(critic4)



figuras = [
        Plano1,
        Esfera1,
        Esfera2,
        Esfera3,
        ParaboloideHiperbolico,
        ParaboloideHiperbolicoReglado,
        ParaboloideHiperbolicoCortes,
        ToroMeridianos,
        ToroParalelos,
        ToroVerticalMorseConstr,
        ToroVerticalMorse
]


class CamposVectoriales(Chapter):
    def __init__(self):
        Chapter.__init__(self, name=u"Campos vectoriales, singularidades e índice")
        for f in figuras:
            self.addPage(f())


if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.book.addChapter(CamposVectoriales())
    visor.chapter.chapterSpecificIn()
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())

