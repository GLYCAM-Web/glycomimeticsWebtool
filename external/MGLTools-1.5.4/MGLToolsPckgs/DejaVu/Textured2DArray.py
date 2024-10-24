## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

import numpy.oldnumeric as Numeric

from DejaVu.colorTool import RGBARamp
from DejaVu.Texture import Texture
from DejaVu.viewerFns import checkKeywords
from DejaVu.colorMap import ColorMap
from DejaVu.IndexedPolygons import IndexedPolygons


class textured2DArray(IndexedPolygons):
    """Draw a quad with a 2D array textured mapped on it using a colormap"""

    keywords = IndexedPolygons.keywords + [
        'array',     # 2D array of data to be turned into texture
        'colormap',  # colormap used for mapping data inot colors
        'min',       # min value used for mapping data inot colors
        'max',       # max value used for mapping data inot colors
        ]

    def __init__(self, name='textured2DArray', check=1, redo=1, **kw):

        # default colormap
        self.colormap = ColorMap('default', RGBARamp())

        # 2d array
        self.array = None

        if not kw.has_key('inheritMaterial'):
            kw['inheritMaterial'] = 0

        if not kw.has_key('culling'):
            kw['culling'] = 'none'

        if not kw.has_key('blendFunctions'):
            kw['blendFunctions'] = ('GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA')

        if not kw.has_key('frontPolyMode'):
            kw['frontPolyMode'] = 'fill'

        if not kw.has_key('backPolyMode'):
            kw['backPolyMode'] = 'fill'

        if not kw.has_key('shading'):
            kw['shading'] = 'flat'

        if not kw.has_key('vertices'):
            kw['vertices'] = ((0.,0,0), (1,0,0), (1,1,0), (0,1,0))

        kw['faces'] = ((0,1,2,3),)
        #kw['faces'] = ( (0, 1, 2), (0, 2, 3) )

        apply( IndexedPolygons.__init__, (self, name, check), kw)
        


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
        redoDisplayChildrenListFlag = apply( IndexedPolygons.Set, (self, check, 0), kw )

        rebuildTexture=False
	val = kw.get( 'array')
        if val is not None:
            array = Numeric.array(val)
            assert len(array.shape)==2
            self.array = val
            rebuildTexture=True
            
	val = kw.get( 'colormap')
        if val is not None:
            assert isinstance(val, ColorMap)
            self.colormap = val
            rebuildTexture=True

        setMinMax = False
	val = kw.get( 'max')
        if val:
            maxi = float(val)
            setMinMax = True
        else:
            maxi = self.colormap.maxi
            
	val = kw.get( 'min')
        if val:
            mini = float(val)
            setMinMax = True
        else:
            mini = self.colormap.mini

        if mini<= maxi and setMinMax:
            self.colormap.configure(mini=mini, maxi=maxi, updateGui=True)

        if rebuildTexture and self.array is not None:
            tex, texCoords = self.buildTexture()
            self.Set(texture=tex, textureCoords=texCoords) 

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



    def buildTexture(self):
        """Build a 2D Texture object and compute texture coordinates for
self.array, using self.colormap to colorize the texture.
"""
        width, height = self.array.shape
        # find smallest power of 2 larger than shape
        dim1=dim2=1
        while dim1<width: dim1 = dim1<<1
        while dim2<height: dim2 = dim2<<1

        # compute texture indices
        r1=float(width)/float(dim1)
        r2=float(height)/float(dim2)
        textCoords = ((0,0), (r1,0), (r1, r2), (0, r2))

        # build texture object for DejaVu
        sl = Numeric.array(Numeric.transpose(self.array))

        # use this line when new color map will be used
        colors = self.colormap.Map(sl.ravel())

        colors.shape = (height, width, -1)
        colors = colors*255
        colors = colors.astype('B')

        tex2DimageArr = Numeric.zeros((dim2,dim1,colors.shape[2]), 'B')
        tex2DimageArr[:height,:width] = colors

        tex = Texture()
        tex.Set(enable=1, image=tex2DimageArr, auto=0)
        tex.width = dim1
        tex.height = dim2

        return tex, textCoords

