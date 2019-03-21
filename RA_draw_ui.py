import bpy
import gpu
import blf
from gpu_extras.batch import batch_for_shader


def RA_modal_Draw(self, context, prefs):
    height = bpy.context.region.height
    width = bpy.context.region.width
    CO = context.object
    
    font_id = 0

    #+ text
    if CO.RA_Unq_mode == True:
        blf.color (font_id,0.9,0.32,0.35,1)
    else:
        blf.color (font_id,0.85,0.85,0.85,1)
    #* Offset
    blf.position(font_id, (width/2) - 200, (height/2) - 250, 0)
    blf.size(font_id, 20, 60)
    blf.draw(font_id, ("{} {}".format("Offset: ",str(round(CO.RA_Offset, 2)))) )
        
    #* Object Selectable
    blf.position(font_id, (width/2) + 50, (height/2) - 250, 0)    
   
    blf.draw(font_id, ("{} {}".format("Selectable: ",str(CO.RA_Sel_Status))) )
    
    #* Object Number "Count"
    blf.position(font_id, (width/2) - 50, (height/2) - 250, 0)
    if CO.RA_Unq_mode == True:
        blf.color (font_id,0.5,0.5,0.5,1)
    else:
        blf.color (font_id,0.85,0.85,0.85,1)
 
    blf.draw(font_id, ("{} {}".format("Count: ",str(round(CO.RA_ObjNum, 2)))) )    
    #* Show/Hide Help
    blf.color (font_id,1,1,1,1)
    text = "Show/Hide Help 'H'"
    blf.position(font_id, (width/2 - blf.dimensions(font_id, text)[0] / 2), (height/2) - 230, 0)
   
    blf.draw(font_id, text)
    #+--------------------------------------------------------------+#
    #* Unique Mode
    blf.color (font_id,0.8,0.4,0.0,1)
    text = "Unique Mode: "
    blf.position(font_id, (width/2 - 84), (height/2) - 270, 0)
    blf.draw(font_id, text)
    #-------------------------#
    if CO.RA_Unq_mode == True:
        blf.color (font_id,0.1,0.94,0.4,1)
        unq_text = "Active"
    else:
        blf.color (font_id,0.6,0.1,0.0,1)
        unq_text = "--------"
    blf.position(font_id, (width/2 + 34), (height/2) - 270, 0)
    blf.draw(font_id, unq_text)
    #+--------------------------------------------------------------+#
    #* Help
    blf.color (font_id,0.6,1,0.6,1)
    if prefs.modal_help == True:
        lines = ["Reset 'R'",
        "Apply 'A'",
        "Join 'J' ends radial mode and merges all objects",
        "Grab 'G'",
        "Unique Mode 'Q' unlinks objects data block",
        "'RMB' and Esc to Cancel",
        "'Shift' to snap offset",
        "'Mouse Wheel' Increase/Decrease Count"
        ]
        for index, l  in enumerate(lines):
            text = l
            blf.position(font_id, (width/2) - 200, (height/2 -200) + 20 * index, 0)
           
            blf.draw(font_id, text)

def RA_draw_B(self, context, prefs):
    height = bpy.context.region.height
    width = bpy.context.region.width
    CO = bpy.context.object
    #+-----------------------------------------------------------------------+#
    vertices = (
    (width/2 - 80 , height/2 - 215),(width/2 + 80, height/2 - 215),
    (width/2 - 90, height/2 - 233),( width/2 + 90, height/2 - 233) ) 

    indices = (
        (0, 1, 2), (2, 1, 3))
    
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    
    shader.bind()
    
    shader.uniform_float("color", (0.8,0.4,0.0,1))
    batch.draw(shader)
    #+-----------------------------------------------------------------------+#
    vertices = (
    (width/2 - 216 , height/2 - 234),(width/2 + 206, height/2 - 234),
    (width/2 - 220, height/2 - 254),( width/2 + 200, height/2 - 254) ) 

    indices = (
        (0, 1, 2), (2, 1, 3))
    
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    
    
    
    shader.bind()
    shader.uniform_float("color", (0.15,0.15,0.15,1))
    batch.draw(shader)
    #+-----------------------------------------------------------------------+#
    vertices = (
    (width/2 - 96 , height/2 - 253),(width/2 + 96, height/2 - 253),
    (width/2 - 86, height/2 - 274),( width/2 + 86, height/2 - 274) ) 

    indices = (
        (0, 1, 2), (2, 1, 3))
    
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    
    shader.bind()
    shader.uniform_float("color", (0.15,0.15,0.15,1))
    batch.draw(shader)