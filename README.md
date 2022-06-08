# blender蜡笔动画工具
## YB_Animator_Tool
blender蜡笔动画工具是一款二维动画便捷插件，主要帮助解决blender制作二维动画时，一些不便捷的地方。
## 功能
对blender的蜡笔图层以分层进行序列帧导出，并且生成CSV律表文件，律表文件效仿绘画软件Clip Studio Paint生成的律表排序法和文件格式。可使用绘画软件Clip Studio Paint的相同方式导入后期软件AE中
## 导出序列帧方法
找到蜡笔属性面板:

![FW1%3AKET8BLIC)@X%QWKRL](https://user-images.githubusercontent.com/47911980/172588219-ba93b81c-9b0c-48a8-b259-5a53b3b41de8.png)

全选蜡笔时间轴左侧所有图层:

![$Y5 $QK~S4IVZOJYQZIIDZD](https://user-images.githubusercontent.com/47911980/172589376-4c7e868b-a234-4015-ac5f-982747b5f8b3.png)

点击导出，等待片刻:

![J~S79ZG}PPOH_41W5B0OE}W](https://user-images.githubusercontent.com/47911980/172589632-c3709fbb-f10c-48d0-8c4f-f51eb774ed1d.png)

## 文件结构
目录树:

![06(_N(}GSXA$RU3PA0NWTNL](https://user-images.githubusercontent.com/47911980/172591558-5364c09f-2e4b-492e-962d-5832e1bc24a8.png)

CSV文件所记录的律表(后缀为*Hide的图层为被隐藏的图层，隐藏的图层不会被加入到导出列队当中):

![$)$6FH_2`WB1TB_$I SWCOR](https://user-images.githubusercontent.com/47911980/172592519-9e9f0501-f36b-430a-9da8-d2b57549e66f.png)

## 待开发功能
之后将会添加一些对渲染属性进行修改的自定义功能，例如，可以自由的选择图片前缀，律表可选择的原画或动画标签等
在功能方面，将会对blender的二维动画模块进行整合，快捷键自由绑定，自由锁定3D旋转等...


感谢您的支持!
源代码可以优化改进的地方，也欢迎提供帮助，源代码注释得非常详细。
其他如有疑问或者BUG反馈，请建立issue提供反馈，谢谢！
