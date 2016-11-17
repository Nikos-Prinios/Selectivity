
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

global use_selective, initial_state,sel_objs,last_selection
global empties, lights,bones,cameras,meshes,nurbs

empties = False
lights = False
bones = False
cameras = False
meshes = False
nurbs = False

use_selective = False

last_selection = []

@persistent
def assembly_handler(scene):
    global empties, lights,bones,cameras,meshes,nurbs,last_selection, use_selective
    if use_selective == True:
        if bpy.context.selected_objects != last_selection:
            last_selection = bpy.context.selected_objects
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH' and meshes == False:
                    obj.select = False
                if obj.type == 'CAMERA' and cameras == False:
                    obj.select = False
                if obj.type == 'LAMP' and lights == False:
                    obj.select = False
                if obj.type == 'EMPTY' and empties == False:
                    obj.select = False
                if obj.type == 'CURVE' and nurbs == False:
                    obj.select = False
                if obj.type == 'ARMATURE' and bones == False:
                    obj.select = False

def update(type,state):
    for obj in bpy.context.selected_objects:
        if obj.type == type and state == False :
            obj.select = False


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
            sub = row.row()
            sub.operator("meshes.selective", icon='MESH_DATA')
            sub.active = meshes
            
            sub = row.row()
            sub.operator("nurbs.selective", icon='CURVE_DATA')
            sub.active = nurbs   
            
            sub = row.row()
            sub.operator("bones.selective", icon='BONE_DATA')
            sub.active = bones
            
            sub = row.row()
            sub.operator("lights.selective", icon='LAMP')
            sub.active = lights

            sub = row.row()
            sub.operator("empties.selective", icon='OUTLINER_OB_EMPTY')
            sub.active = empties
            
            sub = row.row()
            sub.operator("cameras.selective", icon='OUTLINER_DATA_CAMERA')
            sub.active = cameras
            
class MESH_SELECTABLE(bpy.types.Operator):
    bl_idname = "meshes.selective"
    bl_label = ""
    
    def execute(self, context):
        global meshes
        meshes = not meshes
        update('MESH',meshes)
        return{'RUNNING_MODAL'}
    
class LIGHT_SELECTABLE(bpy.types.Operator):
    bl_idname = "lights.selective"
    bl_label = ""
    
    def execute(self, context):
        global lights
        lights = not lights
        update('LAMP',lights)
        return{'RUNNING_MODAL'}

class BONE_SELECTABLE(bpy.types.Operator):
    bl_idname = "bones.selective"
    bl_label = ""
    
    def execute(self, context):
        global bones
        bones = not bones
        update('ARMATURE',bones)
        return{'RUNNING_MODAL'}

class CAMERA_SELECTABLE(bpy.types.Operator):
    bl_idname = "cameras.selective"
    bl_label = ""
    
    def execute(self, context):
        global cameras
        cameras = not cameras
        update('CAMERA',cameras)
        return{'RUNNING_MODAL'}
    
class NURBS_SELECTABLE(bpy.types.Operator):
    bl_idname = "nurbs.selective"
    bl_label = ""
    
    def execute(self, context):
        global nurbs
        nurbs = not nurbs
        update('CURVE',nurbs)
        return{'RUNNING_MODAL'}

class EMPTY_SELECTABLE(bpy.types.Operator):
    bl_idname = "empties.selective"
    bl_label = ""
    
    def execute(self, context):
        global empties
        empties = not empties
        update('EMPTY',empties)
        return{'RUNNING_MODAL'}
   
class OBJECT_OT_activate(bpy.types.Operator):
    bl_idname = "objects.activate"
    bl_label = "Activate Selective"
 
    def execute(self, context):
        global use_selective
        use_selective = not use_selective
        last_selection = bpy.context.selected_objects
        return{'RUNNING_MODAL'}

bpy.app.handlers.scene_update_post.clear()
bpy.app.handlers.scene_update_post.append(assembly_handler)


# ----------------- Registration -------------------     
def register():
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(assembly_handler)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.app.handlers.scene_update_post.remove(assembly_handler)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

