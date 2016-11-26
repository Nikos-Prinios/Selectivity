
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
global use_selective
      
def prop_update(self,context):
    global use_selective
    
    if use_selective == True:
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.hide_select = not context.scene.meshes
                if obj.select == True and obj.hide_select == True :
                    obj.select = False
                
            if obj.type == 'CAMERA':
                obj.hide_select = not context.scene.cameras
                if obj.select == True and obj.hide_select == True :
                    obj.select = False

            if obj.type == 'LAMP':
                obj.hide_select = not context.scene.lights
                if obj.select == True and obj.hide_select == True :
                    obj.select = False

            if obj.type == 'EMPTY':
                obj.hide_select = not context.scene.empties
                if obj.select == True and obj.hide_select == True :
                    obj.select = False
                
            if obj.type == 'CURVE':
                obj.hide_select = not context.scene.nurbs
                if obj.select == True and obj.hide_select == True :
                    obj.select = False
                
            if obj.type == 'ARMATURE' :
                obj.hide_select = not context.scene.bones
                if obj.select == True and obj.hide_select == True :
                    obj.select = False
S = bpy.types.Scene        
S.meshes = bpy.props.BoolProperty(name="Meshes", default = False, update = prop_update)
S.nurbs = bpy.props.BoolProperty(name="Nurbs", default = False, update = prop_update)
S.cameras = bpy.props.BoolProperty(name="Cameras", default = False, update = prop_update)
S.lights = bpy.props.BoolProperty(name="Lights", default = False, update = prop_update)
S.empties = bpy.props.BoolProperty(name="Empties", default = False,update = prop_update)
S.bones = bpy.props.BoolProperty(name="Bones", default = False, update = prop_update)

bpy.types.Object.init = bpy.props.BoolProperty(name="init",description="Initial state",default = True)



use_selective = False

def initial_read():
    for obj in bpy.context.scene.objects:
        obj.init = obj.hide_select

def initial_write():
    for obj in bpy.context.scene.objects:
        obj.hide_select = obj.init


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
        if not use_selective :
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
        global use_selective
        
        use_selective = not use_selective
        if use_selective:
            initial_read()
            prop_update(self, bpy.context)
        else:
            initial_write()
        return{'RUNNING_MODAL'}

# ----------------- Registration -------------------     
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
