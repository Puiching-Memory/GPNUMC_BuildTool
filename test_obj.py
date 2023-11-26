import open3d as o3d
import numpy as np
import re
import mcschematic
from rich.progress import track
  
# 指定OB文件路径  
file_path = '3.obj'
  
# 使用Open3D读取OBJ文件  
mesh = o3d.io.read_triangle_mesh(file_path,True)
#mesh.textures = [o3d.geometry.Image('Model_0.jpg')]
print(np.asarray(mesh.triangle_uvs))

  
# 显示点云  
o3d.visualization.draw_geometries([mesh])

