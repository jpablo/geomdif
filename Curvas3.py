# -*- coding: utf-8 -*-
from superficie.Book import Page
from math import pi, sin, cos
from superficie.util import Vec3, _1
from superficie.VariousObjects import Curve3D, TangentPlane2
from superficie.Animation import AnimationGroup, Animation
from PyQt4 import QtGui

__author__ = "jpablo"
__date__ = "$24/11/2009 11:06:25 PM$"

from superficie.Book import Chapter


class HeliceRectificada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")
        
        tmin = -4 * pi
        tmax = 4 * pi
        sq2 = 2 ** (0.5)
        ## ============================================
        def helicerec(s):
            return Vec3(cos((1. / sq2) * s), sin((1. / sq2) * s), (1. / sq2) * s)
        def tangente(s):
            return Vec3(-1. / sq2 * sin(s / sq2) , 1. / sq2 * cos(s / sq2) , 1. / sq2)
        def normal(s):
            return Vec3(-cos(s / sq2) , -sin(s / sq2) , 0)
        def binormal(s):
            return Vec3(1. / sq2 * sin(s / sq2) , -1. / sq2 * cos(s / sq2) , 1. / sq2)
        
        curva = Curve3D(helicerec, (tmin, tmax, 100), _1(206, 75, 150), 2, parent=self)

        #=======================================================================
        # planos
        #=======================================================================
        def embed(fn):
            return lambda u, v: fn(u)
        
        plano_osculador = TangentPlane2(embed(helicerec), embed(tangente), embed(normal), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)
        plano_normal = TangentPlane2(embed(helicerec), embed(normal), embed(binormal), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)
        plano_rectificante = TangentPlane2(embed(helicerec), embed(binormal), embed(tangente), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)
        
        plano_osculador.setRange((-1.5, 1.5, 30))
        plano_normal.setRange((-1.5, 1.5, 30))
        plano_rectificante.setRange((-1.5, 1.5, 30))
        
        def set_origen(n):
            pt = curva.domainPoints[n]
            plano_osculador.setOrigin((pt, 0))
            plano_normal.setOrigin((pt, 0))
            plano_rectificante.setOrigin((pt, 0))
            
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
                curva.fields['binormal']], 
            rango ) ])


#class SerieOrden4(Page):
#    def __init__(self):
#        Page.__init__(self, u"Desarrollo en serie")
#        def param(s):
#            return Vec3()
#        
#        curva = Curve3D(param, (tmin, tmax, 100), parent=self)


figuras = [HeliceRectificada]

class Curvas3(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas III")
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
