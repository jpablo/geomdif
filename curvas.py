import sys
from pivy.coin import *
from pivy.gui.soqt import *
from PyQt4 import QtCore, QtGui
from math import *
from superficie.VariousObjects import Sphere, Tube, Line, Bundle
from superficie.util import intervalPartition, Vec3


def malla(a,b,n):
    l = b - a
    return [l*(i/(n-1.)) + a for i in range(n)]

## ---------------------------------- CILINDRO ----------------------------------- ##

def Cilindro(col):
    sep = SoSeparator()

    cyl = SoCylinder()
    cyl.radius.setValue(0.98)
    cyl.height.setValue(8*pi)
    cyl.parts = SoCylinder.SIDES

    light = SoShapeHints()
    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor= col
    mat.diffuseColor = col
    mat.transparency.setValue(0.5)

    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.X
    rot.angle = pi/2

    trans = SoTransparencyType()
    trans.value = SoTransparencyType.DELAYED_BLEND

    sep.addChild(light)
    sep.addChild(rot)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(cyl)

    return sep

## ---------------------------------- ESFERA--------------------------------- ##

def Esfera(col):
    sep= SoSeparator()

    comp = SoComplexity()
    comp.value.setValue(1)
    comp.textureQuality.setValue(0.9)

    esf= SoSphere()
    esf.radius = 2.97

    light = SoShapeHints()
    light.VertexOrdering = SoShapeHints.COUNTERCLOCKWISE
    light.ShapeType = SoShapeHints.UNKNOWN_SHAPE_TYPE
    light.FaceType  = SoShapeHints.UNKNOWN_FACE_TYPE

    mat = SoMaterial()
    mat.emissiveColor= col
    mat.diffuseColor = col
    mat.transparency.setValue(0.4)

    trans = SoTransparencyType()
    trans.value = SoTransparencyType.SORTED_OBJECT_BLEND

    sep.addChild(comp)
    sep.addChild(light)
    sep.addChild(trans)
    sep.addChild(mat)
    sep.addChild(esf)

    return sep
## ------------------------------- HELICE CIRCULAR ------------------------------- ##

tmin = -4*pi
tmax =  4*pi

puntos = [[cos(t),sin(t),t] for t in malla(tmin,tmax,200)]

# 1 implica primer derivada, 2 implica segunda derivada
def param1hc(t):
    return Vec3(cos(t),sin(t),t)
def param2hc(t):
    return Vec3(-sin(t),cos(t),1)
def param3hc(t):
    return Vec3(-cos(t),-sin(t),0)


# Dibuja la helice y el cilindro
def helicecircular():
    haz1hc = Bundle(param1hc,param2hc,(tmin/13.,tmax/13.,50),(128./255,1,0),1.5)
    sep = SoSeparator()

    sep.addChild(Line(puntos,(.8,.8,.8),2).root)
    sep.addChild(Cilindro((1,0,0.5)))
    sep.addChild(haz1hc.root)

    return sep

## ------------------------------- HELICE REFLEJADA ------------------------------- ##

puntitos = [[cos(t),sin(t),-t] for t in malla(tmin,tmax,200)]

# Dibuja las helices y el cilindro
def helicereflejada():
    haz2hc = Bundle(param1hc,param2hc,(tmin/13.,tmax/13.,50),(116./255,0,63./255),1.5)
    sep = SoSeparator()

    sep.addChild(Line(puntos,(1,1,1),2).root)
    sep.addChild(Line(puntitos,(128./255,0,64./255),2).root)
    sep.addChild(Cilindro((7./255,83./255,150./255)))
    sep.addChild(haz2hc.root)

    return sep

## -------------------------------LOXODROMA------------------------------- ##


tmin = -50*pi
tmax = 50*pi

pmin = 0
pmax = 2*pi

r = 3
m = tan(pi/60)
t0= pi/2

puntos2 = [[r*cos(t)/cosh(m*(t-t0)),r*sin(t)/cosh(m*(t-t0)),r*tanh(m*(t-t0))] for t in malla(tmin,tmax,2000)]

puntitos2 = [[0,r*cos(t),r*sin(t)] for t in malla(pmin,pmax,200)]

# La rotacion para poder pintar los meridianos
def rot(ang):
    rot = SoRotationXYZ()
    rot.axis = SoRotationXYZ.Z
    rot.angle = ang

    return rot

# Dibuja la loxodroma y la esfera

def Loxi():
    sep = SoSeparator()

    sep.addChild(Line(puntos2,(1,1,0),3).root)
    sep.addChild(Esfera((28./255,119./255,68./255)))
    mer= Line(puntitos2,(72./255,131./255,14./255))
    for i in range(24):
        sep.addChild(rot(2*pi/24))
        sep.addChild(mer.root)

    return sep

## ------------------------------------------------------------------------ ##

# Vectores para los "haces"




# Lista de figuras

figuras=[
    (helicecircular,"Helice Circular"),
    (helicereflejada,"Helice Reflejada"),
    (Loxi,"Loxodroma")
]

print 1
if __name__ == "__main__":
    from superficie.util import main
    from superficie.Viewer import Viewer
    print 1
    app = main()
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter()
    ## ============================    
    for f,n in figuras:
        visor.addPage()
        fig = f()
        fig.getGui = lambda: QtGui.QLabel("<center><h1>%s</h1></center>" % n)
        visor.addChild(fig)
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    SoQt.mainLoop()
