import bpy
from .Ui.Ui import RENDER_OT_open_keys_render_popup
from .Operators.Output import KEYS_OT_output

bl_info = {
    "name": "YB_Animator_Tool",
    "author": "YB_",
    "description": "Tool for Blender animation,export grease pencil layers as keyframes and CSV",
    "blender": (4, 0, 0),
    "version": (1, 1, 3),
    "location": "Crayon Keyframe Rendering is in the render menu at the top",
    "warning": "",
    "category": "YB_Animator",
    "doc_url": "https://github.com/yongbin1999/YB_Animator_Tool"
}


class YBAnimatorPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    layer_tag: bpy.props.StringProperty(
        name="Layer Tag",
        default="Keys",
        update=lambda self, context: update_layer_tag(context)
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "layer_tag")

# Update callback function


def update_layer_tag(context):
    prefs = bpy.context.preferences.addons[__name__].preferences
    bpy.types.Scene.layer_tag = prefs.layer_tag


def render_menu_func(self, context):
    self.layout.operator(
        RENDER_OT_open_keys_render_popup.bl_idname, icon='RENDER_STILL')

# Registration


def register():
    bpy.utils.register_class(YBAnimatorPreferences)
    bpy.utils.register_class(KEYS_OT_output)
    bpy.utils.register_class(RENDER_OT_open_keys_render_popup)
    bpy.types.TOPBAR_MT_render.append(render_menu_func)

    addon_prefs = bpy.context.preferences.addons[__name__].preferences
    bpy.types.Scene.layer_tag = bpy.props.StringProperty(
        name="Layer Tag",
        default=addon_prefs.layer_tag
    )


def unregister():
    bpy.utils.unregister_class(YBAnimatorPreferences)
    bpy.utils.unregister_class(KEYS_OT_output)
    bpy.utils.unregister_class(RENDER_OT_open_keys_render_popup)
    bpy.types.TOPBAR_MT_render.remove(render_menu_func)
    del bpy.types.Scene.layer_tag


if __name__ == "__main__":
    register()
