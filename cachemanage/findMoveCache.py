import os, shutil,distutils
import hou 
import json

#This is a test

class FindMoveCache:
    
    def __init__(self,node=None):
        self.node = node
        self.hipPath = None
        self.jsonFile = None
        self.pathNonExist =  "Files don't Exist"

    def selectNode(self):
        node = hou.selectedNodes()[0]
        return node

    def savePathToJson(self):
        cachedFilesList = []
        cachedFileDict = {'cachedFiles':cachedFilesList}
        objLevel = hou.node("/obj")
        objChildren = objLevel.allSubChildren()
        filecacheNodeCount = 0
        for kid in objChildren:
            if 'filecache'in kid.type().nameWithCategory() and kid.isBypassed() != True:
                pathParm = kid.parm('file').eval()
                temp_cachedFileName = pathParm.split('.')[0] 
                temp_cachedFileName = temp_cachedFileName.split('/')
                
                cachedFileName = temp_cachedFileName[-1]

                temp_cachedFileName.pop()

                path = temp_cachedFileName
                lastFolder = path[-1]
                path = "/".join(path)+'/'
                if 'geo' not in lastFolder:
                    print lastFolder
                    if not os.path.exists(path):
                        path += self.pathNonExist
                    filecacheNode = kid.path()
                    filecacheNodeCount += 1
                    cachedFilesList.append({'path':path, 'name':cachedFileName, 'filecacheNode':filecacheNode})

        cachedFileDict['cachedFiles'] = cachedFilesList
        new_string = json.dumps(cachedFileDict, indent=2, sort_keys=True)
        filecache_node_count = {'Filecache Node Found': '{}'.format(filecacheNodeCount)}
        new_line = '\n'
        new_string_b = json.dumps(filecache_node_count, indent=2, sort_keys=True)


        #print new_string

        hipLocation = self.sceneFileLocation()
        print hipLocation
        file_name = '{}/cachedFileDict.json'.format(hipLocation)
        with open(file_name,'w') as j:
            j.write(new_string)
#            j.write(new_line)
#            j.write(new_string_b)

        self.jsonFile = file_name
    
    def getPathFromJson(self):
        hipPath = self.hipPath
        jsonFile = self.jsonFile
        jsonFile = '{}/cachedFileDict.json'.format(hipPath)
        with open(jsonFile) as j:
            data = json.load(j)
        loadedDict = json.dumps(data, indent=2, sort_keys=True)
        print loadedDict
        cachedFilePathList = []
        valueOfDict = data.get('cachedFiles')
        for item in valueOfDict:
            path = item.get('path')
            if path not in cachedFilePathList and self.pathNonExist not in path:
                path = str(path)
                cachedFilePathList.append(path)
        print cachedFilePathList 


        return cachedFilePathList

#        Get file path Dictionary
#        if create object merge to help track down filecache nodes

# Check if in sop level

    def filePathDict(self,node,createObjMerge=0):
        
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

    def sceneFileLocation(self):
  
        sceneFilePath = hou.hipFile.path()
        sceneFilePath = sceneFilePath.split('/')
        sceneFilePath = sceneFilePath[:-1]
        sceneFileLocation  = '/'.join(sceneFilePath) + '/'
        self.hipPath = sceneFileLocation
        return sceneFileLocation


    def targetDirChooser(self):
        # create initial path for select target dir
        sceneFileLocation = self.sceneFileLocation()
        targetDir = hou.ui.selectFile(sceneFileLocation, "Choose Directory. Don't dive into selected Folder!!!", True, hou.fileType.Directory) 
        # Check if dir exists
        while not os.path.isdir(targetDir):
            targetDir = targetDir.split('/')[:-1]
            if len(targetDir) < 1:
                break
            targetDir = '/'.join(targetDir)
        # remove last /
        print '\n\nThe target dir before was {}'.format(targetDir)
        if targetDir[-1] == '/':
            targetDir[:-1]
        print '\n\nThe target dir is {}'.format(targetDir)
        return targetDir

    def copyPasteCache(self,filePathList,targetDir):
        confirm = hou.ui.displayConfirmation('Confirm to copy paste all current caches in this Object', hou.severityType.Message, None, None,None,None, hou.confirmType.OverwriteFile)
        if confirm == True:
            for filepath in filePathList:
                
                thisFilePath = filepath.split('/')
                print 'after split \n{}\n'.format(thisFilePath)
            
                fileName = thisFilePath[-1]
                
                thisFilePath = thisFilePath[:-1]
             
                thisFilePath = '/'.join(thisFilePath)
                #Make sure last ends with /
                if thisFilePath[-1] !='/':
                    thisFilePath += '/'

                src = thisFilePath
                print ' after join \n{}\n'.format(thisFilePath)
            
                # get rid of first part of the path, which is the scene file path
                sceneFileLocation = self.sceneFileLocation()
                thisFilePath = thisFilePath.replace(sceneFileLocation,'')
               # print '\n\ntarget path section is\n\n{}'.format(thisFilePath)
                dst = targetDir + thisFilePath 
                print 'source is \n{}\ntarget is\n{}'.format(src,dst)

                try:
                    shutil.move(src, dst)
                except IOError as io_err:
                    os.makedirs(os.path.dirname(dst))
                    shutil.move(src, dst)
                except :
                    print '\n'*4
                    print "Something wrong with {}".format(src)
                
#                try:
#                    distutils.dir_util.copy_tree(src, dst)
#                except IOError as io_err:
#                    os.makedirs(os.path.dirname(dst))
#                    distutils.dir_util.copy_tree(src, dst)
#                except :
#                    print '\n'*4
#                    print "Something wrong with {}".format(src)

    #def commonPath(self, node):
    #    objmerge = hou.ui.displayConfirmation("Create Object Merge?")
    #    filePathDict = self.filePathDict(node,objmerge)
    #    pathList = self.pathList(filePathDict)
    #    commonPath = findCommonPath.commonPath(pathList)        
    #    print 'Common path is "{}".'.format(commonPath)
    #    return commonPath     

