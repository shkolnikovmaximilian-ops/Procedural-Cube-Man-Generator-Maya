import maya.cmds as cmds
import math
import random

from PySide6 import QtWidgets, QtCore, QtGui

### Making the Geometry ###

def create_torso(self, hip_y, torso_length, torso_width):

     segment_count = 4
     segment_height = (torso_length / segment_count)
     torso_depth = torso_width * 0.42
     seam_gap = 0.025

     for i in range(segment_count):

        segment_y = (hip_y +segment_height * i + segment_height / 2.0)

        self.create_box("Torso_Segment_{}".format(i + 1), (0, segment_y, 0), (torso_width, segment_height - seam_gap, torso_depth))

        return hip_y + torso_length