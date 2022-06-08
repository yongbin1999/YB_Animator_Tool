import bpy
from ..Operators.Output import (

    keys_output

)


# 指定UI在面板上绘制
class UI_PT_KEYS_RENDER(bpy.types.Panel):
    """序列帧渲染_YB"""  # 这个是面板注释
    bl_label = "序列帧渲染_YB"  # 面板的名字
    bl_idname = "UI_PT_KEYS_RENDER"  # 唯一标识符，不可重复
    bl_space_type = 'PROPERTIES'  # 在属性面板绘制
    bl_region_type = 'WINDOW'
    bl_context = "data"  # 渲染窗口下的物体选项卡

    # 主要绘制部分

    def draw(self, context):

        layout = self.layout

        # 获取当前场景名
        scene = bpy.context.scene

        # 获取渲染路径
        file = scene.render
        # 切分面板
        row = layout.row()

        # 暴露属性
        row = layout.row()
        row.prop(file, "filepath")

        # 执行渲染操作
        row = layout.row()
        row.scale_y = 1.5
        row.operator("keys.output", icon='EXPORT', text="全选导出关键帧")

    # 注册

    def register():

        bpy.utils.register_class(keys_output)

    # 注销

    def unregister():

        bpy.utils.unregister_class(keys_output)
