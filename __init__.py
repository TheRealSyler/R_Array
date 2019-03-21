
import bpy,math,mathutils,blf,rna_keymap_ui

from .RA_draw_ui import *
from mathutils import Matrix
from bpy.types import (
                        PropertyGroup,
                        Menu
                        )
from bpy.props import (
                        IntProperty,
                        FloatProperty,
                        BoolProperty
                        )
#// join objects option in modal operator
#// Reset array option in modal operator
#// Modal operator Ui
#// add Radial Array hotkey 
#// preferences add hotkey in addon preferences menu
#// addon menu ui
#// add modal selectable toggle
#// add modal apply option
#// add modal ui tooltips
#// add make unique
#// add create collection toggle


bl_info = {
    "name" : "R.Array",
    "author" : "Syler",
    "version": (0, 0, 1, 2),
    "description": "Adds Radial Array Operator",
    "blender" : (2, 80, 0),
    "category" : "Object"
}
#+ handle the keymap
addon_keymaps = []

def add_hotkey(): 
    #* Ctrl Q call R_Array
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(R_Array.bl_idname, 'Q', 'PRESS', ctrl=True)
    addon_keymaps.append(km)

def remove_hotkey():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]
#--------------------------------------------------------------------------------------#
def RA_Update_Sel_Status(self, context):
    if self.RA_Sel_Status == True:
        for ob in self.RA_Parent.children:
            ob.hide_select = False
    if self.RA_Sel_Status == False:
        for ob in self.RA_Parent.children:
            ob.hide_select = True
            
def RA_Update_ObjNum(self, context):
    
    if self.RA_Status == True:
        
        if len(self.RA_Parent.children) == self.RA_ObjNum:  
            pass
        
        #+ Add Objects
        if len(self.RA_Parent.children) < self.RA_ObjNum:
            object_list = []
            object_to_copy = self.RA_Parent.children[0]
            # append already existing objects to object list
            for c in self.RA_Parent.children:
                object_list.append(c)
            
            
            for i in range (len(self.RA_Parent.children), self.RA_ObjNum):
                object_list.append(object_to_copy.copy())
                
                
                
            # Add Objects To Collection
            for index, ob in enumerate(object_list):
                
                # Reset Matrix
                ob.matrix_basis = mathutils.Matrix()
                
                # set object location to RA_Parent + RA_Offset
                ob.location[1] = self.RA_Parent.location[1] + self.RA_Parent.RA_Offset
                # create angle variable 
                angle = math.radians(360/self.RA_Parent.RA_ObjNum)               
                
                # rotate object
                R = mathutils.Matrix.Rotation(angle * (index), 4, 'Z')
                T = mathutils.Matrix.Translation([0, 0, 0])     
                M = T @ R @ T.inverted()
                ob.location = M @ ob.location
                ob.rotation_euler.rotate(M)
                
                
                # Parent Object 
                ob.parent = self.RA_Parent
                self.RA_Parent.matrix_parent_inverse = ob.matrix_world.inverted()
                ob.RA_Parent = self.RA_Parent
                
                # make objects selectable/unselectable
                if self.RA_Sel_Status == True:
                    ob.hide_select = False
                if self.RA_Sel_Status == False:
                    ob.hide_select = True
    
                # Change Object Name
                ob.name = "RA - " + self.RA_Name + " - " + str(index)
                # set RA Status
                ob.RA_Status = True
                # Link object
                try:
                    self.RA_Parent.users_collection[0].objects.link(ob)
                    #print ("For LINK")
                except:
                    #print ("PASS Linking object to collection failed")
                    pass
    
        #+ Remove Objects
        if len(self.RA_Parent.children) > self.RA_ObjNum:
                
            # deselect all objects
            for d in bpy.context.view_layer.objects:
                d.select_set(False)
            bpy.context.view_layer.objects.active = None
            
            # Make selectable and Select all objects that will be deleted
            for i in range (self.RA_ObjNum, len(self.RA_Parent.children)):
                self.RA_Parent.children[i].hide_select = False
                self.RA_Parent.children[i].select_set(True)
            # Delete Objects     
            bpy.ops.object.delete()
            # select control Object
            bpy.context.view_layer.objects.active = self.RA_Parent
            self.RA_Parent.select_set(True)
            for index, ob in enumerate(self.RA_Parent.children):
                # Reset Matrix
                ob.matrix_basis = mathutils.Matrix()
            
                # set object location to RA_Parent + RA_Offset
                ob.location[1] = self.RA_Parent.location[1] + self.RA_Parent.RA_Offset
                # create angle variable 
                angle = math.radians(360/self.RA_Parent.RA_ObjNum)
            
                # rotate object
                R = mathutils.Matrix.Rotation(angle * (index), 4, 'Z')
                T = mathutils.Matrix.Translation([0, 0, 0])     
                M = T @ R @ T.inverted()
                ob.location = M @ ob.location
                ob.rotation_euler.rotate(M)

def RA_Update_Offset(self, context):
    
    if self.RA_Status == True:              
        for ob in self.RA_Parent.children:      
            # define variables
            loc = mathutils.Vector((0.0, self.RA_Offset, 0.0))            
            rot = ob.rotation_euler
            # rotate location    
            loc.rotate(rot)
            # apply rotation
            ob.location = loc
    else:
        pass
#--------------------------------------------------------------------------------------#
class R_Array(bpy.types.Operator):  
    bl_idname = 'sop.r_array'
    bl_label = 'Radial Array'
    bl_description = 'Radial Array S.Operator'
    bl_options = {'REGISTER', 'UNDO'}

    
    
    
    #?Useless !?
    @classmethod
    def poll(cls, context):
       return True
    
    def execute(self, context):
        
        #Create Bpy.context Variable
        C = bpy.context
        active_object = C.active_object
        
        
        # call modal if RA_Status = True
        try:
            if active_object.RA_Status == True:
                bpy.ops.sop.ra_modal('INVOKE_DEFAULT')
                return {'FINISHED'}
        except:
            pass
        # Check Selected Cancel if NOT Mesh
        if C.selected_objects == [] or C.active_object.type != 'MESH':
            self.report({'INFO'}, "No Mesh Selected")
            return {'CANCELLED'}
        
        
        # Create Variables
        L_Objects = []                              # object list 
        ob = active_object                          # active object reference 
        ob_collections = ob.users_collection        # active Object collections
        f_name = ob.name                            # Object Name 
        point = ob.location.copy()                  # Middle point 
        is_col_new  = True

        
        # Create New Collection             
        if bpy.context.preferences.addons[__name__].preferences.col_toggle == True:
            for q in bpy.data.collections:
                if q.name == "RA -" + f_name:
                    collection = q
                    is_col_new = False
                    try:
                        for col in ob_collections:
                            col.objects.unlink(ob)
                        collection.objects.link(ob)
                    except:
                        pass
        
                
            if is_col_new == True:
                # create and link new collection
                collection = bpy.data.collections.new(name="RA -" + f_name)
                bpy.context.scene.collection.children.link(collection)
                print ("NEW")
                # Move Object to collection
                for col in ob_collections:
                    col.objects.unlink(ob)
                collection.objects.link(ob)
        else:
            collection = ob_collections[0]

        # Create/Location/Name/Status/set RA_Parent/Link Empty and other memery
        empty = bpy.data.objects.new( "empty", None )
        empty.location = point
        empty.name = ".RA - " + ob.name + " - Control Empty"
        empty.RA_Status = True
        empty.RA_Parent = empty
        empty.RA_Name = f_name
        empty.RA_Sel_Status = bpy.context.preferences.addons[__name__].preferences.selectable
        collection.objects.link(empty)
         
        # Move object
        ob.location[1] = ob.location[1] + ob.RA_Offset

        # Deselect Active Object and select Control Object
        ob.select_set(False)
        empty.select_set(True)

        # set empty as active object 
        bpy.context.view_layer.objects.active = empty

        # create duplicate objects
        for o in range(0, empty.RA_ObjNum):

            if o == 0:
                L_Objects.append(ob)
            if o != 0:
                L_Objects.append(ob.copy())
        # Add Objects To Collection
        for index, ob in enumerate(L_Objects):
            # create angle variable 
            angle = math.radians(360/empty.RA_ObjNum)

           
            # rotate object
            R = mathutils.Matrix.Rotation(angle * (index), 4, 'Z')
            T = mathutils.Matrix.Translation([0, 0, 0])     
            M = T @ R @ T.inverted()
            ob.location = M @ ob.location
            ob.rotation_euler.rotate(M)

            # Parent Object 
            ob.parent = empty
            empty.matrix_parent_inverse = ob.matrix_world.inverted()
            ob.RA_Parent = empty

            # make objects selectable/unselectable
            if empty.RA_Sel_Status == True:
                ob.hide_select = False
            if empty.RA_Sel_Status == False:
                ob.hide_select = True

            # Change Object Name
            ob.name = "RA - " + str(f_name) + " - " + str(index)
            # Set RA Status
            ob.RA_Status = True
            
            # Link object
            try:
                collection.objects.link(ob)
                #print ("For LINK")
            except:
                #print ("PASS Linking object to collection failed")
                pass
        bpy.ops.sop.ra_modal('INVOKE_DEFAULT')
        
        return {'FINISHED'} 
#--------------------------------------------------------------------------------------#
class RA_Modal(bpy.types.Operator):
    # Change Radial Array
    bl_idname = "sop.ra_modal"
    bl_label = "Radial Array Modal"
    bl_options = {"REGISTER", "UNDO", "BLOCKING", "GRAB_CURSOR", "INTERNAL"} #- add later!?  

    first_mouse_x: IntProperty()
    I_RA_Offset: FloatProperty()
    I_RA_ObjNum: IntProperty()
    unq_mode: BoolProperty()
    

    def modal(self, context, event):
        
        # context shortcut
        C = context
        OB = C.object
        context.area.tag_redraw() #?
        prefs = bpy.context.preferences.addons[__name__].preferences
        # -------------------------------------------------------------#     
        #+ change offset        
        if event.type == 'MOUSEMOVE' :
            delta = self.first_mouse_x - event.mouse_x
            if event.shift:
                C.object.RA_Offset = round((self.I_RA_Offset + delta * 0.01))
            else:
                C.object.RA_Offset = self.I_RA_Offset + delta * 0.01
         # -------------------------------------------------------------#
        #+ add/remove Objects      
        if event.type == 'WHEELUPMOUSE' and OB.RA_Unq_mode == False:
            OB.RA_ObjNum = OB.RA_ObjNum + 1
            
        if event.type == 'WHEELDOWNMOUSE' and OB.RA_Unq_mode == False:
            OB.RA_ObjNum = OB.RA_ObjNum - 1
        # -------------------------------------------------------------#
        #+ call the tarnslation operator
        if event.type == 'G' and event.value == "PRESS":
               
            C.tool_settings.use_snap = True
            C.tool_settings.snap_elements = {'FACE'}
            C.tool_settings.use_snap_align_rotation = True
           
            bpy.ops.transform.translate('INVOKE_DEFAULT')
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        # -------------------------------------------------------------#
        
        #+ join objects               
        if event.type == 'J' and event.value == "PRESS":
            objects = OB.RA_Parent.children
            location = OB.RA_Parent.location
            cursor_location = bpy.context.scene.cursor.location.copy()
            
            # deselect objects and select control object
            for o in C.selected_objects:
                o.select_set(False)
            C.object.RA_Parent.hide_select = False
            bpy.context.view_layer.objects.active = C.object.RA_Parent
            C.object.RA_Parent.select_set(True)
            
            # Delete control object 
            bpy.ops.object.delete()

            for ob in objects:
                ob.hide_select = False
                ob.select_set(True)
            bpy.context.view_layer.objects.active = objects[0]
            
                      
            bpy.context.scene.cursor.location = location
            bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)                 
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')             
            bpy.ops.object.join()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.context.scene.cursor.location = cursor_location 
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        # -------------------------------------------------------------#      
        
        #+ Reset                   
        if event.type == 'R' and event.value == "PRESS":
            
            objects = OB.RA_Parent.children
            name = OB.RA_Parent.RA_Name
            # deslect all objects
            for o in C.selected_objects:
                o.select_set(False)
            # select objects
            for ob in objects:
               if ob != objects[0]:
                    ob.hide_select = False
                    ob.select_set(True) 
            # delete objects
            bpy.ops.object.delete()
                
            # select object and clear parent and other memery
            objects[0].location = objects[0].RA_Parent.location   
            objects[0].RA_Parent.select_set(True)
            bpy.ops.object.delete()
            objects[0].hide_select = False
            bpy.context.view_layer.objects.active = objects[0]
            objects[0].select_set(True)
            objects[0].parent = None
            objects[0].name = name
            try:
                del objects[0]["RA_Parent"]
                del objects[0]["RA_Status"]
            except:
                pass
            
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}
        #+ Apply                   
        if event.type == 'A' and event.value == "PRESS":
            
            objects = OB.RA_Parent.children
            # deslect all objects
            for o in C.selected_objects:
                o.select_set(False)
            # select and delete control object
            objects[0].RA_Parent.select_set(True)
            bpy.ops.object.delete()
            # select objects    
            for ob in objects:
            
               ob.hide_select = False
               ob.select_set(True)
               ob.RA_Status = False
               ob.parent = None

            bpy.context.view_layer.objects.active = objects[0]
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}    
        #+ Make Unique Mode toggle
        if event.type == 'Q' and event.value == "PRESS":
            objects = OB.RA_Parent.children
            if OB.RA_Unq_mode == True:
                for ob in objects:
                    ob.data = objects[0].data
                OB.RA_Unq_mode = False
            else:
            #* make unique data    
                for ob in objects:
                    ob.data = ob.data.copy()
                OB.RA_Unq_mode = True
        #+ Selectable toggle
        if event.type == 'S' and event.value == "PRESS":
            if OB.RA_Sel_Status == True:
                OB.RA_Sel_Status = False
            else:
                OB.RA_Sel_Status = True
        #+ Help Mode toggle
        if event.type == 'H' and event.value == "PRESS":
            if prefs.modal_help == True:
                prefs.modal_help = False
            else:
                prefs.modal_help = True
        # -------------------------------------------------------------# 
        #+ Finish/Cancel Modal        
        elif event.type == 'LEFTMOUSE':
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            C.object.RA_Offset = self.I_RA_Offset
            C.object.RA_ObjNum = self.I_RA_ObjNum
            bpy.types.SpaceView3D.draw_handler_remove(self.ra_draw_b, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # context shortcut
        C = context
        if  C.object.RA_Status == True:
            for o in C.selected_objects:
                o.select_set(False)
            bpy.context.view_layer.objects.active = C.object.RA_Parent
            C.object.RA_Parent.select_set(True)
           
            
        
        if C.object:
            # set initial Variable values
            self.first_mouse_x = event.mouse_x
            self.I_RA_Offset = C.object.RA_Offset
            self.I_RA_ObjNum = C.object.RA_ObjNum
            self.unq_mode = C.object.RA_Unq_mode
            self.prefs = bpy.context.preferences.addons[__name__].preferences
            ###-------------------------------------------###
            args = (self, context, self.prefs)
            
            
            self.ra_draw_b = bpy.types.SpaceView3D.draw_handler_add(RA_draw_B, args, 'WINDOW', 'POST_PIXEL')
            self._handle = bpy.types.SpaceView3D.draw_handler_add(RA_modal_Draw, args, 'WINDOW', 'POST_PIXEL')
            
            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}
#--------------------------------------------------------------------------------------#
class RA_Prefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    # here you define the addons customizable props
    offset:     bpy.props.FloatProperty(default=5)
    objnum:     bpy.props.IntProperty(default=6)
    selectable: bpy.props.BoolProperty(default= True, description="False = Only Control Object is selectable")
    modal_help: bpy.props.BoolProperty(default= False, description="True = Display Help text in modal")
    col_toggle: bpy.props.BoolProperty(default= False, description="True = Create New Collection")
    # here you specify how they are drawn
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        split = box.split()
        col = split.column() 
        # Layout ---------------------------------------------------------------- #
        col.label(text="Default Values:")
        col.prop(self, "offset",text="Default Offset")
        col.prop(self, "objnum",text="Default Count")
        col.prop(self, "selectable",text="Selectable")
        col.prop(self, "modal_help",text="Modal Help")
        col.label(text ="Options:")
        col.prop(self, "col_toggle",text="Create New Collection")
        col.label(text="Keymap:")
        
        
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps['Object Mode']
        #kmi = km.keymap_items[0]
        kmi = get_hotkey_entry_item(km, 'sop.r_array', 'sop.r_array')
        
        if addon_keymaps:
            km = addon_keymaps[0].active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

    

def get_addon_preferences():
    ''' quick wrapper for referencing addon preferences '''
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences
def get_hotkey_entry_item(km, kmi_name, kmi_value):
    '''
    returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
    if there are multiple hotkeys!)
    '''
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].idname == kmi_value:
                return km_item
    return None 

classes = (
    RA_Prefs,
    R_Array,
    RA_Modal,
)


def register():
    print ("----------------------------------")
    print ("S.Ops Init")
    print ("----------------------------------")
    
    #+ add hotkey
    add_hotkey()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Init Props 
    
    bpy.types.Object.RA_Parent = bpy.props.PointerProperty(
    name="RA Parent",
    description="RA Parent Object Reference",
    type=bpy.types.Object
    )

    bpy.types.Object.RA_ObjNum = bpy.props.IntProperty(
    name="RA ObjNum",
    description="RA Object Number",
    default = bpy.context.preferences.addons[__name__].preferences.objnum,
    min = 1,
    update = RA_Update_ObjNum
    )
   
    bpy.types.Object.RA_Offset = bpy.props.FloatProperty(
    name="Offset",
    description="Radial Array Offset",
    default = bpy.context.preferences.addons[__name__].preferences.offset,
    update = RA_Update_Offset
    )   
       
    bpy.types.Object.RA_Status = bpy.props.BoolProperty(
    name="Status",
    description="Radial Array Status",
    default = False
    )
    
    bpy.types.Object.RA_Sel_Status = bpy.props.BoolProperty(
    name="Selectable",
    description="False = Only Control Object is selectable",
    default = bpy.context.preferences.addons[__name__].preferences.selectable,
    update = RA_Update_Sel_Status
    )

    bpy.types.Object.RA_Unq_mode = bpy.props.BoolProperty(
    name="Unique Mode",
    description="True = all objects have a unique data block(Disables Count in Modal)",
    default = False
    )
    bpy.types.Object.RA_Name = bpy.props.StringProperty(
    name="Name",
    description="Radial Array Name",
    default = "Nameing Error"
    )
    
   
    print ("----------------------------------")
    print ("S.Ops Register End")
    print ("----------------------------------") 


def unregister():
    print ("----------------------------------")
    print ("S.Ops unRegister Start")
    print ("----------------------------------") 
    #+ remove hotkey
    remove_hotkey()
    
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
  

 
   
    
    print ("----------------------------------")
    print ("S.Ops unRegister End")
    print ("----------------------------------") 
  
if __name__ == "__main__":
    register()





