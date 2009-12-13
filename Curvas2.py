# -*- coding: utf-8 -*-
__author__="jpablo"
__date__ ="$24/11/2009 11:06:25 PM$"

from math import *

from PyQt4 import QtCore, QtGui
from pivy.coin import *

try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.VariousObjects import Bundle2, Bundle, Bundle3
from superficie.VariousObjects import Line, GraphicObject, Curve3D, Sphere, Arrow
from superficie.base import Chapter
from superficie.base import Page
from superficie.util import Vec3,_1
from superficie.util import intervalPartition
from superficie.util import connect, connectPartial
from superficie.Animation import Animation
from superficie.gui import onOff, CheckBox, Slider, Button, VisibleCheckBox, SpinBox
from superficie.gui import DoubleSpinBox
from superficie.Plot3D import ParametricPlot3D


class HeliceRectificada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")
        tmin = -2 * pi
        tmax =  2 * pi
        npuntos = 200
        ## ============================================
        puntos = (1/2**(1/2))*[[cos(t), sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)

        self.setupAnimations([curva])
#        bpuntos = 100
#        bundle = Bundle(param1hc, param2hc, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5,visible=True,parent=self)
#        bundle.hideAllArrows()
#        bundle2 = Bundle(param1hc, param3hc, (tmin, tmax, bpuntos), _1(116, 0, 63), 1.5,visible=True,parent=self)
#        bundle2.hideAllArrows()
#
#        mathead = SoMaterial()
#        mathead.ambientColor  = _1(120, 237, 119)
#        mathead.diffuseColor  = _1(217, 237, 119)
#        mathead.specularColor = _1(184, 237, 119)
#        mathead.shininess = .28
#        bundle.setHeadMaterial(mathead)
#
#        mattube = SoMaterial()
#        mattube.ambientColor  = _1(213, 227, 232)
#        mattube.diffuseColor  = _1(213, 227, 232)
#        mattube.specularColor = _1(213, 227, 232)
#        mattube.shininess = .28
#        bundle2.setMaterial(mattube)
#
#        matHead = SoMaterial()
#        matHead.ambientColor  = _1(0, 96, 193)
#        matHead.diffuseColor  = _1(0, 96, 193)
#        matHead.specularColor = _1(0, 96, 193)
#        matHead.shininess = .28
#        bundle2.setHeadMaterial(matHead)
#
#        self.setupAnimations([curva,bundle,bundle2])

figuras = [HeliceRectificada]

class Curvas2(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Curvas II")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    print "Hello";