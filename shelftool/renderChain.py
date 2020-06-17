import hou

def run():
    nodes = hou.selectedNodes()
    nodes = list(nodes)
    
    # Check if selected nodes are in different object, or context
    inDifferentObject = False
    for index,node in enumerate(nodes):
        if index !=0:
            if node.parent() != nodes[index-1].parent():
                inDifferentObject = True

    if inDifferentObject == False:
        print '\n list before sorted is \n'
        for node in nodes:
            print node.name()
            
        # sort by y position
        def byPy(x,y):
            pos1= x.position()[1]
            pos2= y.position()[1]
            if pos1-pos2<0:
                return 1
            else:
                return -1

        nodes.sort(byPy)

        print '\n list after sorted is \n'
        for node in nodes:
            print node.name()



    for index,node in enumerate(nodes):
        if index ==0:
            print "Selected nodes in the chain are: \n"
        
        else:
            prenode = nodes[index-1]
            parm1 = node.parm("prerender")
            parm2 = node.parm("postrender")
            parm3 = node.parm("tprerender")
            parm4 = node.parm("tpostrender")
            parm1.set("opparm -c `opfullpath('../{}')` execute".format(prenode))
            parm2.set("opparm `opfullpath('.')` tprerender 0".format())
            parm3.set("1")
            parm4.set("1")
            print "{}. ".format(index) + node.name() + '\n'
            
    nodes[0].setCurrent(True,True)
    nodes[-1].setCurrent(True,False)




