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
            if bone.get("support") == 'base':
                bn['prop'] = 'Base'
                bn.color.palette = 'THEME04'
            else:
                bn['prop'] = 'Extended'
                bn.color.palette = 'THEME03'
        else:
            pos = Vector(np.fromstring(bone.get('pos'), sep=' '))
            bn['prop'] = 'Collision'
            bn.color.palette = 'THEME01'
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
    if context.view_layer.objects.active != None:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

    armature = None
    for collection in bpy.data.collections:
        for obj in collection.all_objects:
            if obj.type == 'ARMATURE':
                armature = obj
                bpy.context.view_layer.objects.active = armature
            #endif
        #endfor
    #endfor
                

    if armature == None:
        armature = bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        armature = bpy.context.view_layer.objects.active
    #endif
    armature.data.name = 'Root'

    # remove default bone
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # prepare bone collection
    armature.data.collections[0].name = 'Base'
    bpy.ops.armature.collection_add()
    armature.data.collections[1].name = 'Extended'
    armature.data.collections[1].is_visible = False
    bpy.ops.armature.collection_add()
    armature.data.collections[2].name = 'Collision'
    armature.data.collections[2].is_visible = False

    armature.show_in_front = True


    if __name__ == '__main__':
#        xmlpath = "D:\\Users\\Utano\\AppData\\Roaming\Blender Foundation\\Blender\\4.0\\scripts\\addons\\mnmSLBoneGenerator\\avatar_skeleton.xml"
        print("local test")
    else:
        xmlpath = os.path.dirname(__file__) + '/avatar_skeleton.xml'

    tree = ET.parse(xmlpath)
    root = tree.getroot()

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    for sub in root.iter(root.tag):
        parse_elements( sub , armature )
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

        # Roll X-Axis calculation
        bone.align_roll(Vector((1.0,0.0,0.0)))
    #endfor

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # set each bone to boneCollection
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    for bone in armature.data.bones:
        bone.select = True
        bpy.ops.armature.collection_assign( name=bone.get('prop') )
        bone.select = False

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)




# local test run
if __name__ == '__main__':
    main(bpy.data, bpy.context)
#endif
