# -*- coding: utf-8 -*-
from superficie.book import Page, Chapter
from math import pi, sin, cos, tan
from superficie.util import Vec3, _1, partial
from superficie.nodes import Curve3D, TangentPlane2, SimpleSphere, Plane
from superficie.animations import AnimationGroup, Animation, Animatable
from PyQt4 import QtGui
from superficie.plots import ParametricPlot3D
from pivy.coin import SoTransparencyType
from superficie.widgets import VisibleCheckBox

class HeliceRectificada(Page):
    u"""La curvatura de una curva $alpha$ parametrizada por longitud de arco en el punto
      $alpha (s)$ (la norma de $alpha’ (s)= ^t(s)$  es $1$) mide la rapidez con que la curva se
      aleja de su recta tangente, y la torsión en el punto $alpha (s)$ mide la rapidez con que
      la curva se aleja de su plano osculador.
    """
    def __init__(self):
        Page.__init__(self, u"Planos osculador, normal, rectificante en Hélice Circular Rectificada")

        tmin = -2 * pi
        tmax = 2 * pi
        ## ============================================
        sq2 = 2 ** 0.5
        inv_sq2 = (1. / sq2)

        def helix(s):
            s_times_sq2 = inv_sq2 * s
            return Vec3(cos(s_times_sq2), sin(s_times_sq2), s_times_sq2)

        def tangent(s):
            s_div_sq2 = s / sq2
            return Vec3(-inv_sq2 * sin(s_div_sq2), inv_sq2 * cos(s_div_sq2), inv_sq2)

        def normal(s):
            s_div_sq2 = s / sq2
            return Vec3(-cos(s_div_sq2), -sin(s_div_sq2), 0)

        def bi_normal(s):
            s_div_sq2 = s / sq2
            return Vec3(inv_sq2 * sin(s_div_sq2), -inv_sq2 * cos(s_div_sq2), inv_sq2)

        curve = Curve3D(helix, (tmin, tmax, 100), _1(206, 75, 150), 2)
        self.addChild(curve)

        #=======================================================================
        # Vectors
        #=======================================================================
        field_tangent = curve.attachField("tangent", tangent).show()
        field_normal = curve.attachField("normal", normal).show()
        field_binormal = curve.attachField("binormal", bi_normal).show()

        #=======================================================================
        # Planes
        #=======================================================================

        def get_points(v1, v2): return v2.p1, v1.p2, v2.p2

        color = (.5, .5, .5)
        plane_osculating = Plane(color, *get_points(field_tangent, field_normal))
        plane_normal = Plane(color, *get_points(field_normal, field_binormal))
        plane_rectifying = Plane(color, *get_points(field_binormal, field_tangent))
        self.addChildren([plane_osculating, plane_normal, plane_rectifying])

        def update_planes(n):
            plane_osculating.setPoints(*get_points(field_tangent, field_normal))
            plane_normal.setPoints(*get_points(field_normal, field_binormal))
            plane_rectifying.setPoints(*get_points(field_binormal, field_tangent))

        r = (5000, 0, len(curve) - 1)
        animation = Animatable(update_planes, r)
        self.setupAnimations([
            AnimationGroup([field_tangent, field_normal, field_binormal, animation], r)
        ])


class Curvas3(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Planos osculador, normal, rectificante")
        figuras = [HeliceRectificada]
        for f in figuras:
            self.addPage(f())


if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.book.addChapter(Curvas3())
    visor.chapter.chapterSpecificIn()
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())
