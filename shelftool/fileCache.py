import hou
from cachemanage import generateNode  # findMoveCache class is called

reload(generateNode)

import os


def run():
    #Define the node
    gNode = generateNode.GenerateNode('filecache')

    filecache = gNode.generateNode()




