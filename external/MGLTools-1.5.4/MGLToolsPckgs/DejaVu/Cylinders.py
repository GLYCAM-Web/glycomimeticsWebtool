## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

############################################################################
#
# Author: Michel F. SANNER
#
# Revision: Guillaume Vareille
#
# Copyright: M. Sanner TSRI 2000
#
#############################################################################

#
# $Header: /opt/cvs/python/packages/share1.5/DejaVu/Cylinders.py,v 1.69 2008/09/03 21:49:01 vareille Exp $
#
# $Id: Cylinders.py,v 1.69 2008/09/03 21:49:01 vareille Exp $
#

# TODO
# 4 - include support for DIFFUSE_AND_AMBIENT
# 6 - KNOWN BUG: color (0,0,0) per vertex does seem to work

import numpy
import numpy.oldnumeric as Numeric, math, sys
from numpy.oldnumeric import array

from opengltk.OpenGL import GL
from opengltk.extent.utillib import solidCylinder

from DejaVu.IndexedGeom import IndexedGeom
import datamodel, viewerConst
from viewerFns import checkKeywords
from mglutil.math.rotax import rotax
from colorTool import glMaterialWithCheck, resetMaterialMemory
from Materials import Materials

class Cylinders(IndexedGeom):
    """Class for sets of cylinders
"""
    keywords = IndexedGeom.keywords + [
        'radii',
        'quality'
        ]

    def __init__(self, name=None, check=1, **kw):

        if not kw.get('shape'):
            kw['shape'] = (0,3)    # default shape for sphere set
        
        self.culling = GL.GL_BACK
        self.inheritCulling = 0

        self.frontPolyMode = GL.GL_FILL
        self.inheritFrontPolyMode = viewerConst.NO
        self.lighting = viewerConst.YES
        self.realFMat = Materials() # used in RedoDisplayList to build 
        self.realBMat = Materials() # used in RedoDisplayList to build 
                                    # material taking getFrom into account
        
        self.oneRadius = viewerConst.YES

        if not kw.get('quality'):
            kw['quality'] = 0
#        quality = kw.get('quality')
#        if quality:
#            self.quality = quality
#        else:
#            self.quality = 3
#        self.v, self.n = self._cylinderTemplate()
        
        self.cyldraw = self.cyldrawWithSharpColorBoundaries

        apply( IndexedGeom.__init__, (self, name, check), kw)
        assert len(self.vertexSet.vertices.ashape)==2
            
        self._modified = False


    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        redoDisplayListFlag0 = False

        # Exceptionnaly this has to be before the call to Geom.Set
        # because we want to override the treatment of it by Geom.Set
        invertNormals = kw.get('invertNormals')
        if invertNormals is not None:
            kw.pop('invertNormals')
            if self.invertNormals != invertNormals:
                self.invertNormals = invertNormals
                redoDisplayListFlag0 = True

        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( IndexedGeom.Set, (self, check, 0), kw)

        redoDisplayListFlag = redoDisplayListFlag or redoDisplayListFlag0

        rad = kw.get('radii')
        if rad:
            redoDisplayListFlag = True
            if type(rad).__name__ in ['list', 'tuple'] and len(rad)==1:
                rad = rad[0]
            if type(rad).__name__ in ('float','int'):
                self.oneRadius = viewerConst.YES
                self.vertexSet.radii = datamodel.ScalarProperties('radii',
                                   [rad], datatype=viewerConst.FPRECISION)
            elif  type(rad).__name__ in ['list', 'tuple'] \
              and len(rad) == len(self.vertexSet.vertices) \
              and type(rad[0]).__name__ in ('float','int'):
                self.oneRadius = viewerConst.NO
                self.vertexSet.radii = datamodel.ScalarProperties('radii', rad,
                                              datatype=viewerConst.FPRECISION)
            else:
                self.oneRadius = viewerConst.YES
                self.vertexSet.radii = datamodel.ScalarProperties(
                        'radii', data=[1.], datatype=viewerConst.FPRECISION)
        elif hasattr(self.vertexSet, 'radii') is False:
            self.vertexSet.radii = datamodel.ScalarProperties(
                'radii', shape=(0,), datatype=viewerConst.FPRECISION)

        v=kw.get('vertices')
        if rad or v:
            redoDisplayListFlag = True
            self.vertexSet.radii.PropertyStatus(len(self.vertexSet))

            if self.vertexSet.radii.status < viewerConst.COMPUTED:
                self.oneRadius = viewerConst.YES
            else:
                self.oneRadius = viewerConst.NO

        quality = kw.get('quality')
        if quality is not None:
            if type(quality).__name__ != 'int':
                raise TypeError ("Cylinders quality should be an integer")
            else:
                redoDisplayListFlag = True
                if quality < 3:
                    if len(self.vertexSet.vertices.array) < 500:
                        quality = 20
                    elif len(self.vertexSet.vertices.array) < 5000:
                        quality = 15
                    elif len(self.vertexSet.vertices.array) < 10000:
                        quality = 10
                    else:
                        quality = 5
                self.quality = quality
                self.v, self.n = self._cylinderTemplate()

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



    def Draw(self):
        #print "Cylinders.Draw"
        #import traceback;traceback.print_stack()

        # for some reason if I do not set this always on MacOSX only the first
        # cylinder gets the right color
        if sys.platform=='darwin':
            self.checkMat = False
        else:
            self.checkMat = True

        if len(self.vertexSet.vertices)==0 or len(self.faceSet.faces)==0:
            return

        if self.getSharpColorBoundaries() in [True, 1]:
            self.cyldraw = self.cyldrawWithSharpColorBoundaries
        else:
            self.cyldraw = self.cyldrawWithInterpolatedColors

        if self.inheritMaterial:
            fp = None
            bp = None
            face = None
        else:
            mat = self.materials[GL.GL_FRONT]
            rmat = self.realFMat
            bind = [10,10,10,10]
            for pInd in range(4):
                bind[pInd], rmat.prop[pInd] = mat.GetProperty(pInd)
            rmat.prop[4] = mat.prop[4]
            rmat.prop[5] = mat.prop[5]
            rmat.binding[:4] = bind
            rmat.binding[4:] = rmat.binding[4:]
            fp = rmat
            #                fp = self.materials[GL.GL_FRONT]
            if fp:
                if self.frontAndBack:
                    face = GL.GL_FRONT_AND_BACK
                    bp = None
                else:
                    face = GL.GL_FRONT
                    mat = self.materials[GL.GL_BACK]
                    rmat = self.realBMat
                    bind = [10,10,10,10]
                    for pInd in range(4):
                        bind[pInd], rmat.prop[pInd]=mat.GetProperty(pInd)
                    rmat.prop[4] = mat.prop[4]
                    rmat.prop[5] = mat.prop[5]
                    rmat.binding[:4] = bind
                    rmat.binding[4:] = rmat.binding[4:]
                    bp = rmat

        c = self.vertexSet.vertices.array

        if self.oneRadius == viewerConst.NO:
            radii = self.vertexSet.radii.array
        else:
            radius = self.vertexSet.radii.array[0]

        pickName = 0
        for i in xrange(len(self.faceSet.faces.array)):
            #print 'CYLINDERS', i, '********************************'
            for j in xrange(len(self.faceSet.faces.array[i])-1):
                vi1 = self.faceSet.faces.array[i][j]
                vi2 = self.faceSet.faces.array[i][j+1]

                if fp:
                    fpp1 = [None,None,None,None,None]
                    fpp2 = [None,None,None,None,None]
                    for m in (0,1,2,3,4):
                        if fp.binding[m] == viewerConst.PER_VERTEX:
                            fpp1[m] = fp.prop[m][vi2]
                            fpp1[m] = array(fpp1[m],copy=1)
                            fpp2[m] = fp.prop[m][vi1]
                            fpp2[m] = array(fpp2[m],copy=1)
                        elif fp.binding[m] == viewerConst.PER_PART:
                            fpp2[m] = fpp1[m] = fp.prop[m][i]
                            fpp1[m] = array(fpp1[m],copy=1)
                            fpp2[m] = array(fpp2[m],copy=1)
                else:
                    fpp1 = fpp2 = None

                if bp and not self.frontAndBack:
                    bpp1 = [None,None,None,None,None]
                    bpp2 = [None,None,None,None,None]
                    for m in (0,1,2,3,4):
                        if bp.binding[m] == viewerConst.PER_VERTEX:
                            bpp1[m] = bp.prop[m][vi2]
                            bpp1[m] = array(bpp1[m],copy=1)
                            bpp2[m] = bp.prop[m][vi1]
                            bpp2[m] = array(bpp2[m],copy=1)
                        elif bp.binding[m] == viewerConst.PER_PART:
                            bpp2[m] = bpp1[m] = bp.prop[m][i]
                            bpp1[m] = array(bpp1[m],copy=1)
                            bpp2[m] = array(bpp2[m],copy=1)
                else:
                    bpp1 = bpp2 = None

                GL.glPushName(pickName)
                if len(self.highlight) > 0:
                    if self.oneRadius:
                        self.cyldraw(c[vi1], c[vi2],
                                 radius, radius,
                                 fpp1, bpp1, fpp2, bpp2, face,
                                 highlightX=self.highlight[vi1],
                                 highlightY=self.highlight[vi2])
                    else:
                        if vi1 < vi2:
                            self.cyldraw(c[vi1], c[vi2],
                                     radii[vi2], radii[vi1],
                                     fpp1, bpp1, fpp2, bpp2, face,
                                     highlightX=self.highlight[vi1],
                                     highlightY=self.highlight[vi2])
                        else:
                            self.cyldraw(c[vi1], c[vi2],
                                     radii[vi1], radii[vi2],
                                     fpp1, bpp1, fpp2, bpp2, face,
                                     highlightX=self.highlight[vi1],
                                     highlightY=self.highlight[vi2])
                else:
                    if self.oneRadius:
                        self.cyldraw(c[vi1], c[vi2],
                                 radius, radius,
                                 fpp1, bpp1, fpp2, bpp2, face)
                    else:
                        if vi1 < vi2:
                            self.cyldraw(c[vi1], c[vi2],
                                     radii[vi2], radii[vi1],
                                     fpp1, bpp1, fpp2, bpp2, face)
                        else:
                            self.cyldraw(c[vi1], c[vi2],
                                     radii[vi1], radii[vi2],
                                     fpp1, bpp1, fpp2, bpp2, face)
                GL.glPopName()
                pickName = pickName +1
        #print 'CYLINDERS done'
        return 1


    def cyldrawWithSharpColorBoundaries(self, 
                x, y, radx, rady, 
                colxf=None, colxb=None,
                colyf=None, colyb=None, face=None,
                highlightX=0, highlightY=0):

        # determine scale and rotation of template
        import math
        sz=0.0
        for i in (0,1,2): sz=sz+(x[i]-y[i])*(x[i]-y[i])
        if sz <= 0.0: return
        sz = math.sqrt(sz)
        sz2 = sz * .5

        valueCos = (y[2]-x[2])/sz
        valueCos = min(valueCos, 1)
        valueCos = max(valueCos, -1)
        rx = -180.0*math.acos(valueCos)/math.pi
        dx = y[0]-x[0]
        dy = y[1]-x[1]
        if math.fabs(dx) < 0.00001 and math.fabs(dy) < 0.00001:
            rz = 0.0
        else:
            rz = -180.0*math.atan2(dx,dy)/math.pi

        GL.glPushMatrix()
        GL.glTranslatef(float(x[0]),float(x[1]),float(x[2]))
        if rz<=180.0 and rz >=-180.0:
            GL.glRotatef(float(rz), 0., 0., 1.)
        GL.glRotatef(float(rx), 1., 0., 0.)

        if colyf:
            for m in (0,1,2,3,4):
                if colyf[m] is not None:
                    glMaterialWithCheck( face, viewerConst.propConst[m],
                                     colyf[m], check=self.checkMat )
            if colyf[1] is not None:
                GL.glColor4fv(colyf[1])
        if colyb and face!=GL.GL_FRONT_AND_BACK:
            for m in (0,1,2,3,4):
                if colyb[m] is not None:
                    glMaterialWithCheck( GL.GL_BACK,
                                     viewerConst.propConst[m],
                                     colyb[m], check=self.checkMat )

        # this tests (colxf==colyf)
        idem = (highlightX == highlightY)
        if idem is True:
            if colxf is None:
                if colyf is not None:
                    idem = False
            else:
                if colyf is None:
                    idem = False
                else:
                    lencol = len(colxf)
                    if lencol != len(colyf):
                        idem = False
                    else:
                        for i in range(lencol):
                            if colxf[i] is not None:
                                if bool(numpy.alltrue(colxf[i] == colyf[i])) is False:
                                    idem = False
                                    break
        if idem is True:
            if colxb is None:
                if colyb is not None:
                    idem = False
            else:
                if colyb is None:
                    idem = False
                else:
                    lencol = len(colxb)
                    if lencol != len(colyb):
                        idem = False
                    else:
                        for i in range(lencol):
                            if colxb[i] is not None:
                                if bool(numpy.alltrue(colxb[i] == colyb[i])) is False:
                                    idem = False
                                    break
        
        if idem is True:
            #print "rady, radx, sz, self.quality, 1, self.invertNormals", rady, radx, sz, self.quality, 1, self.invertNormals
            if highlightX != 0:
                GL.glStencilFunc(GL.GL_ALWAYS, 1, 1)
                solidCylinder(float(rady), float(radx), sz, self.quality, 1, self.invertNormals)
                GL.glStencilFunc(GL.GL_ALWAYS, 0, 1)
            else:
                solidCylinder(float(rady), float(radx), sz, self.quality, 1, self.invertNormals)
        else:
            midRadius = (radx + rady) * .5
            if highlightX != 0:
                GL.glStencilFunc(GL.GL_ALWAYS, 1, 1)
                solidCylinder(midRadius, float(radx), sz2, self.quality, 1, self.invertNormals)
                GL.glStencilFunc(GL.GL_ALWAYS, 0, 1)
            else:
                solidCylinder(midRadius, float(radx), sz2, self.quality, 1, self.invertNormals)
            GL.glTranslatef(0, 0, float(sz2))
            if colxf:
                for m in (0,1,2,3,4):
                    if colxf[m] is not None:
                        glMaterialWithCheck( face, viewerConst.propConst[m],
                                     colxf[m], check=self.checkMat )
                if colxf[1] is not None:
                    GL.glColor4fv(colxf[1])
            if colxb and face!=GL.GL_FRONT_AND_BACK:
                for m in (0,1,2,3,4):
                    if colxb[m] is not None:
                        glMaterialWithCheck( GL.GL_BACK,
                                     viewerConst.propConst[m],
                                     colxb[m], check=self.checkMat )
            if highlightY != 0:
                GL.glStencilFunc(GL.GL_ALWAYS, 1, 1)
                solidCylinder(float(rady), midRadius, sz2, self.quality, 1, self.invertNormals)
                GL.glStencilFunc(GL.GL_ALWAYS, 0, 1)
            else:
                solidCylinder(float(rady), midRadius, sz2, self.quality, 1, self.invertNormals)
        
        GL.glPopMatrix()


    def cyldrawWithInterpolatedColors(self, 
                x, y, radx, rady, colxf=None, colxb=None,
                colyf=None, colyb=None, face=None, **kw):
        # draw a cylinder going from x to y with radii rx, and ry and materials
        # colxf and colxb for front and back mterial in x
        # colyf and colyb for front and back mterial in y
        # face can be GL_FRONT_AND_BACK or something else

        # determine scale and rotation of template
        import math
        sz=0.0
        for i in (0,1,2): sz=sz+(x[i]-y[i])*(x[i]-y[i])
        if sz <= 0.0: return
        sz = math.sqrt(sz)

        valueCos = (y[2]-x[2])/sz
        valueCos = min(valueCos, 1)
        valueCos = max(valueCos, -1)
        rx = -180.0*math.acos(valueCos)/math.pi
        dx = y[0]-x[0]
        dy = y[1]-x[1]
        if math.fabs(dx) < 0.00001 and math.fabs(dy) < 0.00001:
            rz = 0.0
        else:
            rz = -180.0*math.atan2(dx,dy)/math.pi

        GL.glPushMatrix()
        GL.glTranslatef(float(x[0]),float(x[1]),float(x[2]))
        if rz<=180.0 and rz >=-180.0: GL.glRotatef(float(rz), 0., 0., 1.)
        GL.glRotatef(float(rx), 1., 0., 0.)

        # draw cylinder
        GL.glBegin(GL.GL_QUAD_STRIP)
        for i in range(self.npoly+1):
            if self.invertNormals:
                GL.glNormal3fv(-self.n[i])
            else:
                GL.glNormal3fv(self.n[i])
            if colxf:
                for m in (0,1,2,3,4):
                    if colxf[m] is not None:
                        #print "colxf[m]",type(colxf[m])
                        #print 'AAAAA', colxf[m]
                        glMaterialWithCheck( face, viewerConst.propConst[m],
                                             colxf[m], check=self.checkMat )
                if colxf[1] is not None:
                    GL.glColor4fv(colxf[1])
            if colxb and face!=GL.GL_FRONT_AND_BACK:
                for m in (0,1,2,3,4):
                    if colxb[m] is not None:
                        glMaterialWithCheck( GL.GL_BACK,
                                             viewerConst.propConst[m],
                                             colxb[m], check=self.checkMat )

            vx = self.v[i][0]
            GL.glVertex3f(float(vx[0]*radx), float(vx[1]*radx), float(vx[2]*sz))

            if colyf:
                for m in (0,1,2,3,4):
                    if colyf[m] is not None:
                        #print 'BBBBB', colyf[m]
                        glMaterialWithCheck( face, viewerConst.propConst[m],
                                             colyf[m], check=self.checkMat )
                if colyf[1] is not None:
                    GL.glColor4fv(colyf[1])
            if colyb and face!=GL.GL_FRONT_AND_BACK:
                for m in (0,1,2,3,4):
                    if colyb[m] is not None:
                        glMaterialWithCheck( GL.GL_BACK,
                                             viewerConst.propConst[m],
                                             colyb[m], check=self.checkMat )
            vy = self.v[i][1]
            GL.glVertex3f(float(vy[0]*rady), float(vy[1]*rady), float(vy[2]*sz))

        GL.glEnd()

        GL.glPopMatrix()


    def _cylinderTemplate(self):

        npoly = self.quality

        v = Numeric.zeros( ((npoly+1),2,3), 'f')
        n = Numeric.zeros( ((npoly+1),3), 'f')
        self.npoly = npoly

        a = -math.pi                 # starting angle
        d = 2*math.pi / npoly         # increment

        for i in range(npoly+1):
            n[i][0] = v[i][0][0] = v[i][1][0] = math.cos(a)
            n[i][1] = v[i][0][1] = v[i][1][1] = math.sin(a)
            n[i][2] = v[i][1][2] = 0.0
            v[i][0][2] = 1.0
            a=a+d

        return v,n


    def _cylinderTemplateDaniel(self, quality=None):
        """ This template doesn't put the last point over the first point
        as done in the other template. In addition, it computes and
        returns face indices. I don't compute normals 
        This template is used by asIndexedyPolygons()"""

        if quality is None:
            quality = self.quality
        elif quality < 3:
            quality = 3


        import numpy.oldnumeric as Numeric, math

        v = Numeric.zeros( ((quality),2,3), 'f')
        n = Numeric.zeros( ((quality),3), 'f')

        f = []

        a = -math.pi                  # starting angle
        d = 2*math.pi / quality  # increment

        # compute vertices
        for i in range(quality):
            v[i][0][0] = v[i][1][0] = math.cos(a)
            v[i][0][1] = v[i][1][1] = math.sin(a)
            v[i][1][2] = 0.0
            v[i][0][2] = 1.0
            a=a+d

        lV = len(v)

        # compute template cylinder faces
        for i in range(lV-1): # cylinder body
            f.append([i, i+1, lV+i+1])
            f.append([lV+i+1, lV+i, i])
        f.append([lV-1, 0, lV]) #close last point to first
        f.append([lV-1, lV, lV+i+1])
        for i in range(lV-2): # cylinder bottom cap
            f.append([0, i+2 ,i+1])
        for i in range(lV-2): # cylinder top cap
            f.append([lV+i+1, lV+i+2, lV])

        return v, f


    def asIndexedPolygons(self, run=1, quality=None, radius=None, **kw):
        """ run=0 returns 1 if this geom can be represented as an
        IndexedPolygon and None if not. run=1 returns the IndexedPolygon
        object."""

        if run==0:
            return 1 # yes, I can be represented as IndexedPolygons

        import numpy.oldnumeric as Numeric, math
        from mglutil.math.transformation import Transformation

        # make a copy of the cylinderTemplate
        if quality is not None:
            assert quality > 2
        tmpltVertices, tmpltFaces = self._cylinderTemplateDaniel(\
            quality=quality)

        centers = self.vertexSet.vertices.array
        faces = self.faceSet.faces.array

        tmpltVertices = Numeric.array(tmpltVertices).astype('f')
        tmpltFaces = Numeric.array(tmpltFaces).astype('f')

        addToFaces = Numeric.ones((tmpltFaces.shape)) * 2*len(tmpltVertices)

        VV = [] # this list stores all vertices of all cylinders
        FF = [] # this list stores all faces of all cylinders

        # now loop over all cylinders in self
        for index in xrange(len(faces)):
            # tv temporarily stores the transformed unit cylinder vertices
            tv = tmpltVertices.__copy__()

            pt0 = centers[faces[index][0]] # bottom of cylinder
            pt1 = centers[faces[index][1]] # top of cylinder

            # get radius for cylinder
            if radius is not None:
                radx = rady = radius #override radii
            elif self.oneRadius:
                radx = rady = radius = self.vertexSet.radii.array[0]
            else:
                radx = self.vertexSet.radii.array[faces[index][1]]
                rady = self.vertexSet.radii.array[faces[index][0]]

            # determine scale and rotation of current cylinder
            sz=0.0
            for nbr in (0,1,2): sz=sz+(pt0[nbr]-pt1[nbr])*(pt0[nbr]-pt1[nbr])
            if sz <= 0.0: return
            sz = math.sqrt(sz)

            rx = -180.0*math.acos((pt1[2]-pt0[2])/sz)/math.pi
            dx = pt1[0]-pt0[0]
            dy = pt1[1]-pt0[1]

            if math.fabs(dx) < 0.00001 and math.fabs(dy) < 0.00001:
                rz = 0.0
            else:
                rz = -180.0*math.atan2(dx,dy)/math.pi

            # prepare rotations matrices of current cylinder
            Rx = Transformation(quaternion=[1,0,0,rx])
            if rz<=180.0 and rz >=-180.0:
                Rz = Transformation(quaternion=[0,0,1,rz])
                R = Rz * Rx
            else:  R = Rx
            r = R.getMatrix()

            k = 0
            for v in tmpltVertices:  # I DO NOT use Numeric.matrixmultiply
                                     # here, in order to gain significant speed
                v0x, v0y, v0z = v[0] # saves some lookups
                v1x, v1y, v1z = v[1]

                tv[k][0]=\
                ([r[0][0]*v0x*radx+r[1][0]*v0y*radx+r[2][0]*v0z*sz+pt0[0],
                  r[0][1]*v0x*radx+r[1][1]*v0y*radx+r[2][1]*v0z*sz+pt0[1],
                  r[0][2]*v0x*radx+r[1][2]*v0y*radx+r[2][2]*v0z*sz+pt0[2]])

                tv[k][1]=\
                ([r[0][0]*v1x*rady+r[1][0]*v1y*rady+r[2][0]*v1z+pt0[0],
                  r[0][1]*v1x*rady+r[1][1]*v1y*rady+r[2][1]*v1z+pt0[1],
                  r[0][2]*v1x*rady+r[1][2]*v1y*rady+r[2][2]*v1z+pt0[2]])

                k = k + 1

            ctv = None
            ctv = Numeric.concatenate( (tv[:,1], tv[:,0] ) )

            # now add the data to the big lists
            VV.extend(list(ctv))
            FF.extend(list(tmpltFaces))

            # increase face indices by lenght of vertices
            tmpltFaces = tmpltFaces + addToFaces 

        VV = Numeric.array(VV).astype('f')
        FF = Numeric.array(FF).astype('f')
        # FIXME: should I compute normals?

        # now we can build the IndexedPolygon geom
        from DejaVu.IndexedPolygons import IndexedPolygons
        cylGeom = IndexedPolygons("cyl", vertices=VV,
                               faces=FF, visible=1,
                               invertNormals=self.invertNormals)

        # copy Cylinders materials into cylGeom
        matF = self.materials[GL.GL_FRONT]
        matB = self.materials[GL.GL_BACK]
        cylGeom.materials[GL.GL_FRONT].binding = matF.binding[:]
        cylGeom.materials[GL.GL_FRONT].prop = matF.prop[:]
        cylGeom.materials[GL.GL_BACK].binding = matB.binding[:]
        cylGeom.materials[GL.GL_BACK].prop = matB.prop[:]

        # if binding per vertex: 
        if cylGeom.materials[GL.GL_FRONT].binding[1] == viewerConst.PER_VERTEX:
            newprop = []
            props = cylGeom.materials[GL.GL_FRONT].prop[1]

            for i in xrange(len(faces)):
                for j in xrange(len(faces[i])-1):
                    vi1 = self.faceSet.faces.array[i][j]
                    vi2 = self.faceSet.faces.array[i][j+1]
                    colx = props[vi2]
                    coly = props[vi1]

                    # add second color to first half of cyl vertices
                    for k in range(len(tmpltVertices)):
                        newprop.append(coly)
                    # add first color to second half of cyl vertices
                    for l in range(len(tmpltVertices)):
                        newprop.append(colx)

            cylGeom.materials[GL.GL_FRONT].prop[1] = newprop         

        # and finally...
        return cylGeom



class CylinderArrows(Cylinders):
    """Class for sets of 3D arrows draw using cylinders"""

    keywords = Cylinders.keywords + [
        'headLength',
        'headRadius',
        ]

    def __init__(self, name=None, check=1, **kw):

        if __debug__:
            if check:
                apply( checkKeywords, (name,self.keywords), kw)

        apply( Cylinders.__init__, (self, name, 0), kw)
        self.headLength = 1.
        self.headRadius = 2.


    def Draw(self):

        # for some reason, under Mac OS X, if I do not always set he material
        # only the first cylinder gets the right color (MS)
        if sys.platform=='darwin':
            self.checkMat = False
        else:
            self.checkMat = True

        if len(self.vertexSet.vertices) == 0:
            return

        if self.inheritMaterial:
            fp = None
            bp = None
            face = None
        else:
            mat = self.materials[GL.GL_FRONT]
            rmat = self.realFMat
            bind = [10,10,10,10]
            for pInd in range(4):
                bind[pInd], rmat.prop[pInd] = mat.GetProperty(pInd)
            rmat.prop[4] = mat.prop[4]
            rmat.prop[5] = mat.prop[5]
            rmat.binding[:4] = bind
            rmat.binding[4:] = rmat.binding[4:]
            fp = rmat
            #                fp = self.materials[GL.GL_FRONT]
            if fp:
                if self.frontAndBack:
                    face = GL.GL_FRONT_AND_BACK
                    bp = None
                else:
                    face = GL.GL_FRONT
                    mat = self.materials[GL.GL_BACK]
                    rmat = self.realBMat
                    bind = [10,10,10,10]
                    for pInd in range(4):
                        bind[pInd], rmat.prop[pInd]=mat.GetProperty(pInd)
                    rmat.prop[4] = mat.prop[4]
                    rmat.prop[5] = mat.prop[5]
                    rmat.binding[:4] = bind
                    rmat.binding[4:] = rmat.binding[4:]
                    bp = rmat

        c = self.vertexSet.vertices.array

        if self.oneRadius == viewerConst.NO:
            radii = self.vertexSet.radii.array
        else:
            radius = self.vertexSet.radii.array[0]

        pickName = 0
        for i in xrange(len(self.faceSet.faces.array)):
            #print 'CYLINDERS', i, '********************************'
            for j in xrange(len(self.faceSet.faces.array[i])-1):
                vi1 = self.faceSet.faces.array[i][j]
                vi2 = self.faceSet.faces.array[i][j+1]

                if fp:
                    fpp1 = [None,None,None,None,None]
                    fpp2 = [None,None,None,None,None]
                    for m in (0,1,2,3,4):
                        if fp.binding[m] == viewerConst.PER_VERTEX:
                            fpp1[m] = fp.prop[m][vi2]
                            fpp1[m] = array(fpp1[m],copy=1)
                            fpp2[m] = fp.prop[m][vi1]
                            fpp2[m] = array(fpp2[m],copy=1)
                        elif fp.binding[m] == viewerConst.PER_PART:
                            fpp2[m] = fpp1[m] = fp.prop[m][i]
                            fpp1[m] = array(fpp1[m],copy=1)
                            fpp2[m] = array(fpp2[m],copy=1)
                else:
                    fpp1 = fpp2 = None

                if bp and not self.frontAndBack:
                    bpp1 = [None,None,None,None,None]
                    bpp2 = [None,None,None,None,None]
                    for m in (0,1,2,3,4):
                        if bp.binding[m] == viewerConst.PER_VERTEX:
                            bpp1[m] = bp.prop[m][vi2]
                            bpp1[m] = array(bpp1[m],copy=1)
                            bpp2[m] = bp.prop[m][vi1]
                            bpp2[m] = array(bpp2[m],copy=1)
                        elif bp.binding[m] == viewerConst.PER_PART:
                            bpp2[m] = bpp1[m] = bp.prop[m][i]
                            bpp1[m] = array(bpp1[m],copy=1)
                            bpp2[m] = array(bpp2[m],copy=1)
                else:
                    bpp1 = bpp2 = None

                GL.glPushName(pickName)
                # compute point at base of cone
                vect = [c[vi2][0]-c[vi1][0],
                        c[vi2][1]-c[vi1][1],
                        c[vi2][2]-c[vi1][2]]
                norm = 1./math.sqrt(vect[0]*vect[0]+vect[1]*vect[1]+vect[2]*vect[2])
                vect = [vect[0]*norm, vect[1]*norm, vect[2]*norm]
                headBase = [c[vi2][0]-self.headLength*vect[0],
                            c[vi2][1]-self.headLength*vect[1],
                            c[vi2][2]-self.headLength*vect[2]]

                if self.oneRadius:
                    # cylinder
                    self.cyldraw(c[vi1], headBase,
                                 radius, radius,
                                 fpp1, bpp1, fpp2, bpp2, face)
                    # cone
                    self.cyldraw(headBase, c[vi2],
                                 0.0, radius*self.headRadius,
                                 fpp1, bpp1, fpp2, bpp2, face)
                else:
                    if vi1 < vi2:
                        self.cyldraw(c[vi1], c[vi2],
                                 radii[vi2], radii[vi1],
                                 fpp1, bpp1, fpp2, bpp2, face)
                    else:
                        self.cyldraw(c[vi1], c[vi2],
                                 radii[vi1], radii[vi2],
                                 fpp1, bpp1, fpp2, bpp2, face)
                    GL.glPopName()
                pickName = pickName +1
        #print 'CYLINDERS done'
        return 1
