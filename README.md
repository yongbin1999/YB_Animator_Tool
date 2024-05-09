# blender动画工具
## YB_Animator_Tool
blender动画工具是一款动画便捷插件，主要帮助解决blender制作动画时，一些不便捷的地方。
## 功能
对blender的蜡笔图层以分层进行序列帧导出，并且生成CSV律表文件，律表文件效仿绘画软件Clip Studio Paint生成的律表排序法和文件格式。可使用绘画软件Clip Studio Paint的相同方式导入后期软件AE中
## 导出蜡笔序列帧方法
选中蜡笔对象，点击渲染菜单中的蜡笔关键帧渲染:

![image](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/e51d208d-a717-4cf1-8f01-849dcb283b99)

![image](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/c1dd67f2-28c3-4624-beb6-88b2a9694eb8)

layertag值为CSV中的标签：

![20240509-100745](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/ea710a24-f4f7-4b1b-82a8-e579e61e1bb9)

![20240509-100756](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/b6d27bfe-db65-4e41-acc3-ecc9ba510519)

## 文件结构
目录树:

![06(_N(}GSXA$RU3PA0NWTNL](https://user-images.githubusercontent.com/47911980/172591558-5364c09f-2e4b-492e-962d-5832e1bc24a8.png)

CSV文件所记录的律表(后缀为*Hide的图层为被隐藏的图层，隐藏的图层不会被加入到导出列队当中):

![$)$6FH_2`WB1TB_$I SWCOR](https://user-images.githubusercontent.com/47911980/172592519-9e9f0501-f36b-430a-9da8-d2b57549e66f.png)

## 待开发功能
之后考虑添加对三维关键帧的渲染，欢迎提供想法

感谢您的支持!
源代码可以优化改进的地方，也欢迎提供帮助，源代码注释得非常详细。
其他如有疑问或者BUG反馈，请建立issue提供反馈，谢谢！

## AE所对接的串帧脚本推荐
青涧1大佬的脚本：
[CsvTimeSheetScript](https://github.com/qingjian1/qingjian_AEScripts)

![20240509-113501](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/98b952cd-b795-4230-8161-98faf9ff56bb)

![20240509-113745](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/7e8513bc-aff7-442d-9d9c-c09b2dae9e67)

![20240509-113551](https://github.com/yongbin1999/YB_Animator_Tool/assets/47911980/c16be9af-5014-4224-b755-3667a6f803e9)
