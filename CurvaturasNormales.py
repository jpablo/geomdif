# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.nodes.pointset import PointSet
from superficie.nodes.line import Line
from superficie.nodes.curve3d import Curve3D, fix_function
from superficie.nodes.arrow import Arrow
from superficie.book import chapter, page
from superficie.book.chapter import Chapter
from superficie.book.page import Page
from superficie.util import Vec3, _1, partial
from superficie.widgets import visible_checkbox, slider
from superficie.widgets.visible_checkbox import VisibleCheckBox
from superficie.widgets.slider import Slider
from superficie.plots import ParametricPlot3D
from superficie.animations import Animation, AnimationGroup

#
pi_2 = 1.5708


class Curve3DParam(Curve3D):

    def __init__(self, func, interval, color=(1, 1, 1), width=1, nvertices=-1, max_distance = None):
        super(Curve3DParam,self).__init__(func, interval, color, width, nvertices, max_distance)

        self.original_function = func
        self.animation = Animation(self.setParam, (1000,0,999))

    def setParam(self, t):
        self.original_function.setParam(t)
        self.function = fix_function(self.original_function, self.intervals[0][0])
        self.updatePoints(self.function)


class AnimatedArrow(Arrow):

    def __init__(self, base_fun, end_fun, s=1000):
        super(AnimatedArrow, self).__init__(base_fun(0), end_fun(0))
        self.base_function = base_fun
        self.end_function = end_fun
        self.steps = s
        self.animation = Animation(self.animateArrow, (1000, 0, self.steps-1))

    def animateArrow(self, t):
        self.setPoints(self.base_function(t), self.end_function(t))


# Tricky global ellipsoid parameters
a = 3.0
b = 2.0
c = 1.0

def createEllipsoid(a,b,c):

    par_e = lambda u, v: Vec3(a * sin(v) * cos(u), b * sin(u) * sin(v), c * cos(v))
    e = ParametricPlot3D(par_e, (0, 2*pi, 100), (0, pi, 100))
    e.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
    e.setTransparency(0.5)
    e.setDiffuseColor(_1(40, 200, 120))

    return e


def createHyperboloid(a,b):

    par_h = lambda u, v: Vec3(u, v, u**2/(a**2)-v**2/(b**2))
    h = ParametricPlot3D(par_h, (-4, 4, 100), (-4, 4, 100))
    h.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
    h.setTransparency(0.5)
    h.setDiffuseColor(_1(220, 200, 80))

    return h


# Tricky global torus parameters
r1 = 3.0
r2 = 1.0

def createTorus(r1,r2):

    par_t = lambda u, v: Vec3((r1 + r2 * cos(v)) * cos(u), (r1 + r2 * cos(v)) * sin(u), r2 * sin(v))
    tor = ParametricPlot3D(par_t, (-pi, pi, 100), (-pi, pi, 100))
    tor.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
    tor.setTransparency(0.5)
    tor.setDiffuseColor(_1(180, 220, 200))

    return tor



class Elipsoide1(Page):
    u"""
      <p>
      En un punto <b>p</b> de una superficie <b>M</b> fijamos <b>N(p)</b>,
      uno de los vectores normales unitarios a <b>T<sub>p</sub>M</b>.
      Un plano que contiene a <b>N(p)</b> corta a <b>M</b> en una curva
      llamada <b>sección normal</b> con vector normal unitario <b>n(p)</b>
      y curvatura <b>k(p)</b>. Si <b>n(p) = N(p)</b> decimos que
      <b>k(p)</b> es positiva y negativa si <b>n(p) = -N(p)</n>.
      <p>
      La <b>curvatura gaussiana</b> de <b>M</b> en <b>p</b> es
      <b>K(p) = k<sub>1</sub>(p)k<sub>2</sub>(p)</b>,
      donde <b>k<sub>1</sub>(p)</b> es la máxima curvatura de las secciones
      normales y <b>k<sub>2</sub>(p)</b> es la mínima.
      <p>
      La interacción muestra todas las secciones normales de la elipsoide en
      el punto <b>(3,0,0)</b>. El vector amarillo es <b>n(p)</b>,
      un vector azul es <b>N(p)</b>, normal a <b>T<sub>p</sub>M</b>,
      y el otro es el vector tangente <b>t(p)</b> a la sección normal.
      <p>
      En la elipsoide, <b>N(p)</b> es siempre opuesto a <b>n(p)</b>
      y por eso <b>K(p)</b> es positiva.
    """

    def __init__(self, parent=None):
        super(Elipsoide1,self).__init__('Secciones normales de un elipsoide en el punto (3,0,0)<br><br>x<sup>2</sup>/9 + y<sup>2</sup>/4 + z<sup>2</sup> = 1')

        self.showAxis(False)

        ellipsoid = createEllipsoid(a, b, c)
        self.addChild(ellipsoid)

        normal = Arrow((a,0,0), (a+1,0,0), 0.03)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                return Vec3(a*cos(s), b*sin(param1)*sin(s), c*cos(param1)*sin(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (a*u, b*sin(pi_2*t)*v, c*cos(pi_2*t)*v)
        normal_plane_function.func_globals['t']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-2.1, 2.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['t'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(a,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(a, b*sin(s)/vn, c*cos(s)/vn)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t #/1000.0
            vn = (b*sin(s))**2 + (c*cos(s))**2
            # ||curve''(0)||
            # nn = a
            return Vec3(a-a/vn, 0, 0) # Vec3(a-nn/vn, 0, 0)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['t']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1,0,20),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Elipsoide2(Page):
    u"""
      En la misma elipsoide, cambiamos al punto <b>(0,0,1)</b>.
      Note cómo varía la longitud de los vectores amarillos <b>n(p)</b>
      al ejecutar la interacción.
    """

    def __init__(self):
        super(Elipsoide2,self).__init__('Secciones normales de un elipsoide en el punto (0,0,1)<br><br>x<sup>2</sup>/9 + y<sup>2</sup>/4 + z<sup>2</sup> = 1')

        self.showAxis(False)

        ellipsoid = createEllipsoid(a, b, c)
        self.addChild(ellipsoid)

        normal = Arrow((0,0,c), (0,0,c+1), 0.03)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                return Vec3(a*cos(param1)*sin(s), b*sin(param1)*sin(s), c*cos(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (a*cos(pi_2*t2)*v, b*sin(pi_2*t2)*v, c*u)
        normal_plane_function.func_globals['t2']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-1.1, 1.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['t2'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(0,0,c)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            vn = sqrt((a*cos(s))**2 + (b*sin(s))**2)
            return Vec3(a*cos(s)/vn, b*sin(s)/vn, c)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t #/1000.0
            vn = (a*cos(s))**2 + (b*sin(s))**2
            # ||curve''(0)||
            # nn = c
            return Vec3(0, 0, c-2.0*c/vn)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['t2']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1,0,20),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Elipsoide3(Page):
    u"""
      <p>
      En una elipsoide hay cuatro puntos donde todas las secciones normales
      tienen la misma curvatura. Por eso se llaman <b>puntos umbílicos</b>.
      La interacción muestra que el vector <b>n(p)</b>, el vector normal
      (amarillo) de la sección normal en el punto <b>p</b>,
      se mantiene constante.
      <p>
      Utilizamos el punto <b>(2.3717, 0, 0.6124)</b>, los otros tres puntos
      umbílicos, no ilustrados, resultan de reflejar en los
      planos <b>XY</b> y <b>YZ</b>.
      <p>
      Las únicas superficies cuyos puntos son todos umbílicos son el plano
      y la esfera.
    """
#(0.6124,0,2.3717)(0.790569415042, 0, 0.612372435696)

    def __init__(self):
        super(Elipsoide3,self).__init__(u'Secciones normales de un elipsoide un punto umbílico<br><br>x<sup>2</sup>/9 + y<sup>2</sup>/4 + z<sup>2</sup> = 1')

        self.showAxis(False)

        ellipsoid = createEllipsoid(a, b, c)
        self.addChild(ellipsoid)

        # umbilic point U = (px, 0, pz)
        #px = sqrt((a**2-b**2)/(a**2-c**2))
        #pz = sqrt((c**2)*(b**2-c**2)/(a**2-c**2))
        pz = sqrt((c**2-b**2)/(c**2-a**2))
        px = sqrt((a**2)*(b**2-a**2)/(c**2-a**2))

        # gradient in umbilic point U
        nx = 2*px/(a**2)
        nz = 2*pz/(c**2)

        n = sqrt(nx**2+nz**2)

        nx = nx/n
        nz = nz/n

        #print px, pz, px**2/(a**2)+pz**2/(c**2), nx, nz

        normal = Arrow((px,0,pz), (px+nx,0,pz+nz), 0.03)
        self.addChild(normal)

        curvature_arrow = Arrow((px,0,pz), (px-0.5*nx,0,pz-0.5*nz), 0.05)
        curvature_arrow.setDiffuseColor(_1(220,200,20))
        self.addChild(curvature_arrow)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                A = (nx**2)/9.0 + nz**2
                C = ((nz**2)/9.0 + nx**2)*cosp**2+(sinp**2)/4.0
                B = (16.0/9.0)*nx*nz*cosp
                D = 2.0*(nx*px/9.0 + nz*pz)
                E = 2.0*(nx*pz - nz*px/9.0)*cosp
                #F = 0
                ins_sqrt = A**2 + C**2 + B**2 - 2.0*A*C
                L1 = (A + C + sqrt(ins_sqrt) )/2.0
                L2 = (A + C - sqrt(ins_sqrt) )/2.0
                dis = 4.0*A*C-B**2
                C1 = (B*E-2.0*C*D)/dis
                C2 = (D*B-2.0*A*E)/dis
                detq = (A*(E**2) + C*(D**2) - B*D*E) #/4.0
                aell = sqrt(dis/(L1*detq))/(1.0+sinp*sinp)
                bell = sqrt(dis/(L2*detq))/(1.0+sinp*sinp)
                theta = atan( B/(A-C) )/2.0
                u = aell*cos(s)*cos(theta) - bell*sin(s)*sin(theta) + C1
                v = bell*sin(s)*cos(theta) + aell*cos(s)*sin(theta) + C2
                return Vec3(px+u*nx-cosp*v*nz, sinp*v, pz+u*nz+cosp*v*nx)

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)

        # Rotation Z_Axis=(0,0,1) -> n=(nx,0,nz) (||n||=1)
        # Rot(x,y,z)=(x*nz+z*nx,y,-x*nx+z*nz)
        normal_plane_function = lambda u, v: (px+u*nx-cos(pi_2*t3)*v*nz, sin(pi_2*t3)*v, pz+u*nz+cos(pi_2*t3)*v*nx)
        normal_plane_function.func_globals['t3']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-3.3, 0.1), (-1.9, 4.9))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.setBoundingBox((-3.5,3.5),(-2.1,2.1),(-1.5,1.5))
        #normal_plane.animation = normal_plane.parameters['t3'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(px,0,pz)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            vn = sqrt((nz*cos(s))**2 + (sin(s))**2 + (nx*cos(s))**2)
            return Vec3(px - nz*cos(s)/vn, sin(s)/vn, pz + nx*cos(s)/vn)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        objects = [curve, normal_plane, tangent_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['t3']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            #curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1,0,20),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Cilindro(Page):
    u"""
      Cualquier entorno de un punto de un cilindro de revolución puede
      acomodarse en otro lugar del cilindro con sólo cuidar de que la
      generatriz se superponga en otra. Por esto el cilindro de
      revolución es una <b>superficie homogénea</b>.
      <p>
      La interacción  muestra todas las posibles secciones normales:
      desde una circunferencia cuya curvatura es <b>-1</b> porque
      <b>n(p)=-N(p)</b>, hasta una recta (la otra no contiene al punto de apoyo)
      que tiene <b>n(p)=0</b>, pasando por elipses de curvatura cuyo vector de
      curvatura también tiene sentido opuesto a <b>N(p)</b>.
      Por eso la curvatura gaussiana es cero: <b>K(p)=0</b>.
    """

    def __init__(self):
        super(Cilindro,self).__init__('Secciones normales de un cilindro recto circular<br><br>x<sup>2</sup> + z<sup>2</sup> = 1')

        self.showAxis(False)

        cyl = SoCylinder()
        cyl.radius.setValue(1.0)
        cyl.height.setValue(4.0)
        cyl.parts = SoCylinder.SIDES

        light = SoShapeHints()

        mat = SoMaterial()
        mat.emissiveColor = _1(80, 120, 200)
        mat.diffuseColor = _1(80, 120, 200)
        mat.transparency.setValue(0.5)

        sep = SoSeparator()
        sep.addChild(light)
        sep.addChild(mat)
        sep.addChild(cyl)

        self.addChild(sep)

        normal = Arrow((0,0,1), (0,0,2), 0.03)
        self.addChild(normal)

        class CylCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                #pi_2*self.param/1000.0
                return Vec3(cos(s), tan(pi_2*self.param) * cos(s), sin(s))

            def setParam(self, t):
                self.param = t

        cylc_obj = CylCurve()
        curve = Curve3DParam(cylc_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)
        curve.setBoundingBox((-3.1,3.1),(-3.1,3.1),(-3.1,3.1))
# Ojo! No basta con "acotar", la vista se recalcula con todo el objeto...

        normal_plane_function = lambda u, v: (cos(pi_2*tc)*v, sin(pi_2*tc)*v, u)
        normal_plane_function.func_globals['tc']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-2.1, 2.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['tc'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(0,0,1)

        def endTangentPoint(t):
            s = pi_2*t #/1000.0
            return Vec3(cos(s), sin(s), 1)

        def endCurvaturePoint(t):
            return Vec3(0, 0, 0.9-cos(pi_2*t)) #/1000.0

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['tc']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,0.99,0,20),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Hiperboloide(Page):
    u"""
      Por cualquier punto de un paraboloide hiperbólico pasan dos rectas
      completamente contenidas en la superficie. Y también pasan dos familias
      de parábolas contenidas en la superficie, cuyas concavidades apuntan a
      lados distintos del plano tangente, como lo muestra la interacción.
      Por eso <b>K(p)</b> es <b>menor que cero en todos los puntos<b> .
    """

    def __init__(self):
        super(Hiperboloide,self).__init__(u'Secciones normales de un paraboloide hiperbólico<br><br>x<sup>2</sup>/4 - y<sup>2</sup>/9 = z')

        self.showAxis(False)

        hyperboloid = createHyperboloid(2,3)
        self.addChild(hyperboloid)

        normal = Arrow((0,0,0), (0,0,1), 0.03)
        self.addChild(normal)

        class Parabole(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                return Vec3(cos(pi_2*self.param)*s, sin(pi_2*self.param)*s, (cos(pi_2*self.param)*s)**2/4 - (sin(pi_2*self.param)*s)**2/9)

            def setParam(self, t):
                self.param = t

        parabole_obj = Parabole()
        curve = Curve3DParam(parabole_obj, (-4.0, 4.0, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (cos(pi_2*th)*v, sin(pi_2*th)*v, u)
        normal_plane_function.func_globals['th']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['th'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(0,0,0)

        def endTangentPoint(t):
            s = pi_2*t #/1000.0
            return Vec3(cos(s), sin(s), 0)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t #/1000.0
            # vn = 1.0
            # ||curve''(0)||
            nn = ((cos(s))**2)/2 - 2*((sin(s))**2)/9
            return Vec3(0, 0, 2.0*nn)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['th']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1.0,0,20),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Toro1(Page):
    u"""
      Para un punto <b>p</b> en el paralelo exterior de un toro de revolución,
      todas las secciones normales tienen su concavidad de un mismo lado del
      plano tangente y, en consecuencia, las curvaturas máxima y mínima de las
      secciones normales tienen el mismo signo (los puntos son <b>elípticos</b>)
      por eso <b>K(p)</b> es mayor que <b>0</b>.
    """

    def __init__(self):
        super(Toro1,self).__init__(u'Secciones normales de un toro en un punto elíptico')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1+r2,0,0), (r1+r2+1,0,0), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                u = s #*rot
                btor = 2.0*u**2 + 16.0 - 36.0*sinp**2
                v = sqrt( (-btor+sqrt(btor**2 - 4.0*(u**4-20.0*u**2+64.0)) )/2.0 )
                return Vec3(u, sinp*v, cosp*v)

            def setParam(self, t):
                self.param = t

        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (2.0, 4.0, 200), color=(0.9, 0.2, 0.1), width=6)

        class TorusCurve2(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                u = s #*rot
                btor = 2.0*u**2 + 16.0 - 36.0*sinp**2
                v = -sqrt( (-btor+sqrt(btor**2 - 4.0*(u**4-20.0*u**2+64.0)) )/2.0 )
                return Vec3(u, sinp*v, cosp*v)

            def setParam(self, t):
                self.param = t

        torusc2_obj = TorusCurve2()
        curve2 = Curve3DParam(torusc2_obj, (2.0, 4.0, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (u, sin(pi_2*tt1)*v, cos(pi_2*tt1)*v)
        normal_plane_function.func_globals['tt1']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['tt1'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(r1+r2,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            return Vec3(r1+r2, sin(s), cos(s))

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = t #/1000.0
            #vn = (b*sin(s))**2 + (c*cos(s))**2
            # ||curve''(0)||
            return Vec3(r1+s*(r2-1/r1), 0, 0)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, curve2, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['tt1']=t
            normal_plane.updateAll()
            curve.setParam(t)
            curve2.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1.0,0,40),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Toro2(Page):
    u"""
      En el cuadro del capítulo "Plano tangente” referente al toro de revolución,
      vimos que para los puntos del paralelo superior el contacto entre el plano
      tangente y el toro es todo el paralelo superior. A lo largo de él, el
      vector normal permanece constante. Como lo muestra la interacción,
      la sección normal definida por el vector tangente al paralelo en el
      punto es una curva muy pegada a su recta tangente, como la curva cuártica.
      Por ello la curvatura normal en esa dirección es <b>cero</b>
      (el vector amarillo desaparece) y como las demás secciones tienen curvatura
      con un mismo signo, en esos puntos <b>parabólicos</b>, <b>K(p)=0</b>.
    """

    def __init__(self):
        super(Toro2,self).__init__(u"Secciones normales de un toro en un punto parabólico")

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1,0,r2), (r1,0,r2+1), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                v = s
                btor = 2.0*v**2 + 12.0*cosp*v + 34.0
                ctor = v**4 + 12.0*cosp*v**3 + (36.0*cosp**2-2.0)*v**2 - 12.0*cosp*v - 35.0
                dis = btor**2 - 4.0*ctor
                if dis < 0.0:
                    #v = 0.0
                    u = -1.0
                else:
                    inside = -btor + sqrt( dis )
                    if inside < 0.0:
                        #v = 0.0
                        u = -1.0
                    else:
                        u = sqrt( inside/2.0 )
                return Vec3(r1+cosp*v, sinp*v, u)

            def setParam(self, t):
                self.param = t


        class TorusCurve2(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                v = s
                btor = 2.0*v**2 + 12.0*cosp*v + 34.0
                ctor = v**4 + 12.0*cosp*v**3 + (36.0*cosp**2-2.0)*v**2 - 12.0*cosp*v - 35.0
                dis = btor**2 - 4.0*ctor
                if dis < 0.0:
                    #v = 0.0
                    u = 1.0
                else:
                    inside = -btor + sqrt( dis )
                    if inside < 0.0:
                        #v = 0.0
                        u = 1.0
                    else:
                        u = -sqrt( inside/2.0 )
                return Vec3(r1+cosp*v, sinp*v, u)

            def setParam(self, t):
                self.param = t


        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (-9.0, 3.0, 100), color=(0.9, 0.2, 0.1), width=6)
        curve.setBoundingBox((-4.1,4.1),(-4.1,4.1),(0.01,1.1))

        torusc2_obj = TorusCurve2()
        curve2 = Curve3DParam(torusc2_obj, (-9.0, 3.0, 100), color=(0.9, 0.2, 0.1), width=6)
        curve2.setBoundingBox((-4.1,4.1),(-4.1,4.1),(-1.1, -0.01))

        normal_plane_function = lambda u, v: (r1+cos(pi_2*tt2)*v, sin(pi_2*tt2)*v, u)
        normal_plane_function.func_globals['tt2']=0.0
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-9.1, 3.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.setBoundingBox((-4.1,4.1),(-4.1,4.1),(-1.1,1.1))
        #normal_plane.animation = normal_plane.parameters['tt2'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(r1,0,r2)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            #vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(r1+cos(s), sin(s), r2)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            #s = pi_2*t/1000.0
            s = t #/1000.0
            #vn = (b*sin(s))**2 + (c*cos(s))**2
            # ||curve''(0)||
            # nn = a
            return Vec3(r1, 0, s*r2)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, curve2, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['tt2']=t
            normal_plane.updateAll()
            curve.setParam(t)
            curve2.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1.0,0,40),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )


class Toro3(Page):
    u"""
      En un punto del paralelo interior del toro, las secciones normales
      varían de corresponder a un meridiano hasta el paralelo mismo;
      los vectores normales del meridiano y del paralelo apuntan a lados
      distintos del plano tangente, así que las curvaturas normales máxima y
      mínima tienen signos distintos y, en consecuencia, <b>K(p)</b> es menor
      que <b>0</b> en los puntos de ese paralelo.
    """

    def __init__(self):
        super(Toro3,self).__init__(u'Secciones normales de un toro en un punto hiperbólico')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1-r2,0,0), (r1-r2-1,0,0), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param #/1000.0
                cosp = cos(param1)
                sinp = sin(param1)
                v = s
                btor = 2.0*v**2 - 20.0
                ctor = v**4 + (16.0 - 36.0*sinp**2)*v**2 + 64.0
                dis = btor**2 - 4.0*ctor
                if dis < 0.0:
                    #v = 0.0
                    u = 4.0
                else:
                    inside = -btor-sqrt(dis)
                    if inside < 0.0:
                        #v = 0.0
                        u = 4.0
                    else:
                        u = sqrt( inside/2.0 )
                return Vec3(u, sinp*v, -cosp*v)

            def setParam(self, t):
                self.param = t

        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (-2.0, 2.0, 200), color=(0.9, 0.2, 0.1), width=6)
        curve.setBoundingBox((-0.05,2.95),(-4.1,4.1),(-1.1,1.1))

        normal_plane_function = lambda u, v: (u, sin(pi_2*tt3)*v, -cos(pi_2*tt3)*v)
        normal_plane_function.func_globals['tt3']=t
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        #normal_plane.animation = normal_plane.parameters['tt3'].asAnimation()

        VisibleCheckBox("Plano Normal", normal_plane, True, parent=self)

        def basePoint(t):
            return Vec3(r1-r2,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t #/1000.0
            #vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(r1-r2, -sin(s), cos(s))

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            #s = pi_2*t/1000.0
            s = t #/1000.0
            #vn = (b*sin(s))**2 + (c*cos(s))**2
            # ||curve''(0)||
            # nn = a
            return Vec3(r1-2*s*r2, 0, 0)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        def setSyncParam(t):
            normal_plane_function.func_globals['tt3']=t
            normal_plane.updateAll()
            curve.setParam(t)
            tangent_arrow.animateArrow(t)
            curvature_arrow.animateArrow(t)

        Slider(rangep=('t', 0,1.0,0,40),func=setSyncParam, duration=4000, parent=self)
        #self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class CurvaturasNormales(Chapter):

    def __init__(self):
        Chapter.__init__(self, name="Curvatura y secciones normales")

        figuras = [
            Elipsoide1,
            Elipsoide2,
            Elipsoide3,
            Cilindro,
            Hiperboloide,
            Toro1,
            Toro2,
            Toro3
        ]

        for f in figuras:
            self.addPage(f())
