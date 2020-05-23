import hou
from cachemanage import findMoveCache
reload(findMoveCache)

class GenerateNode:
    def __init__(self,type='filecache',connectNode = None, connect = 1, px=0,py=1,connectToDop = False):
        self.type = type
        self.connectNode = connectNode
        self.connect = connect
        self.px = px
        self.py = py
        self.connectToDop = connectToDop

# This is only works for filecache for now!!!
    def addParm(self,node=None,parm="cache_version",value = 1):
        #This is only work for adding parm to filecache node type
        if not node:    
            node = hou.selectedNodes()[0] #select the filecache just created
        #create parameters
        ptg = node.parmTemplateGroup()

        ## If node type is file cache
        # if self.type == "filecache": this is alternative. But this and below if statement is not needed, 
        #as the method is only running for filecache
        if 'filecache'in node.type().nameWithCategory():
            target = ptg.findIndicesForFolder("Save to File") # find Save to File folder
            houParmTmp = hou.IntParmTemplate(parm, 'Version', 1)

##############        houParmTmp.setJoinWithNext(True)
            ptg.appendToFolder(target,houParmTmp)
            node.setParmTemplateGroup(ptg)
            #set default value
            node.parm(parm).set(value)
        return parm
## For later, add arbitrary parm to arbitrary filetype 
        #if ptg.findFolder("Extras") == None:
        #    parm_folder = hou.FolderParmTemplate("extras", "Extras")
        #    parm_folder.addParmTemplate(hou.IntParmTemplate("cache_version", 'Version', 1))
        #    ptg.append(parm_folder)
        #    node.setParmTemplateGroup(ptg)
        #else:
        #    print "The folder 'Extras' exists!"

    def generateNode(self):
        if not self.connectNode:    
            selnode = hou.selectedNodes()[0]
        else:
            selnode = self.connectNode
        parent  = selnode.parent()
            # Get position from selected node
        selnodePos = selnode.position()
            # Create position for the node to be created
        position   = [selnodePos[0]-self.px,selnodePos[1]-self.py]
        name = hou.ui.readInput("Enter name:", buttons=("OK", "Cancel"))
        if name[0] == 0:
            name = name[1].split()
            name = "_".join(name)
            objname = name
            node =   parent.createNode(self.type,objname)
            node.setPosition(position)
            if self.connect == 1:
                node.setInput(0,selnode)
            if self.connectToDop:
                secSelNode=hou.selectedNodes()[1]
                secSelNode.setInput(1,node)
            #select the just created node
            node.setCurrent(True,True)
            #   ONLY when created node is a filecache !!!
            if self.type == "filecache":
                addedParm = self.addParm()
                print 'self.type is filecache'
                # Specify the path
                # Used external Class
                fmc = findMoveCache.FindMoveCache()
                sceneFileLocation = fmc.sceneFileLocation()
                # Variable from external class
                if sceneFileLocation[-1] == '/':
                    sceneFileLocation = sceneFileLocation[:-1]
                parm = "{}/geo/$OS/v`ch('{}')`/$OS.$F4.bgeo.sc".format(sceneFileLocation,addedParm)
                node.parm('file').set(parm)

            return node
        else:
            print "Canceled!"

