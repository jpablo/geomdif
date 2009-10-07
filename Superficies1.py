# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore, uic
from pivy.coin import *
from math import *
try:
    from pivy.quarter import QuarterWidget
    Quarter = True
except ImportError:
    from pivy.gui.soqt import *
    Quarter = False

from superficie.base import Chapter, Page
from superficie.Plot3D import Plot3D, RevolutionPlot3D,ParametricPlot3D, RevolutionParametricPlot3D
from superficie.gui import Slider, SpinBox
from superficie.VariousObjects import BasePlane, Sphere
from superficie.util import Vec3

class Plano1(Page):
    def __init__(self):
        "El plano x + y + z - 2.5 = 0"
        Page.__init__(self, "Plano")

        z = 2
        plano = Plot3D(lambda x,y: z-x-y, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(z-x-y), (-1,1),(-1,1))
        plano1.setLinesVisible(True)
        plano1.setMeshVisible(False)
        plano.setDiffuseColor((252. / 255, 144. / 255 , 0. / 255 ))
        plano1.setDiffuseColor((1,0,0))
        baseplane = BasePlane()

        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(baseplane)



class ParaboloideEliptico(Page):
    def __init__(self):
        "x^2 + y^2 - z = 0"
        Page.__init__(self, u"Paraboloide El√≠ptico")

        z = 0.5
        par = RevolutionPlot3D(lambda r,t: r**2+z,(0,1),(0,2*pi))
        par1 = RevolutionPlot3D(lambda r,t: h*(r**2 +z),(0,1),(0,2*pi))
        par1.setLinesVisible(True)
        par1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setZ(0)
        baseplane.setRange((-2,2,7))

        self.addChild(par)
        self.addChild(par1)
        self.addChild(baseplane)

class ParaboloideHiperbolico(Page):
    def __init__(self):
        "x^2 - y^2 - z = 0"
        Page.__init__(self, u"Paraboloide Hiperb√≥lico")

        z = 1.5
        plano = Plot3D(lambda x,y: x**2 - y**2+z, (-1,1),(-1,1))
        plano1 = Plot3D(lambda x,y: h*(x**2 - y**2+z), (-1,1),(-1,1))
        plano1.setLinesVisible(True)
        plano1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setZ(0)
        baseplane.setRange((-2,2,7))

        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(baseplane)

class LasilladelMono(Page):
    def __init__(self):
        "x^3 - 3xy^2 - z = 0"
        Page.__init__(self, u"La silla del mono")

        plano = Plot3D(lambda x,y: x**3 - 3*x*y**2 +2.5, (-1,1),(-1,1))
#        plano.setScaleFactor((1,1,.6))

        def cVec(pto):
            "pto: Vec3"
            return pto*1.1
        plano.addVectorField(cVec)

#        def setXscale(t):
#            scale.scaleFactor = (1,1,t)
#        Slider(
#            rangep=('z', .2, 1, 1,  20),
#            func=setXscale,
#            parent=self
#        )
#


        plano1 = Plot3D(lambda x,y: h*(x**3 - 3*x*y**2 + 2.5), (-1,1),(-1,1))
#        plano1.setScaleFactor((1,1,.6))
        plano1.setLinesVisible(True)
        plano1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setZ(0)
        baseplane.setRange((-2,2,7))

        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(baseplane)

class Superficiecuartica(Page):
    def __init__(self):
        "x^4 + 2x^2y^2 + y^4 -z = 0"
        Page.__init__(self, u"Superficie Cu√°rtica")

#        plano = Plot3D(lambda x,y: x**4 + 2*x**2*y**2 + y**4 + 1, (-1,1),(-1,1))
        plano = RevolutionPlot3D(lambda r,t: r**4 + 1,(0,1),(0,2*pi))
#        plano.setScaleFactor((1,1,.6))
        plano1 = RevolutionPlot3D(lambda r,t: h*(r**4 + 1),(0,1),(0,2*pi))
        plano1.setLinesVisible(True)
        plano1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setZ(0)
        baseplane.setRange((-2,2,7))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(baseplane)

class Conoderevolucion(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Cono de Revoluci√≥n")

        plano = RevolutionPlot3D(lambda r,t: r + 1,(0,1),(0,2*pi))
        plano1 = RevolutionPlot3D(lambda r,t: h*(r + 1),(0,1),(0,2*pi))
        plano1.setLinesVisible(True)
        plano1.setMeshVisible(False)

        baseplane = BasePlane()
        baseplane.setZ(0)
        baseplane.setRange((-2,2,7))
        self.addChild(plano)
        self.addChild(plano1)
        self.addChild(baseplane)

class Esfera(Page):
    def __init__(self):
        "x^2 + y^2 = z^2"
        Page.__init__(self, u"Esfera")

        r = .998
        esf = ParametricPlot3D(lambda t,f: (r*sin(t)*cos(f),r*sin(t)*sin(f),r*cos(t)) , (0,pi,70),(0,2*pi,70))
        
        def proyK(x,y):
            den = x**2+y**2+1-2*k+k**2
            return ((-2*x*(k-1))/den, (-2*y*(k-1))/den, 1 + 2*(k-1)*(1-k)/den)

        def proyZm1(u,v):
            "proy desde el polo norte al plano z=-1"
            den = u**2+v**2+4
            x = u - t*(u-4*u/den)
            y = v - t*(v-4*v/den)
            z = -1 -t*(-2+8/den)
            return (x,y,z)

        def proyZ1(u,v):
            "proy desde el polo sur al plano z=1"
            den = u**2+v**2+4
            x = u - t*(u-4*u/den)
            y = v - t*(v-4*v/den)
            z = 1 -t*(2-8/den)
            return (x,y,z)

        def proyC(r,t):
            return (2*r / (r**2+1), t, (r**2-1) / (r**2+1))
        def proyCz0(r,t):
            return (r, t, 0)

        stereo = ParametricPlot3D(proyZm1, (-3,3,70),(-3,3,70))
        stereo.setLinesVisible(True)
        stereo.setMeshVisible(False)
        stereo.setMeshDiffuseColor((248./255,45./255,50./255))
        stereo2 = ParametricPlot3D(proyZ1, (-3,3,70),(-3,3,70))
        stereo2.setLinesVisible(True)
        stereo2.setMeshVisible(False)
        stereo2.setMeshDiffuseColor((2./255,96./255,200./255))

        baseplane = BasePlane()
        baseplane.setZ(-1.005)
        baseplane.setRange((-4,4,7))
        self.addChild(esf)
        self.addChild(stereo2)
        self.addChild(stereo)
        self.addChild(baseplane)

class Helicoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Helicoide")

        plano1 = ParametricPlot3D(lambda u,v: (sinh(v)*cos(u),sinh(v)*sin(u),u), (-pi,pi,60),(-2,2))
        plano1.setVerticesPerColumn(2)

        ## Esto no funciona por la forma en que se toma la lista de puntos
#        quad.mesh.verticesPerRow = 15

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = plano1.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )
        self.addChild(plano1)

class Catenoide(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Catenoide")

        plano = ParametricPlot3D(lambda u,v: (cosh(v)*cos(u),cosh(v)*sin(u),v),(0,2*pi,60),(-1,1))
        plano.setVerticesPerColumn(2)

        Slider(
            rangep = ('z', 2, 60, 2, 59),
            func = plano.setVerticesPerColumn,
            duration = 3000,
            parent = self
        )

        self.addChild(plano)

class Toro(Page):
    def __init__(self):
        ""
        Page.__init__(self, u"Toro")
        tmin,tmax,npuntos = (0,40*pi,300)

        a = 1
        b = 0.5
        c = .505
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        toro = ParametricPlot3D(toroParam1,(0,2*pi,150),(0,2*pi,100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        delta = 0
        p_eli = Sphere((.9571067805, .9571067805, .35+delta),0.02,visible=True)
        p_eli.setDiffuseColor((194. /255 , 38. /255, 69./255))
        p_eli.setEmissiveColor((194. /255 , 38. /255, 69./255))
        p_eli.setAmbientColor((194. /255 , 38. /255, 69./255))
        p_eli.setDiffuseColor((194. /255 , 38. /255, 69./255))
        p_eli.setSpecularColor((194. /255 , 38. /255, 69./255))
        p_eli.setShininess(1)



        p_par = Sphere ((0., 1., 0.5+delta),0.02,visible=True)
        p_par.setDiffuseColor((240./255,108./255,21./255))
        p_par.setEmissiveColor((240./255,108./255,21./255))
        p_par.setAmbientColor((240./255,108./255,21./255))
        p_par.setDiffuseColor((240./255,108./255,21./255))
        p_par.setSpecularColor((240./255,108./255,21./255))
        p_par.setShininess(1)

        p_hyp = Sphere ((-.4571067812, .4571067812, .35+delta),0.02,visible=True)
        p_hyp.setDiffuseColor((78./255,186./255,69./255))
        p_hyp.setEmissiveColor((78./255,186./255,69./255))
        p_hyp.setAmbientColor((78./255,186./255,69./255))
        p_hyp.setDiffuseColor((78./255,186./255,69./255))
        p_hyp.setSpecularColor((78./255,186./255,69./255))
        p_hyp.setShininess(1)

## plano elíptico

        ptoeli = (pi/4,pi/4)
        ptopar = (pi/2,pi/2)
        ptohyp = (3*pi/4, 3*pi/4)

        def eliv(v):
            return Vec3(-1./4*sin(v)*2**(1/2), -1./4*sin(v)*2**(1/2), .5*cos(v))
        def eliu(u):
            return Vec3([[-(1+1.4*2**(1/2))*sin(u), (1+1./4*2**(1/2))*cos(u), 0]])

        ve = eliv(pi/2)
        ve.normalize()
        ue = eliu(pi/2)
        ue.normalize()
        def planoe(h,t):
            return Vec3(toroParam1(*ptoeli)) + h*ve + t*ue
        plane_eli = ParametricPlot3D(planoe,(-.5,.5),(-.5,.5))

## plano parabólico

        def parv(v):
            return Vec3(0,-.5 * sin(v), 0.5 * cos(v))
        def paru(u):
            return Vec3(-sin(u), cos(u),0)

        vp = parv(pi/2)
        vp.normalize()
        up = paru(pi/2)
        up.normalize()
        def planop(h,t):
            return Vec3(toroParam1(*ptopar)) + h*vp + t*up
        plane_par = ParametricPlot3D(planop,(-.5,.5),(-.5,.5))


## plano hyperbólico

        def hypv(v):
            return Vec3(1./4*sin(v)*2**(1/2), -1/.4*sin(v)*2**(1/2), .5*cos(v))
        def hypu(u):
            return Vec3(-(1-1./4*2**(1/2))*sin(u), (1-1./4*2**(1/2))*cos(u), 0)

        vh = hypv(pi/2)
        vh.normalize()
        uh = hypu(pi/2)
        uh.normalize()
        def planoe(h,t):
            return Vec3(toroParam1(*ptohyp)) + h*vh + t*uh
        plane_eli = ParametricPlot3D(planoe,(-.5,.5),(-.5,.5))


        self.addChild(toro)
        self.addChild(p_eli)
        self.addChild(p_par)
        self.addChild(p_hyp)
        self.addChild(plane_eli)
        self.addChild(plane_par)
        self.addChild(plane_hyp)

figuras = [
    Plano1,
    ParaboloideEliptico,
    ParaboloideHiperbolico,
    LasilladelMono,
    Superficiecuartica,
    Conoderevolucion,
    Esfera,
    Helicoide,
    Catenoide
    Toro
    ]

class Superficies1(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Superficies")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"



if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies1())
    visor.getChapterObject().chapterSpecificIn()
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

