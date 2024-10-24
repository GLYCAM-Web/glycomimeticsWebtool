## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

#############################################################################
#
# Author: Michel F. SANNER, Sophie Coon
#
# Copyright: M. Sanner TSRI 2000
#
#############################################################################

# $Header: /opt/cvs/python/packages/share1.5/DejaVu/GleObjects.py,v 1.30 2007/09/25 22:44:24 vareille Exp $
#
# $Id: GleObjects.py,v 1.30 2007/09/25 22:44:24 vareille Exp $
#

try:
    import gle
except:
    print 'Sorry you need the GLE extension module'
 
from DejaVu.viewerFns import checkKeywords
from DejaVu.Geom import Geom
from DejaVu.triangle_strip import Triangle_strip
from opengltk.OpenGL import GL
import numpy.oldnumeric as Numeric

class GleObject(Triangle_strip):

    keywords = Triangle_strip.keywords + [
        'normalStyle',
        'joinStyle'
        ]
    
    def __init__(self, name=None, check=1, **kw):

        self.normalStyle = gle.TUBE_NORM_PATH_EDGE
        self.joinStyle = gle.TUBE_JN_ANGLE

        apply( Triangle_strip.__init__, (self, name, check), kw)


    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object:
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        if kw.has_key('materials') and kw['materials']:
            materials = Numeric.array((kw['materials']),'f')
        else:
            materials = Numeric.array(((0.,0.,1.,1.),),'f')

        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( Triangle_strip.Set, (self, check, 0), kw )

        nm = kw.get( 'normalStyle')
        # nm can be TUBE_NORM_FACET, TUBE_NORM_EDGE, TUBE_NORM_PATH_EDGE
        if nm:
            self.normalStyle = self.normalStyle & ~gle.TUBE_NORM_MASK
            self.normalStyle = self.normalStyle | nm
            gle.gleSetJoinStyle (self.normalStyle | self.joinStyle)

        ja = kw.get( 'joinStyle')
        # ja can be TUBE_JN_RAW, TUBE_JN_ANGLE, TUBE_JN_CUT, TUBE_JN_ROUND,
        #           TUBE_JN_CAP 
        if ja:
            self.joinStyle = self.joinStyle & ~gle.TUBE_JN_MASK
            self.joinStyle = self.joinStyle | ja
            gle.gleSetJoinStyle (self.normalStyle | self.joinStyle)

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



    def extrude(self):
        """Virtual Method to do the extrusion along a 3D path with a 2D shape
        using the gle extrusion. We then get the geometry information
        using the extrusion method in Feedback mode. This will then be
        used to build a triangle strip."""
        pass

    def asIndexedPolygons(self, run=1, quality=None, **kw):
        """ run=0 returns 1 if this geom can be represented as an
        IndexedPolygon and None if not. run=1 returns the IndexedPolygon
        object."""

        if run==0:
            return 1 # yes, I can be represented as IndexedPolygons
        faces = self.faceSet.faces.array
        verts = self.vertexSet.vertices.array
        size = faces.shape
        # number of triangles in each face (containing triangle strip
        # vertices) from faces array. 
        ntr = size[1]-2
        # new length of triangles array
        nfaces = size[0]*ntr
        new_faces = Numeric.zeros((nfaces, 3), 'i')
        i = 0
        for f in faces:
            for n in range(ntr):
                if (n/2)*2 == n:
                    new_faces[i] = [f[n], f[n+1], f[n+2]]
                else:
                    new_faces[i] = [f[n+2], f[n+1], f[n]]
                i = i + 1
        from DejaVu.IndexedPolygons import IndexedPolygons
        new_obj = IndexedPolygons('gleobj',  vertices = verts,
                                  faces = new_faces, visible=1,
                                  invertNormals=self.invertNormals)
        return new_obj

class GleExtrude(GleObject):

    keywords = GleObject.keywords + [
        'shape2D',
        'trace3D',
        'contourUp',
        'capsFlag'
        ]

    def __init__(self, name=None, check=1, **kw):
        
        if __debug__:
            if check:
                apply( checkKeywords, (name,self.keywords), kw)

        apply( GleObject.__init__, (self, name, 0), kw)
        self.Set(trace3D = kw.get('trace3D'),
                 shape2D = kw.get('shape2D'),
                 contourUp =  kw.get( 'contourUp'),
                 capsFlag = kw.get('capsFlag'))


    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object:
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        capsFlag = kw.get('capsFlag')
        if capsFlag is None:
            if not hasattr(self, 'capsFlag'):
                self.capsFlag = 0
        else:
            self.capsFlag = capsFlag

        shape2D = kw.get('shape2D')
        if shape2D is None:
            if not hasattr(self, 'shape2D'):
                self.shape2D = None
        else:
            self.shape2D = shape2D
        
        contourUp = kw.get('contourUp')
        if contourUp is None:
            if not hasattr(self, 'contourUp'):
                self.contourUp= (0.,0.,1.)
        else:
            self.contourUp = contourUp

        trace3D = kw.get('trace3D')
        if trace3D is None:
            if not hasattr(self, 'trace3D'):
                self.trace3D = Numeric.zeros( (0,3), 'f')
        else:
            self.trace3D = trace3D
                
        if kw.has_key('materials') and kw['materials']:
            materials = Numeric.array((kw['materials']),'f')
            redoDisplayListFlag0 = True
        else:
            materials = Numeric.array(((0.,0.,1.,1.),),'f')

        if not shape2D is None:
            v,n,s = self.extrude()
            if self.capsFlag == 1:
                v, n, s = self.addCaps(v, n, s)
            redoDisplayListFlag = True
            if v is not None:
                kw['vertices']=v
            if n is not None:
                kw['vnormals']=n
            if s is not None:
                kw['stripBegin']=[0] + list( s[:-1,0] )
                kw['stripEnd'] = list( s[:,0])

        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( GleObject.Set, (self, check, 0), kw )

        redoDisplayListFlag = redoDisplayListFlag or redoDisplayListFlag0

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


        
    def addCaps(self, v, n, s):
        """ Method to add front and end caps to the extruded geometry."""
        # calculate the length of each strip
        lenStrip = 2*self.shape2D.lenShape
        # 1- Front Cap:
        #================
        # Get the midPoint of the front cap
        frontMid = self.trace3D[1]
        # Get the coordinates of the contourPoints of the cap
        shapePoints = v[1:lenStrip:2]
        # Organize the points so the strip creates the cap
        frontCapPts = []
        for point in shapePoints.tolist():
            frontCapPts.append(point)
            frontCapPts.append(frontMid)
        # Add the new strip to the front of the vertices
        vertices = Numeric.concatenate( (frontCapPts, v) )

        #Compute normal of the cap by computing the cross product of (M3 M1).
        if self.shape2D.vertDup == 0:
            fm1 = shapePoints[0] - frontMid
            fm3 = shapePoints[1] - frontMid

        elif self.shape2D.vertDup == 1:
            fm1 = shapePoints[0] - frontMid
            fm3 = shapePoints[2] - frontMid
            
        # Cross product
        nc = [[(fm3[1]*fm1[2] - fm3[2]*fm1[1]),
               (fm3[0]*fm1[2] - fm3[2]*fm1[0]),
               (fm3[0]*fm1[1] - fm3[0]*fm1[1])],]

        frontNorm = Numeric.array(nc*lenStrip, 'd')
        # Add the normals to the normal array
        normals = Numeric.concatenate( (frontNorm, n) )
        lastVert = s[-1][0]+lenStrip

        strip = Numeric.concatenate((s, [[lastVert,lastVert],]))

        # 2- End cap:
        #================
        # Get the midPoint of the end cap
        endMid = self.trace3D[-2]
        # Get the coordinates of the contourPoints of the last cap
        endShape = v[-lenStrip:-1:2]
        # Organize the points so the strip creates the cap
        endCapPts = []
        # Definition of the strip 
        for point in endShape.tolist():
            endCapPts.append(endMid)
            endCapPts.append(point)
        # Add the new strip to the front of the vertices
        vertices = Numeric.concatenate( (vertices, endCapPts) )

        #Compute normal of the cap by computing the cross product of 2 vectors\
        # defined by the mid cap point and a point of the shape.
        if self.shape2D.vertDup == 0:
            em1 = endShape[0] - endMid
            em3 = endShape[1] - endMid

        elif self.shape2D.vertDup == 1:
            em1 = endShape[2] - endMid
            em3 = endShape[0] - endMid

        # Cross product
        nc = [[(em3[1]*em1[2] - em3[2]*em1[1]),
               (em3[0]*em1[2] - em3[2]*em1[0]),
               (em3[0]*em1[1] - em3[0]*em1[1])],]

        endNorm = Numeric.array(nc*lenStrip, 'd')

        # Add the normals to the normal array
        normals = Numeric.concatenate( (normals, endNorm) )
        lastVert = strip[-1][0]+lenStrip

        strip = Numeric.concatenate((strip, [[lastVert,lastVert],]))
        return vertices, normals, strip
        
    
    def extrude(self):
        """Virtual Method to do the extrusion along a 3D path with a 2D shape
        using the gle extrusion. We then get the geometry information
        using the extrusion method in Feedback mode. This will then be
        used to build a triangle strip."""
        
        from gle import glec
        gle.gleSetJoinStyle ( self.normalStyle | self.joinStyle )
        glec.gleFeedBack()

        contpts = Numeric.array(self.shape2D.contpts)
        contourPoints = contpts[:,:2]
        contnorm = Numeric.array(self.shape2D.contnorm)
        contourNormals = contnorm[:,:2]
        
        gle.gleExtrusion(contourPoints, contourNormals,
                         self.contourUp,
                         self.trace3D,
                         self.materials[1028].prop[0][:,:3] )

        glec.gleTextureMode(0)
        v,n,s = glec.gleGetTriangleMesh()

        vinv = Numeric.zeros( v.shape, 'd')
        vinv[::2] = v[1::2]
        vinv[1::2] = v[::2]

        ninv = Numeric.zeros( n.shape, 'd')
        ninv[::2] = n[1::2]
        ninv[1::2] = n[::2]

        return vinv, ninv, s

    def getFaces(self):
        """returns a handle to the faces array"""
        return self.IndexedFaceSet.faces.array
    
#
# WARNING the extrusion in this object ONLY works after this object has
# been added to a viewer
#
class GlePolyCylinder(GleExtrude):
    
    keywords = GleExtrude.keywords + [
        'trace3D',
        'radius'
        ]
    
    def __init__(self, name=None, check=1, **kw):

        if __debug__:
            if check:
                apply( checkKeywords, (name,self.keywords), kw)

        r = kw.get('radius')
        if not r: r=1.0
        self.radius = r
        apply( GleExtrude.__init__, (self, name, 0), kw)

        self.Set(trace3D = kw.get( 'trace3D'))


    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( GleExtrude.Set, (self, check, 0), kw)

        if kw.has_key('materials') and kw['materials']:
            materials = Numeric.array((kw['materials']),'f')
        else:
            materials = Numeric.array(((0.,0.,1.,1.),),'f')
        self.trace3D = kw.get('trace3D')
        if not self.trace3D:
            v,n,s = (None,None,None)
            redoDisplayListFlag = True
        else:
            v,n,s = self.extrude()
            redoDisplayListFlag = True
        if v:
            kw['vertices']=v
        if n:
            kw['vnormals']=n
        if s:
            kw['stripBegin']=[0] + list( s[:,0] )
            
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



    def extrude(self):
        """Virtual Method to do the extrusion along a 3D path with a 2D shape
        using the gle extrusion. We then get the geometry information
        using the extrusion method in Feedback mode. This will then be
        used to build a triangle strip."""
        
        from gle import glec
        gle.gleSetJoinStyle ( self.joinStyle | self.normalStyle )
        glec.gleFeedBack()

        #DisplayFunction of the old GlePolyCylinder
        GL.glColorMaterial (GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT)
        GL.glEnable (GL.GL_COLOR_MATERIAL)
        #glEnable(GL_LIGHTING)
        if self.viewer is not None:
            self.viewer.enableOpenglLighting()
        colors = self.materials[GL.GL_FRONT].prop[0][:,:3]
        gle.glePolyCylinder(self.trace3D, colors, self.radius)
        GL.glDisable (GL.GL_COLOR_MATERIAL)
        
        glec.gleTextureMode(0)
        v,n,s = glec.gleGetTriangleMesh()

        return v,n,s
    

class GlePolyCone(GlePolyCylinder):

    keywords = GleExtrude.keywords + [
        'trace3D',
        'radii'
        ]

    def __init__(self, name=None, check=1, **kw):

        if __debug__:
            if check:
                apply( checkKeywords, (name,self.keywords), kw)

        apply( GlePolyCylinder.__init__, (self, name, 0), kw )

        apply( self.Set, (), kw)

        
    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object:
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( GlePolyCylinder.Set, (self, check, 0), kw )

        r = kw.get('radii')
        if r is not None:
            assert len(r)
            self.radii = r

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

        
    
    def extrude(self):
        """Extrude a cone with radii specified at each point
        of the extrusion"""

        assert len(self.radii)==len(self.trace3D)
        from gle import glec
        gle.gleSetJoinStyle ( self.joinStyle | self.normalStyle )
        glec.gleFeedBack()

        #DisplayFunction of the old GlePolyCylinder
        GL.glColorMaterial (GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT)
        GL.glEnable (GL.GL_COLOR_MATERIAL)

        if self.viewer is not None:
            self.viewer.enableOpenglLighting()

        colors = self.materials[GL.GL_FRONT].prop[0][:,:3]
        gle.glePolyCone(self.trace3D, colors, self.radii)
        GL.glDisable (GL.GL_COLOR_MATERIAL)
        
        glec.gleTextureMode(0)
        v,n,s = glec.gleGetTriangleMesh()

        return v,n,s


