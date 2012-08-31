# -*- coding: utf-8 -*-
from math import *

from PyQt4 import QtGui
from pivy.coin import *

from superficie.nodes.pointset import PointSet
from superficie.nodes.line import Line
from superficie.nodes.plane import Plane
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
from superficie.viewer.Viewer import Viewer
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
    u"""<b>Curvaturas normales</b> en el punto (3,0,0)
      de la elipsoide (1/9)x^2 + (1/4)y^2 + z^2 = 1
    """

    def __init__(self):
        super(Elipsoide1,self).__init__('Elipsoide 1')

        self.showAxis(False)

        ellipsoid = createEllipsoid(a, b, c)
        self.addChild(ellipsoid)

        normal = Arrow((a,0,0), (a+1,0,0), 0.03)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param/1000.0
                return Vec3(a*cos(s), b*sin(param1)*sin(s), c*cos(param1)*sin(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (u, sin(pi_2*t)*v, cos(pi_2*t)*v)
        normal_plane = ParametricPlot3D(normal_plane_function, (-3.1, 3.1), (-2.1, 2.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['t'].asAnimation()

        def basePoint(t):
            return Vec3(a,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(a, b*sin(s)/vn, c*cos(s)/vn)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t/1000.0
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

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Elipsoide2(Page):
    u"""<b>Curvaturas normales</b> en el punto (0,0,1)
      de la elipsoide (1/9)x^2 + (1/4)y^2 + z^2 = 1
    """

    def __init__(self):
        super(Elipsoide2,self).__init__('Elipsoide 2')

        self.showAxis(False)

        ellipsoid = createEllipsoid(a, b, c)
        self.addChild(ellipsoid)

        normal = Arrow((0,0,c), (0,0,c+1), 0.03)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param/1000.0
                return Vec3(a*cos(param1)*sin(s), b*sin(param1)*sin(s), c*cos(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (cos(pi_2*t2)*v, sin(pi_2*t2)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-3.1, 3.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['t2'].asAnimation()

        def basePoint(t):
            return Vec3(0,0,c)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            vn = sqrt((a*cos(s))**2 + (b*sin(s))**2)
            return Vec3(a*cos(s)/vn, b*sin(s)/vn, c)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t/1000.0
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

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Elipsoide3(Page):
    u"""<b>Curvaturas normales</b> en el punto <b>umbílico</b>
      (2.3717,0,0.6124)
      de la elipsoide (1/9)x^2 + (1/4)y^2 + z^2 = 1
    """
#(0.6124,0,2.3717)(0.790569415042, 0, 0.612372435696)

    def __init__(self):
        super(Elipsoide3,self).__init__('Elipsoide 3')

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
                param1 = pi_2*self.param/1000.0
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
        normal_plane = ParametricPlot3D(normal_plane_function, (-3.3, 0.1), (-1.9, 4.9))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.setBoundingBox((-3.5,3.5),(-2.1,2.1),(-1.5,1.5))
        normal_plane.animation = normal_plane.parameters['t3'].asAnimation()

        def basePoint(t):
            return Vec3(px,0,pz)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            vn = sqrt((nz*cos(s))**2 + (sin(s))**2 + (nx*cos(s))**2)
            return Vec3(px - nz*cos(s)/vn, sin(s)/vn, pz + nx*cos(s)/vn)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        objects = [curve, normal_plane, tangent_arrow]
        self.addChildren( objects )

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Cilindro(Page):
    u"""<b>Curvaturas normales</b> en un punto del cilindro
      $x^2 + z^2 = 1$.
    """

    def __init__(self):
        super(Cilindro,self).__init__('Cilindro')

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
                return Vec3(cos(s), tan(pi_2*self.param/1000.0) * cos(s), sin(s))

            def setParam(self, t):
                self.param = t

        cylc_obj = CylCurve()
        curve = Curve3DParam(cylc_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)
        curve.setBoundingBox((-3.1,3.1),(-3.1,3.1),(-3.1,3.1))
# Ojo! No basta con "acotar", la vista se recalcula con todo el objeto...

        normal_plane_function = lambda u, v: (cos(pi_2*tc)*v, sin(pi_2*tc)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-2.1, 2.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['tc'].asAnimation()

        def basePoint(t):
            return Vec3(0,0,1)

        def endTangentPoint(t):
            s = pi_2*t/1000.0
            return Vec3(cos(s), sin(s), 1)

        def endCurvaturePoint(t):
            return Vec3(0, 0, 1.0-cos(pi_2*t/1000.0))

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Hiperboloide(Page):
    u"""<b>Curvaturas normales</b> en el punto (0,0,0)
      de la hiperboloide (1/4)x^2 - (1/9)y^2 = z
    """

    def __init__(self):
        super(Hiperboloide,self).__init__('Hiperboloide')

        self.showAxis(False)

        hyperboloid = createHyperboloid(2,3)
        self.addChild(hyperboloid)

        normal = Arrow((0,0,0), (0,0,1), 0.03)
        self.addChild(normal)

        class Parabole(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                return Vec3(cos(pi_2*self.param/1000.0)*s, sin(pi_2*self.param/1000.0)*s, (cos(pi_2*self.param/1000.0)*s)**2/4 - (sin(pi_2*self.param/1000.0)*s)**2/9)

            def setParam(self, t):
                self.param = t

        parabole_obj = Parabole()
        curve = Curve3DParam(parabole_obj, (-4.0, 4.0, 200), color=(0.9, 0.2, 0.1), width=6)

        normal_plane_function = lambda u, v: (cos(pi_2*th)*v, sin(pi_2*th)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['th'].asAnimation()

        def basePoint(t):
            return Vec3(0,0,0)

        def endTangentPoint(t):
            s = pi_2*t/1000.0
            return Vec3(cos(s), sin(s), 0)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = pi_2*t/1000.0
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

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Toro1(Page):
    u"""<b>Curvaturas normales</b> en el punto (4,0,0)
      del toro...
    """

    def __init__(self):
        super(Toro1,self).__init__('Toro 1')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1+r2,0,0), (r1+r2+1,0,0), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param/1000.0
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
                param1 = pi_2*self.param/1000.0
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
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['tt1'].asAnimation()

        def basePoint(t):
            return Vec3(r1+r2,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            return Vec3(r1+r2, sin(s), cos(s))

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            s = t/1000.0
            #vn = (b*sin(s))**2 + (c*cos(s))**2
            # ||curve''(0)||
            return Vec3(r1+s*(r2-1/r1), 0, 0)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))

        objects = [curve, curve2, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class Toro2(Page):
    u"""<b>Curvaturas normales</b> en el punto (3,0,1)
      del toro...
    """

    def __init__(self):
        super(Toro2,self).__init__('Toro 2')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1,0,r2), (r1,0,r2+1), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param/1000.0
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
                param1 = pi_2*self.param/1000.0
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
        curve.setBoundingBox((-0.1,4.1),(-4.1,4.1),(0.01,1.1))

        torusc2_obj = TorusCurve2()
        curve2 = Curve3DParam(torusc2_obj, (-9.0, 3.0, 100), color=(0.9, 0.2, 0.1), width=6)
        curve2.setBoundingBox((-0.1,4.1),(-4.1,4.1),(-1.1, -0.01))

        normal_plane_function = lambda u, v: (r1+cos(pi_2*tt2)*v, sin(pi_2*tt2)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-3.1, 3.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['tt2'].asAnimation()

        def basePoint(t):
            return Vec3(r1,0,r2)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            #vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(r1+cos(s), sin(s), r2)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            #s = pi_2*t/1000.0
            s = t/1000.0
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

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )


class Toro3(Page):
    u"""<b>Curvaturas normales</b> en el punto (2,0,0)
      del toro...
    """

    def __init__(self):
        super(Toro3,self).__init__('Toro 3')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1-r2,0,0), (r1-r2-1,0,0), 0.03)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                param1 = pi_2*self.param/1000.0
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
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        normal_plane.setTransparency(0.75)
        normal_plane.setTransparencyType(SoTransparencyType.SCREEN_DOOR)
        normal_plane.animation = normal_plane.parameters['tt3'].asAnimation()

        def basePoint(t):
            return Vec3(r1-r2,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            s = pi_2*t/1000.0
            #vn = sqrt((b*sin(s))**2 + (c*cos(s))**2)
            return Vec3(r1-r2, -sin(s), cos(s))

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            #s = pi_2*t/1000.0
            s = t/1000.0
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

        self.setupAnimations( [ AnimationGroup( objects, (1000,0,999) ) ] )



class CurvaturasNormales(Chapter):

    def __init__(self):
        Chapter.__init__(self, name="Curvaturas Normales")

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
