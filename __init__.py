ADDON_NAME = "mnm_slbg"
ADDON_OPERATOR_IDNAME = "mnm.slbg"

bl_info = {
    "name": "SL Bone Generator",
    "author": "Utano Mayonaka",
    "version": (1, 1, 0),
    "blender": (3, 3, 0),
    "support": "TESTING",
    "location": "View3D > Toolshelf > MnMSLbg",
    "description": "Add a Armature, and Generate bones group from SecondLife bento version",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}

if "bpy" in locals():
    import imp
    if "mnm_sl_bone_generator" in locals():
        imp.reload(mnm_sl_bone_generator)
else:
    from mnmSLBoneGenerator import mnm_sl_bone_generator


###===================================
### import block 
###===================================

import bpy
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
    bl_description = "Create a amature, and bones group from SL bento skeleton"
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
            box.label(text='File not exists. Require avatar_skeleton.xml.')
    #END def
#END class

class MNM_OT_mnm_slbg(Operator):
    bl_idname = ADDON_OPERATOR_IDNAME
    bl_label = "SL bones group generator"
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