## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 


import numpy.oldnumeric as Numeric
from opengltk.OpenGL import GL
from OpenCSG import opencsglib as OpenCSG
from DejaVu.Clip import ClippingPlane
from DejaVu.Geom import Geom
from DejaVu.IndexedPolygons import IndexedPolygons

class DejaVuPrimitive(OpenCSG.PythonPrimitive):

    def __init__(self, geom):
        apply( OpenCSG.PythonPrimitive.__init__, (self, self.render, OpenCSG.Intersection, 0))
        # does not work for some reason
        #OpenCSG.PythonPrimitive(self.render, OpenCSG.Intersection, 1)
        self.geom = geom
        self.dpyListCSG = None


    def redoDisplayListCSG(self):
        if self.dpyListCSG is not None:
            GL.glDeleteLists(1, self.dpyListCSG)
        
        g = self.geom
        self.dpyListCSG = GL.glGenLists(1)
        GL.glNewList(self.dpyListCSG, GL.GL_COMPILE)
##         if isinstance(g, Spheres):
##             g.DisplayFunction()
##         else:
        self.drawpolygons()
        GL.glEndList()


    def drawpolygons(self):
        g = self.geom
        vertices = g.getVertices()
        faces = g.getFaces()
        normals = g.getFNormals()
        GL.glDisable(GL.GL_CULL_FACE)
        for i,f in enumerate(faces):
            GL.glBegin(GL.GL_POLYGON)
            GL.glNormal3fv(normals[i])
            for vi in f:
                GL.glVertex3fv(vertices[vi])
            GL.glEnd()
            i+=1

            
    def render(self, mode='render'):
        # call with mode='csg' to render simple shape to setup Zbuffer for CSG
        # call with mode='render' to render by calling geom's draw function
        if self.geom:
            #import traceback
            #print traceback.print_stack()
            #print self.geom
            #print "========================================================="
            root = self.geom.viewer.rootObject

            instance = [0]
            p = self.geom.parent
            while p:
                instance.append(0)
                p = p.parent

            #mat = Numeric.array(GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)).astype('f')
            #print 'mat OK', mat
            GL.glPushMatrix()
            GL.glLoadIdentity()
            self.geom.viewer.currentCamera.BuildTransformation()
            self.geom.BuildMat(self.geom, root, True, instance)

            #mat = Numeric.array(GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)).astype('f')
            #print 'mat PB', mat
            #print 'render ', mode, self.geom
            if mode=='csg':
                if self.dpyListCSG is None:
                    self.redoDisplayListCSG()
                GL.glCallList(self.dpyListCSG)
            elif mode=='render':
                obj = self.geom
                if not obj.inheritMaterial:
                    obj.InitMaterial(0)
                    obj.InitColor(0)
                obj.DisplayFunction()
                
            GL.glPopMatrix()




class CsgGeom(Geom):

    keywords = Geom.keywords + [
        'primitives',
        'algo',
        'depthalgo',
        ]

    def __init__(self, name=None, check=1, **kw):

        # C++ primitives
        self.primitives = OpenCSG.PrimitiveVector()

        # python subclasses used to call python implementation or render
        self.pyprimitives = []

        algo = kw.get('algo')
        if algo is None:
            kw['algo'] = OpenCSG.Goldfeather

        depthalgo = kw.get('depthalgo')
        if depthalgo is None:
            kw['depthalgo'] = OpenCSG.DepthComplexitySampling

        apply( Geom.__init__, (self, name, check), kw)


    def clearPrimitives(self):
        self.primitives.clear()
        self.pyprimitives = []


    def setPrimitives(self, *args):
        self.clearPrimitives()

        for g in args:
            assert isinstance(g, Geom)
            prim = DejaVuPrimitive(g)
            #self.primitives.append(prim)
            OpenCSG.PrimitiveVector_add(self.primitives, prim)
            self.pyprimitives.append(prim)


    def Set(self, check=1, redo=1, updateOwnGui=True, **kw):
        """set data for this object: primitives
check=1 : verify that all the keywords present can be handle by this func 
redo=1 : append self to viewer.objectsNeedingRedo
updateOwnGui=True : allow to update owngui at the end this func
"""
        #print "CsgGeom.Set"

        redrawFlag, \
        updateOwnGuiFlag, \
        redoViewerDisplayListFlag, \
        redoDisplayListFlag, \
        redoTemplateFlag, \
        redoDisplayChildrenListFlag = apply( Geom.Set, (self, check, 0), kw)
        
        p = kw.get( 'primitives')
	if p:
            assert isinstance(p, OpenCSG.PythonPrimitiveVector)
            self.primitives = p

        a = kw.get( 'algo')
	if a:
            if a =='automatic':
                a = OpenCSG.Automatic
            elif a== 'goldfeather':
                a = OpenCSG.Goldfeather
            elif a == 'scs':
                a = OpenCSG.SCS
            assert a in (OpenCSG.Automatic, OpenCSG.Goldfeather, OpenCSG.SCS)
            self.algo = a

        d = kw.get( 'depthalgo')
	if d:
            if d =='DepthComplexitySampling':
                d = OpenCSG.DepthComplexitySampling
            elif d== 'NoDepthComplexitySampling':
                d = OpenCSG.NoDepthComplexitySampling
            elif d == 'OcclusionQuery':
                d = OpenCSG.OcclusionQuery
            assert d in (OpenCSG.DepthComplexitySampling,
                         OpenCSG.NoDepthComplexitySampling,
                         OpenCSG.OcclusionQuery)
            self.depthalgo = d

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
        GL.glEnable(GL.GL_DEPTH_TEST);
        GL.glClear( GL.GL_STENCIL_BUFFER_BIT)
        GL.glDisable(GL.GL_FOG)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        
        OpenCSG.render(self.primitives, self.algo, self.depthalgo)

        GL.glDepthFunc(GL.GL_EQUAL)

        # FIXME should only enable fog if it is on in camera
        GL.glEnable(GL.GL_FOG)
        self.SetupGL()
        for p in self.pyprimitives:
            p.render()

        GL.glDepthFunc(GL.GL_LESS);
