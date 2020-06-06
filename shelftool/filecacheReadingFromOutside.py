# find the filecache that reads cache from files that is outside of $HIP
import hou
selNodes = hou.selectedNodes()

nodeList = []
sceneFilePath = hou.hipFile.path()
node = selNodes[0]
if 'Sop' in node.type().nameWithCategory():
    obj = node.node("..")
    
    print 'the sop is in {}'.format(obj)
    # all sops for the foreach loop
    children = obj.children()

    for index,kid in enumerate(children):
        if 'filecache'in kid.type().nameWithCategory():
            path = kid.parm("file").eval()
#            print "file path is {}".format(path)
            # this is wrong. $HIP won't exist because it's evalued 
            if '$HIP' not in path: 
                pathSplit = path.split("/geo")
#                print "first half of the path is {}".format(pathSplit[0])
                if pathSplit[0] not in sceneFilePath:
                    nodeList.append(kid.name())
                    
print "Qualified filecache nodes are below:"
for node in nodeList:
    print node
