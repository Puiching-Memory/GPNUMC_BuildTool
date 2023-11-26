import open3d as o3d
import numpy as np
import re
import mcschematic
from rich.progress import track
  
# 指定OB文件路径  
file_path = "on.fbx"  
  
# 使用Open3D读取OBJ文件  
mesh = o3d.io.read_triangle_mesh(file_path)
print(mesh.vertex_colors)
#mesh.compute_vertex_normals()
#pcd = mesh.sample_points_uniformly(number_of_points=50000)
#pcd.colors = mesh.vertex_colors

o3d.visualization.draw_geometries([mesh])

# 显示点云  
#o3d.visualization.draw_geometries([pcd])



