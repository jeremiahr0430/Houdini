import hou
from cachemanage import findMoveCache
reload(findMoveCache)

class GenerateNode:

    def __init__(self,type='filecache',connectNode = None, connect = 1, px=0,py=1,connectToDop = False,inputName = hou.ui.readInput("Enter name:", buttons=("OK", "Cancel"))):
        self.type = type
        self.connectNode = connectNode
        self.connect = connect
        self.px = px
        self.py = py
        self.connectToDop = connectToDop

        self.userInput = inputName

        self.userInputString = self.replaceSpace(inputName[1])
        self.userInputFolderName = None
        self.nodeCreated = None

    def getFolderName(self,inputString):    
        # return None if there' no folder name
        inputString = self.replaceSpace(inputString)
        if "/" in inputString:
            slashSplit = inputString.split('/')
            folderName = slashSplit[0]+'/'
            name = slashSplit[1]
        else:
            folderName = None
            name = inputString
        self.userInputFolderName = folderName
        return folderName,name

    def replaceSpace(self,name):
        if " " in name:
            name = name.split()
            name = "_".join(name)
        return name

# This is only works for filecache for now!!!
    def addParm(self,node=None,parm="version",value = 1):
        def addParmForType(location = 'Save to File'):
            target = ptg.findIndicesForFolder(location) # find Save to File folder
            # Create the parm to Add
            houParmTmp = hou.IntParmTemplate(parm, parm, 1)
            ptg.appendToFolder(target,houParmTmp)
            node.setParmTemplateGroup(ptg)
            #set default value
            node.parm(parm).set(value)
        #This is only work for adding parm to filecache node type
        if not node:    
            node = hou.selectedNodes()[0] #select the filecache just created
        #create parameters
        ptg = node.parmTemplateGroup()

        ## If node type is file cache
        if 'filecache'in node.type().nameWithCategory():
            addParmForType()
        if 'rop_alembic' in node.type().nameWithCategory():
            addParmForType('Main')
        return parm

    def adjustParmForType(self,folderName = None, createdNode = None,pathParm = 'file',cachedFileName = '$OS.$FF.bgeo.sc', secondParm = 'missingframe', thirdParm = 'loadfromdisk'):
        # Specify the path
        # Used external Class
        fmc = findMoveCache.FindMoveCache()
        sceneFileLocation = fmc.sceneFileLocation()
        # Variable from external class
        if sceneFileLocation[-1] == '/':
            sceneFileLocation = sceneFileLocation[:-1]
        # rop_alembic feature is added in addParm method
        parmA = self.addParm()
        parmB = self.addParm(None,'takes')
        if folderName != None:
            parm = "{}/geo/{}$OS/v`ch('{}')`/t`ch('{}')`/{}".format(sceneFileLocation,folderName,parmA,parmB,cachedFileName)
        else:
            parm = "{}/geo/$OS/v`ch('{}')`/t`ch('{}')`/{}".format(sceneFileLocation,parmA,parmB,cachedFileName)

        createdNode.parm(pathParm).set(parm)
        createdNode.parm(secondParm).set(1)
        if thirdParm != None:
            createdNode.parm(thirdParm).set(1)

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
        
        # Get the name of the node
        name = self.userInput   
        
        if name[0] == 0: # OK button is clicked
            # check if folder name is needed
            # if '/' is in the user input string, than what's before '/' is the folder name
            folderAndName = self.getFolderName(name[1]) 
            print 'folderAndName is {} \n'.format(folderAndName)

            folderName = folderAndName[0]
            objname = folderAndName[1]

            self.nodeCreated =   parent.createNode(self.type,objname)
            self.nodeCreated.setPosition(position)
            if self.connect == 1:
                self.nodeCreated.setInput(0,selnode)
            # deal with output
            #if selnode output
            if self.connectToDop:
                secSelNode=hou.selectedNodes()[1]
                secSelNode.setInput(1,self.nodeCreated)
            #select the just created node
            self.nodeCreated.setCurrent(True,True)
            #   ONLY when created node is a filecache !!!
            if self.type == "filecache":
                print 'self.type is filecache'
                self.adjustParmForType(self.userInputFolderName, self.nodeCreated)
            elif self.type == 'rop_alembic':
                print 'self.type is rop_alembic'
                self.adjustParmForType(self.userInputFolderName, self.nodeCreated,'filename','$OS.abc','trange',None)

            return self.nodeCreated
        
        else:
            print "Canceled!"



