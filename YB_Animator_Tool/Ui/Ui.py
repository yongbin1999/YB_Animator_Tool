import bpy
from ..Operators.KeyframeRenderer import KEYS_OT_output

class RENDER_OT_open_keys_render_popup(bpy.types.Operator):
    """渲染蜡笔关键帧"""
    bl_idname = "render.open_keys_render_popup"
    bl_label = "Crayon Keyframe Rendering"

    def execute(self, context):
        # 检查是否选择了蜡笔对象
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "未选中任何对象")
            return {'CANCELLED'}
        
        # 在 Blender 4.3 中检查是否为蜡笔对象
        if not (obj.type == 'GREASE_PENCIL' or 
                (hasattr(obj.data, 'layers') and hasattr(obj.data, 'stroke_depth_order'))):
            self.report({'ERROR'}, "请先选择一个蜡笔对象")
            return {'CANCELLED'}
            
        bpy.ops.keys.output('INVOKE_DEFAULT')
        return {'FINISHED'}