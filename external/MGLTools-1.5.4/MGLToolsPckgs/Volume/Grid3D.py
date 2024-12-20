## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

import numpy.oldnumeric as Numeric

class Grid3D:
    """Class to represent 3D discret volumetric data.
The data has to be a Numeric array od shape 3
"""
    
    def __init__(self, data, origin, stepSize, header, crystal=None):

        assert isinstance(data, Numeric.ArrayType)
        assert len(data.shape)==3
        assert len(origin)==3
        assert len(stepSize)==3

        # header dict
        self.header = header
        
        # actual values at the grid points
        self.data = data

        # number of grid points along 3 dimensions
        self.dimensions = data.shape

        # 3D coordinates of lower left front corner (i.e. (0,0,0) grid point) 
        self.origin = origin

        # grid step size
        self.stepSize = stepSize

        # crystal object, used to cnvert between fractioanl and cartesian space
        # will be an instance mglutil.math.crystal.Crystal
        self.crystal = crystal


    def centerPoint(self):
        """compute and return a center point of this grid"""
        orig = self.origin
        dims = self.dimensions
        size = self.stepSize
        pt = (orig[0] + (dims[0]*size[0])*0.5,
              orig[1] + (dims[1]*size[1])*0.5,
              orig[2] + (dims[2]*size[2])*0.5)
        if self.crystal:
            pt = grid3D.crystal.toCartesian(pt)
        return pt
        
    def stats(self):
        """returns the mimn, max, mean and standard deviation of a list of values"""
        return self.data.min(), self.data.max(), self.data.mean(), self.data.std()
    

    def normalize(self):
        """if data is given the values in data are modified, else the Grid3D
data attribute is used as data
"""
        data = self.data

        mymin, mymax, mymean, mystdev = self.stats()
        for i in xrange(data.shape[0]):
            for j in xrange(data.shape[1]):
                for k in xrange(data.shape[2]):
                    data[i][j][k] = (data[i][j][k]-mymean)/mystdev
        self.header['amean'] = mymean
        self.header['arms'] = mystdev
        self.header['amax'] = mymax
        self.header['amin'] = mymin


    def getOriginReal(self):
        """return the origin of the grid in real space"""
        origin = self.origin
        if self.crystal:
            origin = self.crystal.toCartesian(self.origin)
        return origin


    def getStepSizeReal(self):
        """return the stepsize of the grid in real space"""
        stepSize = self.stepSize
        from math import sqrt
        if self.crystal:
            vx = self.crystal.toCartesian( (stepSize[0], 0, 0) )
            vy = self.crystal.toCartesian( (0, stepSize[1], 0) )
            vz = self.crystal.toCartesian( (0, 0, stepSize[2]) )
            stepSize = (sqrt(vx[0]*vx[0]+vx[1]*vx[1]+vx[2]*vx[2]),
                        sqrt(vy[0]*vy[0]+vy[1]*vy[1]+vy[2]*vy[2]),
                        sqrt(vz[0]*vz[0]+vz[1]*vz[1]+vz[2]*vz[2]))
        return stepSize


    def overlapWithBox(self, grid3D, Box):
        """Compute the indices of self.data representing the corners
of a box in the grid.
"""
        inds1 = [0,0,0]
        inds2 = [0,0,0]

        stepSize = grid3D.getStepSizeReal()

        origin = grid3D.getOriginReal()

        bside = (Box.xside, Box.yside, Box.zside) 

        # compute the box indices in related to the grid's origin
        # find the center of the box, go to each edge, then set the edges
        # in relation to the grid3D origin
        for i in (0,1,2):
            inds1[i] = ( Box.center[i] - bside[i]*0.5 - origin[i] ) / stepSize[i]
            inds2[i] = ( Box.center[i] + bside[i]*0.5 - origin[i] ) / stepSize[i]
            
        return inds1,inds2
        
    def overlapWithGrid(self, grid):
        """Compute the indices into self.data representing the overlap between
this grid and the one provided as an argument.  Both grids have to have the
same stepSize.
"""
        assert self.stepSize[0]==grid.stepSize[0]
        assert self.stepSize[1]==grid.stepSize[1]
        assert self.stepSize[2]==grid.stepSize[2]

        bc1 = [0,0,0]
        bc2 = [0,0,0]

        stepSize = self.getStepSizeReal()
        origin = self.getOriginReal()
        origin1 = grid.getOriginReal()

        shape1 = grid.data.shape
        for i in (0,1,2):
            bc1[i] = ( origin1[i] - origin[i] ) / stepSize[i]
            bc2[i] = bc1[i] + shape1[i] - 1

        shape = self.data.shape
        for i in (0,1,2):
            bc1[i] = int(round(bc1[i]))
            if bc1[i] < 0: bc1[i]=0
            if bc1[i] > shape[i]: bc1[i]=shape[i]
            bc2[i] = int(round(bc2[i]))
            if bc2[i] < 0: bc2[i]=0
            if bc2[i] > shape[i]: bc2[i]=shape[i]
            
        return bc1, bc2


    def get2DOrthoSlice(self, axis, sliceNum):
        """Return a 2D array corresponding to an axis aligned slice orthogonal
to axis at index along this axis.  We also return the real vertices
corresponding the corner of the quad for this slice.
axis cand be 'x', 'y' or 'z'
sliceNum varies from 0 to max(extent(axis))
"""

        if axis=='x': axisInd = 0
        elif axis=='y': axisInd = 1
        elif axis=='z': axisInd = 2
        else:
            raise ValueError ("axis can only be 'x', 'y', or 'z', got %s"%\
                              str(axis))

        dims = self.dimensions
        dx, dy, dz = (dims[0]-1,dims[1]-1,dims[2]-1)
        if sliceNum < 0:
            raise ValueError ("sliceNum has to be positive")
          
        if sliceNum > dims[axisInd]:
            raise ValueError ("sliceNum for axis %s too large, max %d got %d"%\
                              (axis, dims[axisInd], sliceNum))

        sx, sy, sz = self.stepSize
        ox, oy, oz = self.origin
        ex, ey, ez = (ox+sx*dx, oy+sy*dy, oz+sz*dz)
        if axis=='x':
            slice = Numeric.array(self.data[sliceNum,:,:])
            x = ox + (sx*0.5)+(sliceNum*sx)
            vertices = [ [x,oy,oz], [x,ey,oz], [x,ey,ez], [x,oy,ez] ]

        elif axis=='y':
            slice = Numeric.array(self.data[:,sliceNum,:])
            y = oy + (sy*0.5)+(sliceNum*sy)
            #vertices = [ [ox,y,oz], [ox,y,ez], [ex,y,ez], [ex,y,oz] ]
            vertices = [ [ox,y,oz], [ex,y,oz], [ex,y,ez], [ox,y,ez] ]

        elif axis=='z':
            slice = Numeric.array(self.data[:,:,sliceNum])
            z = oz + (sz*0.5)+(sliceNum*sz)
            vertices = [ [ox,oy,z], [ex,oy,z], [ex,ey,z], [ox,ey,z] ]

        if self.crystal:
            nv = []
            for v in vertices:
                nv.append( tuple(self.crystal.toCartesian(v)) )
            vertices = nv

        return slice, vertices


class Grid3DD(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char in [Numeric.Float64, Numeric.Float]
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)
                        

class Grid3DF(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char in [Numeric.Float32, Numeric.Float16,
                                   Numeric.Float8, Numeric.Float0]
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)
                        

class Grid3DI(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char in [Numeric.Int32, Numeric.Int]
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)


class Grid3DSI(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char == Numeric.Int16
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)


class Grid3DUI(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char in [Numeric.UInt32, Numeric.UInt]
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)


class Grid3DUSI(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char == Numeric.UInt16
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)


class Grid3DUC(Grid3D):
    def __init__(self, data, origin, stepSize, header, crystal=None):
        assert data.dtype.char in [Numeric.Int0, Numeric.UInt8]
        Grid3D.__init__(self, data, origin, stepSize, header, crystal)
        

ArrayTypeToGrid = {
    Numeric.Float64:Grid3DD, Numeric.Float:Grid3DD,
    Numeric.Float32:Grid3DF, Numeric.Float16:Grid3DF,
    Numeric.Float8:Grid3DF, Numeric.Float0:Grid3DF,
    Numeric.Int32:Grid3DI, Numeric.Int:Grid3DI,
    Numeric.Int16:Grid3DSI,
    Numeric.UInt8:Grid3DUC,
    }

GridTypeToArray = {
    'Grid3DD'  :Numeric.Float,
    'Grid3DF'  :Numeric.Float16,
    'Grid3DF'  :Numeric.Float0,
    'Grid3DI'  :Numeric.Int,
    'Grid3DSI' :Numeric.Int16,
    'Grid3DUC' :Numeric.UInt8,
}

