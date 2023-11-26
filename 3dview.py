import open3d as o3d
import numpy as np
import re
import mcschematic
from rich.progress import track
mc_block = {
    "minecraft:white_concrete": (205, 210, 211),
    "minecraft:light_gray_concrete": (124, 124, 114),
    "minecraft:gray_concrete": (53, 56, 60),
    "minecraft:black_concrete": (8, 10, 15),
    "minecraft:brown_concrete": (96, 59, 32),
    "minecraft:red_concrete": (141, 33, 33),
    "minecraft:orange_concrete": (222, 96, 0),
    "minecraft:yellow_concrete": (238, 173, 21),
    "minecraft:lime_concrete": (94, 168, 25),
    "minecraft:green_concrete": (72, 90, 36),
    "minecraft:cyan_concrete": (21, 117, 133),
    "minecraft:light_blue_concrete": (35, 134, 195),
    "minecraft:blue_concrete": (44, 46, 142),
    "minecraft:purple_concrete": (99, 31, 154),
    "minecraft:magenta_concrete": (165, 46, 155),
    "minecraft:pink_concrete": (210, 99, 140),
}
# 指定OB文件路径  
file_path = "三饭堂.fbx"  
  
# 使用Open3D读取OBJ文件  
mesh = o3d.io.read_triangle_mesh(file_path)  
o3d.visualization.draw_geometries([mesh])
# 显示点云  
#o3d.visualization.draw_geometries([mesh])

# fit to unit cube

#mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()),
#           center=mesh.get_center())
#o3d.visualization.draw_geometries([mesh])



print('执行体素化')
voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh,
                                                              voxel_size=1)
#o3d.visualization.draw_geometries([voxel_grid])
#print(len(voxel_grid.get_voxels()))
all_list = voxel_grid.get_voxels()
print(len(all_list))

schem = mcschematic.MCSchematic()

for i in track(range(0,len(voxel_grid.get_voxels())-1)):
    s = str(all_list[i])
    result = re.findall(r'\d+', s)  
    
    # 将列表转换为整数  
    result = list(map(int, result))
    #print(result)

    #print(voxel_grid.get_voxel_center_coordinate((result[0],result[1],result[2])).tolist())
    rgba = (result[3],result[4],result[5])
    rsumm = 999
    tar_block = ""
    for i in mc_block.keys():
        # mc_block[i]
        summ = 0
        for c1, c2 in zip(rgba, mc_block[i]):
            summ = summ + abs(c1 - c2)

        if summ < rsumm:
            rsumm = summ
            tar_block = i

    ##print(tar_block)

    #schem.setBlock((round(result[1]), round(result[2]), round(result[0])), tar_block)
    schem.setBlock((round(result[1]), round(result[2]), round(result[0])), "minecraft:stone")

print('保存schem文件')
schem.save("./", 'abc', mcschematic.Version.JE_1_20_1)

#o3d.visualization.draw_geometries([voxel_grid])

#o3d.io.write_voxel_grid("output.ply",voxel_grid)

