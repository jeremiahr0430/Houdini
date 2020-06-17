
# findFileCache.py  This is for create file path dictionary
import hou



# Check if in sop level
def filePathDict(node,createObjMerge=0):
    
    filePathDict = {} #create empty dictionary
    print '\n'*4+'updated!!!!!!!!!!!!!!!'
    if 'Sop' in node.type().nameWithCategory():
        obj = node.node("..")
        
        print 'the sop is in {}'.format(obj)
        # all sops for the foreach loop
        children = obj.children()
        
        filenodes = []
        pathList = ''
        pos = node.position()
        print '\n'*2+'Results are blow!!!!!!!!!!!!!\n'
        commonPath = ''
        for index,kid in enumerate(children):
            if 'filecache'in kid.type().nameWithCategory():
                kidName = kid.name()
                filenodes.append(kidName)
                
                path = kid.parm('file').eval()
                pathList += path+'\n'

                filePathDict.update({kidName:path})
                # Output info to python shell
                print 'filecache {} is {}.\nThe path is {}\n'.format(index,kidName,path)
                
                if createObjMerge:
                    # objmerge to track down all filecache nodes
                    objmerge= obj.createNode("object_merge",kidName)
                    objmerge.parm("objpath1").set(kid.path())
                    # set pos
                    objmergePos = [pos[0],pos[1]]
                    objmergePos[0]-=20
                    objmerge.setPosition(objmergePos)
                    objmerge.moveToGoodPosition()
                    #select last objmerge
                    objmerge.setCurrent(True,True)
                    
                    
                
            
            
    print filenodes,'\n',pathList       
    return filePathDict  


