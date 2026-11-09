import maya.cmds as cmds
import math
import random

from PySide6 import QtWidgets, QtCore, QtGui

### Making the Geometry ###

def create_cube(self, name, position, dimensions, rotation=(0, 0, 0)):

    obj = cmds.polyCube(name=name, width=dimensions[0], height=dimensions[1], depth=dimensions[2])[0]
    cmds.xform(obj, worldSpace=True, translation=position)
    cmds.xform(obj, worldSpace=True, rotation=rotation)
    cmds.parent(obj, self.GROUP)
    cmds.sets( obj, edit=True, forceElement=self.shading_group)

    return obj

def create_torso(self, hip_y, torso_length, torso_width):

     segment_count = 4
     segment_height = (torso_length / segment_count)
     torso_depth = torso_width * 0.42
     seam_gap = 0.025

     for i in range(segment_count):

        segment_y = (hip_y +segment_height * i + segment_height / 2.0)

        self.create_cube("Torso_Segment_{}".format(i + 1), (0, segment_y, 0), (torso_width, segment_height - seam_gap, torso_depth))

        return hip_y + torso_length