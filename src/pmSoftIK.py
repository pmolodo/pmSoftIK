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
        outputAttrs = (self.constraintTranslate,
                       self.constraintTranslateX,
                       self.constraintTranslateY,
                       self.constraintTranslateZ)
        if plug in outputAttrs:
            # First, check that we have sufficient information / connections
            useDefaults = False
            matrices = {'start':self.startJointWorldMatrix,
                        'target':self.targetWorldMatrix,
                        'inverse':self.constraintParentInverseMatrix}
            for matrixType, attr in matrices.iteritems():
                data = dataBlock.inputValue(attr).data()
                if data.isNull():
                    useDefaults = True
                    break
                matrices[matrixType] = om.MFnMatrixData(data)
            
            if useDefaults:
                localPos = om.MPoint()
            else:
                # Compute start/target world positions
                startWorldPos = om.MPoint() * matrices['start'].matrix()
                targetWorldPos = om.MPoint() * matrices['target'].matrix()
                targetDist = startWorldPos.distanceTo(targetWorldPos)
                
                chainLength = dataBlock.inputValue(self.chainLength).asDistance().value()
                softRatio = dataBlock.inputValue(self.softRatio).asDouble()
                if softRatio == 0:
                    finalRatio = 1.0
                else:
                    softDist = softRatio * chainLength
                    hardDist = chainLength - softDist
                    finalDistance = self._getFinalDist(targetDist, softDist, hardDist)
                    finalRatio = finalDistance / targetDist
                
                # Yay API - we can only add an MVector to an MPoint
                finalWorldPos = (        (startWorldPos  * (1.0 - finalRatio)) + 
                                  om.MVector(targetWorldPos * finalRatio))
                localPos = finalWorldPos * matrices['inverse'].matrix()
                
            for dir in 'XYZ':
                attr = getattr(self, 'constraintTranslate' + dir)
                outHandle = dataBlock.outputValue(attr)
                outHandle.setMDistance(om.MDistance(getattr(localPos, dir.lower())))
                dataBlock.setClean(attr)
            dataBlock.setClean(self.constraintTranslate)
        else:
            return om.kUnknownParameter


    def _getFinalDist(self, x, softDist, hardDist):
        if x <= hardDist:
            return x
        
        # from  http://www.xsi-blog.com/userContent/anicholas/softik/Equation.gif
        # ...
        #                     hardDist - x
        #                     ------------
        #                        softDist
        #  softDist * ( 1 - e              ) + hardDist
        
        return softDist * (1 - math.exp( (hardDist - x) / softDist )) + hardDist
    
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
                                       om.MFnNumericData.kDouble, .1)
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
                       cls.softRatio,
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
