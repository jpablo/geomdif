# -*- coding: utf-8 -*-
__author__="jpablo"
__date__ ="$24/11/2009 11:06:25 PM$"

from math import *

from PyQt4 import QtGui
from pivy.coin import *

try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.VariousObjects import Line, Arrow
from superficie.base import Chapter
from superficie.base import Page
from superficie.util import Vec3
from superficie.util import intervalPartition


class HeliceRectificada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")
        tmin = -4 * pi
        tmax =  4 * pi
        npuntos = 400
        sq2  = 2**(0.5)

        ## ============================================
        puntos = [[(1./sq2)*cos(t), (1./sq2)*sin(t), (1./sq2)*t] for t in intervalPartition((tmin, tmax, npuntos))]
        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)

        or1    = -7./4*pi*sq2
        or2    = 0
        or3    = 3./2*pi*sq2

        def helicerec(s):
            return Vec3((1./sq2)*cos(s), (1./sq2)*sin(s), (1./sq2)*s)
        def tangente(s):
            return Vec3( -1./sq2*sin(s/sq2) , 1./sq2*cos(s/sq2) , 1./sq2 )
        def normal(s):
            return Vec3( -cos(s/sq2) , -sin(s/sq2) , 0 )
        def binormal(s):
            return Vec3( 1./sq2*sin(s/sq2) , -1./sq2*cos(s/sq2) , 1./sq2 )

        tan1 = Arrow(helicerec(or1),helicerec(or1)+tangente(or1),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor1 = Arrow(helicerec(or1),helicerec(or1)+normal(or1),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin1 = Arrow(helicerec(or1),helicerec(or1)+binormal(or1),extremos=True,escalaVertice=1,visible=True,parent=self)

#        mattube = SoMaterial()
#        mattube.ambientColor  = _1(206, 205, 202)
#        mattube.diffuseColor  = _1(206, 205, 202)
#        mattube.specularColor = _1(206, 205, 202)
#        mattube.shininess = .28
#        tan1.setMaterial(mattube)
#        tan1.setAmbientColor(_1(255, 0, 0))


        tan2 = Arrow(helicerec(or2),helicerec(or2)+tangente(or2),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor2 = Arrow(helicerec(or2),helicerec(or2)+normal(or2),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin2 = Arrow(helicerec(or2),helicerec(or2)+binormal(or2),extremos=True,escalaVertice=1,visible=True,parent=self)


        tan3 = Arrow(helicerec(or3),helicerec(or3)+tangente(or3),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor3 = Arrow(helicerec(or3),helicerec(or3)+normal(or3),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin3 = Arrow(helicerec(or3),helicerec(or3)+binormal(or3),extremos=True,escalaVertice=1,visible=True,parent=self)

        self.setupAnimations([curva])

class CurvaConica(Page):
    def __init__(self):
        Page.__init__(self, u"Curva Cónica Rectificada")
        tmin = -pi
        tmax =  5 * pi
        npuntos = 400
        sq2  = 2**(0.5)

        ## ============================================
        puntos = [[ (t/sq2+1)*(cos(ln(t/sq2+1)),(t/sq2+1)*sin(ln(t/sq2+1))) , t/sq2+1 ] for t in intervalPartition((tmin, tmax, npuntos))]
        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)

        or1    = 0
        or2    = 2*pi
        or3    = 4*pi

        def conicarec(s):
            return Vec3( (s/sq2+1)*(cos(ln(s/sq2+1)),(s/sq2+1)*sin(ln(s/sq2+1))) , s/sq2+1 )
        def sangense(s):
            return Vec3(  )
        def normal(s):
            return Vec3(  )
        def binormal(s):
            return Vec3(  )

        tan1 = Arrow(conicarec(or1),conicarec(or1)+tangente(or1),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor1 = Arrow(conicarec(or1),conicarec(or1)+normal(or1),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin1 = Arrow(conicarec(or1),conicarec(or1)+binormal(or1),extremos=True,escalaVertice=1,visible=True,parent=self)

        tan2 = Arrow(conicarec(or2),conicarec(or2)+tangente(or2),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor2 = Arrow(conicarec(or2),conicarec(or2)+normal(or2),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin2 = Arrow(conicarec(or2),conicarec(or2)+binormal(or2),extremos=True,escalaVertice=1,visible=True,parent=self)


        tan3 = Arrow(conicarec(or3),conicarec(or3)+tangente(or3),extremos=True,escalaVertice=1,visible=True,parent=self)
        nor3 = Arrow(conicarec(or3),conicarec(or3)+normal(or3),extremos=True,escalaVertice=1,visible=True,parent=self)
        bin3 = Arrow(conicarec(or3),conicarec(or3)+binormal(or3),extremos=True,escalaVertice=1,visible=True,parent=self)

        self.setupAnimations([curva])


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