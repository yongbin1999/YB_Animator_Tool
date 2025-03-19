import bpy
import os
import json
import datetime

def get_layer_structure(obj, gp_data):
    """
    获取蜡笔图层的层次结构
    
    参数:
        obj: 当前选中的蜡笔对象
        gp_data: 蜡笔数据
        
    返回:
        包含完整层次结构的字典和原始可见性状态
    """
    # 记录所有图层和图层组的可见性状态
    original_layer_visibility = {}
    original_group_visibility = {}
    
    # 基本结构
    structure = {
        'name': obj.name,
        'type': obj.type,
        'hierarchical_structure': []  # 将用于存储嵌套结构
    }
    
    # 记录所有图层的信息，以便后续查找
    all_layers = {}
    for idx, layer in enumerate(gp_data.layers):
        # 获取图层的UI显示顺序索引
        ui_index = idx
        if hasattr(layer, 'info') and hasattr(layer.info, 'ui_order'):
            ui_index = layer.info.ui_order
        elif hasattr(layer, 'ui_order'):
            ui_index = layer.ui_order
        
        all_layers[layer.name] = {
            'name': layer.name,
            'visible': not layer.hide,
            'type': 'layer',
            'index': ui_index,  # 保存图层的显示顺序索引
            'frames': []   # 用于存储该图层的关键帧信息
        }
        original_layer_visibility[layer.name] = layer.hide
        
        # 收集图层的关键帧信息
        frame_list = []
        if hasattr(layer, 'frames'):
            for frame in layer.frames:
                frame_list.append(frame.frame_number)
        all_layers[layer.name]['frames'] = sorted(frame_list)
    
    # 尝试使用Blender 4.0+ 的API (首选方法)
    if hasattr(gp_data, 'tree_structure'):
        try:
            print("使用Blender 4.0+ tree_structure API获取图层结构")
            # 获取官方的树结构
            tree_data = gp_data.tree_structure()
            
            # 创建一个图层组字典用于快速查找
            all_groups = {}
            if hasattr(gp_data, 'layer_groups'):
                for idx, group in enumerate(gp_data.layer_groups):
                    all_groups[group.name] = {
                        'name': group.name,
                        'visible': not group.hide,
                        'type': 'group',
                        'index': idx,
                        'children': []
                    }
                    original_group_visibility[group.name] = group.hide
            
            # 转换树结构
            def convert_tree_item(item):
                if item.type == 'LAYER':
                    if item.name in all_layers:
                        return all_layers[item.name].copy()
                    else:
                        print(f"警告: 在all_layers中找不到图层 {item.name}")
                        return None
                elif item.type == 'GROUP':
                    if item.name in all_groups:
                        group_data = all_groups[item.name].copy()
                        group_data['children'] = []
                        
                        # 处理子元素
                        for child in item.children:
                            child_data = convert_tree_item(child)
                            if child_data:
                                group_data['children'].append(child_data)
                        
                        return group_data
                    else:
                        print(f"警告: 在all_groups中找不到组 {item.name}")
                        return None
                return None
            
            # 转换整个树
            root_items = []
            for item in tree_data:
                converted = convert_tree_item(item)
                if converted:
                    root_items.append(converted)
            
            # 使用官方API获取的结构
            structure['hierarchical_structure'] = root_items
            print(f"使用tree_structure API获取了 {len(root_items)} 个根项目")
            return structure, original_layer_visibility, original_group_visibility
            
        except Exception as e:
            print(f"使用tree_structure API出错: {str(e)}")
            print("回退到手动构建层次结构...")
    
    # 如果有图层组，使用手动方法构建层次结构
    print("使用手动方法构建图层层次结构")
    if hasattr(gp_data, 'layer_groups'):
        # 采用提供的方法获取层次结构
        
        # 首先创建图层组映射
        all_groups = {}
        for idx, group in enumerate(gp_data.layer_groups):
            # 获取组的UI显示顺序
            ui_index = idx
            if hasattr(group, 'info') and hasattr(group.info, 'ui_order'):
                ui_index = group.info.ui_order
            elif hasattr(group, 'ui_order'):
                ui_index = group.ui_order
            
            all_groups[group.name] = {
                'name': group.name,
                'visible': not group.hide,
                'type': 'group',
                'index': ui_index,  # 保存顺序索引
                'children': []  # 存储子项
            }
            original_group_visibility[group.name] = group.hide
        
        # 建立父子关系映射 (使用parent属性)
        parent_map = {}
        for group in gp_data.layer_groups:
            if hasattr(group, 'parent') and group.parent:
                parent_map[group.name] = group.parent.name
            else:
                parent_map[group.name] = None
            print(f"图层组: {group.name}, 父组: {parent_map[group.name]}")
        
        # 找出顶级(根)组
        root_groups = [g for g in gp_data.layer_groups if parent_map[g.name] is None]
        
        # 按索引排序根组
        root_groups.sort(key=lambda g: all_groups[g.name]['index'])
        
        # 递归构建层次结构的函数
        def build_group_structure(group):
            group_data = all_groups[group.name].copy()
            
            # 查找该组的子组
            child_groups = [g for g in gp_data.layer_groups 
                          if parent_map.get(g.name) == group.name]
            # 按索引排序子组
            child_groups.sort(key=lambda g: all_groups[g.name]['index'])
            
            # 查找该组包含的图层
            group_layers = []
            
            # 首先尝试直接从组获取图层
            if hasattr(group, 'layers'):
                # 某些版本直接有layers属性
                try:
                    for layer in group.layers:
                        if layer.name in all_layers:
                            group_layers.append(all_layers[layer.name].copy())
                except (AttributeError, TypeError):
                    # 如果直接访问失败，忽略错误继续使用其他方法
                    pass
            
            # 如果上述方法未找到图层，检查图层的parent属性
            if not group_layers:
                for layer in gp_data.layers:
                    if hasattr(layer, 'parent') and layer.parent:
                        if layer.parent.name == group.name:
                            group_layers.append(all_layers[layer.name].copy())
            
            # 打印诊断信息
            print(f"组 {group.name} 包含 {len(group_layers)} 个图层, {len(child_groups)} 个子组")
            
            # 按索引排序图层
            group_layers.sort(key=lambda l: l.get('index', 0))
            
            # 递归处理子组
            for child_group in child_groups:
                child_data = build_group_structure(child_group)
                group_data['children'].append(child_data)
            
            # 添加图层到当前组
            group_data['children'].extend(group_layers)
            
            return group_data
        
        # 从根组开始构建层次结构
        root_items = []
        for root_group in root_groups:
            root_data = build_group_structure(root_group)
            root_items.append(root_data)
        
        # 查找不属于任何组的独立图层
        independent_layers = []
        for layer_name, layer_data in all_layers.items():
            is_independent = True
            
            # 检查层是否有父组
            if hasattr(gp_data.layers[layer_name], 'parent') and gp_data.layers[layer_name].parent:
                is_independent = False
            else:
                # 检查所有组的layers属性中是否包含此图层
                for group in gp_data.layer_groups:
                    if hasattr(group, 'layers'):
                        try:
                            if any(l.name == layer_name for l in group.layers):
                                is_independent = False
                                break
                        except (AttributeError, TypeError):
                            # 忽略错误继续检查
                            continue
            
            if is_independent:
                independent_layers.append(layer_data.copy())
        
        # 按索引排序独立图层
        independent_layers.sort(key=lambda l: l.get('index', 0))
        print(f"发现 {len(independent_layers)} 个独立图层")
        
        # 将独立图层添加到结构中
        root_items.extend(independent_layers)
        
        structure['hierarchical_structure'] = root_items
    else:
        # 如果没有图层组，直接添加所有图层，按索引排序
        all_layers_list = [data.copy() for _, data in all_layers.items()]
        all_layers_list.sort(key=lambda l: l.get('index', 0))
        structure['hierarchical_structure'] = all_layers_list
        print(f"无图层组，共发现 {len(all_layers_list)} 个图层")
    
    return structure, original_layer_visibility, original_group_visibility

def validate_structure(structure_data, gp_data):
    """验证结构数据的完整性
    
    参数:
        structure_data: 图层结构数据字典
        gp_data: 蜡笔数据
        
    返回:
        验证过的结构数据
    """
    # 添加导出验证信息
    structure_data['_export_info'] = {
        'total_layers': len(gp_data.layers),
        'has_groups': hasattr(gp_data, 'layer_groups'),
        'total_groups': len(gp_data.layer_groups) if hasattr(gp_data, 'layer_groups') else 0,
        'validated': True
    }
    
    # 检查是否所有图层都已包含在结构中
    all_layers = set(layer.name for layer in gp_data.layers)
    found_layers = set()
    
    # 递归收集结构中的所有图层
    def collect_layers(items):
        for item in items:
            if item.get('type') == 'layer':
                found_layers.add(item['name'])
            elif item.get('type') == 'group' and 'children' in item:
                collect_layers(item['children'])
    
    # 收集图层
    collect_layers(structure_data['hierarchical_structure'])
    
    # 记录可能缺失的图层
    missing_layers = all_layers - found_layers
    if missing_layers:
        structure_data['_export_info']['missing_layers'] = list(missing_layers)
        print(f"警告: 结构中缺少图层: {missing_layers}")
    
    return structure_data

def export_layer_json(render_filepath, obj, gp_data, folder_name, file_basename, time_range=None):
    """
    导出图层结构到JSON文件
    
    参数:
        render_filepath: 渲染文件路径
        obj: 蜡笔对象 
        gp_data: 蜡笔数据
        folder_name: 输出文件夹名称
        file_basename: JSON文件的基本名称（不含扩展名）
        time_range: 可选的时间范围字典，包含frame_start和frame_end
        
    返回:
        (成功状态, 信息消息)
    """
    try:
        # 获取图层结构
        structure_data, _, _ = get_layer_structure(obj, gp_data)
        
        # 创建输出目录
        csv_dir = os.path.join(render_filepath, folder_name)
        os.makedirs(csv_dir, exist_ok=True)
        
        # 创建JSON文件路径
        jsonfile = os.path.join(csv_dir, f"{file_basename}_structure.json")
        
        # 验证结构数据
        validated_structure = validate_structure(structure_data, gp_data)
        
        # 添加时间范围信息
        if time_range:
            validated_structure['_export_info']['frame_start'] = time_range['frame_start']
            validated_structure['_export_info']['frame_end'] = time_range['frame_end']
        
        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 写入JSON文件
        with open(jsonfile, 'w', encoding='utf-8') as f:
            # 添加JSON元数据和版本信息
            json_data = {
                "metadata": {
                    "version": "1.0",
                    "blender_version": bpy.app.version_string,
                    "grease_pencil_type": obj.type,
                    "created": bpy.path.basename(bpy.data.filepath) or "未保存文件",
                    "export_date": current_time,
                    "description": f"图层结构数据 - {obj.name}_{gp_data.name}"
                },
                "structure": validated_structure
            }
            
            # 如果有时间范围信息，添加到元数据中
            if time_range:
                json_data["metadata"]["frame_range"] = f"{time_range['frame_start']}-{time_range['frame_end']}"
            
            # 使用indent=2确保JSON文件格式美观易读
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"成功导出JSON文件到: {jsonfile}")
        print(f"总共处理: {len(gp_data.layers)} 图层, {len(gp_data.layer_groups) if hasattr(gp_data, 'layer_groups') else 0} 图层组")
        return True, f"已导出图层结构到 {jsonfile}"
    
    except Exception as e:
        import traceback
        error_msg = f"导出JSON失败: {str(e)}"
        print(error_msg)
        print(f"JSON导出详细错误: {traceback.format_exc()}")
        return False, error_msg 