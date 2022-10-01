import bpy
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
import math
import numpy as np
from distutils.util import strtobool
from mathutils import Vector

def parse_elements( element , armature ):
    pbone = None

    if "name" in element.attrib and (element.tag == "bone" or element.tag == "collision_volume"):
        pbone = armature.data.edit_bones[element.attrib['name']]
    #endif

    for bone in element:
        #print(bone.get('name'))

        bname = bone.get('name')
        exists_bone = False
        
        for ebone in armature.data.edit_bones:
            if ebone.name == bname:
                exists_bone = True
                break
            #endif
        #endfor
    
        if exists_bone:
            bn = armature.data.edit_bones[bname]
        else:
            bn = armature.data.edit_bones.new(bname)
        #endif

        if bone.tag == "bone":
            pos = Vector(np.fromstring(bone.get('pivot'), sep=' '))
            bn.use_connect = strtobool(bone.get('connected'))
            bn.layers[1] = bone.get("support") == 'base'
            bn.layers[2] = bone.get("support") != 'base'
            bn['prop'] = 'Base' if bone.get("support") != 'base' else 'Extended'
        else:
            pos = Vector(np.fromstring(bone.get('pos'), sep=' '))
            bn.layers[0] = False
            bn.layers[7] = True
            bn['prop'] = 'Collision'
        #endif
        
        end = Vector(np.fromstring(bone.get('end'), sep=' '))

        if pbone != None:
            bn.parent = pbone
        #endif

        bn.head = pos
        bn.tail = end
    #endfor
    
        
    for sub in element:
        parse_elements( sub , armature )
    #endfor


def main(self, context):
    armature = None
    for collection in bpy.data.collections:
        for obj in collection.all_objects:
            if obj.type == 'ARMATURE':
                armature = obj
            #endif
        #endfor
    #endfor
                

    if armature == None:
        armature = bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        armature = bpy.context.view_layer.objects.active
    #endif


    # prepare bone groups
    if len(armature.pose.bone_groups) < 1:
        armature.pose.bone_groups.new(name='Base')
    else:
        armature.pose.bone_groups[0].name = 'Base'
    #endif
    armature.pose.bone_groups[0].color_set = 'THEME03'

    if len(armature.pose.bone_groups) < 2:
        armature.pose.bone_groups.new(name='Extended')
    else:
        armature.pose.bone_groups[1].name = 'Extended'
    #endif
    armature.pose.bone_groups[1].color_set = 'THEME04'

    if len(armature.pose.bone_groups) < 3:
        armature.pose.bone_groups.new(name='Collision')
    else:
        armature.pose.bone_groups[2].name = 'Collision'
    #endif
    armature.pose.bone_groups[2].color_set = 'THEME02'


#    xmlpath = os.path.dirname(__file__) + '/avatar_skeleton.xml'
    xmlpath = "D:\\Users\\Utano\\AppData\\Roaming\Blender Foundation\\Blender\\3.3\\scripts\\addons\\mnmSLBoneGenerator\\avatar_skeleton.xml"
    tree = ET.parse(xmlpath)
    root = tree.getroot()

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    if 'Bone' in armature.data.edit_bones:
        armature.data.edit_bones.remove(armature.data.edit_bones['Bone'])

    for sub in root.iter(root.tag):
        parse_elements( sub , armature)
    #endfor
        
    for bone in armature.data.edit_bones:
        pbone = bone.parent
        if pbone != None:
            if bone.use_connect:
                bone.tail = pbone.tail + bone.tail
            else:
                bone.head = pbone.head + bone.head
                bone.tail = bone.head+bone.tail
            #endif
        else:
            bone.tail += bone.head
        #endif
    #endfor
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for bone in armature.pose.bones:
        if 'prop' in armature.data.edit_bones[bone.name]:
            bone.bone_group = armature.pose.bone_groups[armature.data.edit_bones[bone.name]['prop']]
        #endif
    #endfor
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



# test run
if __name__ == '__main__':
    main(bpy.data, bpy.context)
#endif
