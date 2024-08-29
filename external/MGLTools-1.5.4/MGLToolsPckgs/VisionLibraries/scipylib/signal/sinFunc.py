########################################################################
#
#    Vision Node - Python source code - file generated by vision
#    Wednesday 21 November 2007 11:50:30 
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
# $Header: /opt/cvs/VisionLibraries/scipylib/signal/sinFunc.py,v 1.1 2007/11/28 23:09:08 mgltools Exp $
#
# $Id: sinFunc.py,v 1.1 2007/11/28 23:09:08 mgltools Exp $
#

# import node's base class node
from NetworkEditor.items import NetworkNode
class sinFunc(NetworkNode):
    mRequiredTypes = {}
    mRequiredSynonyms = [
    ]
    def __init__(self, constrkw = {},  name='sinFunc', **kw):
        kw['constrkw'] = constrkw
        kw['name'] = name
        apply( NetworkNode.__init__, (self,), kw)
        code = """def doit(self, fs=10, num_samples=5, frequency=1, amplitude=1, phase=0):
    from scipy import pi, sin, arange
    x=arange(0,num_samples)/float(fs)
    y=sin(x*2*pi*frequency+phase)*amplitude
    self.outputData( x=x, y=y)
    return
"""
        self.configure(function=code)
        self.inputPortsDescr.append(
            {'singleConnection': True, 'name': 'fs', 'cast': True, 'datatype': 'float', 'balloon': 'sampling frequency', 'required': True, 'height': 12, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.inputPortsDescr.append(
            {'singleConnection': True, 'name': 'num_samples', 'cast': True, 'datatype': 'None', 'balloon': 'number of samples', 'required': True, 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.inputPortsDescr.append(
            {'singleConnection': True, 'name': 'frequency', 'cast': True, 'datatype': 'None', 'balloon': 'center frequency', 'required': True, 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.inputPortsDescr.append(
            {'singleConnection': True, 'name': 'amplitude', 'cast': True, 'datatype': 'None', 'balloon': 'amplitude', 'required': True, 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.inputPortsDescr.append(
            {'singleConnection': True, 'name': 'phase', 'cast': True, 'datatype': 'None', 'balloon': 'phase', 'required': True, 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.outputPortsDescr.append(
            {'name': 'x', 'datatype': 'None', 'balloon': 'ordinate', 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.outputPortsDescr.append(
            {'name': 'y', 'datatype': 'None', 'balloon': 'abscissa', 'height': 8, 'width': 12, 'shape': 'diamond', 'color': 'white'})
        self.widgetDescr['fs'] = {
            'initialValue': 100.0, 'labelGridCfg': {'column': 0, 'row': 1}, 'width': 75, 'height':21, 'master': 'node', 'widgetGridCfg': {'column': 1, 'labelSide': 'left', 'row': 1}, 'labelCfg': {'text': 'fs'}, 'class': 'NEThumbWheel', 'oneTurn': 10.0}
        self.widgetDescr['num_samples'] = {
            'initialValue': 100.0, 'labelGridCfg': {'column': 0, 'row': 2}, 'width': 75, 'height':21,'master': 'node', 'widgetGridCfg': {'column': 1, 'labelSide': 'left', 'row': 2}, 'labelCfg': {'text': 'num_samples'}, 'class': 'NEThumbWheel', 'oneTurn': 10.0,'min':1}
        self.widgetDescr['frequency'] = {
            'initialValue': 1.0, 'labelGridCfg': {'column': 0, 'row': 3}, 'width': 75, 'height':21,'master': 'node', 'widgetGridCfg': {'column': 1, 'labelSide': 'left', 'row': 3}, 'labelCfg': {'text': 'frequency'}, 'class': 'NEThumbWheel', 'oneTurn': 10.0}
        self.widgetDescr['amplitude'] = {
            'initialValue': 1.0, 'labelGridCfg': {'column': 0, 'row': 4}, 'width': 75, 'height':21,'master': 'node', 'widgetGridCfg': {'column': 1, 'labelSide': 'left', 'row': 4}, 'labelCfg': {'text': 'amplitude'}, 'class': 'NEThumbWheel', 'oneTurn': 10.0}
        self.widgetDescr['phase'] = {
            'initialValue': 0.0, 'labelGridCfg': {'column': 0, 'row': 5}, 'width': 75, 'height':21,'master': 'node', 'widgetGridCfg': {'column': 1, 'labelSide': 'left', 'row': 5}, 'labelCfg': {'text': 'phase'}, 'class': 'NEThumbWheel', 'oneTurn': 10.0}


    def beforeAddingToNetwork(self, net):
        try:
            ed = net.getEditor()
        except:
            import traceback; traceback.print_exc()
            print 'Warning! Could not import widgets'

