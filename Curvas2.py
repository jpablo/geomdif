# -*- coding: utf-8 -*-
__author__ = "jpablo"
__date__ = "$24/11/2009 11:06:25 PM$"

from math import *

from PyQt4 import QtGui
from pivy.coin import *

#try:
#    from pivy.quarter import QuarterWidget
#    Quarter = True
#except ImportError:
#    from pivy.gui.soqt import *
#    Quarter = False

from superficie.VariousObjects import Arrow, Curve3D
from superficie.Book import Chapter
from superficie.Book import Page
from superficie.util import Vec3, _1
from superficie.Animation import AnimationGroup


class HeliceRectificada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")
        tmin = -4 * pi
        tmax = 4 * pi
        npuntos = 400
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
        curva.setField("tangente", tangente)
        curva.setField("normal", normal)
        curva.setField("binormal", binormal)
        curva.fields['tangente'].show()
        curva.fields['normal'].show()
        curva.fields['binormal'].show()
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
    def __init__(self):
        Page.__init__(self, u"Curva Cónica Rectificada")
 
        tmin = 0
        tmax = 5 * pi
        npuntos = 400
        L2 = log(2)
        sq2 = 2 ** (0.5)
        sq2i = 1. / sq2
        sq3 = 3 ** (0.5)
        sq3i = 1. / sq3
        sq6 = 6 ** (0.5)
        sq6i = 1. / sq6

        ## ============================================
        # puntos = [[ (t/sq2+1)*cos(log(t/sq2+1)),(t/sq2+1)*sin(log(t/sq2+1)) , t/sq2+1 ] for t in intervalPartition((tmin, tmax, npuntos))]
        #------ curva = Line(puntos,_1(119, 178, 0), 2,parent=self, nvertices=1)
        
        def Conica(t):
            return Vec3((t / sq2 + 1) * cos(log(t / sq2 + 1)), (t / sq2 + 1) * sin(log(t / sq2 + 1)) , t / sq2 + 1) 

        curva = Curve3D(Conica, (tmin, tmax, npuntos), width=3, parent=self)

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
        curva.setField("tangente", tangente)
        curva.setField("normal", normal)
        curva.setField("binormal", binormal)
        curva.fields['tangente'].show()
        curva.fields['normal'].show()
        curva.fields['binormal'].show()
        rango = (8000,0,len(curva)-1)
        self.setupAnimations([ AnimationGroup( [ 
                curva.fields['tangente'], curva.fields['normal'], curva.fields['binormal']], 
                rango ) ])

#        origen = [0, pi, 2 * pi, 3 * pi, 4 * pi]
#
#        for p in origen:
#            tan = Arrow(conicarec(p), conicarec(p) + tangente(p), extremos=True, escalaVertice=1, visible=True, parent=self)
#            nor = Arrow(conicarec(p), conicarec(p) + normal(p), extremos=True, escalaVertice=1, visible=True, parent=self)
#            bin = Arrow(conicarec(p), conicarec(p) + binormal(p), extremos=True, escalaVertice=1, visible=True, parent=self)

#        self.addChild(curva)
#        self.setupAnimations([curva])


figuras = [HeliceRectificada, CurvaConica]
class Curvas2(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Curvas II")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
#    app = main(sys.argv)
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
#    SoQt.mainLoop()
    sys.exit(app.exec_())
