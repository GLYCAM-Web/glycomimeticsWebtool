## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

#############################################################################
#
# Author: Alex T. GILLET
#
# Copyright: A. Gillet TSRI 2003
#
#############################################################################
#
# $Header: 
#
# $Id: w
#
##
# class to draw a arrow in DejaVu
##
from opengltk.OpenGL import GL
import numpy.oldnumeric as Numeric
from numpy.oldnumeric import array
from IndexedGeom import IndexedGeom
import datamodel, viewerConst
from viewerFns import checkKeywords
from Materials import Materials
from colorTool import glMaterialWithCheck, resetMaterialMemory

class Arrows(IndexedGeom):
    """Class for sets of arrows"""



    keywords = IndexedGeom.keywords 

    def __init__(self, name=None, check=1, **kw):

        if __debug__:
            if check:
                apply( checkKeywords, (name,self.keywords), kw)

	if not kw.get('shape'):
	    kw['shape'] = (0,3)    # default shape for sphere set

        apply( IndexedGeom.__init__, (self, name, 0), kw)
        
        self.culling = GL.GL_BACK
        self.inheritCulling = 0
        
	assert len(self.vertexSet.vertices.ashape)==2

        self.frontPolyMode = GL.GL_FILL
	self.inheritFrontPolyMode = viewerConst.NO
	self.lighting = viewerConst.YES
        self.realFMat = Materials() # used in RedoDisplayList to build 
        self.realBMat = Materials() # used in RedoDisplayList to build 
                                    # material taking getFrom into account
        self.radius = 0.2
        self.oneRadius = viewerConst.YES
        self._arrowTemplate(4)
        
        Arrows.Set(self)

        self._modified = False


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
        redoDisplayChildrenListFlag = apply( IndexedGeom.Set, (self, check, 0), kw )

        v=kw.get('vertices')
        if v:
            redoDisplayListFlag = True
            self.oneRadius = viewerConst.NO

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

        if len(self.vertexSet.vertices) == 0:
            return 0

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
        #if self.oneRadius == viewerConst.NO:
            #radii = self.vertexSet.radii.array

        pickName = 0
        for i in xrange(len(self.faceSet.faces.array)):
            for j in xrange(len(self.faceSet.faces.array[i])-1):
                vi1 = self.faceSet.faces.array[i][j]
                vi2 = self.faceSet.faces.array[i][j+1]
                #print vi1,vi2
                if fp:
                    fpp1 = [None,None,None,None,None]
                    fpp2 = [None,None,None,None,None]
                    for m in (0,1,2,3,4):
                        if fp.binding[m] == viewerConst.PER_VERTEX:
                            fpp1[m] = fp.prop[m][vi2]
                            # to make sure array is contiguous
                            fpp1[m] = array(fpp1[m],copy=1)
                            fpp2[m] = fp.prop[m][vi1]
                            fpp2[m] = array(fpp2[m],copy=1)
                        elif fp.binding[m] == viewerConst.PER_PART:
                            fpp2[m]= fpp1[m] = fp.prop[m][i]
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
                else:
                    bpp1 = bpp2 = None

                GL.glPushName(pickName)
                self.arrowdraw(c[vi1], c[vi2],fpp1, bpp1, fpp2, bpp2,face)
                GL.glPopName()
                pickName = pickName +1
        return 1


    def _arrowTemplate(self, npoly):    

        assert (npoly >1)
        import numpy.oldnumeric as Numeric, math

        self.npoly = npoly
        self.v = Numeric.zeros( ((npoly+2),3), 'f')

        a = -math.pi 		# starting angle
        d = 2*math.pi / npoly 	# increment

        # coord of 1st point of arrow
        self.v[0][0] = 0.
        self.v[0][1] = 0.
        self.v[0][2] = 0.
        # coord of 2st point of arrow 
        self.v[1][0] = 0.
        self.v[1][1] = 0.
        self.v[1][2] = 1.
        # coord of the others points
        for i in range(npoly):
            h = i+2
            self.v[h][0] = math.cos(a)/10.
            self.v[h][1] = math.sin(a)/10.
            self.v[h][2] = 0.75
            a=a+d

    def arrowdraw(self, x, y, colxf=None, colxb=None,
                  colyf=None, colyb=None,face=None):
        # draw a cylinder going from x to y
        # col for materials
        # face can be GL_FRONT_AND_BACK or something else

        # determine scale and rotation of template
        import math
        sz=0.0
        for i in (0,1,2): sz=sz+(x[i]-y[i])*(x[i]-y[i])
        if sz <= 0.0: return
        sz = math.sqrt(sz)

        rx = -180.0*math.acos((y[2]-x[2])/sz)/math.pi
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

        # draw arrow
        GL.glBegin(GL.GL_LINES)
        
        if colxf:
            
            for m in (0,1,2,3,4):
                if colxf[m] is not None:
                    glMaterialWithCheck( face, viewerConst.propConst[m],
                                         colxf[m] )
        if colxb and face!=GL.GL_FRONT_AND_BACK:
            for m in (0,1,2,3,4):
                if colxb[m] is not None:
                    glMaterialWithCheck( GL.GL_BACK,
                                         viewerConst.propConst[m],
                                         colxb[m] )
                    
        GL.glVertex3f(float(self.v[0][0]), float(self.v[0][1]), float(self.v[0][2]*sz))
        GL.glVertex3f(float(self.v[1][0]), float(self.v[1][1]), float(self.v[1][2]*sz))
        for i in range(self.npoly):
            h = i+2
            vx = self.v[h]
            GL.glVertex3f(float(self.v[1][0]), float(self.v[1][1]),
                          float(self.v[1][2]*sz))
            GL.glVertex3f(float(vx[0]*sz), float(vx[1]*sz), float(vx[2]*sz))

        GL.glEnd()

        GL.glPopMatrix()             



#############################################################################
#
# Author: Yong Zhao
#
# Copyright: Y.Zhao, 2004
#
#############################################################################

from DejaVu.Cylinders import Cylinders
#from opengltk.OpenGL import GL
from math import sqrt
#import numpy.oldnumeric as Numeric
from warnings import warn
from mglutil.util.defaultPalettes import ChooseColor
import types

class Axis:
    """This class displays an axis in a viewer"""
    
    def __init__(self, point1=None, point2=None,  point=None, unitVector=None,
                 length = 1.0, viewer=None,
                 radius = 1.0, color='white', name=None):
        """constructor: two ways of building the axis:
1) by specifing point and unit vector, axis goes throw 'point', with center at
   the point, unit vector gives the direction of axis

2) by two points, axis goes throw the center (average) of the two points,
   axis pointing to the direction of ( point1--> point2)

if both definitions are specified  2) will overwrite 1)

"""
        if point is not None and unitVector is not None:
            p=Numeric.array(point, 'f')
            v=Numeric.array(unitVector, 'f')
            self.point1=p - 0.5 * v
            self.point2=p + 0.5 * v
            
        if point1 is not None and point2 is not None:
            self.point1=Numeric.array(point1,'f')
            self.point2=Numeric.array(point2,'f')
        
        
        self.length=length
        self.radius=radius  
        self.viewer = viewer
        self.color=self.getColor(color)
        if name is None:
            name='Axis'
        self.shaft = Cylinders(name=name, quality=20, materials = [self.color],
                               inheritMaterial=0,
                               culling=GL.GL_NONE)
        if self.viewer:
            self.viewer.AddObject(self.shaft)            
        self.display()

    def getColor(self, color):
        """returns the color of axis, color can be string (e.g. 'red' ) or
tuple (e.g.  (1., 0., 0.)  )
The default color is white (1,1,1)
"""
        if type(color) == types.TupleType and len(color)==3:
            return color
        if type(color) == types.StringType:
            if color in ChooseColor.keys():
                return ChooseColor[color]

        return ChooseColor['white']
        
        
        

    def display(self):
        """Display the """
##                    |\
##  |-----------------| \    
##  |-----------------| /   <- summit
##                    |/  
## v1,v2           v3,v4

        # v = [v1, v2, v3, v4, summit]
        v = self.calculateVertices(self)
        # faces = [ [v1,v2],[v2,v3], [v3,v4], [v4,v5],[v5,summit] ]        
        faces = [ [0,1], [1,2], [2,3], [3,4]  ]
        # radii
        r=self.radius
        radii=( 0.0, r, r, 2*r, 0.0)
        self.shaft.Set( vertices=v,
                        faces=faces,
                        radii=radii,
                        materials = [self.color],
                        )
        
##         self.shaft = Cylinders("shaft", vertices=v,
##                                faces=faces,
##                                radii=radii,
##                                quality=20, materials = [(1,0,0)],
##                                inheritMaterial=0,
##                                cull =GL.GL_NONE)

##         self.shaft = Cylinders("shaft", vertices=v[:3],
##                                faces=faces[:2],
##                                radii=radii[:2],
##                                quality=20, materials = [(1,0,0)],
##                                inheritMaterial=0,
##                                cull =GL.GL_NONE)

##         self.arrow = Cylinders("arrow", vertices=v[2:],
##                                #faces=faces[2:],
##                                faces = [ [0,1], [1,2] ],
##                                radii=radii[2:],
##                                quality=20, materials = [(1,0,0)],
##                                inheritMaterial=0,
##                                cull =GL.GL_NONE)

        if self.viewer:
            self.shaft.Set(culling=GL.GL_NONE,
                           backPolyMode=GL.GL_FILL,
                           vertices=v,
                           faces=faces,
                           radii=radii,
                           materials = [self.color],
                           )
##             self.viewer.AddObject(self.shaft)            
            self.viewer.Redraw()


    def calculateVertices(self, center=None):
        """ tail -> head """
        p1=self.point1
        p2=self.point2
        #if not center:
        center = (p1+p2) /2.0
        vector = p2-p1
        distance = sqrt( (p2[0]-p1[0])**2 +(p2[1]-p1[1])**2 +(p2[2]-p1[2])**2 )
        if distance < 0.000001:
            warn("The two points specified are too close.")
            return
        half = vector * (self.length / distance/2.0) 
        head= center + half
        tail= center - half
        # the arrow's length is 10% of shaft
        summit = center + vector *  \
                 (self.length / distance /2.0 * 1.2)

##
##                    |\
##  |-----------------| \    
##  |-----------------| /   <- summit
##                    |/  
## d_tail,       d_head
##  tail           head      summit

        d_half = vector * ((self.length+0.0001) / distance/2.0)
        d_tail= center - d_half               
        d_head= center + d_half
        head=head.tolist()
        tail=tail.tolist()
        d_head=d_head.tolist()
        d_tail=d_tail.tolist()
        summit = summit.tolist()
        
        return [d_tail, tail, d_head, head, summit]


    def configure(self, length=None, radius=None, point1=None, point2=None,
                  viewer=None , color =None):
        """ change the configuration of axis"""
        update=False
        if length is not None and length != self.length:
            self.length=length
            update=True
        
        if point1 is not None and point1 != self.point1:
            self.point1 = point1
            update=True

        if point2 is not None and point2 != self.point2:
            self.point2 = point2
            update=True
        
        if radius is not None and radius != self.radius:
            self.radius = radius
            update=True

        if viewer is not None and viewer != self.viewer:
            self.viewer = viewer
            update=True

        if color is not None and color != self.color:
            self.color = color
            update=True

        if update:
            self.display()

        ## Fixme:
        ## after changing point1, point2, some parts of the axis is not upated.

    def getShaft(self):
        return self.shaft


    

# fixme unit tests to be added
# example of useage
"""
from DejaVu.Arrows import Axis
xx= Axis(point=[0,0,0 ], unitVector=[1,0,0], length=60.,  viewer=self.GUI.VIEWER, radius=0.3, color='red', name='X axis')
yy= Axis(point=[0,0,0 ], unitVector=[0,1,0], length=60.,  viewer=self.GUI.VIEWER, radius=0.3, color='green', name='Y axis')
zz= Axis(point=[0,0,0 ], unitVector=[0,0,1], length=60.,  viewer=self.GUI.VIEWER, radius=0.3, color='blue', name='Z axis')

"""
