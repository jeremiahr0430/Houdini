from cachemanage import generateNode
reload(generateNode)
import hou

def run():
    def finish_it(nullName,null_node,objMergeName):
        null_node.setName(nullName)
        nullName = null_node.name() # rehash name


        objMergePath = null_node.path()
        print "path to fill in on obj merge node created later is %s" % objMergePath


        # create render object and object merge

        renderObj = hou.node("/obj").createNode("geo","{}_render".format(objMergeName))
        renderObjPath = renderObj.path()

        objMerge = hou.node(renderObjPath).createNode("object_merge",objMergeName)

        # reset parm for created object merge node
        objMerge.parm("objpath1").set(objMergePath)

        objMerge.parm("xformtype").set(1)

        #select created render object
        renderObj.setCurrent(True) 
# Run Func Starts here !!!            
    null_node_class= generateNode.GenerateNode('null')
    print 'Before create node, userInput is {}'.format(null_node_class.userInput)
    null_node = null_node_class.generateNode()

    nullName = null_node_class.userInputString
    objMergeName = nullName
    nullName = 'OUT_to_{}'.format(nullName)
    
    nullParent = null_node.parent()

# check if name exists   
    existList = [kid for kid in nullParent.children() if kid.name() == nullName] 
    print 'Name clashing! the nodes are below: \n {}'.format(existList)
    if len(existList) >=1: 
        # Ask if still continue
        confirm = hou.ui.displayConfirmation('The is one object with the same name. Continue?', hou.severityType.Message, None, None,None,None, hou.confirmType.OverwriteFile)
        if confirm == True:
            increment = 0
            # Apend a digit to the null name
            while len(existList) >=1: 
                increment +=1
                nullName = "{}{}".format(nullName,increment)
                existList = [kid for kid in nullParent.children() if kid.name() == nullName] 
            finish_it(nullName,null_node,objMergeName)
        else:
            null_node.destroy()
    else:
        finish_it(nullName,null_node,objMergeName)
