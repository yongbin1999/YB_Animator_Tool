from .Ui.Ui import UI_PT_KEYS_RENDER
import bpy
bl_info = {
    "name": "蜡笔绘画工具",
    "author": "YB(通过点击下方文档，可以进入插件主页，查看更新状况)",
    "description": "方便于二维作画(导出前，请全选时间轴左下角的蜡笔图层)",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "蜡笔层右侧层属性(后续将会开发更多二维作画工具)",
    "warning": "",
    "category": "YB_Animator",
    "doc_url": "https://github.com/yongbin1999/YB_Animator_Tool"
}


# 注册
def register():

    bpy.utils.register_class(UI_PT_KEYS_RENDER)

    print("启动插件")


# 注销
def unregister():

    bpy.utils.unregister_class(UI_PT_KEYS_RENDER)

    print("关闭插件")
