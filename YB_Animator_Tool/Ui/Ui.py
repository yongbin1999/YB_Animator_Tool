import bpy
from ..Operators.Output import KEYS_OT_output

class RENDER_OT_open_keys_render_popup(bpy.types.Operator):
    """打开关键帧渲染"""
    bl_idname = "render.open_keys_render_popup"
    bl_label = "Crayon Keyframe Rendering"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="UI_MT_keys_render_settings")
        return {'FINISHED'}

# 窗口界面
class UI_MT_keys_render_settings(bpy.types.Menu):
    bl_label = "Keyframe Rendering Settings"
    bl_idname = "UI_MT_keys_render_settings"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Basic Settings:")
        row = box.row()

        # 设置图层标识
        row.prop(context.scene, "layer_tag", text="LayerTag")
        # 渲染路径
        row.prop(context.scene.render, "filepath")
        # 执行渲染操作
        row = layout.row()
        row.scale_y = 3
        row.operator("keys.output", icon='EXPORT', text="Render Crayon Keyframes")

