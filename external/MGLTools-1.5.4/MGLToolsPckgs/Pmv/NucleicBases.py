## Automatically adapted for numpy.oldnumeric Jul 23, 2007 by 

# This module handles drawing of Nucleic Bases DNA and RNA
# Author: Sargis Dallakyan (sargis at scripps.edu)
# $Header: /opt/cvs/python/packages/share1.5/Pmv/NucleicBases.py,v 1.12.2.1 2008/12/03 20:50:17 sargis Exp $
# $Date: 2008/12/03 20:50:17 $
# $Id: NucleicBases.py,v 1.12.2.1 2008/12/03 20:50:17 sargis Exp $
from DejaVu.IndexedPolygons import IndexedPolygons
from mglutil.math import crossProduct,norm
import numpy.oldnumeric as Numeric, math
from copy import copy
from opengltk.OpenGL import GL,GLU

class Pyrimidine_old(IndexedPolygons):
    """Used for drawing pyrimidines: Thymine  Uracil  Cytosine"""
    def __init__(self, name=None, color = (0,0,1), **kw):
        self.vertices = []
        vertex = [-0.3,0, 0 ] #N1 - stating point
        self.vertices.append(vertex)
        vertex = [-1.16211294,  0.75792228, 0] #C2
        self.vertices.append(vertex)
        vertex = [-0.99117465, 2.13082724, 0] #N3
        self.vertices.append(vertex)
        vertex = [0,2.8, 0] #C4
        self.vertices.append(vertex)
        vertex = [ 1.37266396,  1.93267237,0] #C5
        self.vertices.append(vertex)
        vertex = [  1.23479297,  0.59071168,0] #C6
        self.vertices.append(vertex)
        vertex = [0.3, 0, 0 ] #N1 - ending point        
        self.vertices.append(vertex)
        
        #z + 0.3 part
        vertex = [-0.3,0, 0.6 ] #N1 - stating point
        self.vertices.append(vertex)
        vertex = [-1.16211294,  0.75792228, 0.6] #C2
        self.vertices.append(vertex)
        vertex = [-0.99117465, 2.13082724, 0.6] #N3
        self.vertices.append(vertex)
        vertex = [0,2.8, 0.6] #C4
        self.vertices.append(vertex)
        vertex = [ 1.37266396,  1.93267237,0.6] #C5
        self.vertices.append(vertex)
        vertex = [  1.23479297,  0.59071168,0.6] #C6
        self.vertices.append(vertex)
        vertex = [0.3, 0, 0.6 ] #N1 - ending point        
        self.vertices.append(vertex)
        self.faces=[[0,1,5,6],[1,2,4,5],[1,2,3,4],[7,13,12,8],[8,12,11,9],
                    [8,11,10,9], [2,1,8,9],
                    [0,6,13,7],[1,0,7,8],[3,2,9,10],[4,3,10,11],[5,4,11,12],
                    [6,5,12,13]]
        kw['vertices'] = self.vertices
        kw['faces'] = self.faces
        kw['shading'] = GL.GL_FLAT
        kw['materials'] = (color,color,color,color,color,color,color,
                           color,color,color,color,color,color,color)
        kw['inheritMaterial'] = False
        apply( IndexedPolygons.__init__, (self, name, 0), kw )

def make_purine(residue, height = 0.4, scale = 1.2):
    """Creates vertices and normals for purines: Adenine Guanine"""
    atoms = residue.atoms
    N9 =  Numeric.array(atoms.objectsFromString('N9')[0].coords)
    C8 =  Numeric.array(atoms.objectsFromString('C8')[0].coords)
    N7 =  Numeric.array(atoms.objectsFromString('N7')[0].coords)
    C5 =  Numeric.array(atoms.objectsFromString('C5')[0].coords)
    C4 =  Numeric.array(atoms.objectsFromString('C4')[0].coords)
    C6 =  Numeric.array(atoms.objectsFromString('C6')[0].coords)
    N1 =  Numeric.array(atoms.objectsFromString('N1')[0].coords)
    C2 =  Numeric.array(atoms.objectsFromString('C2')[0].coords)
    N3 =  Numeric.array(atoms.objectsFromString('N3')[0].coords)
    N9_C8 = C8-N9
    N9_C4 = C4-N9
    C8_C4 = height*norm(C4-C8)
    normal = height*Numeric.array(crossProduct(N9_C8, N9_C4, normal=True))
    #center1 = (N9+C8+N7+C4+C5)/5.0
    #center2 = (C4+C5+C6+N1+C2+N3)/6.0    
    center2 = (C4+C5+C6+N1+C2+N3+N9+C8+N7)/9.0    
    center1 = center2
    vertices = Numeric.zeros((20,3),Numeric.Float)

    vertices[0] = scale*(C8 - normal - center1) + center1
    vertices[1] = scale*(N7 - normal - center1) + center1
    vertices[2] = scale*(C5 - normal - center2) + center2
    vertices[3] = scale*(C4 - normal - center2) + center2
    vertices[4] = scale*(C6 - normal - center2) + center2
    vertices[5] = scale*(N1 - normal - center2) + center2      
    vertices[6] = scale*(C2 - normal - center2) + center2      
    vertices[7] = scale*(N3 - normal - center2) + center2    
    
    vertices[8] = scale*(C8 + normal - center1) + center1
    vertices[9] = scale*(N7 + normal - center1) + center1
    vertices[10] = scale*(C5 + normal - center2) + center2
    vertices[11] = scale*(C4 + normal - center2) + center2
    vertices[12] = scale*(C6 + normal - center2) + center2      
    vertices[13] = scale*(N1 + normal - center2) + center2      
    vertices[14] = scale*(C2 + normal - center2) + center2
    vertices[15] = scale*(N3 + normal - center2) + center2    
    
    vertices[16] = scale*(N9 - C8_C4 - normal - center1) + center1     
    vertices[17] = scale*(N9 - C8_C4 + normal - center1) + center1     
    vertices[18] = scale*(N9 + C8_C4 + normal - center1) + center1     
    vertices[19] = scale*(N9 + C8_C4 - normal - center1) + center1

    
    faces = Numeric.array([[19,3,2,1,0,16,16],
                       [17,8,9,10,11,18,18], 
                       [3,7,6,5,4,2,2],
                       [10,12,13,14,15,11,11],
                       [16,0,8,17,17,17,17], [0,1,9,8,8,8,8], [1,2,10,9,9,9,9], 
                           [2,4,12,10,10,10,10], 
                       [4,5,13,12,12,12,12], [5,6,14,13,13,13,13], 
                           [6,7,15,14,14,14,14],
                           [7,3,11,15,15,15,15],
                       [3,19,18,11,11,11,11] ])
    return vertices,faces

def make_pyrimidine(residue, height = 0.4, scale = 1.2):
    """Creates vertices and normals for pyrimidines:Thymine  Uracil  Cytosine"""
    atoms = residue.atoms
    N1 =  Numeric.array(atoms.objectsFromString('N1')[0].coords)
    C2 =  Numeric.array(atoms.objectsFromString('C2')[0].coords)
    N3 =  Numeric.array(atoms.objectsFromString('N3')[0].coords)
    C4 =  Numeric.array(atoms.objectsFromString('C4')[0].coords)
    C5 =  Numeric.array(atoms.objectsFromString('C5')[0].coords)
    C6 =  Numeric.array(atoms.objectsFromString('C6')[0].coords)
    N1_C2 = C2-N1
    N1_C6 = C6-N1
    C2_C6 = height*norm(C6-C2)
    normal = height*Numeric.array(crossProduct(N1_C2, N1_C6, normal=True))
    center = (N1+C2+N3+C4+C5+C6)/6.0
    vertices = Numeric.zeros((14,3),Numeric.Float)
    vertices[0] = scale*(C2 - normal - center) + center
    vertices[1] = scale*(N3 - normal - center) + center
    vertices[2] = scale*(C4 - normal - center) + center
    vertices[3] = scale*(C5 - normal - center) + center
    vertices[4] = scale*(C6 - normal - center) + center
    
    vertices[5] = scale*(C2 + normal - center) + center
    vertices[6] = scale*(N3 + normal - center) + center
    vertices[7] = scale*(C4 + normal - center) + center
    vertices[8] = scale*(C5 + normal - center) + center
    vertices[9] = scale*(C6 + normal - center) + center
    vertices[10] = scale*(N1 - C2_C6 - normal - center) + center
    vertices[11] = scale*(N1 - C2_C6 + normal - center) + center
    vertices[12] = scale*(N1 + C2_C6 + normal - center) + center
    vertices[13] = scale*(N1 + C2_C6 - normal - center) + center
    
    faces = Numeric.array([[13,4,3,2,1,0,10],
                           [11,5,6,7,8,9,12],
                           [0,5,11,10,10,10,10], [1,6,5,0,0,0,0,], [2,7,6,1,1,1,1], 
                           [3,8,7,2,2,2,2], [4,9,8,3,3,3,3], [13,12,9,4,4,4,4]])
    return vertices, faces

def Add_Nucleic_Bases(g, properties = None):
    """
    Adds Nucleic Bases to g.
    g is a geometry created in Pmv.secondaryStructureCommands
    properties is class that holds information about Nucleic Acids colors and size
    """
    path3D = g.SS.exElt.path3D
    residues = g.SS.residues
    total_res = len(residues)
    vertex_count = 0
    vertices = []
    res_faces = []
    materials = []
    height_purine = height_pyrimidine = 0.4

    if properties:
        color_A = properties.color_A
        color_G = properties.color_G
        color_T = properties.color_T
        color_C = properties.color_C
        color_U = properties.color_U
        scale_purine = properties.scale_purine
        scale_pyrimidine = properties.scale_pyrimidine
        height_purine = properties.height_purine
        height_pyrimidine = properties.height_pyrimidine
        
    else:
        color_A = [1,0,0]
        color_G = [0,0,1]
        color_T = [0,1,0]
        color_C = [1,1,0]
        color_U = [1,0.5,0]
        scale_purine = scale_pyrimidine = 1.3    
        height_purine = height_pyrimidine = 0.4
    for i in range(total_res):
        faces = []        
        NA_type = residues[i].type.strip()
        l_c = g.SS.exElt.getExtrudeProperties([residues[i]], 'colors', )
        if NA_type in ['A', 'G']:
            base_vertices, base_faces = make_purine(residues[i],
                                                     height_purine, scale_purine)
            pscale = scale_purine
            if NA_type == 'A':
                #28 = number of vertices for the base 20 + 8
                materials.extend(28*[color_A])
                residues[i]._coil_colors = len(l_c)*[color_A]
            elif NA_type == 'G':
                materials.extend(28*[color_G])
                residues[i]._coil_colors = len(l_c)*[color_G]
            connetct_to_base =  Numeric.array(residues[i].atoms.
                                              objectsFromString('N9')[0].coords)
        else:
            base_vertices, base_faces = make_pyrimidine(residues[i],
                                              height_pyrimidine, scale_pyrimidine)
            pscale = 0.9*scale_pyrimidine
            if NA_type == 'T':
                #22 = number of vertices for the base 14 + 8
                materials.extend(22*[color_T])
                residues[i]._coil_colors = len(l_c)*[color_T]                
            elif NA_type == 'C':
                materials.extend(22*[color_C])
                residues[i]._coil_colors = len(l_c)*[color_C]                
            elif NA_type == 'U':
                materials.extend(22*[color_U])
                residues[i]._coil_colors = len(l_c)*[color_U]                
            connetct_to_base =  Numeric.array(residues[i].atoms.
                                              objectsFromString('N1')[0].coords)
        vertices.extend(base_vertices.tolist())

        
        #           v5 *-----------*v1
        #             /|          /|
        #            / |         / |
        #           /  |        /  |       
        #        v6*-----------*v2 |       
        # path-----|-- |       | --|--->connetct_to_base
        #          |   *-------|---*v0
        #          |  /v4      |  / 
        #          | /         | /  
        #          |/          |/  
        #          *-----------*       
        #         v7          v3        
        
        O4 = Numeric.array(returnStarOrQuote(residues[i].atoms, 'O4')[0].coords)
        C4 = Numeric.array(returnStarOrQuote(residues[i].atoms, 'C4')[0].coords)
        
        C1 = Numeric.array(returnStarOrQuote(residues[i].atoms, 'C1')[0].coords)
        C3 = Numeric.array(returnStarOrQuote(residues[i].atoms, 'C3')[0].coords)
        C2 = Numeric.array(returnStarOrQuote(residues[i].atoms, 'C2')[0].coords)
        
        #cent is a vector towards which bases are extruded
        cent = C4 #this was a center of the sugar ring
                
        #copy is needed were, otherwise base_vertices will get changed too
        v_4 = copy(base_vertices[-4]); v_5 = copy(base_vertices[-3])
        v_6 = copy(base_vertices[-2]); v_7 = copy(base_vertices[-1])

        dist = (v_5+v_4+v_6+v_7)/4.0 - cent
        if i == total_res - 1:
            pathPoint = path3D[4*i]
        else:
            pathPoint = path3D[4*i+1]
        
        #here we measure distance between backbone and last 4 vertices of bases
        d_v = v_4 - pathPoint
        distToV_4 = Numeric.innerproduct(d_v,d_v)
        d_v = v_5 - pathPoint
        distToV_5 = Numeric.innerproduct(d_v,d_v)
        d_v = v_6 - pathPoint
        distToV_6 = Numeric.innerproduct(d_v,d_v)
        d_v = v_7 - pathPoint
        distToV_7 = Numeric.innerproduct(d_v,d_v)
        
        distList1 = [distToV_4,distToV_5,distToV_6,distToV_7]
        distList2 = [distToV_4,distToV_5,distToV_6,distToV_7]
        
        distList1.sort()
        if pscale > 1:
            pscale *= pscale
        
        for enum in enumerate(distList2):
            if enum[1] == distList1[0]:
                distList2[enum[0]] = 0.1*pscale
            elif enum[1] == distList1[1]:
                distList2[enum[0]] = 0.1*pscale
            elif enum[1] == distList1[2]:
                distList2[enum[0]] = 0.5*pscale
            elif enum[1] == distList1[3]:
                distList2[enum[0]] = 0.5*pscale

            
        #max_d = max([distToV_4,distToV_5,distToV_6,distToV_7])
        #dist needs to be scaled so that connection to the backbone wont be thin



        v_4 = v_4 - distList2[0]*dist
        vertices.append(v_4.tolist())

        v_5 = v_5 - distList2[1]*dist
        vertices.append(v_5.tolist())

        v_6 = v_6 - distList2[2]*dist
        vertices.append(v_6.tolist())

        v_7 = v_7 - distList2[3]*dist
        vertices.append(v_7.tolist())

        p_1 = copy(v_4)
        p_2 = copy(v_5)
        p_3 = copy(v_6)
        p_4 = copy(v_7)
        dToBase = (p_1+p_2+p_3+p_4)/4. - pathPoint
        
        p_1 = p_1 - dToBase
        p_2 = p_2 - dToBase
        p_3 = p_3 - dToBase
        p_4 = p_4 - dToBase
        
        #base_face are number from 0, we need to add vertex_count here
        
        base_faces += vertex_count
        faces.extend(base_faces.tolist())        
        
        #now do the faces
        len_base_vertices = len(base_vertices)
        stem_start = vertex_count + len_base_vertices - 4
        
        faces.append([stem_start + 1, stem_start + 5,stem_start + 4,stem_start,
                      stem_start,stem_start,stem_start])
        faces.append([stem_start+1, stem_start+2,stem_start + 6,stem_start + 5,
                      stem_start + 5,stem_start + 5,stem_start + 5])
        faces.append([stem_start, stem_start+4, stem_start + 7, stem_start + 3,
                      stem_start + 3,stem_start + 3,stem_start + 3])
        faces.append([stem_start+2, stem_start+3,stem_start + 7,stem_start + 6,
                      stem_start + 6,stem_start + 6,stem_start + 6])
        faces.append([stem_start+7, stem_start+4,stem_start + 5,stem_start + 6,
                      stem_start + 6,stem_start + 6,stem_start + 6])

        vertices.append(p_1.tolist())
        vertices.append(p_2.tolist())
        vertices.append(p_3.tolist())
        vertices.append(p_4.tolist())

        stem_start += 4
        
        faces.append([stem_start + 1, stem_start + 5,stem_start + 4,stem_start,
                      stem_start,stem_start,stem_start])
        faces.append([stem_start+1, stem_start+2,stem_start + 6,stem_start + 5,
                      stem_start + 5,stem_start + 5,stem_start + 5])
        faces.append([stem_start, stem_start+4, stem_start + 7, stem_start + 3,
                      stem_start + 3,stem_start + 3,stem_start + 3])
        faces.append([stem_start+2, stem_start+3,stem_start + 7,stem_start + 6,
                      stem_start + 6,stem_start + 6,stem_start + 6])
        faces.append([stem_start+7, stem_start+4,stem_start + 5,stem_start + 6,
                      stem_start + 6,stem_start + 6,stem_start + 6])
        
#        #1-2-6-5
#        faces.append([stem_start + 7, stem_start + 8,stem_start + 12,stem_start+11,
#                      stem_start+11,stem_start+11,stem_start+11])
#        #1-4-8-5
#        faces.append([stem_start+7, stem_start+10,stem_start + 14,stem_start + 11,
#                      stem_start + 11,stem_start + 11,stem_start + 11])
#        #3-4-8-7
#        faces.append([stem_start+9, stem_start+10, stem_start + 14, stem_start + 13,
#                      stem_start + 13,stem_start + 13,stem_start + 13])
#        #2-3-7-6
#        faces.append([stem_start+8, stem_start+9,stem_start + 13,stem_start + 12,
#                      stem_start + 12,stem_start + 12,stem_start + 12])

        vertex_count = vertex_count + len_base_vertices + 8
        residues[i]._base_faces = faces
        
    faces = []
    for residue in residues:
        faces.extend(residue._base_faces)
            
    geom_bases = IndexedPolygons('Bases', vertices=vertices, faces=faces, 
                                 inheritShading = False,shading = GL.GL_FLAT,
                                 materials = materials, inheritMaterial = False,)


    return geom_bases

def returnStarOrQuote(atoms, txt):
        atom = atoms.objectsFromString(txt+'\*')
        if not atom:
            atom = atoms.objectsFromString(txt+'\'')
        return atom

    
if __name__ == '__main__':
    from DejaVu import Viewer
    vi = Viewer()
    from DejaVu import NucleicBases
    b = NucleicBases.Pyrimidine_old('b')
    vi.AddObject(b)
    while(1):
        vi.update()
