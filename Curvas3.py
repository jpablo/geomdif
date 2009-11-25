# -*- coding: utf-8 -*-
__author__="jpablo"
__date__ ="$24/11/2009 11:06:25 PM$"

from superficie.base import Chapter

figuras = []

class Curvas3(Chapter):
    def __init__(self):
        Chapter.__init__(self,name="Curvas III")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    print "Hello";