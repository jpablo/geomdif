# -*- coding: utf-8 -*-
from superficie.Book import Page
from math import pi, sin, cos, tan
from superficie.util import Vec3, _1, partial
from superficie.VariousObjects import Curve3D, TangentPlane2
from superficie.Animation import AnimationGroup, Animation
from PyQt4 import QtGui
from superficie.Plot3D import ParametricPlot3D
from pivy.coin import SoTransparencyType
from superficie.gui import VisibleCheckBox

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


class CampoVectorial(Page):
    def __init__(self):
        Page.__init__(self, u"Campo Vectorial")

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
            curva = Curve3D(make_curva(ct),(-20,20,80), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(1).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (10000, 0, 79))
        self.setupAnimations([a1])


figuras = [HeliceRectificada, CampoVectorial]

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
