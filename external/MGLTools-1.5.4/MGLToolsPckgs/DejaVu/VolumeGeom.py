## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

#############################################################################
#
# Author: Anna Omelchenko, Michel Sanner
#
# Copyright: M. Sanner TSRI 2003
#
#############################################################################

#
# $Header: /opt/cvs/python/packages/share1.5/DejaVu/VolumeGeom.py,v 1.17 2007/07/24 17:30:41 vareille Exp $
#
# $Id: VolumeGeom.py,v 1.17 2007/07/24 17:30:41 vareille Exp $
#

""" Module implementing a special DejaVu geometric object - VolumeGeom.
The DisplayFunction() uses volume rendering methods. """

import numpy.oldnumeric as Numeric


class CropBox:

    def __init__(self, volgeom):
        self.volgeom = volgeom
        self.xmin = 0 #bounds of crop box
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.zmin = 0
        self.zmax = 0
        self.midx = 0 #center of crop box
        self.midy = 0
        self.midz = 0

        self.volSize = [0, 0, 0] # volume size along the 3 dimensions

        self.callbackFunc = []

        self.crop = None
        self.volgeom.cropStatus = 1
        

    def __repr__(self):
        return "<CropBox> (%d,%d,%d)  x(%d,%d) y(%d,%d) z(%d,%d)" % \
               (self.dx, self.dy, self.dz, self.xmin, self.xmax,
                self.ymin, self.ymax, self.zmin, self.zmax)


    def setVolSize(self, size):
        assert len(size)==3
        self.volSize = size

    def setSize(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def update(self):
        self.dx = self.xmax - self.xmin
        self.dy = self.ymax - self.ymin
        self.dz = self.zmax - self.zmin

        self.crop.SetSlabs( max(0, self.xmin), min(self.xmax, self.volSize[0]),
                            max(0, self.ymin), min(self.ymax, self.volSize[1]),
                            max(0, self.zmin), min(self.zmax, self.volSize[2]))
##          self.crop.SetSlabs( self.xmin, self.xmax, self.ymin, self.ymax,
##                              self.zmin, self.zmax)
        if self.volgeom.viewer:
            self.volgeom.viewer.Redraw()

        for f in self.callbackFunc:
            f(self)
            
    def updateX(self):
        self.dx = self.xmax - self.xmin
        self.crop.SetXSlab(max(0, self.xmin), min(self.xmax, self.volSize[0]))
        if self.volgeom.viewer:
            self.volgeom.viewer.Redraw()

        for f in self.callbackFunc:
            f(self)
            
    def updateY(self):
        self.dy = self.ymax - self.ymin
        self.crop.SetYSlab(max(0, self.ymin), min(self.ymax, self.volSize[1]))
        if self.volgeom.viewer:
            self.volgeom.viewer.Redraw()
            
        for f in self.callbackFunc:
            f(self)

    def updateZ(self):
        self.dz = self.zmax - self.zmin
        self.crop.SetZSlab(max(0, self.zmin), min(self.zmax, self.volSize[2]))
        if self.volgeom.viewer:
            self.volgeom.viewer.Redraw()
            
        for f in self.callbackFunc:
            f(self)
            
    def ScaleX(self, event, matrix, transXY, transZ):
        if transZ<0: delta = 1
        else: delta = -1
        xmin = self.xmin+delta
        xmax = self.xmax-delta
        if xmin == xmax:
            xmax = xmin+1
        if xmin < 0 : xmin = 0
        if xmax > self.volSize[0]: xmax =self.volSize[0]
        if xmin > xmax : return
        self.xmin = xmin
        self.xmax = xmax
        self.updateX()


    def ScaleY(self, event, matrix, transXY, transZ):
        if transZ<0: delta = 1
        else: delta = -1
        ymin = self.ymin+delta
        ymax = self.ymax-delta
        if ymin == ymax:
            ymax = ymin+1
        if ymin < 0: ymin = 0
        if ymax > self.volSize[1]: ymax = self.volSize[1]
        if ymin > ymax : return
        self.ymin = ymin
        self.ymax = ymax
        self.updateY()


    def ScaleZ(self, event, matrix, transXY, transZ):
        if transZ<0: delta = 1
        else: delta = -1
        zmin = self.zmin+delta
        zmax = self.zmax-delta
        if zmin == zmax:
            zmax = zmin+1
        if zmin < 0: zmin = 0
        if zmax > self.volSize[2]: zmax = self.volSize[2]
        if zmin > zmax : return
        self.zmin = zmin
        self.zmax = zmax
        self.updateZ()

       
    def ScaleAll(self, event, matrix, transXY, transZ):
        if transZ<0: delta = 1
        else: delta = -1
        xmin = self.xmin+delta
        xmax = self.xmax-delta
        if xmin == xmax:
            xmax = xmin+1
        if xmin < 0 : xmin = 0
        if xmax > self.volSize[0]: xmax =self.volSize[0]
        if xmin > xmax : return
        self.xmin = xmin
        self.xmax = xmax
        
        ymin = self.ymin+delta
        ymax = self.ymax-delta
        if ymin == ymax:
            ymax = ymin+1
        if ymin < 0: ymin = 0
        if ymax > self.volSize[1]: ymax = self.volSize[1]
        if ymin > ymax : return
        self.ymin = ymin
        self.ymax = ymax
        
        zmin = self.zmin+delta
        zmax = self.zmax-delta
        if zmin == zmax:
            zmax = zmin+1
        if zmin < 0: zmin = 0
        if zmax > self.volSize[2]: zmax = self.volSize[2]
        if zmin > zmax : return
        self.zmin = zmin
        self.zmax = zmax
        self.update()



    def TranslationX(self, event, matrix, transXY, transZ):
        if transZ>0: delta = 2
        else: delta = -2
        self.xmin = self.xmin+delta
        self.xmax = self.xmax+delta
        if self.xmin == self.xmax:
            self.xmax = self.xmin+1
        if self.xmin < 0 :
            self.xmax = self.xmax-self.xmin
            self.xmin = 0
        if self.xmax > self.volSize[0]:
            self.xmin = self.xmin - (self.xmax-self.volSize[0])
            self.xmax = self.volSize[0]
        self.updateX()

        
    def TranslationY(self, event, matrix, transXY, transZ):
        if transZ>0: delta = 2
        else: delta = -2
        self.ymin = self.ymin+delta
        self.ymax = self.ymax+delta
        if self.ymin == self.ymax:
            self.ymax = self.ymin+1
        if self.ymin < 0 :
            self.ymax = self.ymax-self.ymin
            self.ymin = 0
        if self.ymax > self.volSize[1]:
            self.ymin = self.ymin - (self.ymax-self.volSize[1])
            self.ymax = self.volSize[1]
        self.updateY()

    def TranslationZ(self, event, matrix, transXY, transZ):
        if transZ>0: delta = 2
        else: delta = -2
        self.zmin = self.zmin+delta
        self.zmax = self.zmax+delta
        if self.zmin == self.zmax:
            self.zmax = self.zmin+1
        if self.zmin < 0 :
            self.zmax = self.zmax-self.zmin
            self.zmin = 0
        if self.zmax > self.volSize[2]:
            self.zmin = self.zmin - (self.zmax-self.volSize[2])
            self.zmax = self.volSize[2]
        self.updateZ()

    def Translate(self,t):
##          #scl = 0.25
##          scl = 1
##          print "t:", t
##          t1 = int(t[0]*scl)
##          t2 = int(t[1]*scl)
##          t3 = int(t[2]*scl)
        t1,t2,t3=Numeric.where(Numeric.less(t,0),-2, 2)
        xmin = self.xmin
        xmax = self.xmax
        ymin = self.ymin
        ymax = self.ymax
        zmin = self.zmin
        zmax = self.zmax
        xmin = xmin + t1
        xmax = xmax + t1
        nx, ny, nz = self.volSize
        if xmin < 0 :
            xmax = xmax-xmin
            xmin = 0
        if xmax > nx:
            xmin = xmin - (xmax-nx)
            xmax = nx
        ymin = ymin + t2
        ymax = ymax + t2
        if ymin < 0 :
            ymax = ymax-ymin
            ymin = 0
        if ymax > ny:
            ymin = ymin - (ymax-ny)
            ymax = ny
        zmin = zmin + t3
        zmax = zmax + t3
        if zmin < 0 :
            zmax = zmax-zmin
            zmin = 0
        if zmax > nz:
            zmin = zmin - (zmax-nz)
            zmax = nz
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
        self.update()


from DejaVu.Geom import Geom

class VolumeGeom(Geom):
    """Base class to render a volumetric object"""

    keywords = Geom.keywords + ['volscale', 'masterObject', 'voltranslate']

    def __init__(self, name=None, check=1, **kw):
        #self.immediateRendering = 1
        #self.transparent = 1
        self.inheritMaterial = 0
        self.inheritXform = 0
        self.viewer = None
        self.boundBox = None

        apply( Geom.__init__, (self, name, check), kw)

        self._modified = False
        #print "immediateRendering:", self.immediateRendering
        #print "transparent:", self.transparent
        self.immediateRendering = 1
        self.transparent = 1

    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object: Set polylines's vertices
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( Geom.Set, (self, check, 0), kw )

        if redo and self.viewer:
            if redoTemplateFlag is True:
                self.redoTemplate()
                redrawFlag = True
            if redoDisplayListFlag is True:
                if self not in self.viewer.objectsNeedingRedo.keys():
                    self.viewer.objectsNeedingRedo[self] = None
                redrawFlag = True
            if redoDisplayChildrenListFlag is True:
                lObjectsNeedingRedo = self.viewer.objectsNeedingRedo.keys()
                for child in self.AllObjects():
                    if child not in lObjectsNeedingRedo:
                        self.viewer.objectsNeedingRedo[child] = None
                redrawFlag = True
            if redoViewerDisplayListFlag is True:
                self.viewer.deleteOpenglList()
                redrawFlag = True
            if updateOwnGui is True and updateOwnGuiFlag is True and self.ownGui is not None:
                self.updateOwnGui()
            if redrawFlag is True:
                self.viewer.Redraw()
        return redrawFlag, updateOwnGuiFlag, redoViewerDisplayListFlag, redoDisplayListFlag, redoTemplateFlag, redoDisplayChildrenListFlag



    def BindMouseToCropScale(self):
        """Bind the trackball to the current cropping box"""
        c = self.viewer.currentCamera
        c.bindActionToMouseButton('cropScaleX', 1, 'Control')
        c.bindActionToMouseButton('cropScaleY', 2, 'Control')
        c.bindActionToMouseButton('cropScaleZ', 3, 'Control')
        c.bindActionToMouseButton('cropScaleAll', 3, 'Meta')

    def BindMouseToCropTranslate(self):
        c = self.viewer.currentCamera
        c.bindActionToMouseButton('cropTransX', 1, 'Meta')
        c.bindActionToMouseButton('cropTransY', 2, 'Meta')
        c.bindActionToMouseButton('cropTransZ', 3, 'Meta')

    def BindMouseToCropTransAll(self):
        c = self.viewer.currentCamera
        c.bindActionToMouseButton('cropTransAll', 1, 'Meta')
        c.bindActionToMouseButton('None', 2, 'Meta')
        c.bindActionToMouseButton('cropScaleAll', 3, 'Meta') 

    def translateCropbox(self, event, matrix, transXY, transZ):
        # FIXME won't work with instance matrices
        m = self.masterObject.GetMatrixInverse()
        for i in range(3):
            m[i][3] = 0
        v = [transXY[0],transXY[1],0,1]
        v = Numeric.reshape(Numeric.array(v),(4,1))
        t = Numeric.dot(m,v)
        t = [t[0][0], t[1][0], t[2][0]]
        self.cropBox.Translate(t)


    def LoadVolume(self, filename):
        #has to be implemented by a 'child' class
        pass


    def AddVolume(self, volume, dataPtr):
        #has to be implemented by a 'child' class
        pass


    def Draw(self):
        #has to be implemented by a 'child' class
        pass
