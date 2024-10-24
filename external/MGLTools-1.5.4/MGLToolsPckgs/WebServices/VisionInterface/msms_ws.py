########################################################################
#
#    Vision Macro - Python source code - file generated by vision
#    Monday 16 January 2006 12:29:40 
#    
#       The Scripps Research Institute (TSRI)
#       Molecular Graphics Lab
#       La Jolla, CA 92037, USA
#
# Copyright: Daniel Stoffler, Michel Sanner and TSRI
#   
# revision: Guillaume Vareille
#  
#########################################################################
#
# $Header$
#
# $Id$
#

from NetworkEditor.macros import MacroNode
class msms_wsMacroNode(MacroNode):
    """Macro Node for MSMS Web Services
Input Ports
    Assign Radii_molecules: MoleculeSet object for which to calculate molecular surface
Output Ports
    IndexedPolygons_indexedPolygons: geom object that represents molecular surface
"""    

    def __init__(self, name='WebMSMS', host = None, **kw):
        kw['name'] = name
        apply( MacroNode.__init__, (self,), kw)
        self.host = self.constrkw['host'] = `host`
        from WebServices.VisionInterface.WSNodes import OpalService
        self.opal_service = OpalService(self.host)

    def beforeAddingToNetwork(self, net):
        MacroNode.beforeAddingToNetwork(self, net)
        ## loading libraries ##
        from MolKit.VisionInterface.MolKitNodes import molkitlib
        net.editor.addLibraryInstance(molkitlib,"MolKit.VisionInterface.MolKitNodes", "molkitlib")

        from DejaVu.VisionInterface.DejaVuNodes import vizlib
        net.editor.addLibraryInstance(vizlib,"DejaVu.VisionInterface.DejaVuNodes", "vizlib")

        from Vision.StandardNodes import stdlib
        net.editor.addLibraryInstance(stdlib,"Vision.StandardNodes", "stdlib")
        
        if self.library and not self.library.libraryDescr.has_key(self.host[1:-1]):
            from WebServices.VisionInterface.WSNodes import addreplaceCategory
            addreplaceCategory(self.host[1:-1])  

    def afterAddingToNetwork(self):
        from NetworkEditor.macros import MacroNode
        MacroNode.afterAddingToNetwork(self)
        ## loading libraries ##
        from MolKit.VisionInterface.MolKitNodes import molkitlib
        from DejaVu.VisionInterface.DejaVuNodes import vizlib
        from Vision.StandardNodes import stdlib
        ## building macro network ##
        WebMSMS = self
        from traceback import print_exc

        ## loading libraries ##
        from MolKit.VisionInterface.MolKitNodes import molkitlib
        self.macroNetwork.getEditor().addLibraryInstance(molkitlib,"MolKit.VisionInterface.MolKitNodes", "molkitlib")

        from DejaVu.VisionInterface.DejaVuNodes import vizlib
        self.macroNetwork.getEditor().addLibraryInstance(vizlib,"DejaVu.VisionInterface.DejaVuNodes", "vizlib")

        from Vision.StandardNodes import stdlib
        self.macroNetwork.getEditor().addLibraryInstance(stdlib,"Vision.StandardNodes", "stdlib")

        try:

            ## saving node input Ports ##
            input_Ports = self.macroNetwork.ipNode
            input_Ports.move(13, 4)
        except:
            print "WARNING: failed to restore MacroInputNode named input Ports in network self.macroNetwork"
            print_exc()
            input_Ports=None
        try:

            ## saving node output Ports ##
            output_Ports = self.macroNetwork.opNode
            output_Ports.move(256, 220)
        except:
            print "WARNING: failed to restore MacroOutputNode named output Ports in network self.macroNetwork"
            print_exc()
            output_Ports=None
        try:

            ## saving node Assign Radii ##
            from MolKit.VisionInterface.MolKitNodes import AssignRadii
            Assign_Radii = AssignRadii(constrkw = {}, name='Assign Radii', library=molkitlib)
            self.macroNetwork.addNode(Assign_Radii,30,68)
            apply(Assign_Radii.getInputPortByName('molecules').configure, (), {'color': '#c64e70', 'cast': True, 'shape': 'oval'})
            apply(Assign_Radii.getInputPortByName('united').configure, (), {'color': 'yellow', 'cast': True, 'shape': 'circle'})
            apply(Assign_Radii.getOutputPortByName('molecules').configure, (), {'color': '#c64e70', 'shape': 'oval'})
            apply(Assign_Radii.getOutputPortByName('radii').configure, (), {'color': 'cyan', 'shape': 'oval'})
        except:
            print "WARNING: failed to restore AssignRadii named Assign Radii in network self.macroNetwork"
            print_exc()
            Assign_Radii=None
        try:

            ## saving node Select Nodes ##
            from MolKit.VisionInterface.MolKitNodes import NodeSelector
            Select_Nodes = NodeSelector(constrkw = {}, name='Select Nodes', library=molkitlib)
            self.macroNetwork.addNode(Select_Nodes,29,135)
            apply(Select_Nodes.getInputPortByName('nodes').configure, (), {'color': '#c64e70', 'cast': True, 'shape': 'oval'})
            apply(Select_Nodes.getInputPortByName('nodeType').configure, (), {'color': 'white', 'cast': True, 'shape': 'oval'})
            apply(Select_Nodes.getInputPortByName('selectionString').configure, (), {'color': 'white', 'cast': True, 'shape': 'oval'})
            apply(Select_Nodes.getOutputPortByName('nodes').configure, (), {'color': '#fe92a0', 'shape': 'oval'})
            Select_Nodes.getInputPortByName("selectionString").widget.set(".*")
        except:
            print "WARNING: failed to restore NodeSelector named Select Nodes in network self.macroNetwork"
            print_exc()
            Select_Nodes=None
        try:

            ## saving node Get xyzr ##
            from Vision.StandardNodes import Generic
            Get_xyzr = Generic(constrkw = {}, name='Get xyzr', library=stdlib)
            self.macroNetwork.addNode(Get_xyzr,30,194)
            apply(Get_xyzr.addInputPort, (), {'name': 'atoms', 'cast': True, 'datatype': 'AtomSet', 'height': 8, 'width': 12, 'shape': 'oval', 'color': '#fe92a0'})
            apply(Get_xyzr.addOutputPort, (), {'name': 'output', 'datatype': 'string', 'height': 12, 'width': 12, 'shape': 'oval', 'color': 'white'})
            code = """def doit(self, atoms):
    lines = ''
    for atom in atoms:
        lines += str(atom.coords[0]) + ' ' + str(atom.coords[1]) + ' ' + str(atom.coords[2]) + ' '+ str(atom.radius)
        lines += "\\n"
    self.outputData(output=lines)
"""

            Get_xyzr.configure(function=code)
        except:
            print "WARNING: failed to restore Generic named Get xyzr in network self.macroNetwork"
            print_exc()
            Get_xyzr=None
        try:

            ## saving node IndexedPolygons ##
            from DejaVu.VisionInterface.GeometryNode import IndexedPolygonsNE
            IndexedPolygons = IndexedPolygonsNE(constrkw = {}, name='IndexedPolygons', library=vizlib)
            self.macroNetwork.addNode(IndexedPolygons,273,147)
            apply(IndexedPolygons.getInputPortByName('coords').configure, (), {'color': 'purple', 'cast': True, 'shape': 'circle'})
            apply(IndexedPolygons.getInputPortByName('indices').configure, (), {'color': 'yellow', 'cast': True, 'shape': 'circle'})
            apply(IndexedPolygons.getInputPortByName('vnormals').configure, (), {'cast': True, 'shape': 'circle'})
            apply(IndexedPolygons.getInputPortByName('colors').configure, (), {'cast': True, 'shape': 'circle'})
            apply(IndexedPolygons.getInputPortByName('name').configure, (), {'color': 'white', 'cast': True, 'shape': 'oval'})
            apply(IndexedPolygons.getInputPortByName('instanceMatrices').configure, (), {'cast': True})
            apply(IndexedPolygons.getInputPortByName('geomOptions').configure, (), {'color': 'cyan', 'cast': True, 'shape': 'oval'})
            apply(IndexedPolygons.getInputPortByName('parent').configure, (), {'color': 'red', 'cast': True, 'shape': 'rect'})
            apply(IndexedPolygons.getOutputPortByName('indexedPolygons').configure, (), {'color': 'red', 'shape': 'rect'})
            apply(IndexedPolygons.getOutputPortByName('allGeometries').configure, (), {'color': 'red', 'shape': 'rect'})
        except:
            print "WARNING: failed to restore IndexedPolygonsNE named IndexedPolygons in network self.macroNetwork"
            print_exc()
            IndexedPolygons=None
        try:

            ## saving node MSMS WS ##
            from Vision.StandardNodes import Generic
            MSMS_WS = Generic(constrkw = {}, name='MSMS WS', library=stdlib)            

            self.macroNetwork.addNode(MSMS_WS,273,37)
            apply(MSMS_WS.addInputPort, (), {'name': 'input_str', 'cast': True, 
                   'datatype': 'string', 'height': 12, 'width': 12, 'shape': 'oval', 'color': 'white'})
            apply(MSMS_WS.addInputPort, (), {'name': 'density', 'datatype': 'float', 'required':False})
            apply(MSMS_WS.getInputPortByName('density').createWidget, (), 
                   {'descr':{'initialValue': 1.0, 'increment':0.1, 'type':'float', 
                     'master': 'ParamPanel', 'oneTurn':10, 'min':1.0, 'labelCfg': {'text': 'density'}, 'class': 'NEDial'}})
            apply(MSMS_WS.addInputPort, (), {'name': 'probe_radius', 'datatype': 'float', 'required':False})
            apply(MSMS_WS.getInputPortByName('probe_radius').createWidget, (), 
                   {'descr':{'initialValue': 1.5, 'increment':0.1, 'type':'float', 
                     'master': 'ParamPanel', 'oneTurn':10, 'min':0.5, 'labelCfg': {'text': 'probe radius'}, 'class': 'NEDial'}})
            apply(MSMS_WS.addInputPort, (), {'name': 'allComp', 'datatype': 'int', 'required':False})
            apply(MSMS_WS.getInputPortByName('allComp').createWidget, (), 
                   {'descr':{'initialValue': 0, 'master': 'ParamPanel', 'labelCfg': 
                       {'text': 'all components'}, 'class': 'NECheckButton'}})
            apply(MSMS_WS.addInputPort, (), {'name': 'getfile', 'datatype': 'boolean'})
            apply(MSMS_WS.getInputPortByName('getfile').createWidget, (), 
                   {'descr':{'master': 'ParamPanel', 'labelCfg': {'text': 'upload output'}, 'class': 'NECheckButton', 'initialValue':True }})


            apply(MSMS_WS.addOutputPort, (), {'name': 'vertices', 'datatype': 'coordinates3D', 'height': 8, 'width': 12, 'shape': 'rect', 'color': 'green'})
            apply(MSMS_WS.addOutputPort, (), {'name': 'indices', 'datatype': 'faceIndices', 'height': 8, 'width': 12, 'shape': 'rect', 'color': 'purple'})
            apply(MSMS_WS.addOutputPort, (), {'name': 'vnormals', 'datatype': 'normals3D', 'height': 8, 'width': 12, 'shape': 'rect', 'color': 'blue'})
            MSMS_WS.host = self.host
            MSMS_WS.opal_service = self.opal_service
            
            code = """def doit(self, input_str, probe_radius, density, allComp, getfile = True):
    self.opal_service.inputFile.Set_name('msms.xyzr')
    self.opal_service.inputFile.Set_contents(input_str)
    options = '-if msms.xyzr -of ws_out '
    options += '-probe_radius ' + str(probe_radius)
    options += ' -density ' + str(density)
    if allComp:
        options += ' -all_components'
    self.opal_service.req._argList = options
    inputFiles = []
    inputFiles.append(self.opal_service.inputFile)
    self.opal_service.req._inputFile = inputFiles
    resp = self.opal_service.run('msmsServicePort')
    if resp:
        for files in resp._outputFile:
            if files._url.split('/')[-1] == 'ws_out.face':
                face_file = files._url
            if files._url.split('/')[-1] == 'ws_out.vert':
                vert_file = files._url
        if getfile:           
            from Pmv.msmsParser import MSMSParser
            msmsParser = MSMSParser()
            import urllib
            opener = urllib.FancyURLopener({})
            in_file = opener.open(face_file)
            msmsParser.getFaces(in_file.readlines())
            in_file = opener.open(vert_file)
            msmsParser.getVert(in_file.readlines())
            self.outputData(vertices = msmsParser.vertices, indices = msmsParser.faces,
                          vnormals = msmsParser.normals)
        else:
            self.outputData(vertices = vert_file, indices = face_file,
                          vnormals = None)
"""
            MSMS_WS.configure(function=code)
        except:
            print "WARNING: failed to restore Generic named MSMS WS in network self.macroNetwork"
            print_exc()
            MSMS_WS=None
        self.macroNetwork.freeze()

        ## saving connections for network WebMSMS ##
        if Assign_Radii is not None and Select_Nodes is not None:
            self.macroNetwork.connectNodes(
                Assign_Radii, Select_Nodes, "molecules", "nodes", blocking=True)
        if Select_Nodes is not None and Get_xyzr is not None:
            self.macroNetwork.connectNodes(
                Select_Nodes, Get_xyzr, "nodes", "atoms", blocking=True)
        if Get_xyzr is not None and MSMS_WS is not None:
            self.macroNetwork.connectNodes(
                Get_xyzr, MSMS_WS, "output", "input_str", blocking=True)
        if MSMS_WS is not None and IndexedPolygons is not None:
            self.macroNetwork.connectNodes(
                MSMS_WS, IndexedPolygons, "vertices", "coords", blocking=True)
        if MSMS_WS is not None and IndexedPolygons is not None:
            self.macroNetwork.connectNodes(
                MSMS_WS, IndexedPolygons, "indices", "indices", blocking=True)
        if MSMS_WS is not None and IndexedPolygons is not None:
            self.macroNetwork.connectNodes(
                MSMS_WS, IndexedPolygons, "vnormals", "vnormals", blocking=True)
        output_Ports = self.macroNetwork.opNode
        if IndexedPolygons is not None and output_Ports is not None:
            self.macroNetwork.connectNodes(
                IndexedPolygons, output_Ports, "indexedPolygons", "new", blocking=True)
        input_Ports = self.macroNetwork.ipNode
        if input_Ports is not None and Assign_Radii is not None:
            self.macroNetwork.connectNodes(
                input_Ports, Assign_Radii, "new", "molecules", blocking=True)
        self.macroNetwork.unfreeze()

        WebMSMS.shrink()

        ## reset modifications ##
        WebMSMS.resetTags()
        WebMSMS.buildOriginalList()
