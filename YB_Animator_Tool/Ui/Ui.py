import bpy
from ..Operators.Output import KEYS_OT_output

class RENDER_OT_open_keys_render_popup(bpy.types.Operator):
    """渲染蜡笔关键帧"""
    bl_idname = "render.open_keys_render_popup"
    bl_label = "Crayon Keyframe Rendering"

    def execute(self, context):
        bpy.ops.keys.output('INVOKE_DEFAULT')
        return {'FINISHED'}
