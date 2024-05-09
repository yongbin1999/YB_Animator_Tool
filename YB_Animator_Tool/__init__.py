import bpy
from .Ui.Ui import RENDER_OT_open_keys_render_popup, UI_MT_keys_render_settings
from .Operators.Output import KEYS_OT_output

bl_info = {
    "name": "YB动画工具",
    "author": "YB(通过点击下方文档，可以进入插件主页，查看更新状况)",
    "description": "用于blender动画",
    "blender": (4, 0, 0),
    "version": (1, 1, 0),
    "location": "蜡笔关键帧渲染在顶部渲染菜单中",
    "warning": "",
    "category": "YB_Animator",
    "doc_url": "https://github.com/yongbin1999/YB_Animator_Tool"
}

def render_menu_func(self, context):
    self.layout.operator(RENDER_OT_open_keys_render_popup.bl_idname, icon='RENDER_STILL')

# 注册
def register():
    bpy.utils.register_class(KEYS_OT_output)
    bpy.utils.register_class(RENDER_OT_open_keys_render_popup)
    bpy.utils.register_class(UI_MT_keys_render_settings)
    bpy.types.TOPBAR_MT_render.append(render_menu_func)
    bpy.types.Scene.layer_tag = bpy.props.StringProperty(
        name="Layer Tag",
        default="动画"
    )

def unregister():
    bpy.utils.unregister_class(KEYS_OT_output)
    bpy.utils.unregister_class(RENDER_OT_open_keys_render_popup)
    bpy.utils.unregister_class(UI_MT_keys_render_settings)
    bpy.types.TOPBAR_MT_render.remove(render_menu_func)
    del bpy.types.Scene.layer_tag


