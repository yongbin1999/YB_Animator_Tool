import bpy
import csv
import os
import datetime


class KEYS_OT_output(bpy.types.Operator):
    """逐帧渲染蜡笔动画关键帧"""
    bl_idname = "keys.output"
    bl_label = "Export Keyframes"
    bl_description = "Render Grease Pencil keyframes frame by frame\n(Make sure the Grease Pencil object is selected)"

    def execute(self, context):
        # 检查当前选中对象
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "未选中任何对象")
            return {'CANCELLED'}

        # 检查是否为蜡笔对象 - 更新检测逻辑
        if not (obj.type == 'GREASE_PENCIL' or
                (hasattr(obj.data, 'layers') and hasattr(obj.data, 'stroke_depth_order'))):
            self.report({'ERROR'}, "请选择一个蜡笔对象")
            return {'CANCELLED'}

        # 获取蜡笔数据
        gp_data = obj.data
        if not gp_data or not hasattr(gp_data, 'layers'):
            self.report({'ERROR'}, "无效的蜡笔数据")
            return {'CANCELLED'}

        # 检查是否有图层
        if len(gp_data.layers) == 0:
            self.report({'ERROR'}, "蜡笔对象没有任何图层")
            return {'CANCELLED'}

        # 发出提示
        def draw(self, context):
            self.layout.label(text="Started")
        context.window_manager.popup_menu(draw)

        # 获取当前场景
        scene = context.scene

        # 渲染设置
        film_transparent = scene.render.film_transparent
        scene.render.film_transparent = True
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.image_settings.color_depth = '16'
        scene.render.image_settings.compression = 0

        # 处理渲染路径
        render_filepath = bpy.path.abspath(scene.render.filepath)
        if not render_filepath.endswith(os.sep):
            render_filepath += os.sep

        # 更新场景渲染路径
        scene.render.filepath = render_filepath
        print("Updated render filepath:", scene.render.filepath)

        # 标准化路径
        if render_filepath.startswith("/"):
            render_filepath = "C:" + render_filepath
        if not (render_filepath.endswith("/") or render_filepath.endswith("\\")):
            render_filepath += "/"

        # 获取图层信息
        GPLayer_List = [layer.name for layer in gp_data.layers]
        GPLayer_sum = len(GPLayer_List)

        # 获取Blender工程设置的时间范围
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        frame_count = frame_end - frame_start + 1

        print(f"工程设置的帧范围: {frame_start} - {frame_end}, 总帧数: {frame_count}")

        # 计算序列号所需的位数 (工程帧数的位数+3)
        digits = len(str(frame_end)) + 3
        print(f"序列号格式将使用 {digits} 位数字")

        # 初始化行和列
        def Create_List(I, J):
            List = []
            for i in range(I):
                List.append([])
                for j in range(J):
                    List[i].append('')
            return List

        # 初始化数据结构
        Layer_TAG = getattr(context.scene, 'layer_tag',
                            'Layer')  # 使用默认值，防止属性不存在
        Frame = ['Frame', Layer_TAG]
        header = Create_List(GPLayer_sum+2, 0)

        # 确保数据数组的大小严格匹配帧范围
        data = Create_List(frame_count, GPLayer_sum+2)

        # 初始化数据 - 使用Blender设置的帧范围
        for i in range(frame_count):
            data[i][0] = frame_start + i  # 从起始帧开始
        for i in range(GPLayer_sum+2):
            header[i] = ''

        # 保存所有图层组和图层的初始可见状态
        original_group_visibility = {}
        original_layer_visibility = {}

        # 记录图层和图层组的可见性状态
        for i, layer_name in enumerate(GPLayer_List):
            layer = gp_data.layers[layer_name]
            original_layer_visibility[layer_name] = layer.hide
            header[i+1] = layer_name

        if hasattr(gp_data, 'layer_groups'):
            for group in gp_data.layer_groups:
                original_group_visibility[group.name] = group.hide
                # 临时显示所有图层组
                group.hide = False

        # 获取文件命名所需信息
        obj_name = obj.name
        data_name = gp_data.name

        # 获取Blender工程文件名
        blend_filename = bpy.path.basename(bpy.data.filepath)
        if not blend_filename:  # 如果文件未保存
            project_name = "未命名项目"
        else:
            project_name = os.path.splitext(blend_filename)[0]  # 去除扩展名

        # 创建输出文件夹名称
        output_folder_name = f"{project_name}_{obj_name}"

        # 开始进度条
        total_frames = frame_count * GPLayer_sum  # 总帧数
        bpy.context.window_manager.progress_begin(0, total_frames)

        # 循环处理每个图层
        for i in range(GPLayer_sum):
            layer_name = GPLayer_List[i]
            layer = gp_data.layers[layer_name]

            # 设置当前图层为活动图层
            try:
                gp_data.layers.active = layer
            except:
                # 如果上面的方法失败，使用替代方法
                for idx, l in enumerate(gp_data.layers):
                    if l.name == layer_name:
                        l.active = True
                    else:
                        l.active = False

            # 获取所在蜡笔图层索引
            GPLayer_index = i + 1

            # 暂时隐藏所有图层，只显示当前图层
            for l in gp_data.layers:
                l.hide = (l.name != layer_name)

            # 帧计数
            keysname = 1

            # 强制跳转到工程设置的起始帧
            scene.frame_set(frame_start)

            # 查找当前图层在起始帧及之后的第一个关键帧
            found_first_keyframe = False
            current_frame = frame_start

            # 先检查起始帧是否就是关键帧
            if hasattr(layer, 'frames') and any(f.frame_number == frame_start for f in layer.frames):
                found_first_keyframe = True
                print(f"在起始帧 {frame_start} 找到关键帧")
            else:
                # 尝试跳到下一个关键帧
                scene.frame_set(frame_start - 1)  # 先设置到起始帧前一帧
                bpy.ops.screen.keyframe_jump(next=True)  # 尝试跳到下一个关键帧

                # 检查是否找到了关键帧，以及是否在范围内
                if scene.frame_current <= frame_end:
                    found_first_keyframe = True
                    current_frame = scene.frame_current
                    print(f"找到第一个关键帧: {current_frame}")
                else:
                    print(f"在指定帧范围 {frame_start}-{frame_end} 内未找到关键帧")

            # 如果没有在范围内找到关键帧，就直接跳过这个图层
            if not found_first_keyframe:
                print(f"图层 {layer_name} 在指定帧范围内没有关键帧，跳过渲染")
                continue

            print(f"开始渲染图层 {layer_name} 的关键帧，从帧 {current_frame} 开始")

            # 开始渲染当前图层的关键帧
            while True:
                # 当前帧号
                current_frame = scene.frame_current

                # 检查是否超出帧范围
                if current_frame > frame_end or current_frame < frame_start:
                    print(
                        f"跳过帧 {current_frame}，超出指定范围 {frame_start}-{frame_end}")
                    break

                # 使用指定位数格式化序列号
                formatted_keysname = str(keysname).zfill(digits)

                # 创建输出路径
                output_path = os.path.join(
                    render_filepath,
                    output_folder_name,
                    layer_name,
                    f"{layer_name}_{formatted_keysname}"
                )
                scene.render.filepath = output_path

                # 确保输出目录存在
                os.makedirs(os.path.dirname(
                    scene.render.filepath), exist_ok=True)

                # 渲染图片
                bpy.ops.render.render(animation=False, write_still=True)

                # 还原渲染路径
                scene.render.filepath = render_filepath

                # 记录关键帧位置 - 调整为从起始帧开始计算
                data_index = current_frame - frame_start
                print(
                    f"处理帧 {current_frame}，数据索引 {data_index}，关键帧编号 {formatted_keysname}")

                if 0 <= data_index < frame_count:
                    data[data_index][GPLayer_index] = keysname
                else:
                    print(f"警告: 索引 {data_index} 超出数据范围 0-{frame_count-1}")

                # 记录当前帧位置，用于检测是否已到最后一帧
                previous_frame = current_frame

                # 跳转到下一个关键帧
                bpy.ops.screen.keyframe_jump(next=True)
                keysname += 1

                # 检测是否处在结尾帧 (如果帧号未变，说明已经是最后一帧)
                if previous_frame == scene.frame_current:
                    break

                # 更新进度条
                bpy.context.window_manager.progress_update(i * frame_count + keysname)

            # 还原图层可见性
            for l in gp_data.layers:
                l.hide = original_layer_visibility[l.name]

        # 还原图层组可见性
        if hasattr(gp_data, 'layer_groups'):
            for group in gp_data.layer_groups:
                group.hide = original_group_visibility[group.name]

        # 还原渲染设置
        scene.render.film_transparent = film_transparent

        # 创建输出目录
        csv_dir = os.path.join(render_filepath, output_folder_name)
        os.makedirs(csv_dir, exist_ok=True)

        # 文件命名格式：物体名称_数据块名称.csv
        csv_filename = f"{obj_name}_{data_name}.csv"
        csvfile = os.path.join(csv_dir, csv_filename)

        # 导出CSV文件
        self.export_csv(csvfile, data, header, Frame)

        # 添加时间范围信息到JSON导出参数
        time_range = {"frame_start": frame_start, "frame_end": frame_end}

        # 从LayerHierarchyExporter模块导入JSON结构数据导出功能
        try:
            from .LayerHierarchyExporter import export_layer_json
            json_success, json_message = export_layer_json(
                render_filepath,
                obj,
                gp_data,
                output_folder_name,
                f"{obj_name}_{data_name}",
                time_range
            )
            if json_success:
                self.report({'INFO'}, json_message)
        except Exception as e:
            self.report({'ERROR'}, f"导出JSON结构时出错: {str(e)}")

        self.report({'INFO'}, f"渲染完成！已导出 {GPLayer_sum} 个图层的关键帧")

        # 结束进度条
        bpy.context.window_manager.progress_end()

        return {'FINISHED'}

    def export_csv(self, csvfile, frame_data, header_data, frame_col_titles):
        """
        导出CSV文件

        参数:
            csvfile: CSV文件路径
            frame_data: 帧数据
            header_data: 表头数据
            frame_col_titles: 列标题 ['Frame', 'Layer']
        """
        try:
            with open(csvfile, 'w', encoding='gbk', errors='replace', newline='') as f:
                writer = csv.writer(f)

                # 写入标题行
                writer.writerow(frame_col_titles)

                # 写入图层名称行
                writer.writerow(header_data)

                # 导出所有帧的数据，按照Blender工程设置的帧范围
                for row in frame_data:
                    writer.writerow(row)

            print(f"成功导出CSV文件到: {csvfile}")
        except Exception as e:
            print(f"CSV导出错误: {str(e)}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
