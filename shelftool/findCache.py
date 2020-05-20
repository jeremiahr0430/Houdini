import hou
from cachemanage import findMoveCache

import os, shutil,distutils

reload(findMoveCache)

def run():
    #create object
    fmc = findMoveCache.FindMoveCache()

    #Define the node
    node = fmc.selectNode() 

    #Get the Dictionary
    filePathDict = fmc.filePathDict(node) 

    #Get the scene file location
    sceneFileLocation = fmc.sceneFileLocation()
    print "\nSceneFileLocation is {}\n".format(sceneFileLocation)

    # Target Dir Window

    targetDir = fmc.targetDirChooser()


    cacheFilePathList = filePathDict.values()
    #print "\nfile path List is {}\n".format(filePathList)


    fmc.copyPasteCache(cacheFilePathList,targetDir)

