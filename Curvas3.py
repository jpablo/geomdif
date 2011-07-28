# -*- coding: utf-8 -*-
from superficie.Book import Page, Chapter
from math import pi, sin, cos, tan
from superficie.util import Vec3, _1, partial
from superficie.Objects import Curve3D, TangentPlane2
from superficie.Animation import AnimationGroup, Animation
from PyQt4 import QtGui
from superficie.Plot3D import ParametricPlot3D
from pivy.coin import SoTransparencyType
from superficie.gui import VisibleCheckBox

__author__ = "jpablo"
__date__ = "$24/11/2009 11:06:25 PM$"


# TODO: el plano no empieza donde debe

class HeliceRectificada(Page):
    u"""La curvatura de una curva $apha$ parametrizada por longitud de arco en el punto
      $alpha (s)$ (la norma de $alpha’ (s)= ^t(s)$  es $1$) mide la rapidez con que la curva se
      aleja de su recta tangente, y la torsión en el punto $alpha (s)$ mide la rapidez con que
      la curva se aleja de su plano osculador.
    """
    def __init__(self):
        Page.__init__(self, u"Planos osculador, normal, rectificante en Hélice Circular Rectificada")
        
        tmin = -4 * pi
        tmax = 4 * pi
        sq2 = 2 ** 0.5
        ## ============================================
        def helicerec(s):
            return Vec3(cos((1. / sq2) * s), sin((1. / sq2) * s), (1. / sq2) * s)
        def tangente(s):
            return Vec3(-1. / sq2 * sin(s / sq2) , 1. / sq2 * cos(s / sq2) , 1. / sq2)
        def normal(s):
            return Vec3(-cos(s / sq2) , -sin(s / sq2) , 0)
        def binormal(s):
            return Vec3(1. / sq2 * sin(s / sq2) , -1. / sq2 * cos(s / sq2) , 1. / sq2)
        
        curva = Curve3D(helicerec, (tmin, tmax, 100), _1(206, 75, 150), 2)
        self.addChild(curva)

        #=======================================================================
        # planos
        #=======================================================================
        def embed(fn):
            # descarta la segunda entrada
            return lambda u, v: fn(u)
        
        plano_osculador = TangentPlane2(embed(helicerec), embed(tangente), embed(normal), (tmin, 0), _1(252, 250, 225))
        plano_normal = TangentPlane2(embed(helicerec), embed(normal), embed(binormal), (tmin, 0), _1(252, 250, 225))
        plano_rectificante = TangentPlane2(embed(helicerec), embed(binormal), embed(tangente), (tmin, 0), _1(252, 250, 225))

        self.addChildren([plano_normal, plano_osculador, plano_rectificante])
        
        plano_osculador.setRange((-1.5, 1.5, 30))
        plano_normal.setRange((-1.5, 1.5, 30))
        plano_rectificante.setRange((-1.5, 1.5, 30))

        def set_origen(n):
            pt = curva.points[n]
            plano_osculador.setOrigin(pt)
            plano_normal.setOrigin(pt)
            plano_rectificante.setOrigin(pt)

        plano_osculador.animation = Animation(set_origen, (8000, 0, len(curva) - 1))
        #=======================================================================
        # Vectores
        #=======================================================================
        curva.setField("tangente", tangente)
        curva.setField("normal", normal)
        curva.setField("binormal", binormal)
        curva.fields['tangente'].show()
        curva.fields['normal'].show()
        curva.fields['binormal'].show()
        rango = (8000,0,len(curva)-1)
        self.setupAnimations([ AnimationGroup( [
                plano_osculador,
                curva.fields['tangente'],
                curva.fields['normal'],
                curva.fields['binormal']
        ],
        rango ) ])


    


class Curvas3(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Planos osculador, normal, rectificante")
        figuras = [HeliceRectificada]
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(Curvas3())
    visor.chapter.chapterSpecificIn()
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())
