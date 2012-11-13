This code is totally unsupported and provided as is.  It wasn't even really
intended for public consumption - it was a small test I made on my own that I
hosted on github as an easy way to coordinate work at home and at school.

However, it seems that a few people have stumbled across this and asked how to
use it, so I decided to provide a basic example showing how to use it.  If you
don't know basic scripting, or can't follow the example, then move on... this
is NOT a complete end-user package.  (There's no command to create/setup a
SoftIk constraint... though you could easily make one from the provided
example...)

First, you'll need to install this script somewhere in your Maya plugin path.
Look at the official maya docs if you need help doing this.

Then, try running this code in a python script editor::

    import pymel.core as pm
    pm.newFile(f=1)
    j1 = pm.joint( p=(0, 0, 0) )
    j2 = pm.joint( p=(4, 0, 0)  )
    j3 = pm.joint( p=(4, 0, 4)  )
    ikHandle = pm.ikHandle( sj=j1, ee=j3)[0]
    handleParent = pm.group()
    cube = pm.polyCube()[0]
    cube.translate.set(4,0,4)

    softConstraint = pm.createNode('pmSoftIkConstraint')

    # This bit is a bit of hack... really, I should have a command that computes this distance,
    # or have the node itself dynamically figure it out.  I don't though. You'll have to figure
    # out the total joint chain length yourself...
    softConstraint.chainLength.set(8)


    j1.worldMatrix[0].connect(softConstraint.startJointWorldMatrix)
    cube.worldMatrix[0].connect(softConstraint.targetWorldMatrix)
    handleParent.parentInverseMatrix[0].connect(softConstraint.constraintParentInverseMatrix)
    softConstraint.constraintTranslateX.connect(ikHandle.translateX)
    softConstraint.constraintTranslateY.connect(ikHandle.translateY)
    softConstraint.constraintTranslateZ.connect(ikHandle.translateZ)

    cube.addAttr('softIkRatio', keyable=True, hidden=False)
    cube.softIkRatio.connect(softConstraint.softRatio)
    cube.softIkRatio.set(.2)

Now, just move the cube around, and see how the ik handle / joint chain responds.
Also, try changing the softIkRatio on the cube to see how it affects the behavior...