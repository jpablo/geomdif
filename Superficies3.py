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

from superficie.book import Chapter, Page
from superficie.plots import Plot3D, ParametricPlot3D
from superficie.widgets import Slider
from superficie.nodes import Sphere, TangentPlane, TangentPlane2, Curve3D
from superficie.util import Vec3, _1, partial
from superficie.animations import Animation

class Elipsoide(Page):
    u"""
    """
    def __init__(self):
        Page.__init__(self, u"Elipsoide")
        param = lambda u,v: (cos(u)*cos(v), 1.5*cos(v)*sin(u), 2*sin(v))
        elipsoide = ParametricPlot3D(param, (-pi, pi), (-pi/2,pi/2))
        col = _1(84,129,121)
        elipsoide.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)
        par1 = lambda u,v: Vec3(-sin(u)*cos(v), 1.5*cos(u)*cos(v), 0)
        par2 = lambda u,v: Vec3(-cos(u)*sin(v), -1.5*sin(u)*sin(v), 2*cos(v))
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225))
        self.addChild(elipsoide)
        self.addChild(tp)
        Slider(rangep=('u', -pi,pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('v', -pi/2,pi/2,0,20),func=tp.setV,parent=self)

class Cilindro(Page):
    u"""En todos los puntos del cilindro de revolución es posible acomodar una porción recortada
      alrededor de otro punto, por eso el cilindro de revolución es una superficie
      homogénea; las curvaturas de las secciones normales, obtenidas al cortar el cilindro con
               plano que contenga a la normal por un punto, varían desde $0$, la mínima, para las
               generatrices) a $1$, la máxima,  para los círculos.
    """
    def __init__(self):
        Page.__init__(self, u"Cilindro")
        param = lambda u,t: Vec3(cos(u),sin(u),t)
        cilindro = ParametricPlot3D(param, (0, 2*pi), (-1,1))
        col = _1(177,89,77)
        cilindro.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)

        def par1(u,t): return Vec3(-sin(u),cos(u),0)
        def par2(u,t): return Vec3(0,0,1)
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225))
        tp.localOriginSphere.hide()
        tp.localYAxis.setColor(col).setWidth(2).show()
        Slider(rangep=('u', 0,2*pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('t', -1,1,0,20),func=tp.setV,parent=self)
        self.addChild(cilindro)
        self.addChild(tp)


class Toro(Page):
    u"""Los puntos del toro de revolución ubicados en la circunferencia exterior son elípticos
                porque el plano tangente en uno de ellos toca al toro sólo en ese punto y deja al toro de
                un solo lado del plano; los puntos de la circunferencia interior son hiperbólicos porque

                el plano tangente en uno de ellos tiene puntos del toro en ambos lados del plano, y los
                puntos de la circunferencia superior son parabólicos porque el plano tangente y el toro
                tienen en común toda esa circunferencia.    """
    def __init__(self):
        Page.__init__(self, u"Toro")
        a = 1
        b = 0.5

        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        toro = ParametricPlot3D(toroParam1,(0,2*pi,150),(0,2*pi,100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        #        delta = 0
        #        p_eli = Sphere((.9571067805, .9571067805, .35+delta),0.02,visible=True)
        #        p_eli.setColor( _1(194,38,69))
        #        p_eli.setShininess(1)
        #
        #        p_par = Sphere ((-0.7071067810, 0.7071067810, 0.5+delta),0.02,visible=True)
        #        p_par.setColor( _1(240,108,21))
        #        p_par.setShininess(1)
        #
        #        p_hyp = Sphere ((0, -0.6464466095, .3535+delta),0.02,visible=True)
        #        p_hyp.setColor( _1(78,186,69))
        #        p_hyp.setShininess(1)

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))

        ## plano parabólico
        ptopar = (0,pi/2)
        plane_par = TangentPlane2(toroParam1,toro_u,toro_v,ptopar,_1(252,250,225))
        plane_par.baseplane.setTransparency(0)

        def curvaPlana(t):
            return plane_par.planeParam(cos(t),sin(t)+1)

        curva = Curve3D(curvaPlana, (-pi,0,30), color=(1,0,0), width=2)

        self.addChild(toro)
        self.addChild(plane_par)
        self.addChild(curva)

        def animaCurva1(n):
            def curva(t): return (t*2*pi,pi/2)
            plane_par.setLocalOrigin(curva(n / 100.))

        def animaCurva2(n):
            def curva(t): return (0,pi/2 - t * (2*pi + pi/2))
            plane_par.setLocalOrigin(curva(n / 100.))

        def animaCurva3(n):
            def curva(t): return (t*2*pi,0)
            plane_par.setLocalOrigin(curva(n / 100.))

        a1 = Animation(animaCurva1, (6000, 0, 100))
        a2 = Animation(animaCurva2, (6000, 0, 100))
        a3 = Animation(animaCurva3, (6000, 0, 100))

        self.setupAnimations([a1,a2,a3])

figuras = [
        Cilindro,
        Elipsoide,
        Toro
]

class Superficies3(Chapter):
    def __init__(self):
        Chapter.__init__(self,name=u"Sección normal, curvatura principal")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies3())
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(False)

    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

