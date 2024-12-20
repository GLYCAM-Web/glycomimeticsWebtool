def trilinterp(pts, map, inv_spacing, origin):
    """returns a list of values looked up in a 3D grid (map) at
3D locations (tcoords).

INPUT:
    pts           3D coordinates of points to lookup
    map,          grid data (has to be a Numeric array)
    inv_spacing,  1. / grid spacing (3-tuple)
    origin	  minimum coordinates in x, y and z
OUTPUT:
    values        values at points
"""
##
##
## Authors: Garrett M. Morris, TSRI, Accelerated C version 2.2 (C++ code)
##          David Goodsell, UCLA, Original FORTRAN version 1.0 (C code)
##          Michel Sanner (python port)
## Date: 10/06/94, march 26 03

    values = []
    invx, invy, invz = inv_spacing
    xlo, ylo, zlo = origin
    maxx = map.shape[0] - 1
    maxy = map.shape[1] - 1
    maxz = map.shape[2] - 1
    
    for i in xrange(len(pts)):
        pt = pts[i]

        u   = (pt[0]-xlo) * invx
        u0  = max(0, int(u))    # clamp at lower bound of volume
        u0  = min(maxx, u0)
        u1  = min(maxx, u0 + 1) # clamp at upper bounds of volume
        u1  = max(0, u1)
        if u0>=maxx: # outside on X+ axis
            p0u = 1.0
            p1u = 0.0
        elif u0<=0: # outside on X- axis
            p0u = 0.0
            p1u = 1.0
        else:
            p0u = u - u0
            p1u = 1. - p0u

        v   = (pt[1]-ylo) * invy
        v0  = max(0, int(v))    # clamp at lower bound of volume
        v0  = min(maxy, v0)
        v1  = min(maxy, v0 + 1) # clamp at upper bounds of volume
        v1  = max(0, v1)
        if v0>=maxy: # outside on Y+ axis
            p0v = 1.0
            p1v = 0.0
        elif v0<=0: # outside on Y- axis
            p0v = 0.0
            p1v = 1.0
        else:
            p0v = v - v0
            p1v = 1. - p0v

        w   = (pt[2]-zlo) * invz
        w0  = max(0, int(w))    # clamp at lower bound of volume
        w0  = min(maxz, w0)
        w1  = min(maxz, w0 + 1) # clamp at upper bounds of volume
        w1  = max(0, w1)
        if w0>=maxz: # outside on Z+ axis
            p0w = 1.0
            p1w = 0.0
        elif w0<=0: # outside on Z- axis
            p0w = 0.0
            p1w = 1.0
        else:
            p0w = w - w0
            p1w = 1. - p0w

        m = 0.0
        m = m + p1u * p1v * p1w * map[ u0 ][ v0 ][ w0 ]
        m = m + p1u * p1v * p0w * map[ u0 ][ v0 ][ w1 ]
        m = m + p1u * p0v * p1w * map[ u0 ][ v1 ][ w0 ]
        m = m + p1u * p0v * p0w * map[ u0 ][ v1 ][ w1 ]
        m = m + p0u * p1v * p1w * map[ u1 ][ v0 ][ w0 ]
        m = m + p0u * p1v * p0w * map[ u1 ][ v0 ][ w1 ]
        m = m + p0u * p0v * p1w * map[ u1 ][ v1 ][ w0 ]
        m = m + p0u * p0v * p0w * map[ u1 ][ v1 ][ w1 ]

	values.append(m)

    return values
