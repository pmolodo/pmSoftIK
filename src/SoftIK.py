import sys
import math

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
        if plug in (self.constraintTranslate,
                    self.constraintTranslateX,
                    self.constraintTranslateY,
                    self.constraintTranslateZ):
            # First, get the softRatio...
            softRatio = dataBlock.inputValue(self.softRatio).asDouble()
            if softRatio == 0:
                return 
            
            # Compute start/target world positions
            startWorldPos = self._getWorldPos(self.startJointWorldMatrix,
                                         dataBlock)
            targetWorldPos= self._getWorldPos(self.targetWorldMatrix,
                                         dataBlock)
            targetDist = dist( startWorldPos, targetWorldPos )
            
            
            chainLength = dataBlock.inputValue(self.chainLength).asDistance().value()
            if softRatio == 0:
                finalDistance = chainLength
            else:
                softDist = softRatio * chainLength
                hardDist = chainLength - softDist
                finalDistance = self._getFinalDist(targetDist, softDist, hardDist)
            finalRatio = finalDistance / targetDistance
            
            finalWorldPos = []
            for startCoord, targetCoord in zip(startWorldPos, targetWorldPos):
                finalWorldPos.append( (1 - finalRatio) * startCoord +
                                      finalRatio * targetCoord          )
        else:
            return om.kUnknownParameter
        
    def _getWorldPos(self, worldMatrixPlug, dataBlock):
        if worldMatrixPlug == self.startJointWorldMatrix:
            return (0, 0, 0)
        return (10, 0, 0)

    def _getDistanceRatio(self, dataBlock):
        
        
    
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
        numAttr.setKeyable(1)
        
        # startJointWorldMatrix
        typedAttr = om.MFnTypedAttribute()
        cls.startJointWorldMatrix = \
            typedAttr.create("startJointWorldMatrix", "sjwm",
                             om.MFnData.kMatrix)
        cls.addAttribute(cls.startJointWorldMatrix)
        
        # targetWorldMatrix
        typedAttr = om.MFnTypedAttribute()
        cls.targetWorldMatrix = \
            typedAttr.create("targetWorldMatrix", "twm",
                             om.MFnData.kMatrix)
        cls.addAttribute(cls.targetWorldMatrix)
        
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
        
        for inAttr in (cls.chainLength,
                       cls.startJointWorldMatrix,
                       cls.targetWorldMatrix,
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
    
    
#==============================================================================
# Utility Functions
#==============================================================================
def dist(pt1, pt2):
    sum = 0
    for v1, v2 in zip(pt1, pt2):
        sum += ((v1-v2)**2) 
    return math.sqrt(sum)