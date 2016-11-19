
#  2016 Nicolas Priniotakis (Nikos) - nikos@easy-logging.net
#
#  This work is free. You can redistribute it and/or modify it under the
#  terms of the Do What The Fuck You Want To Public License, Version 2,
#  as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.


bl_info = {
	"name": "Selectivity",
	"author": "Nicolas Priniotakis (Nikos)",
	"version": (0,0,1,0),
	"blender": (2, 7, 8, 0),
	"api": 44539,
	"category": "3D View",
	"location": "View3D > Header",
	"description": "Select only the desired types of objects",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",}
''' version 0.1b '''

import bpy
from bpy.types import Header
from bpy.app.handlers import persistent

global use_selective, last_selection

last_selection = []


@persistent      
def prop_update(self,context):
    global use_selective, last_selection
    if use_selective == True:
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH' and context.scene.meshes == False:
                obj.select = False
            if obj.type == 'CAMERA' and context.scene.cameras == False:
                obj.select = False
            if obj.type == 'LAMP' and context.scene.lights == False:
                obj.select = False
            if obj.type == 'EMPTY' and context.scene.empties == False:
                obj.select = False
            if obj.type == 'CURVE' and context.scene.nurbs == False:
                obj.select = False
            if obj.type == 'ARMATURE' and context.scene.bones == False:
                obj.select = False

@persistent
def update(scene):
    global last_selection
    if bpy.context.selected_objects != last_selection:
        last_selection = bpy.context.selected_objects
        prop_update(scene,bpy.context)
        
bpy.types.Scene.meshes = bpy.props.BoolProperty(name="Meshes", default = False, update = prop_update)
bpy.types.Scene.nurbs = bpy.props.BoolProperty(name="Nurbs", default = False, update = prop_update)
bpy.types.Scene.cameras = bpy.props.BoolProperty(name="Lights", default = False, update = prop_update)
bpy.types.Scene.lights = bpy.props.BoolProperty(name="Meshes", default = False, update = prop_update)
bpy.types.Scene.empties = bpy.props.BoolProperty(name="Empties", default = False,update = prop_update)
bpy.types.Scene.bones = bpy.props.BoolProperty(name="Bones", default = False, update = prop_update)

use_selective = False

class selective_panel(Header):
    bl_space_type = 'VIEW_3D'
    bl_label = "Selective"
    bl_idname = "OBJECT_PT_Selective"
    bl_region_type = 'HEADER'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        global use_selective
        global empties, lights,bones,cameras,meshes,nurbs,others
        if not use_selective == True :
            row = layout.row()
            row.separator()
            row.operator("objects.activate", icon='UNPINNED', text='Selectivity : OFF')
            row.active = False
        else :
            row = layout.row(align=True)
            row.separator()
            row.operator("objects.activate", icon='PINNED', text='')  
            row = layout.row()
          
            row.prop(bpy.context.scene,"meshes", "", icon='MESH_DATA')
            row.prop(bpy.context.scene,"nurbs", "", icon='CURVE_DATA')
            row.prop(bpy.context.scene,"bones", "", icon='BONE_DATA')
            row.prop(bpy.context.scene,"lights", "", icon='LAMP')
            row.prop(bpy.context.scene,"empties", "", icon='OUTLINER_OB_EMPTY')
            row.prop(bpy.context.scene,"cameras", "", icon='OUTLINER_DATA_CAMERA')
            
   
class OBJECT_OT_activate(bpy.types.Operator):
    bl_idname = "objects.activate"
    bl_label = "Activate Selective"
 
    def execute(self, context):
        global use_selective, last_selection
        last_selection = bpy.context.selected_objects
        print(last_selection)
        use_selective = not use_selective
        update(self)
        return{'RUNNING_MODAL'}

bpy.app.handlers.scene_update_post.clear()
bpy.app.handlers.scene_update_post.append(update)

# ----------------- Registration -------------------     
def register():
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(update)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.app.handlers.scene_update_post.remove(update)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
