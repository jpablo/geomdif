# -*- coding: utf-8 -*-
from math import pi, sin, cos, tan, sqrt
from PyQt4 import QtGui
from pivy.coin import SoTransparencyType
from superficie.util import Vec3, _1, partial
from superficie.nodes import Curve3D, Line, Arrow, BasePlane, Plane
from superficie.animations import AnimationGroup, Animation
from superficie.plots import ParametricPlot3D, Plot3D
from superficie.widgets import VisibleCheckBox, Slider
from superficie.book import Chapter, Page


class Plano1(Page):
    ## meridianos
    def __init__(self):
        Page.__init__(self, u"Sobre el plano")

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
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

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

        a1 = Animation(animaTangentes, (10000, 0, 79), times=2)
        self.setupAnimations([a1])


class Esfera2(Page):
    ## paralelos
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

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
        self.setupAnimations([AnimationGroup(tangentes, (6000, 0, 99), times=2)])


class Esfera3(Page):
    ## meridianos
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

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
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

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
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

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
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

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

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])


class ToroMeridianos(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el toro")
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

        a1 = Animation(animaTangentes, (6000, 0, 99), times=2)
        self.setupAnimations([a1])


class ToroParalelos(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el toro")
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

        a1 = Animation(animaTangentes, (6000, 0, 99), times=2)
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
    u"""Construcción de un campo de Morse sobre un toro.<br><br>
        Los vectores del campo de Morse en un punto dado sobre el toro
        son las proyecciones en el plano tangente en el punto del campo
        gravitacional constante en el espacio dado por el vector (0,0,-g).
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
        for n in range(0,20):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_down_curve.append(p)
            points_up_curve.append( Vec3( p[0], p[1], -p[2] ) )
            q = nextPoint(p, 0.25)

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
        arrow.setDiffuseColor(_1(220,40,20))
        arrow.setWidthFactor( 0.25 )
        arrow.add_tail( 0.025 )

        vectorial_fields_curves.append( arrow )


        cnf = CurveNormalField(curve)
        vectorial_fields_curves_bk.append(cnf)

        arrown = AnimatedArrow( cnf.basePoint, cnf.endPoint )
        arrown.setDiffuseColor(_1(220,240,20))
        arrown.setWidthFactor( 0.25 )
        #arrown.add_tail( 0.025 )

        vectorial_fields_curves.append( arrown )

        cgf = CurveGravityField(curve)
        vectorial_fields_curves_bk.append(cgf)

        arrowg = AnimatedArrow( cgf.basePoint, cgf.endPoint )
        arrowg.setDiffuseColor(_1(20,40,220))
        arrowg.setWidthFactor( 0.25 )
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
                    vec_field.animateArrow(int(t))

            q = (curves[0])[int(t)]
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            u = v.cross( unitNormalToTorusAt(p) )
            tangent_plane.setPoints( p, v+p, u+p )

        Slider(rangep=('t', 0,38,1,39), func=setSyncParam, duration=10000, parent=self)


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
            for n in range(0,20):
                p = projAtTorus(q)
                v = valMorseFieldAt(p)
                if v.length() < 0.01:
                    break
                points_down_curve.append(p)
                points_up_curve.append( Vec3( p[0], p[1], -p[2] ) )
                q = nextPoint(p, 0.25)

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
        for n in range(0,40):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_curve1.append(p)
            q = nextPoint(p, 0.25)

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
        for n in range(0,40):
            p = projAtTorus(q)
            v = valMorseFieldAt(p)
            if v.length() < 0.01:
                break
            points_curve2.append(p)
            q = nextPoint(p, 0.25)

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
                    vec_field.animateArrow(int(t))

        Slider(rangep=('t', 0,38,1,39), func=setSyncParam, duration=10000, parent=self)


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
        Chapter.__init__(self, name="Campos Vectoriales")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(CamposVectoriales())
    visor.chapter.chapterSpecificIn()
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())
