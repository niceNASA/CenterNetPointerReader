# 轮廓式仪表盘识别系统

## CenterNetReadGPU

该项目为GPU版本的轮廓式仪表盘识别系统

运行前请先参考以下视频教程配置CenterNet环境，务必确保有可用的GPU（推荐使用NVIDIA帕斯卡架构的显卡），一定要删除 CenterNet\src\lib\models\networks\DCNv2 后再重新编译

> CenterNet环境配置教程视频：
> 
> https://www.bilibili.com/video/BV1r44y1a75j?spm_id_from=333.999.0.0
> 
> CenterNet详细使用说明见Github：
> 
> https://github.com/xingyizhou/CenterNet

```bash
# 运行识别
# 在CenterNet\src目录下执行以下指令
python demo.py multi_pose --demo ../images/ --load_model ../models/model_best.pth --dataset pointer512

# 若需要实时展示识别结果，请将CenterNet\src\lib\detectors\multi_pose.py中的第175行反注释
```

Pointer512数据集位于CenterNet\data\pointer512，因为模型权重文件较大无法上传，请参考CenterNet教程自行训练模型后再使用。



## pointerHandler

该文件夹中为基于SpringBoot和LayUI的演示图像界面程序

要运行该程序请使用IDEA打开该文件夹，然后修改pointerHandler\pointerHandler\src\main\java\com\pointerhandler\controller\UploadController.java中的绝对路径为运行环境中demo.py的相应位置



## tools_logs

该文件夹中为本项目研究过程中使用的一些工具程序和记录的日志



Copyright ©️ 2022 niceNASA
