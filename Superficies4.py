# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pivy.coin import *
from math import *

from superficie.nodes import BasePlane, Curve3D
from superficie.nodes.arrow import Arrow
from superficie.book import Chapter, Page
from superficie.plots import ParametricPlot3D, Plot3D, RevolutionPlot3D
from superficie.widgets import Slider
from superficie.util import _1, connect, Vec3, main
from superficie.animations import Animation


class Helicoide(Page):
    u"""
      En este cuadro generamos una sección de una helicoide como superficie
      reglada y luego pegamos los dos segmentos rectilíneos de los bordes
      obteniendo una cateoide. Las medidas y la curvatura gaussiana no se
      alteran en ningún estado del proceso, son superficies localmente
      isométricas, aunque una es reglada pero no es una superficie de
      revolución, cualidad que sí tiene la segunda.
      <p>
      Superficies:
      <ul>
      <li>Helicoide: <b>(v cos u, v sen u, au)</b> con <b>0&le;u&le;2&pi;, v&isin;&real;</b></li>
      <li>Catenoide: <b>(a cosh v cos u, a cosh v sen u, av)</b> con <b>0&le;u&le;2&pi;, v&isin;&real;</b></li>
      </ul>
    """
    def __init__(self):
        super(Helicoide, self).__init__(u"Isometría local entre una helicoide y una catenoide")
        self.camera_position = (8.2, 8.2, 8.2)
        self.camera_viewAll = False

        def param(u, v, t):
            x = cos(t) * sinh(v) * sin(u) + sin(t) * cosh(v) * cos(u)
            y = -cos(t) * sinh(v) * cos(u) + sin(t) * cosh(v) * sin(u)
            z = u * cos(t) + v * sin(t)
            return x,y,z

        helic1 = ParametricPlot3D(param, (-pi, pi, 60), (-2, 2))
        ht = helic1.getParameter('t')
        ht.timeline.setDuration(3000)
        ht.updateRange((0,pi/2,0))
        helic1.setVerticesPerColumn(2)

        helic1.setAmbientColor(_1(202, 78, 70))
        helic1.setDiffuseColor(_1(202, 78, 70))
        helic1.setSpecularColor(_1(202, 78, 70))

        s = Slider(
            rangep=('z', 2, 60, 2, 59),
            func=helic1.setVerticesPerColumn,
            duration=3000,
            parent=self
        )
        self.addChild(helic1)

        params = [s,ht]
        ## no queremos los controles
        for p in params:
            p.hide()
        anims = [p.asAnimation() for p in params]
        self.setupAnimations(anims)

class Catenoide(Page):
    u"""
      Como lo muestra la interacción, la catenoide es la superficie de
      revolución generada por la catenaria; cuando se corta a lo largo de una
      de ellas puede llevarse, con sólo convertir en rectas los meridianos,
      en parte de una helicoide.
      <p>
      Superficies:
      <ul>
      <li>Helicoide: <b>(v cos u, v sen u, au)</b> con <b>0&le;u&le;2&pi;, v&isin;&real;</b></li>
      <li>Catenoide: <b>(a cosh v cos u, a cosh v sen u, av)</b> con <b>0&le;u&le;2&pi;, v&isin;&real;</b></li>      </ul>
    """
    def __init__(self):
        super(Catenoide,self).__init__(u"Cortamos una catenoide para obtener parte de una helicoide")
        self.camera_position = (8.2, 8.2, 8.2)
        self.camera_viewAll = False

        def param(u, v, t):
            t2 = pi/2 - t
            x = cos(t2) * sinh(v) * sin(u) + sin(t2) * cosh(v) * cos(u)
            y = -cos(t2) * sinh(v) * cos(u) + sin(t2) * cosh(v) * sin(u)
            z = u * cos(t2) + v * sin(t2)
            return x,y,z

        cat = ParametricPlot3D(param, (-pi, pi, 60), (-2, 2))
        ht = cat.getParameter('t')
        ht.timeline.setDuration(3000)
        ht.updateRange((0,pi/2,0))
        cat.setVerticesPerColumn(2)

        cat.setAmbientColor(_1(4, 73, 143))
        cat.setDiffuseColor(_1(4, 73, 143))
        cat.setSpecularColor(_1(4, 73, 143))

        s = Slider(
            rangep=('z', 2, 60, 2, 59),
            func=cat.setVerticesPerColumn,
            duration=3000,
            parent=self
        )

        self.addChild(cat)
        params = [s,ht]
        ## no queremos los controles
        for p in params:
            p.hide()
        anims = [p.asAnimation() for p in params]
        self.setupAnimations(anims)


class Mobius(Page):
    u"""
      Una superficie es <b>orientable</b> si puede subdividirse en
      “triángulos” que la cubren sin traslaparse y cortándose sólo en vértices
      o en aristas completas, y todos estos “triángulos” tienen la misma orientación.
      Entonces es posible recorrer cualquier curva
      cerrada en la superficie con un vector normal que al terminar tiene la
      posición original.
      <p>
      Pero en el círculo central de una Banda de Möbius, obtenida al pegar
      los bordes de una tira después de dar media vuelta a uno de ellos,
      un vector normal termina su recorrido en sentido opuesto como lo
      muestra la interacción.
    """
    def __init__(self):
        super(Mobius,self).__init__(u"No orientabilidad de la Banda de Möbius")
#        self.camera_position = (3.0, 2.8, 2.8)

        def par(u,v):
            return cos(u) + v*cos(u/2)*cos(u), sin(u) + v*cos(u/2)*sin(u), v*sin(u/2)

        mobius = ParametricPlot3D(par, (-pi, pi, 60), (-.5, .5, 14))
        mobius.setTransparency(0.5)

        def curva(t): return par(t,0)
        def puntos(u): return Vec3(cos(u)*sin(u/2.0), sin(u/2.0)*sin(u),-cos(u/2.0))

        cm = Curve3D(curva, (-pi, pi, 200), color=_1(255, 255, 255), width=3)
        aceleracion_cm = cm.attachField("aceleracion", puntos).setLengthFactor(1).setWidthFactor(.5)
        aceleracion_cm.animation.setDuration(12000)

        self.addChild(mobius)
        self.addChild(cm)
        self.addChild( Arrow( (-1,0,0), (0,0,0), 0.02 ) )

        self.setupAnimations([aceleracion_cm])



class Superficies4(Chapter):
    def __init__(self):
        super(Superficies4,self).__init__(u"Isometría y orientación de superficies")

        figuras = [
            Helicoide,
            Catenoide,
            Mobius,
        ]

        for f in figuras:
            self.addPage(f())


if __name__ == "__main__":
    visor = main(Superficies4)

