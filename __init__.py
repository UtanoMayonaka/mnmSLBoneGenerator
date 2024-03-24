ADDON_NAME = "mnm_slbg"
ADDON_OPERATOR_IDNAME = "mnm.slbg"

bl_info = {
    "name": "SL Bone Generator",
    "author": "Utano Mayonaka",
    "version": (1, 2, 0),
    "blender": (4, 0, 0),
    "support": "COMMUNITY",
    "location": "View3D > Toolshelf > MnMSLbg",
    "description": "Add a Armature, and Generate bones from SecondLife bento version (need to avatar_skeleton.xml).",
    "warning": "",
    "wiki_url": "",
    "doc_url": "https://github.com/UtanoMayonaka/mnmSLBoneGenerator",
    "tracker_url": "https://github.com/UtanoMayonaka/mnmSLBoneGenerator/issues",
    "category": "Object",
}


import bpy

try:
    from . import mnm_sl_bone_generator
except SystemError:
    import mnm_sl_bone_generator

if "bpy" in locals():
    from importlib import reload
    if "mnm_sl_bone_generator" in locals():
        reload(mnm_sl_bone_generator)


###===================================
### import block 
###===================================

import os
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, EnumProperty, StringProperty
from addon_utils import *


###===================================
### main class block 
###===================================

class MNM_PT_mnm_slbg(Panel):
    bl_label = "MnM SLbg"
    bl_idname = "MNM_PT_" + ADDON_NAME
    bl_description = "Create a amature, and bones from SL bento skeleton (need to avatar_skeleton.xml)."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_order = 0
    bl_category = "MnMSLbg"


    def draw(self, context):
        draw_layout = self.layout

        xmlpath = os.path.dirname(__file__) + '/avatar_skeleton.xml'
        if os.path.isfile(xmlpath):
            button_row = draw_layout.row()
            button_row.operator(ADDON_OPERATOR_IDNAME)
            box = draw_layout.box()
            box.label(text='Generate SL Bones group')
        else:
            box = draw_layout.box()
            box.label(text='File not exists. Require avatar_skeleton.xml (file is in under official browser ./character directory).')
    #END def
#END class

class MNM_OT_mnm_slbg(Operator):
    bl_idname = ADDON_OPERATOR_IDNAME
    bl_label = "SL bones generator"
    bl_description = "Add armature, and generate SL bones group."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mnm_sl_bone_generator.main(self, context)

        return {'FINISHED'}
    #END def
#END class


###===================================
### register block 
###===================================

classes = (
    MNM_PT_mnm_slbg,
    MNM_OT_mnm_slbg,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == '__main__':
    register()