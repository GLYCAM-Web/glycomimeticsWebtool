## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

#############################################################################
#
# Author: Michel F. SANNER
#
# Copyright: M. Sanner TSRI 2000
#
#############################################################################

#
# $Header: /opt/cvs/python/packages/share1.5/DejaVu/Displayable.py,v 1.47.2.2 2009/06/11 23:02:22 vareille Exp $
#
# $Id: Displayable.py,v 1.47.2.2 2009/06/11 23:02:22 vareille Exp $
#

from opengltk.OpenGL import GL
import types
import numpy.oldnumeric as Numeric
import Materials, viewerConst
from viewerFns import getkw
from colorTool import OneColor, glMaterialWithCheck, resetMaterialMemory

class OutLine:
    """Base class for wire frame used for outlined polygons"""

    def Reset(self):
	"""Reset members to default values"""

	self.factor = 1.5
	self.unit = 0.000001
	self.lineWidth = 1
	self.color = (0., 0., 0., .3)
        self.colorAsMaterial = False # set to True to use Object's material
                                     # to color lines
	self.dpyList = None
        self.lighting = False

        
    def Set(self, redo=0,**kw):
	"""Set members"""

	val = getkw(kw, 'factor')
	if val is not None:
	    assert type(val).__name__ == 'float'
	    self.factor = val

	val = getkw(kw, 'unit')
	if val is not None:
	    assert type(val).__name__ == 'float'
	    self.unit = val

	val = getkw(kw, 'lineWidth')
	if val is not None:
	    assert val >= 1
	    self.lineWidth = int(val)

	val = getkw(kw, 'color')
	if val is not None:
	    color = OneColor( val )
	    if color: self.color = color

	val = getkw(kw, 'lighting')
	if val is not None:
	    assert val in [False, True]
	    self.lighting = val

	val = getkw(kw, 'colorAsMaterial')
	if val is not None:
	    assert val in [False,True]
	    self.colorAsMaterial = val

        if self.geom.viewer is not None:
            self.geom.RedoDisplayList()
        
	if len(kw):
	    print 'WARNING2: Keyword(s) %s not used' % kw.keys()


    def __init__(self, geom, **kw):

        self.geom = geom
	self.Reset()
	self.Set( factor = getkw(kw, 'factor'),
		  unit = getkw(kw, 'unit'),
		  lineWidth = getkw(kw, 'lineWidth'),
		  color = getkw(kw, 'color') )

	if len(kw):
	    print 'WARNING3: Keyword(s) %s not used' % kw.keys()


    def __repr__(self):
	return '<%s> factor=%5.2f unit=%5.2f lineWidth=%5.2f color=%s' % \
	       (self.__class__, self.factor, self.unit, self.lineWidth,
		str(self.color) )


class LineStipple:
    """Base class for line stippling information"""

    def Reset(self):
	"""Reset members to default values"""

	self.factor = 1
	self.pattern = 0x7878

    
    def Set(self, **kw):
	"""Set members"""

	val = getkw(kw, 'factor')
	if val:
	    assert type(val).__name__ == 'int' and val > 0
	    self.factor = val

	val = getkw(kw, 'pattern')
	if val:
	    assert val > 0x0000 and val < 0xFFFF
	    self.pattern = val

	if len(kw):
	    print 'WARNING4: Keyword(s) %s not used' % kw.keys()


    def __init__(self, **kw):

	self.Reset()
	self.Set( factor = getkw(kw, 'factor'),
		  pattern = getkw(kw, 'pattern'))

	if len(kw):
	    print 'WARNING5: Keyword(s) %s not used' % kw.keys()


    def __repr__(self):
	return '<%s> factor=%f pattern=%s' % ( self.__class__,
		self.factor, hex(self.pattern) )


class PolygonStipple:
    """Base class for polygon stippling information"""

    def Reset(self):
	"""Reset members to default values"""

	self.pattern = Numeric.ones( (128,)) * 0xFF
	self.pattern = self.pattern.astype('B')
    
    def Set(self, **kw):
	"""Set members"""

	val = getkw(kw, 'pattern')
	if val is not None:
	    assert type(val).__name__ == 'ndarray'
	    assert val.shape[0] == 128
	    assert val.dtype.char == 'B'
	    self.pattern = val

	if len(kw):
	    print 'WARNING6: Keyword(s) %s not used' % kw.keys()


    def __init__(self, **kw):

	self.Reset()
	self.Set( pattern = getkw(kw, 'pattern'))

	if len(kw):
	    print 'WARNING7: Keyword(s) %s not used' % kw.keys()


    def __repr__(self):
	return '<%s>\n pattern=%s' % ( self.__class__, map(hex,self.pattern) )


class Displayable:
    """Base class for all object that can be viewed"""

    def Set(self, **kw):
        """set data for this object"""

        # currently all these attributs are in GEOM
        # they should move here
        pass


    def __init__(self):

        self.materials = { GL.GL_FRONT:Materials.Materials(),
        		   GL.GL_BACK:Materials.Materials() }
        self.texture = None
        
        self.frontPolyMode = GL.GL_FILL
        self.backPolyMode = GL.GL_FILL
        self.frontAndBack = viewerConst.NO
        self.shading = GL.GL_SMOOTH
        self.lighting = viewerConst.NO
        self.culling = GL.GL_BACK
        #self.antiAliased = 0
        #self.antialiased = viewerConst.NO
        self.primitiveType = None
        
        self.inheritMaterial = viewerConst.YES
        self.inheritFrontPolyMode = viewerConst.YES
        self.inheritBackPolyMode = viewerConst.YES
        self.inheritShading = viewerConst.YES
        self.inheritLighting = viewerConst.YES
        self.inheritCulling = viewerConst.YES
        self.inheritPointWidth = viewerConst.YES
        self.inheritLineWidth = viewerConst.YES
        self.inheritStippleLines = viewerConst.YES
        self.inheritStipplePolygons = viewerConst.YES
        
        self.dpyList = None     # OpenGL display list used to draw this object
        self.lineWidth = 2
        self.pointWidth = 2

        from DejaVu.Transformable import Transformable
        if isinstance(self, Transformable):
        	self.drawOutline = viewerConst.NO
        	self.outline = OutLine(self)
        	self.linestipple = LineStipple()
        	self.stippleLines = viewerConst.NO
        	self.polygonstipple = PolygonStipple()
        	self.stipplePolygons = viewerConst.NO

        self.transparent = viewerConst.NO

        self.depthMask = 1 # 0: zbuffer is readOnly for transparent objects
                           # 1: zbuffer is read write for transparent objects
        self.srcBlendFunc = GL.GL_SRC_ALPHA
        #self.dstBlendFunc = GL.GL_ONE #GL.GL_ONE_MINUS_SRC_COLOR
        # ONE_MINUS_SRC_ALPHA works for colorMapEditor
        self.dstBlendFunc = GL.GL_ONE_MINUS_SRC_ALPHA 

        
    def InitMaterial(self, num=0):
	"""Setup GL material
only sets the material if binding mode is OVERALL or PER_INSTANCE (i.e. per
instance matrix) which are the 2 only material bindngs for which the material
is not set in the display list"""

	prop = self.materials[GL.GL_FRONT]
	if self.frontAndBack: f = GL.GL_FRONT_AND_BACK
	else: f = GL.GL_FRONT
        resetMaterialMemory()
        
        b, p = prop.GetProperty(0)
        if prop.binding[0] == viewerConst.OVERALL:
	    glMaterialWithCheck(f, GL.GL_AMBIENT, p[0])
        elif prop.binding[0] == viewerConst.PER_INSTANCE:
	    glMaterialWithCheck(f, GL.GL_AMBIENT, p[num])

        b, p = prop.GetProperty(1)
	if prop.binding[1] == viewerConst.OVERALL:
	    glMaterialWithCheck(f, GL.GL_DIFFUSE, p[0])
        elif prop.binding[1] == viewerConst.PER_INSTANCE:
	    glMaterialWithCheck(f, GL.GL_DIFFUSE, p[num])
		
        b, p = prop.GetProperty(2)
	if prop.binding[2] == viewerConst.OVERALL:
	    glMaterialWithCheck(f, GL.GL_EMISSION, p[0])
        elif prop.binding[3] == viewerConst.PER_INSTANCE:
	    glMaterialWithCheck(f, GL.GL_EMISSION, p[num])

        b, p = prop.GetProperty(3)
	if prop.binding[2] == viewerConst.OVERALL:
	    glMaterialWithCheck(f, GL.GL_SPECULAR, p[0])
	elif prop.binding[2] == viewerConst.PER_INSTANCE:
	    glMaterialWithCheck(f, GL.GL_SPECULAR, p[num])

	if prop.binding[4] == viewerConst.OVERALL:
	    GL.glMaterialf(f, GL.GL_SHININESS, float(prop.prop[4][0]))
        elif prop.binding[4] == viewerConst.PER_INSTANCE:
	    GL.glMaterialf(f, GL.GL_SHININESS, float(prop.prop[4][num]))
            
	if not self.frontAndBack:
	    prop = self.materials[GL.GL_BACK]
	    f = GL.GL_BACK
            if prop.binding[0] == viewerConst.OVERALL:
		glMaterialWithCheck(f, GL.GL_AMBIENT, prop.prop[0][0])
            elif prop.binding[0] == viewerConst.PER_INSTANCE:
		glMaterialWithCheck(f, GL.GL_AMBIENT, prop.prop[0][num])
                
	    if prop.binding[1] == viewerConst.OVERALL:
		glMaterialWithCheck(f, GL.GL_DIFFUSE, prop.prop[1][0])
            elif prop.binding[1] == viewerConst.PER_INSTANCE:
		glMaterialWithCheck(f, GL.GL_DIFFUSE, prop.prop[1][num])
                
	    if prop.binding[2] == viewerConst.OVERALL:
		glMaterialWithCheck(f, GL.GL_SPECULAR, prop.prop[3][0])
            elif prop.binding[2] == viewerConst.PER_INSTANCE:
		glMaterialWithCheck(f, GL.GL_SPECULAR, prop.prop[3][num])

            if prop.binding[3] == viewerConst.OVERALL:
		glMaterialWithCheck(f, GL.GL_EMISSION, prop.prop[2][0])
            elif prop.binding[3] == viewerConst.PER_INSTANCE:
		glMaterialWithCheck(f, GL.GL_EMISSION, prop.prop[2][num])

	    if prop.binding[4] == viewerConst.OVERALL:
		GL.glMaterialf(f, GL.GL_SHININESS, float(prop.prop[4][0]))
            elif prop.binding[4] == viewerConst.PER_INSTANCE:
                GL.glMaterialf(f, GL.GL_SHININESS, float(prop.prop[4][num]))

    def InitColor(self, num=0):
	"""Setup GL color (used when lighting is turned off)
only sets the color if binding mode is OVERALL or PER_INSTANCE (i.e. per
instance matrix) which are the 2 only colors which are not set in the
display list"""

        
        prop = self.materials[GL.GL_FRONT]
        if prop.binding[1] == viewerConst.OVERALL:
            material = prop.prop[prop.diff][0]
            if not material.flags.contiguous:
                material = Numeric.array(material,copy=1)
            GL.glColor4fv ( material.tolist() )
        elif prop.binding[1] == viewerConst.PER_INSTANCE:
            material = prop.prop[prop.diff][num]
            if not material.flags.contiguous:
                material = Numeric.array(material,copy=1)
            GL.glColor4fv ( material.tolist() )
## =======

##         mat = self.materials[GL.GL_FRONT]
##         # without tolist() we hang if array is not contiguous !
## 	GL.glColor4fv ( mat.prop[mat.diff][0].tolist() )
## >>>>>>> 1.8.2.1


    def _WidthAndStipple(self):
        """Set the line or points width
"""
        #print "_WidthAndStipple", self.stippleLines , self.inheritStippleLines , self

        GL.glPointSize(self.getPointWidth())

        GL.glLineWidth(self.getLineWidth())

        if self.getStippleLines() in (True, 1):
            GL.glEnable(GL.GL_LINE_STIPPLE)
            ls = self.linestipple
            GL.glLineStipple(ls.factor, ls.pattern)
        else:
            GL.glDisable(GL.GL_LINE_STIPPLE)

        if self.getStipplePolygons() in (True, 1):
            GL.glEnable(GL.GL_POLYGON_STIPPLE)
            ps = self.polygonstipple
            GL.glPolygonStipple(self.polygonstipple.pattern)
        else:
            GL.glDisable(GL.GL_POLYGON_STIPPLE)


    def getPointWidth(self):
        #print "getPointWidth", self.name
        obj = self
        while obj.inheritPointWidth:
            if obj.parent:
                obj = obj.parent
            else:
                break
        return obj.pointWidth


    def getLineWidth(self):
        #print "getLineWidth", self.name
        obj = self
        while obj.inheritLineWidth:
            if obj.parent:
                obj = obj.parent
            else:
                break
        return obj.lineWidth


    def getStippleLines(self):
        #print "getStippleLines", self.name
        obj = self
        while obj.inheritStippleLines:
            if obj.parent:
                obj = obj.parent
            else:
                break
        return obj.stippleLines


    def getStipplePolygons(self):
        #print "getStipplePolygons", self.name
        obj = self
        while obj.inheritStipplePolygons:
            if obj.parent:
                obj = obj.parent
            else:
                break
        return obj.stipplePolygons


#    def _AntiAliasing(self):
#	"""Turn line or points antialiasing on or of"""
#
#	if self.antialiased==viewerConst.YES:
#	    if self.primitiveType == GL.GL_POINTS or \
#	       self.frontPolyMode == GL.GL_POINT or \
#	       self.backPolyMode == GL.GL_POINT:
#		GL.glEnable(GL.GL_POINT_SMOOTH)
#
#	    elif self.primitiveType in viewerConst.LINES_PRIMITIVES or \
#		 self.frontPolyMode == GL.GL_LINE or \
#		 self.backPolyMode == GL.GL_LINE:
#		GL.glEnable(GL.GL_LINE_SMOOTH)
#
#	    GL.glEnable(GL.GL_BLEND)
#	else:
#	    GL.glDisable(GL.GL_LINE_SMOOTH)
#	    GL.glDisable(GL.GL_BLEND)


    def SetupGL(self):
        """Setup OpenGL rendering state for this object
"""
        #print "SetupGL", self

        if not self.inheritMaterial:
            self.InitMaterial()
            self.InitColor()

        if self.GetLighting():
            #glEnable(GL_LIGHTING)
            if self.viewer is not None:
                self.viewer.enableOpenglLighting()

            shading = self.GetShading()

	    if shading != GL.GL_NONE:
                if self.normals is not None:
                    if (shading==GL.GL_SMOOTH and \
                        len(self.normals)!=len(self.vertexSet)) or \
                        (shading==GL.GL_FLAT and \
                         len(self.normals)!=len(self.faceSet)):
                        self.GetNormals()
                        self.viewer.objectsNeedingRedo[self] = None

		GL.glShadeModel(shading)

	else: # no lighting
	    GL.glDisable(GL.GL_LIGHTING)

	if not self.inheritCulling:
	    if self.culling in (GL.GL_BACK, GL.GL_FRONT, GL.GL_FRONT_AND_BACK):
		GL.glCullFace(self.culling)
		GL.glEnable(GL.GL_CULL_FACE)
	    else: GL.glDisable(GL.GL_CULL_FACE)

	if not self.inheritFrontPolyMode:
            mode =self.frontPolyMode
            if self.frontPolyMode==viewerConst.OUTLINED:
                mode = GL.GL_FILL
	    if self.frontAndBack:
		GL.glPolygonMode(GL.GL_FRONT_AND_BACK, mode)
	    else:
		GL.glPolygonMode(GL.GL_FRONT, mode)

	if not self.inheritBackPolyMode:
            mode = self.backPolyMode
            if self.backPolyMode==viewerConst.OUTLINED:
                mode = GL.GL_FILL
	    GL.glPolygonMode(GL.GL_BACK, mode)

	#self._AntiAliasing()
	self._WidthAndStipple()


    def showOwnGui(self):
        #print "showOwnGui", self
        if self.ownGui is None:
            self.createOwnGui()
        if self.ownGui.winfo_ismapped() == 0:
            self.ownGui.deiconify()
        self.ownGui.lift()


    def hideOwnGui(self):
        #print "hideOwnGui", self
        if (self.ownGui is not None) and (self.ownGui.winfo_ismapped() == 0):
            self.ownGui.withdraw()


