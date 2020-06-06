"""
State:          PythonStateTest
State type:     pythonStateTest
Description:    PythonStateTest
Author:         _69051
Computer Name:  DESKTOP-8DE7T06
Date Created:   May 23, 2020 - 08:55:22
"""

# Usage: This sample adds points to the construction plane.
# 
# If you embedded the state in a SOP HDA:
# 1) Dive in the HDA and add a SOP Add node
# 2) Open the Add node property page and promote the Number of Points parm (Alt+MMB)
# 3) LMB in the viewer to add points.
# 
# If you created a file python state:
# 1) Create an empty geometry and dive in.
# 2) Create an Embedded HDA: Subnetwork, RMB, Create Digital Asset..., Operator Name: test, Save To Library: Embedded, Accept.
# 3) Dive in the Embedded HDA and add a SOP Add node
# 4) Open the Add node property page and promote the Number of Points parm (Alt+MMB)
# 5) Set Node Default State: test in Type Operator Properties, Accept.
# 6) LMB in the viewer to add points.

import hou
import viewerstate.utils as su

class State(object):
    MSG = "LMB to add points to the construction plane."

    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer
        self.node = None
        self.collisiongeo = None
        self.multiparm = None
        self.placedobject = False
        self.placedpos = hou.Vector3()
        self.hitnormal = hou.Vector3()
        
    def onEnter(self, kwargs):
        self.node = kwargs["node"]

        if not self.node:
            raise

        self.scene_viewer.setPromptMessage( State.MSG )
        
        self.collisiongeo = self.node.node("COMPLEXCOLLISION").geometry()
        self.multiparm = self.node.parm("iPlacements")
        
        numberofentries = self.GetNumberOfMultiparmEntries(kwargs)
        self.multiparm.set(numberofentries+1)
        
        print self.collisiongeo
 
    def GetNumberOfMultiparmEntries(self, kwargs):
        return self.multiparm.evalAsInt()

    def onInterrupt(self,kwargs):
        print "Interrupt"
        pass

    def onResume(self, kwargs):
        self.scene_viewer.setPromptMessage( State.MSG )

    def onMouseWheelEvent(self, kwargs):
        
        ui_event = kwargs['ui_event']
        device = ui_event.device()
        scroll = device.mouseWheel()

        numentries = self.GetNumberOfMultiparmEntries(kwargs)
        currentvalues = self.node.parm("iID_{}".format(numentries)).evalAsInt()
        print numentries
#        if numentries > 1 and currentvalues <0:
#            preNumentries = numentries-1
#            previousValues = self.node.parm("iID_{}".format(preNumentries)).eval()
#            self.node.parm("iID_%s" % numentries).set(max(previousValues,0))
#        else:
        self.node.parm("iID_%s" % numentries).set(max(currentvalues+scroll,0))


        print scroll
        return False

    def onMouseEvent(self, kwargs):
        """ Find the position of the point to add by 
            intersecting the construction plane. 
        """
        ui_event = kwargs["ui_event"]
        device = ui_event.device()
        origin, direction = ui_event.ray()
        reason = ui_event.reason()
        control = device.isCtrlKey()

        gi = su.GeometryIntersector(self.collisiongeo, scene_viewer= self.scene_viewer)
        gi.intersect(origin, direction)


        # Check if we didn't hit anything
        if gi.prim_num >= 0:
            hitposition = gi.position
            numentries = self.GetNumberOfMultiparmEntries(kwargs)
            
            print "I hit a primtive"

#            if reason ==  hou.uiEventReason.Picked:
#                print "Single Click"
#                self.multiparm.set(numentries+1)
            if self.placedobject == False:
                self.node.parmTuple("vPosition_%s" % numentries).set(hitposition)
            
# Mouse Down
            if reason == hou.uiEventReason.Start:
                self.placedpos = hitposition
                self.hitnormal = gi.normal
                self.placedobject = True

# Mouse Moving
            if reason == hou.uiEventReason.Active and control != True:

                if self.placedobject == True:
                    pos = hou.hmath.intersectPlane(self.placedpos,self.hitnormal, origin, direction)
                    scale = hitposition.distanceTo(self.placedpos)
                    self.node.parm('fScale_%s' %numentries).set(scale)
                    print hitposition.distanceTo(self.placedpos)


            elif reason == hou.uiEventReason.Active and control == True:

                if self.placedobject == True:
#scale = hitposition[0] - self.placedpo[0]
#scale = 
                    pos = hou.hmath.intersectPlane(self.placedpos,self.hitnormal, origin, direction)
                    rot = hitposition.distanceTo(self.placedpos) * 2
                    self.node.parm('rot_%s' %numentries).set(rot)
                    print hitposition.distanceTo(self.placedpos)
# mouse up
            if reason == hou.uiEventReason.Changed:
                self.multiparm.set(numentries+1)
                self.placedobject = False

                numentries = self.GetNumberOfMultiparmEntries(kwargs)
                if numentries>1:
                    preNumentries = numentries-1
                    previousValues = self.node.parm("iID_{}".format(preNumentries)).eval()
                    self.node.parm("iID_%s" % numentries).set(max(previousValues,0))

        return True


def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = kwargs["type"].definition().sections()["DefaultState"].contents()
    state_label = "PythonStateTest"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon(kwargs["type"].icon())


    return template
