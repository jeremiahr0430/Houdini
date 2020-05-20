from cachemanage import generateNode
reload(generateNode)
import hou

def run():
            
    null_node = generateNode.GenerateNode('null')
    null_node = null_node.generateNode()

    nullName = null_node.name()
    null_node.setName('OUT_to_{}'.format(nullName))
    nullName = null_node.name() # rehash name


    objMergePath = null_node.path()
    print "path to fill in on obj merge node created later is %s" % objMergePath


    # create render object and object merge

    renderObj = hou.node("/obj").createNode("geo","{}_render".format(nullName))
    renderObjPath = renderObj.path()

    objMerge = hou.node(renderObjPath).createNode("object_merge",nullName)

    # reset parm for created object merge node
    objMerge.parm("objpath1").set(objMergePath)

    objMerge.parm("xformtype").set(1)

    #select created render object
    renderObj.setCurrent(True) 


