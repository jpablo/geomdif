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
from superficie.utils import refine_by_distance, refine_by_angle

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
                return Vec3(a*cos(s), b*sin(pi_2*self.param/1000.0)*sin(s), c*cos(pi_2*self.param/1000.0)*sin(s))

            def setParam(self, t):
                self.param = t

            #def tangent(self, s):
            #    return Vec3(-a*sin(s), b*sin(pi_2*self.param/1000.0)*cos(s), c*cos(pi_2*self.param/1000.0)*cos(s))

            #def tangentNormalized(self, s):
            #    vt = self.tangent(s)
            #    nvt = sqrt(vt[0]*vt[0] + vt[1]*vt[1] + vt[2]*vt[2])
            #    vt /= nvt
            #    return vt

            #def curvatureVector(self, s):
            #    vt = self.tangent(s)
            #    nvt = vt[0]*vt[0] + vt[1]*vt[1] + vt[2]*vt[2]
            #    vn = -self.__call__(s)
                #nvn = math.sqrt(vn[0]*vn[0] + vn[1]*vn[1] + vn[2]*vn[2])
            #    vn /= nvt
            #    return vn

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (u, sin(pi_2*t)*v, cos(pi_2*t)*v)
        normal_plane = ParametricPlot3D(normal_plane_function, (-3.1, 3.1), (-2.1, 2.1))
        #normal_plane.setTransparency(0.4)
        #normal_plane.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['t'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        def basePoint(t):
            return Vec3(a,0,0)

        def endTangentPoint(t):
            # ||curve'(0)||
            vn = sqrt((b*sin(pi_2*t/1000.0))**2 + (c*cos(pi_2*t/1000.0))**2)
            return Vec3(a, b*sin(pi_2*t/1000.0)/vn, c*cos(pi_2*t/1000.0)/vn)

        def endCurvaturePoint(t):
            # ||curve'(0)||**2
            vn = (b*sin(pi_2*t/1000.0))**2 + (c*cos(pi_2*t/1000.0))**2
            # ||curve''(0)||
            nn = a
            return Vec3(a-nn/vn, 0, 0)

        tangent_arrow = AnimatedArrow(basePoint, endTangentPoint)
        tangent_arrow.setDiffuseColor(_1(20,10,220))
        #self.addChild(tangent_arrow)

        curvature_arrow = AnimatedArrow(basePoint, endCurvaturePoint)
        curvature_arrow.setDiffuseColor(_1(220,200,20))
        #self.addChild(curvature_arrow)

        objects = [curve, normal_plane, tangent_arrow, curvature_arrow]
        self.addChildren( objects )

        #self.setupAnimations( curve_and_plane )
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

        normal = Arrow((0,0,c), (0,0,c+1), 0.05)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                return Vec3(a*cos(pi_2*self.param/1000.0)*sin(s), b*sin(pi_2*self.param/1000.0)*sin(s), c*cos(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (cos(pi_2*t2)*v, sin(pi_2*t2)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-3.1, 3.1))
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['t2'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        self.setupAnimations( curve_and_plane )


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

        #px = sqrt((a**2-b**2)/(a**2-c**2))
        #pz = sqrt((c**2)*(b**2-c**2)/(a**2-c**2))
        pz = sqrt((c**2-b**2)/(c**2-a**2))
        px = sqrt((a**2)*(b**2-a**2)/(c**2-a**2))

        #print px, pz, px**2+pz**2, px**2/(a**2)+pz**2/(c**2)

        nx = 2*px/(a**2)
        nz = 2*pz/(c**2)

        n = sqrt(nx**2+nz**2)

        nx = nx/n
        nz = nz/n

        normal = Arrow((px,0,pz), (px+nx,0,pz+nz), 0.05)
        self.addChild(normal)

        class Ellipse(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                return Vec3(a*cos(s), b*sin(pi_2*self.param/1000.0)*sin(s), c*cos(pi_2*self.param/1000.0)*sin(s))

            def setParam(self, t):
                self.param = t

        ellipse_obj = Ellipse()
        curve = Curve3DParam(ellipse_obj, (-3.14, 3.14, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (px+u*nx-cos(pi_2*t3)*v*nz, sin(pi_2*t3)*v, pz+u*nz+cos(pi_2*t3)*v*nx)
        normal_plane = ParametricPlot3D(normal_plane_function, (-2.1, 0.1), (-3.3, 3.3))
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['t3'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        self.setupAnimations( curve_and_plane )



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
#       light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
#       light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
#       light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

        mat = SoMaterial()
        mat.emissiveColor = _1(80, 120, 200)
        mat.diffuseColor = _1(80, 120, 200)
        mat.transparency.setValue(0.5)

        sep = SoSeparator()
        sep.addChild(light)
        sep.addChild(mat)
        sep.addChild(cyl)

        self.addChild(sep)

        normal = Arrow((0,0,1), (0,0,2), 0.05)
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
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (cos(pi_2*tc)*v, sin(pi_2*tc)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-2.1, 2.1))
        self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['tc'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        self.setupAnimations( curve_and_plane )


class Hiperboloide(Page):
    u"""<b>Curvaturas normales</b> en el punto (0,0,0)
      de la hiperboloide (1/4)x^2 - (1/9)y^2 = z
    """

    def __init__(self):
        super(Hiperboloide,self).__init__('Hiperboloide')

        self.showAxis(False)

        hyperboloid = createHyperboloid(2,3)
        self.addChild(hyperboloid)

        normal = Arrow((0,0,0), (0,0,1), 0.05)
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
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (cos(pi_2*th)*v, sin(pi_2*th)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        #normal_plane.setTransparency(0.4)
        #normal_plane.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['th'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        #self.setupAnimations( curve_and_plane )
        self.setupAnimations( [ AnimationGroup( curve_and_plane, (1000,0,1000) ) ] )


class Toro1(Page):
    u"""<b>Curvaturas normales</b> en el punto (4,0,0)
      del toro...
    """

    def __init__(self):
        super(Toro1,self).__init__('Toro 1')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1+r2,0,0), (r1+r2+1,0,0), 0.05)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                v = s * cos(pi_2*self.param/1000.0)
                u = s * sin(pi_2*self.param/1000.0)
                return Vec3((r1 + r2 * cos(v)) * cos(u), (r1 + r2 * cos(v)) * sin(u), r2 * sin(v))

            def setParam(self, t):
                self.param = t

        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (-pi, pi, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (u, sin(pi_2*tt1)*v, cos(pi_2*tt1)*v)
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        #normal_plane.setTransparency(0.4)
        #normal_plane.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['tt1'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        #self.setupAnimations( curve_and_plane )
        self.setupAnimations( [ AnimationGroup( curve_and_plane, (1000,0,1000) ) ] )


class Toro2(Page):
    u"""<b>Curvaturas normales</b> en el punto (3,0,1)
      del toro...
    """

    def __init__(self):
        super(Toro2,self).__init__('Toro 2')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1,0,r2), (r1,0,r2+1), 0.05)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                v = s * cos(pi_2*self.param/1000.0) + pi_2
                u = s * sin(pi_2*self.param/1000.0)
                return Vec3((r1 + r2 * cos(v)) * cos(u), (r1 + r2 * cos(v)) * sin(u), r2 * sin(v))

            def setParam(self, t):
                self.param = t

        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (-pi, pi, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (r1+cos(pi_2*tt2)*v, sin(pi_2*tt2)*v, u)
        normal_plane = ParametricPlot3D(normal_plane_function, (-1.1, 1.1), (-3.1, 3.1))
        #normal_plane.setTransparency(0.4)
        #normal_plane.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['tt2'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        #self.setupAnimations( curve_and_plane )
        self.setupAnimations( [ AnimationGroup( curve_and_plane, (1000,0,1000) ) ] )


class Toro3(Page):
    u"""<b>Curvaturas normales</b> en el punto (2,0,0)
      del toro...
    """

    def __init__(self):
        super(Toro3,self).__init__('Toro 3')

        self.showAxis(False)

        torus = createTorus(r1, r2)
        self.addChild(torus)

        normal = Arrow((r1-r2,0,0), (r1-r2-1,0,0), 0.05)
        self.addChild(normal)

        class TorusCurve(object):

            def __init__(self, t=0.0):
                self.param = t

            def __call__(self, s):
                v = s * cos(pi_2*self.param/1000.0) + pi
                u = s * sin(pi_2*self.param/1000.0)
                return Vec3((r1 + r2 * cos(v)) * cos(u), (r1 + r2 * cos(v)) * sin(u), r2 * sin(v))

            def setParam(self, t):
                self.param = t

        torusc_obj = TorusCurve()
        curve = Curve3DParam(torusc_obj, (-pi, pi, 200), color=(0.9, 0.2, 0.1), width=6)
        #curve.animation.setFrameRange(0, 1000)
        #curve.animation.setDuration(1000)

        normal_plane_function = lambda u, v: (u, sin(pi_2*tt3)*v, -cos(pi_2*tt3)*v)
        normal_plane = ParametricPlot3D(normal_plane_function, (-4.1, 4.1), (-4.1, 4.1))
        #normal_plane.setTransparency(0.4)
        #normal_plane.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        #self.addChild(normal_plane)

        normal_plane.animation = normal_plane.parameters['tt3'].asAnimation()
        #normal_plane.animation.setFrameRange(0, 1000)
        #normal_plane.animation.setDuration(1000)

        curve_and_plane = [curve, normal_plane]
        self.addChildren( curve_and_plane )

        #self.setupAnimations( curve_and_plane )
        self.setupAnimations( [ AnimationGroup( curve_and_plane, (1000,0,1000) ) ] )


class CurvaturasNormales(Chapter):

    def __init__(self):
        Chapter.__init__(self, name="Ejemplos de Curvaturas Normales")

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
