# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pivy.coin import *
from math import *
try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.nodes import Sphere, BasePlane, Line, Curve3D
from superficie.book import Chapter, Page
from superficie.plots import Plot3D, RevolutionPlot3D
from superficie.util import _1, Vec3, intervalPartition

class Plano(Page):
    u"""En cada punto del plano, los vectores tangentes a curvas que pasan por el punto forman
      un plano completo llamado el plano tangente en el punto, y el vector normal unitario a
      ese plano es el vector normal a la superficie en el punto, que en este caso tiene
      dirección constante.
    """
    def __init__(self):
        "El plano x + 2y + 3z - 4 = 0"
        Page.__init__(self, "Plano")
        plano = Plot3D(lambda x,y: (-x-2*y+4)/3, (-2,2),(-2,2))
#       plano.setMeshDiffuseColor(_1(240,170,69))
        plano.setAmbientColor(_1(189, 121 , 106 ))
        plano.setDiffuseColor(_1(189, 121 , 106 ))
        plano.setSpecularColor(_1(189, 121 , 106 ))
        self.setupPlanes((-2,2,7))

        p_1 = Sphere((2, -2, 2),0.02)
        p_1.setColor( _1(214,44,109))
        p_1.setShininess(1)

        p_2 = Sphere((1, 2, -1./3),0.02)
        p_2.setColor( _1(116,112,35))
        p_2.setShininess(1)
        
#        pun2_1 = [[-3t/2, sin(t), t] for t in intervalPartition((tmin, tmax, npuntos))]
#        curva = Line(puntos,(1, 1, 1), 2,parent=self, nvertices=1)
#        recta2_1

        p_3 = Sphere((-1, -1, 7./3),0.02)
        p_3.setColor( _1(52,171,215))
        p_3.setShininess(1)

#       Calculando las curvas que pasan por los 3 puntos anteriores.

        npuntos  = 20
#        npuntos1 = 50

        tmin1_3 = 1.1
        tmax1_3 = 2.
#        tmin1_4 = 0
#        tmax1_4 = 7.9**0.5

        puntos1_1 = [ (2,-2,2), (2,-1,4./3) ]
        puntos1_2 = [ (2,-2,2), (1.5,1,1./6) ]
        puntos1_3 = [[t, -1./4*t**3., 1./3*(4-t+1./2*t**3.)] for t in intervalPartition((tmin1_3, tmax1_3, npuntos))]
#        puntos1_4 = [[t, (8-t**2.)**0.5, 1./3*(4-t-2*(8-t**2.)**0.5)] for t in intervalPartition((tmin1_4, tmax1_4, npuntos1))]

        curva1_1 = Line(puntos1_1, (1, 0, 0), 2, nvertices=1)
        curva1_2 = Line(puntos1_2, (0, 0, 1), 2, nvertices=1)
        curva1_3 = Line(puntos1_3, (0, 1, 0), 2, nvertices=1)
#        curva1_4 = Line(puntos1_4, (1, 1, 0), 2, parent=self, nvertices=1)

        tmin2_3 = 0.
        tmax2_3 = 1.
#        tmin2_4 = 0
#       tmax2_4 = 3**0.5

        puntos2_1 = [(1, 2, -1./3),(0,1,2./3)]
        puntos2_2 = [(1, 2, -1./3),(1,0,1)]
        puntos2_3 = [[t, 2*t**3., 1./3*(4-t-4*t**3.)] for t in intervalPartition((tmin2_3, tmax2_3, npuntos))]
#        puntos2_4 = [[t, (3-t**2.)**0.5, 1./3*(4-t-2*(3-t**2.)**0.5)] for t in intervalPartition((tmin2_4, tmax2_4, npuntos1))]

        curva2_1 = Line(puntos2_1, (1, 0, 0), 2, nvertices=1)
        curva2_2 = Line(puntos2_2, (0, 0, 1), 2, nvertices=1)
        curva2_3 = Line(puntos2_3, (0, 1, 0), 2, nvertices=1)
#        curva2_4 = Line(puntos2_4, (1, 1, 0), 2, parent=self, nvertices=1)

        tmin3_3 = -0.5
        tmax3_3 = -1.
#        tmin3_4 = 0
#        tmax3_4 = 1.99**0.5

        puntos3_1 = [(-1, -1, 7./3),(0.8,0.8,8./15)]
        puntos3_2 = [(-1, -1, 7./3),(-2,-1,8./3)]
        puntos3_3 = [[t, t**3., 1./3*(4-t-2*t**3.)] for t in intervalPartition((tmin3_3, tmax3_3, npuntos))]
#        puntos3_4 = [[t, (2-t**2.)**0.5, 1./3*(4-t-2*(2-t**2.)**0.5)] for t in intervalPartition((tmin3_4, tmax3_4, npuntos1))]

        curva3_1 = Line(puntos3_1, (1, 0, 0), 2, nvertices=1)
        curva3_2 = Line(puntos3_2, (0, 0, 1), 2, nvertices=1)
        curva3_3 = Line(puntos3_3, (0, 1, 0), 2, nvertices=1)
#        curva3_4 = Line(puntos3_4, (1, 1, 0), 2, parent=self, nvertices=1)

        self.addChild(plano)
        self.addChild(p_1)
        self.addChild(p_2)
        self.addChild(p_3)
        self.addChildren([curva1_1,curva1_2,curva1_3])
        self.addChildren([curva2_1,curva2_2,curva2_3])
        self.addChildren([curva3_1,curva3_2,curva3_3])

        self.setupAnimations([curva1_1,curva1_2,curva1_3,curva2_1,curva2_2,curva2_3,curva3_1,curva3_2,curva3_3])
#        self.setupAnimations([curva1_4,curva2_4,curva3_4])
#       self.setupAnimations([curva3_1,curva3_2])

class ParaboloideEliptico(Page):
    u"""En cada punto del paraboloide elíptico, el plano tangente en el punto deja todo el
         paraboloide en uno de los semiespacios que define; el vector normal $N$ a la
         superficie varía con el punto pero nunca llega a ser perpendicular al eje del
         paraboloide.
    """
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Elíptico")

        z = 0.

        par = RevolutionPlot3D(lambda r,t: r**2+z,(0,1),(0,2*pi))
#       par.setAmbientColor(_1(157, 168, 136 ))
#       par.setDiffuseColor(_1(157, 168, 136 ))
#       par.setSpecularColor(_1(157, 168, 136 ))
        baseplane = BasePlane()
        baseplane.setHeight(-0.5)
        baseplane.setRange((-2,2,7))

        p_0 = Sphere((0, 0, 0),0.02)
        p_0.setColor( _1(124, 96, 144))
        p_0.setShininess(1)

        p_1 = Sphere((0.28**(0.5), 0.6 , 0.64),0.02)
        p_1.setColor( _1(178, 194, 9))
        p_1.setShininess(1)

        p_2 = Sphere((-0.8, 0.6, 1),0.02)
        p_2.setColor( _1(184, 126, 42))
        p_2.setShininess(1)

#        puntos0_1 = [[t, , 1./3*(4-t-2*t**3.)] for t in intervalPartition((tmin3_3, tmax3_3, npuntos))]

#        curva0_1 = Line(puntos2_1, (1, 0, 0), 2, parent=self, nvertices=1)

        def cir1_1(t):
            return Vec3(t, (0.64-t**2.)**0.5, 0.64)
        def cir1_2(t):
            return Vec3(t, -(0.64-t**2.)**0.5, 0.64)
        def cir2_1(t):
            return Vec3(t, (1-t**2.)**0.5, 1)
        def cir2_2(t):
            return Vec3(t, -(1-t**2.)**0.5, 1)
        

        npuntos = 50

        rango1 = [(-0.799,0.799,npuntos)]
        rango2 = [(-0.999,0.999,npuntos)]
        
        curva1_1 = Curve3D(cir1_1, rango1, width=2)
        curva1_2 = Curve3D(cir1_2, rango1, width=2)
        curva2_1 = Curve3D(cir2_1, rango2, width=2)
        curva2_2 = Curve3D(cir2_2, rango2, width=2)

        self.addChild(par)
        self.addChild(baseplane)
        self.addChild(p_0)
        self.addChild(p_1)
        self.addChild(p_2)

class ParaboloideHiperbolico(Page):
    u"""Para el paraboloide hiperbólico, el plano tangente en cada punto corta a la superficie
               en dos rectas y hay parte de la superficie en cada uno de los semiespacios definidos
               por él. Hay curvas en la superficie cuyos vectores de aceleración apuntan a lados distintos
              del plano tangente.
    """
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperbólico")

        z = 1.5
        parab = Plot3D(lambda x,y: x**2 - y**2+z, (-1,1),(-1,1))
        parab.setAmbientColor(_1(145, 61 , 74 ))
        parab.setDiffuseColor(_1(127,119,20))
        parab.setSpecularColor(_1(145, 61 , 74 ))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))              

        self.addChild(parab)
        self.addChild(baseplane)


class Superficiecuartica(Page):
    u"""Para esta superficie cuártica, el orden de contacto con su plano tangente en (0,0,0)
                es mayor que el usual pues los vectores de aceleración de las generatrices en ese punto se
                anulan y por eso el punto se llama punto plano.
    """
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cuártica")

        cuart = RevolutionPlot3D(lambda r,t: r**4 + 1,(0,1),(0,2*pi))
        cuart.setDiffuseColor(_1(168,211,8))
        cuart.setSpecularColor(_1(168,211,8))

        baseplane = BasePlane()
        baseplane.setHeight(0)
        baseplane.setRange((-2,2,7))
        self.addChild(cuart)
        self.addChild(baseplane)


figuras = [
    Plano,
    ParaboloideEliptico,
    ParaboloideHiperbolico,
    Superficiecuartica
    ]

class Superficies2(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Plano tangente")
        for f in figuras:
            self.addPage(f())
        self.whichPage = 0

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies2())
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

