import maya.cmds as cmds
import math
import random

from PySide6 import QtWidgets, QtCore, QtGui


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




def create_neck(self, torso_top, torso_width, head_width):

    neck_height = head_width * 0.35
    neck_width = head_width * 0.38
    neck_depth = neck_width * 0.85
    neck_center = (torso_top + neck_height / 2.0)

    self.create_cube("Neck", (0, neck_center, 0), (neck_width, neck_height, neck_depth))

    return torso_top + neck_height





def create_arms(self, torso_top, torso_width, arm_length, limb_width, hand_gap):

    shoulder_y = (torso_top - torso_width * 0.12)
    shoulder_offset = (torso_width * 0.48)
        
    arm_angle = math.radians(45)
    segment_length = arm_length / 2.0
    horizontal = (math.cos(arm_angle) * segment_length)
    vertical = (math.sin(arm_angle) * segment_length)
    arm_depth = limb_width * 0.9
    
    hand_size = limb_width * 1.15

    for side in [-1, 1]:
        
        side_name = ("Left" if side == -1 else "Right")

        shoulder = (side * shoulder_offset, shoulder_y, 0)

        elbow = (side * (shoulder_offset + horizontal), shoulder_y - vertical, 0)

        wrist = (side * (shoulder_offset + horizontal * 2), shoulder_y - vertical * 2, 0)



    self.create_segment(side_name + "_Upper_Arm", shoulder, elbow, limb_width, arm_depth)

    

    self.create_segment(side_name + "_Lower_Arm", elbow, wrist, limb_width * 0.9, arm_depth)

    direction_x = (side * math.cos(arm_angle))
    direction_y = (-math.sin(arm_angle))

    hand_offset = (hand_gap + hand_size * 0.5)

    hand_position = (wrist[0] + direction_x * hand_offset, wrist[1] + direction_y * hand_offset, 0)

    hand_rotation = (0, 0, -side * 45)

    self.create_cube(side_name + "_Hand", hand_position, (hand_size, hand_size, hand_size * 0.8), hand_rotation)





def create_head(self, neck_top, head_width):

    head_height = head_width * 1.12
    head_depth = head_width * 0.75
    head_center_y = (neck_top + head_height / 2.0)
    
    self.create_cube("Head", (0, head_center_y, 0), (head_width, head_height, head_depth))



def create_legs(self, hip_y, leg_length, torso_width, limb_width, foot_gap):

    spacing = torso_width * 0.22
    
    foot_height = limb_width * 0.5
    foot_width = limb_width * 1.2
    foot_depth = limb_width * 1.8
    
    ankle_y = foot_height + foot_gap
    
    knee_y = (hip_y + ankle_y) / 2.0

    leg_depth = limb_width * 0.9

    for side in [-1, 1]:

        side_name = ("Left" if side == -1 else "Right")

        x = side * spacing

        hip = (x, hip_y, 0)
        
        knee = (x, knee_y, 0)

        ankle = (x, ankle_y, 0)

    self.create_segment(side_name + "_Upper_Leg", hip, knee, limb_width, leg_depth)


    self.create_segment(side_name + "_Lower_Leg", knee, ankle, limb_width, leg_depth)


    self.create_cube(side_name + "_Foot", (x, foot_height / 2.0, limb_width * 0.45), (foot_width, foot_height, foot_depth))

    
    
    
def create_segment(self, name, start, end, width, depth):

    start = tuple(start)
    end = tuple(end)

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dz = end[2] - start[2]

    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    midpoint = ((start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0, (start[2] + end[2]) / 2.0)
    angle = math.degrees(math.atan2(-dx, dy))

    return self.create_cube(name, midpoint, (width, length, depth), rotation=(0, 0, angle))




def create_material(self, color):

    material_name = "CubeMan_Material"

    if cmds.objExists(material_name):
            
        cmds.delete(material_name)

    self.material = cmds.shadingNode("lambert", asShader=True, name=material_name)

    cmds.setAttr(self.material + ".color", color[0], color[1], color[2], type="double3")
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material_name + "SG")
    cmds.connectAttr(self.material + ".outColor", shading_group + ".surfaceShader", force=True)

    self.shading_group = shading_group




def generate(self, arm_length, leg_length, torso_length, limb_width, torso_width, head_width, hand_gap, foot_gap, color):

    if cmds.objExists(self.GROUP):

        cmds.delete(self.GROUP)


    cmds.group(empty=True, name=self.GROUP)

    self.create_material(color)    

    foot_height = limb_width * 0.5
    
    ankle_y = (foot_height + foot_gap)
    
    hip_y = (ankle_y + leg_length)

    torso_top = self.create_torso(hip_y, torso_length, torso_width)

    neck_top = self.create_neck(torso_top, torso_width, head_width)


    self.create_head(neck_top, head_width)

    self.create_arms(torso_top, torso_width, arm_length, limb_width, hand_gap)

    self.create_legs(hip_y, leg_length, torso_width, limb_width, foot_gap)

    cmds.select(self.GROUP, replace=True)  

    cmds.viewFit(all=True)

    class CubeManGeneratorUI(QtWidgets.QDialog):

        WINDOW_TITLE = "Procedural CubeMan Generator"

    
    
    
def __init__(self, parent=None):

    super(CubeManGeneratorUI, self).__init__(parent)

    self.generator = ProceduralCubeMan()

    self.character_color = QtGui.QColor(166, 166, 166)

    self.setWindowTitle(self.WINDOW_TITLE)

    self.setMinimumWidth(390)

    self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)

    self.build_ui()




def create_slider(self, layout, label, minimum, maximum, default, decimals=2):

    container = QtWidgets.QWidget()
    container_layout = QtWidgets.QVBoxLayout(container)
    container_layout.setContentsMargins(0, 2, 0, 2)
    header = QtWidgets.QHBoxLayout()
    text_label = QtWidgets.QLabel(label)
    value_field = QtWidgets.QDoubleSpinBox()
    value_field.setDecimals(decimals)
    value_field.setRange(minimum, maximum)
    value_field.setSingleStep(0.1)
    value_field.setValue(default)
    value_field.setFixedWidth(85)

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

    scale = 100

    slider.setRange(int(minimum * scale), int(maximum * scale))
        
    slider.setValue(int(default * scale))

    slider.valueChanged.connect(lambda value: value_field.setValue(value / scale))

    value_field.valueChanged.connect(lambda value: slider.setValue(int(round(value * scale))))
    header.addWidget(text_label)
    header.addStretch()
    header.addWidget(value_field)
    container_layout.addLayout(header)
    container_layout.addWidget(slider)
    layout.addWidget(container)
    return value_field



def create_section(self, title, parent_layout):

    group = QtWidgets.QGroupBox(title)
    layout = QtWidgets.QVBoxLayout(group)
    layout.setSpacing(6)
    parent_layout.addWidget(group)

    return layout




def build_ui(self):
        
    main_layout = QtWidgets.QVBoxLayout(self)

    main_layout.setContentsMargins(14, 14, 14, 14)

    main_layout.setSpacing(10)

    title = QtWidgets.QLabel("Procedural CubeMan Generator")
    title.setAlignment(QtCore.Qt.AlignCenter)
    title.setStyleSheet(""" font-size: 18px; font-weight: bold; padding: 8px; """)
    main_layout.addWidget(title)

    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)

    scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

    content = QtWidgets.QWidget()
    content_layout = QtWidgets.QVBoxLayout(content)
    content_layout.setSpacing(12)
    scroll.setWidget(content)

    main_layout.addWidget(scroll)





