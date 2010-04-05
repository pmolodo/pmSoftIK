import maya.OpenMaya as om
import maya.OpenMayaMPx as omx
#import maya.OpenMayaAnim as oma

#nodeName = "pmSoftIkNode"
nodeName = "pmSoftIkConstraint"
nodeId = om.MTypeId(0x88320)

#class SoftIkConstraint(omx.MPxNode):
class SoftIkConstraint(omx.MPxConstraint):
    #endJointAttr = None
    chainLength = None
    startJointWorldMatrix = None
    constraintParentInverseMatrix = None
    #constraintRotatePivot = None
    #constraintRotatePivotTranslate = None
    constraintTranslateX = None
    constraintTranslateY = None
    constraintTranslateZ = None
    constraintTranslate = None
     
    
    def __init__(self):
        super(SoftIkConstraint, self).__init__()
    
    # TODO: comp
    def compute(self, plug, dataBlock):
        print "compute called on:", plug.name()
        
        if plug == self.test2:
            pass
#            dataHandle = dataBlock.inputValue( self.test1 )
#            distance = dataHandle.asDistance()
#            distance.setValue(distance.value() + 1)
#            outputHandle = dataBlock.outputValue( self.test2 )
#            outputHandle.setMDistance( distance )
#            dataBlock.setClean( plug )
        else:
            return om.kUnknownParameter
    
    @classmethod
    def creator(cls):
        return omx.asMPxPtr( cls() )

    @classmethod
    def initialize(cls):
        # test1
        unitAttr = om.MFnUnitAttribute()
        cls.test1 = unitAttr.create("test1", "t1",
                                              om.MFnUnitAttribute.kDistance, 0)
        cls.addAttribute(cls.test1)
        unitAttr.setKeyable(1)
        unitAttr.setStorable(1)

        unitAttr = om.MFnUnitAttribute()
        cls.test2 = unitAttr.create("test2", "t2",
                                              om.MFnUnitAttribute.kDistance, 0)
        cls.addAttribute(cls.test2)
        unitAttr.setStorable(1)
        unitAttr.setWritable(1)
        
        unitAttr = om.MFnUnitAttribute()
        cls.test3 = unitAttr.create("test3", "t3",
                                              om.MFnUnitAttribute.kDistance, 0)
        cls.addAttribute(cls.test3)

        cls.attributeAffects(cls.test1, cls.test2)
        cls.attributeAffects(cls.test2, cls.test3)
        
        
#        # chainLength
#        unitAttr = om.MFnUnitAttribute()
#        cls.chainLength = unitAttr.create("chainLength", "cl",
#                                              om.MFnUnitAttribute.kDistance, 0)
#        cls.addAttribute(cls.chainLength)
#        unitAttr.setKeyable(1)
#        
#        # startJointWorldMatrix
#        typedAttr = om.MFnTypedAttribute()
#        cls.startJointWorldMatrix = \
#            typedAttr.create("startJointWorldMatrix", "sjwm",
#                             om.MFnData.kMatrix)
#        cls.addAttribute(cls.startJointWorldMatrix)
#        
#        # constraintParentInverseMatrix
#        typedAttr = om.MFnTypedAttribute()
#        cls.constraintParentInverseMatrix = \
#            typedAttr.create("constraintParentInverseMatrix", "cpim",
#                             om.MFnData.kMatrix)   
#        typedAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)
#        cls.addAttribute(cls.constraintParentInverseMatrix)
#        
#        # constraintTranslate
#        unitAttr = om.MFnUnitAttribute()
#        cls.constraintTranslateX = \
#            unitAttr.create("constraintTranslateX", "ctx",
#                            om.MFnUnitAttribute.kDistance, 0)
#        unitAttr.setWritable(0)
#        unitAttr = om.MFnUnitAttribute()
#        cls.constraintTranslateY = \
#            unitAttr.create("constraintTranslateY", "cty",
#                            om.MFnUnitAttribute.kDistance, 0)
#        unitAttr.setWritable(0)
#        unitAttr = om.MFnUnitAttribute()
#        cls.constraintTranslateZ = \
#            unitAttr.create("constraintTranslateZ", "ctz",
#                            om.MFnUnitAttribute.kDistance, 0)
#        unitAttr.setWritable(0)
#        numAttr = om.MFnNumericAttribute()
#        cls.constraintTranslate = \
#            numAttr.create("constraintTranslate", "ct",
#                           cls.constraintTranslateX,
#                           cls.constraintTranslateY,
#                           cls.constraintTranslateZ)
#        cls.addAttribute(cls.constraintTranslate)
#        numAttr.setWritable(0)
#        
#        for inAttr in (cls.chainLength, cls.startJointWorldMatrix,
#                       cls.constraintParentInverseMatrix):
#            for outAttr in (cls.constraintTranslate,):
#                cls.attributeAffects(inAttr, outAttr)
#        for inAttr in (cls.chainLength, cls.startJointWorldMatrix,
#                       cls.constraintParentInverseMatrix):
#            for outAttr in (cls.constraintTranslate,
#                            cls.constraintTranslateX,
#                            cls.constraintTranslateY,
#                            cls.constraintTranslateZ):
#                cls.attributeAffects(inAttr, outAttr)

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