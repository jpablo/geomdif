# -*- coding: utf-8 -*-
__author__ = "jpablo"
__date__ = "$24/11/2009 11:06:25 PM$"

from math import *

from PyQt4 import QtGui
from pivy.coin import *


from superficie.nodes import Arrow, Curve3D, Cylinder
from superficie.book import Chapter
from superficie.book import Page
from superficie.util import Vec3, _1
from superficie.animations import AnimationGroup


class HeliceRectificada(Page):
    u"""Esta  hélice está recorrida con velocidad constante $1$, por eso a intervalos
         iguales corresponden tramos de la hélice de igual longitud que los segmentos del
         dominio. En cada punto hemos ilustrado el triedro de Frenet formado por el
         vector tangente $^t$, el vector normal $^n$ y el vector binormal $^b$
    """
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")
        tmin =-2 * pi
        tmax = 2 * pi
        npuntos = 400
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

        self.addChild(Cylinder(_1(185, 46, 61), tmax - tmin - .5, 1))

        curva = Curve3D(helicerec, (tmin, tmax, 100), _1(206, 75, 150), 2)
        self.addChild(curva)
        curva.attachField("tangente", tangente).setLengthFactor(1.25).setWidthFactor(.5)
        curva.attachField("normal", normal).setLengthFactor(1.25).setWidthFactor(.5).setDiffuseColor((0,1,0))
        curva.attachField("binormal", binormal).setLengthFactor(1.25).setWidthFactor(.5).setDiffuseColor((0,0,1))
#        curva.derivative = tangente
#        curva.tangent_vector.show()

#        origen = [-3.8*pi, -2.8*pi, -1.8*pi,-.8*pi,0,.8*pi, 1.8*pi, 2.8*pi,3.8*pi]
#        curva1 = Curve3D(helicerec,(tmin,tmax,100),parent=self)
#        for p in origen:
#            tan = Arrow(helicerec(p),helicerec(p)+tangente(p),extremos=True,escalaVertice=1,visible=True,parent=self)
#            nor = Arrow(helicerec(p),helicerec(p)+normal(p),extremos=True,escalaVertice=1,visible=True,parent=self)
#            bin = Arrow(helicerec(p),helicerec(p)+binormal(p),extremos=True,escalaVertice=1,visible=True,parent=self)


##        mattube = SoMaterial()
##        mattube.ambientColor  = _1(206, 205, 202)
##        mattube.diffuseColor  = _1(206, 205, 202)
##        mattube.specularColor = _1(206, 205, 202)
##        mattube.shininess = .28
##        tan1.setMaterial(mattube)
##        tan1.setAmbientColor(_1(255, 0, 0))

        rango = (8000,0,len(curva)-1)
        self.setupAnimations([ AnimationGroup( [ 
                curva.fields['tangente'], curva.fields['normal'], curva.fields['binormal']], 
                rango ) ])

class CurvaConica(Page):
    u"""Esta curva cónica sí está parametrizada por la longitud de arco, por eso los vectores tangentes tienen norma $1$."""
    def __init__(self):
        Page.__init__(self, u"Curva Cónica Rectificada")

#        self.cono = SoCone()
#        self.cono.height = 20
#        self.cono.bottomRadius = 2
#
#        self.addChild(self.cono)

        tmin = 0
        tmax = 5 * pi
        npuntos = 400
        L2 = log(2)
        sq2 = 2 ** 0.5
        sq2i = 1. / sq2
        sq3 = 3 ** 0.5
        sq3i = 1. / sq3
        sq6 = 6 ** 0.5
        sq6i = 1. / sq6

        ## ============================================
        def Conica(t):
            return Vec3((t / sq2 + 1) * cos(log(t / sq2 + 1)), (t / sq2 + 1) * sin(log(t / sq2 + 1)) , t / sq2 + 1) 

        curva = Curve3D(Conica, (tmin, tmax, npuntos), width=3)
        self.addChild(curva)

        def conicarec(s):
            return Vec3((s / sq2 + 1) * cos(log(s / sq2 + 1)), (s / sq2 + 1) * sin(log(s / sq2 + 1)) , s / sq2 + 1)
        def tangente(s):
            return Vec3(sq3i * (sin(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2)))) + cos(L2) * (cos(log(sq2 * (s + sq2))) - sin(log(sq2 * (s + sq2))))), \
                    sq3i * (sin(L2) * (-cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2)))) + cos(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2))))), \
                    sq3i)
        def normal(s):
            return Vec3(-sq2i * (sin(L2) * (-cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2)))) + cos(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2))))), \
                    sq2i * (sin(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2)))) + cos(L2) * (cos(log(sq2 * (s + sq2))) - sin(log(sq2 * (s + sq2))))), \
                    0)
        def binormal(s):
            return Vec3(-sq6i * (sin(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2)))) + cos(L2) * (cos(log(sq2 * (s + sq2))) - sin(log(sq2 * (s + sq2))))), \
                    sq6i * (sin(L2) * (cos(log(sq2 * (s + sq2))) - sin(log(sq2 * (s + sq2)))) - cos(L2) * (cos(log(sq2 * (s + sq2))) + sin(log(sq2 * (s + sq2))))), \
                    sq6i)
        curva.attachField("tangente", tangente)
        curva.attachField("normal", normal)
        curva.attachField("binormal", binormal)
        curva.fields['tangente'].show()
        curva.fields['normal'].show()
        curva.fields['binormal'].show()
        rango = (8000,0,len(curva)-1)
        self.setupAnimations([ AnimationGroup( [ 
                curva.fields['tangente'], curva.fields['normal'], curva.fields['binormal']], 
                rango ) ])


figuras = [CurvaConica, HeliceRectificada]

class Curvas2(Chapter):
    def __init__(self):
        Chapter.__init__(self, name=u"Rectificación")
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
    visor.addChapter(Curvas2())
    visor.chapter.chapterSpecificIn()
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    visor.notasStack.show()
    sys.exit(app.exec_())
