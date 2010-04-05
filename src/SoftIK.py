import sys

import maya.OpenMaya as om
import maya.OpenMayaMPx as omx
#import maya.OpenMayaAnim as oma

#nodeName = "pmSoftIkNode"
nodeName = "pmSoftIkConstraint"
nodeId = om.MTypeId(0x88320)

#class SoftIkConstraint(omx.MPxNode):
class SoftIkConstraint(omx.MPxConstraint):
    def __init__(self):
        super(SoftIkConstraint, self).__init__()
    
    # TODO: comp
    def compute(self, plug, dataBlock):
        print "compute called on:", plug.name()
        if plug in (self.constraintTranslate,
                    self.constraintTranslateX,
                    self.constraintTranslateY,
                    self.constraintTranslateZ):
            pass
        else:
            return om.kUnknownParameter
    
    @classmethod
    def creator(cls):
        return omx.asMPxPtr( cls() )

    @classmethod
    def initialize(cls):
        # chainLength
        unitAttr = om.MFnUnitAttribute()
        cls.chainLength = unitAttr.create("chainLength", "cl",
                                              om.MFnUnitAttribute.kDistance, 0)
        cls.addAttribute(cls.chainLength)
        unitAttr.setKeyable(1)
        
        # softRatio
        numAttr = om.MFnNumericAttribute()
        cls.softRatio = numAttr.create("softRatio", "sr",
                                       om.MFnNumericData.kDouble, .05)
        cls.addAttribute(cls.softRatio)
        unitAttr.setKeyable(1)
        
        # startJointWorldMatrix
        typedAttr = om.MFnTypedAttribute()
        cls.startJointWorldMatrix = \
            typedAttr.create("startJointWorldMatrix", "sjwm",
                             om.MFnData.kMatrix)
        cls.addAttribute(cls.startJointWorldMatrix)
        
        # constraintParentInverseMatrix
        typedAttr = om.MFnTypedAttribute()
        cls.constraintParentInverseMatrix = \
            typedAttr.create("constraintParentInverseMatrix", "cpim",
                             om.MFnData.kMatrix)   
        typedAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)
        cls.addAttribute(cls.constraintParentInverseMatrix)
        
        # constraintTranslate
        unitAttr = om.MFnUnitAttribute()
        cls.constraintTranslateX = \
            unitAttr.create("constraintTranslateX", "ctx",
                            om.MFnUnitAttribute.kDistance, 0)
        unitAttr.setWritable(0)
        unitAttr = om.MFnUnitAttribute()
        cls.constraintTranslateY = \
            unitAttr.create("constraintTranslateY", "cty",
                            om.MFnUnitAttribute.kDistance, 0)
        unitAttr.setWritable(0)
        unitAttr = om.MFnUnitAttribute()
        cls.constraintTranslateZ = \
            unitAttr.create("constraintTranslateZ", "ctz",
                            om.MFnUnitAttribute.kDistance, 0)
        unitAttr.setWritable(0)
        numAttr = om.MFnNumericAttribute()
        cls.constraintTranslate = \
            numAttr.create("constraintTranslate", "ct",
                           cls.constraintTranslateX,
                           cls.constraintTranslateY,
                           cls.constraintTranslateZ)
        cls.addAttribute(cls.constraintTranslate)
        numAttr.setWritable(0)
        
        for inAttr in (cls.chainLength, cls.startJointWorldMatrix,
                       cls.constraintParentInverseMatrix):
            for outAttr in (cls.constraintTranslate,):
                cls.attributeAffects(inAttr, outAttr)


# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = omx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( nodeName, nodeId, SoftIkConstraint.creator,
                              SoftIkConstraint.initialize )
    except:
        sys.stderr.write( "Failed to register node: %s" % nodeName )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = omx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( nodeId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % nodeName )
        raise