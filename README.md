# GPNUMC_BuildTool

GPNU[广东技术师范大学]MineCraft 建筑工具

# 功能

* [X] .OBJ文件自动转换为.schem文件，这可以被创世神(EditWorld mod)载入
* [ ] 方块匹配颜色
* [ ] 表面平滑
* [X] 提供更多3D文件格式支持

# 2.0更改注意事项

* 正在向open3D迁移,各类api会经常更改

# 结构

main.py:主程序

objloadN.py:导入和分析.OBJ文件

output.py:生成和导出.schem文件

# 所需库

* python3.10/3.11（经过测试）
* mcschematic
* numpy
* rich
* open3d

# OBJ-3D软件导出注意事项

### For Blender:

导出OBJ,坐标轴选择Y/Z

# 文档

* [schem文件格式[中文wiki]](https://minecraft.fandom.com/zh/wiki/Schematic%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F "https://minecraft.fandom.com/zh/wiki/Schematic%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F")

# 版权

所有者:@PUICHING_Memory

仅供内部调试使用，任何由个人操作导致的损坏概不负责！

协议：GPLV3
