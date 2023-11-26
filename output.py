"""
导出为.schem文件
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""


import mcschematic
import numpy as np
import multiprocessing
import open3d
from rich.progress import track


class SchemN:
    def __init__(self, v: list, vn: list, f: list) -> None:
        self.v = v  # 顶点列表
        self.f = f  # 面列表
        self.vn = vn  # 法向量列表
        self.f_v = []  # 面对应的点索引列表
        self.f_uv = []  # 面对应的uv纹理坐标索引列表
        self.f_vn = []  # 面对应的法向量索引列表
        self.block = []  # 方块坐标列表[X,Y,Z]
        self.point_list = [] #监测点坐标列表

        for i in range(0,len(self.f)):
            self.f_v.append([])
            for i2 in self.f[i]:
                self.f_v[i].append(i2[0])

        for i in range(0,len(self.f)):
            self.f_uv.append([])
            for i2 in self.f[i]:
                self.f_uv[i].append(i2[1])

        for i in range(0,len(self.f)):
            self.f_vn.append([])
            for i2 in self.f[i]:
                self.f_vn[i].append(i2[2])

        #print(self.f)

        self._GenerateFace()  # 计算点,线性插值
    def _GenerVolite(self):
        pass



    def _GenerateFace(self):
        for i in range(0,len(self.f)-1):
            VN = self.vn[self.f_vn[i][0]-1]
            A = self.v[self.f_v[i][0]-1]
            B = self.v[self.f_v[i][1]-1]
            C = self.v[self.f_v[i][2]-1]

            self.point_list = []
            '''
            for x in np.arange(
                int(min(A[0], B[0], C[0], D[0]))-0.5, int(max(A[0], B[0], C[0], D[0]) + 1),0.1
            ):
                for y in np.arange(
                    int(min(A[1], B[1], C[1], D[1]))-0.5, int(max(A[1], B[1], C[1], D[1]) + 1),0.1
                ):
                    for z in np.arange(
                        int(min(A[2], B[2], C[2], D[2]))-0.5,
                        int(max(A[2], B[2], C[2], D[2]) + 1),
                        0.1
                    ):
                        point = [x, y, z]
                        #print(point,VN)
                        if self.is_on_plane(point,A,VN) == True:
                            self.block.append(point)
            '''
            for x in np.arange(
                int(min(A[0], B[0], C[0]))-0.5, int(max(A[0], B[0], C[0]) + 1),0.1
            ):
                for y in np.arange(
                    int(min(A[1], B[1], C[1]))-0.5, int(max(A[1], B[1], C[1]) + 1),0.1
                ):
                    for z in np.arange(
                        int(min(A[2], B[2], C[2]))-0.5,
                        int(max(A[2], B[2], C[2]) + 1),
                        0.1
                    ):
                        point = [x, y, z]
                        self.point_list.append(point)
                        #print(point,VN)
                        #if self.is_on_plane(point,A,VN) == True:
                            #self.block.append(point)

            #arr = multiprocessing.Array('i', list(range(len(self.point_list))))
            #p = multiprocessing.Process(target=self.thr_detect, args=(self.point_list,A,VN))
            #p.start()
            #p.join()
  

        print('block:',len(self.block))
        print('frame:',len(self.f))

    def thr_detect(self,point_list,A,VN):

        for i in point_list:
            if self.is_on_plane_dot(i,A,VN) == True:
                self.block.append(i)

    def volin(self):
        """
        体素重构
        ---
        """
        pass

    def is_on_plane_grid(self):
        """
        计算一个点是否在一个面上
        ---
        计算方法:构建平面方程
        """ 
        pass

    def is_on_plane_dot(self, point1: list, point2: list,VN:float) -> bool:
        """
        计算一个点是否在一个面上
        ---
        计算方法:取面的其中一个端点,与输入点取差值得到向量,与该面的法向量求点积,点积=0则该点在该面之内
        """ 
        # 计算向量point-plane_point  
        vector = np.array([point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2]])
        #print(vector)
        # 计算向量与平面法向量的点积  
        dot_product = np.dot(vector, VN)
        # 如果点积为0，那么点在平面上  
        if np.allclose(dot_product, 0):  
            return True  
        else:  
            return False
        return

    def Exp_sch(self, filename: str):
        schem = mcschematic.MCSchematic()
        for i in track(self.block,description='生成schem文件'):
            schem.setBlock((round(i[1]), round(i[2]), round(i[0])), "minecraft:stone")

        print('保存schem文件')
        schem.save("./", filename, mcschematic.Version.JE_1_20_1)
