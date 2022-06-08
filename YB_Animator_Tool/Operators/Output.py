import bpy
import csv


class keys_output(bpy.types.Operator):
    """逐帧渲染蜡笔动画关键帧"""
    bl_idname = "keys.output"
    bl_label = "导出关键帧"
    bl_description = "逐帧渲染蜡笔动画关键帧\n(多层导出需要全选时间轴左侧的蜡笔图层)"


    def execute(self, context):
        
        # 发出提示
        def draw(self, context):
            self.layout.label(text="开始运行")
        bpy.context.window_manager.popup_menu(draw)
        # bpy.types.BlendData.temp_data()
        #bpy.context.space_data.context = 'DATA'
        # 获取当前场景名
        scene = bpy.context.scene

        #渲染设置
        film_transparent=True
        scene.render.image_settings.color_mode = 'RGBA'
        scene.render.image_settings.color_depth = '16'
        scene.render.image_settings.compression = 0
        if scene.render.film_transparent == False:
            scene.render.film_transparent = True
            film_transparent=False

        # 保存一份渲染路径
        render_filepath = scene.render.filepath
        print(render_filepath)
        if render_filepath[0:1] == "/":
            render_filepath = "C:"+render_filepath
        if render_filepath.endswith("/") or render_filepath.endswith("\\") is not True:
            render_filepath += "/"

        # 获取当前选中蜡笔
        Layer = bpy.context.object.data.name_full

        # 蜡笔图层列表
        GPLayer_List = bpy.data.grease_pencils[Layer].layers.keys()[:]

        # 蜡笔图层总数
        GPLayer_sum = len(GPLayer_List)

        # 获取结束帧
        frame_end = scene.frame_end

        # 初始化行和列
        def Create_List(I, J):
            List = []
            for i in range(I):
                List.append([])  # List.append()为在列表后面追加元素
                for j in range(J):
                    List[i].append('')
            return List
        Frame = ['Frame', '动画']
        header = Create_List(GPLayer_sum+2, 0)
        data = Create_List(frame_end+5, GPLayer_sum+2)
        for i in range(frame_end):
            data[i][0] = i+1
        for i in range(GPLayer_sum+2):
            header[i] = ''

        # 获取当前选中图层名
        #Layer = bpy.context.object.data.name_full

        # 跳转到第0层
        bpy.ops.gpencil.layer_active(layer=0)
        print(scene.frame_current)
        # 检测是否处在蜡笔模式
        if bpy.context.object.mode != 'PAINT_GPENCIL':
            bpy.ops.gpencil.paintmode_toggle()

        # 检测图层是否被隐藏
        Hide_True_Layer = []
        for i in range(GPLayer_sum):
            Hide_True_Layer.append(i+1)
            if bpy.context.object.data.layers[i].hide == True:
                print("Hide")
                header[i+1] = GPLayer_List[i]+"*Hide"
                Hide_True_Layer[i] = i
            else:
                header[i+1] = GPLayer_List[i]

        # 循环跳转图层
        for i in range(GPLayer_sum):
            bpy.ops.gpencil.layer_active(layer=i)

            print(bpy.data.grease_pencils[Layer].layers.active_note)

            # 获取所在蜡笔图层层数
            GPLayer_index = bpy.data.grease_pencils[Layer].layers.active_index+1

            # 获取当前选中蜡笔层
            GPLayer = bpy.data.grease_pencils[Layer].layers.active_note

            # 渲染时隐藏其他图层
            Hide_Layer = []
            for i in range(GPLayer_sum):
                Hide_Layer.append(i)
                if bpy.context.object.data.layers[i].hide == False:
                    if GPLayer_index-1 != i:
                        Hide_Layer[i] = i
                        bpy.context.object.data.layers[i].hide = True

            # 获取当前选中的关键帧
            # keys=scene.frame_current

            # 帧计数
            keysname = 1

            # 跳转到第一帧
            bpy.ops.screen.frame_jump(end=False)

            # 确认在第一帧
            bpy.ops.screen.keyframe_jump(next=True)
            bpy.ops.screen.keyframe_jump(next=False)
            print(scene.frame_current)

            # 屏蔽掉隐藏图层的渲染
            if header[GPLayer_index] != GPLayer+"*Hide":

                # 开始渲染
                for i in range(frame_end):

                    # 修改当前场景渲染路径
                    scene.render.filepath = render_filepath + "\ " + str(bpy.context.scene. name_full)+"_"+str(Layer) + "\ " + str(GPLayer) + "\ " + \
                        str(keysname)  # .zfill(5)

                    # 渲染图片
                    bpy.ops.render.render(animation=False, write_still=True)

                    # 还原渲染路径
                    scene.render.filepath = render_filepath

                    # 记录关键帧位置
                    logkeys = scene.frame_current

                    # 帧记录写入列表
                    data[logkeys-1][GPLayer_index] = keysname

                    # 跳转到下一个关键帧
                    bpy.ops.screen.keyframe_jump(next=True)
                    keysname += 1

                    # 检测是否处在结尾帧
                    if logkeys == scene.frame_current:
                        bpy.ops.screen.keyframe_jump(next=True)
                    if logkeys == scene.frame_current:
                        break

            # 还原对应的图层
            for i in range(GPLayer_sum):
                if Hide_Layer[i] == i:
                    bpy.context.object.data.layers[i].hide = False
                if Hide_True_Layer[i] == i:
                    bpy.context.object.data.layers[i].hide = True



        if film_transparent==False:
            scene.render.film_transparent = False

        # 创建CSV文件
        csvfile = render_filepath[:-1] + "\ " + str(bpy.context.scene. name_full)+"_"+str(Layer) + "\ " + \
            str(Layer)+ "." + "csv"
            
        # 将列表写入CSV文件
        with open(str(csvfile), 'w', encoding='ANSI', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(Frame)
            writer.writerow(header)
            writer.writerows(data)
            
        

        return {'FINISHED'}

        
   