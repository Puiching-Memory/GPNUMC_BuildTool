"""
导出为.schem文件
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""


import mcschematic
import numpy as np
#import itertools
import multiprocessing as mp
#import open3d
#import math
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
        self.points = [] # 点云坐标列表
        
        self.maxinsert = 1 #动态点插值阈值,大于则忽略
        self.inserttimes = 2 #点插值阶数

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

        self._GenerateFace()  # 计算

    def mp_center(self,fun,**kargs):
        '''
        多进程管理器
        ---
        '''
        pool = mp.Pool(mp.cpu_count)
        pool.apply_async(fun, args=kargs)
        pool.close()
        pool.join()

    def _GenerateFace(self):
        for i in track(range(0,len(self.f)-1),description='分析面'):
            VN = self.vn[self.f_vn[i][0]-1]
            A = self.v[self.f_v[i][0]-1]
            B = self.v[self.f_v[i][1]-1]
            C = self.v[self.f_v[i][2]-1]

            #self.points.extend([A,B,C])

            '''#点积法
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
                        if self.is_on_plane_dot(point,A,VN) == True:
                            self.block.append(point)
            '''
            #print('check face',i)
            #self.mp_center()
            self.point_liner_inset(A,B,C)

        #self.points = np.unique(self.points)
        #print(self.points)
        print('block:',len(self.block))
        print('point:',len(self.points))
        print('frame:',len(self.f))


    def volin(self):
        """
        体素重构
        ---
        """
        pass

    def point_liner_inset(self,PointA,PointB,PointC):
        """
        线性点插值
        ---
        """
        
        points = []
        points.append(PointA)
        points.append(PointB)
        points.append(PointC)

        for t in range(0,self.inserttimes):
            temp = []
            for A in points:
                for B in points:
                    if A==B:
                        continue
                    scale = 1 #细分系数

                    #构建点向量
                    dotA = np.array([A[0],A[1],A[2]])
                    dotB = np.array([B[0],B[1],B[2]])

                    #构建两点之间的向量
                    arrAB = np.subtract(dotA,dotB)

                    #计算两点之间的向量的模
                    disAB = np.linalg.norm(arrAB)
                    
                    #扩增细分系数
                    while np.linalg.norm(arrAB/scale) > self.maxinsert:
                        scale = scale + 1
                    
                    if scale == 1:
                        continue
                    #print('scale',scale)
                    for i in range(1,scale):
                        #print((dotA-arrAB/scale*i).tolist())
                        temp.append((dotA-arrAB/scale*i).tolist())
            #print('插值+',len(temp))
            points.extend(temp)
                        #points.append((dotA-arrAB/2).tolist())
                    #print('A',dotA,'B',dotB,'C',dotC)
                    #print('A-B',disAB,'A-C',disAC,"B-C",disBC)
                    #print('2/AB',dotA-arrAB/2)
        #删除重复元素
        re = []
        for x in points:
            if x in re:
                #print('skip')
                continue
            else:
                re.append(x)
        self.points.extend(re)

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
        for i in track(self.points,description='生成schem文件'):
            schem.setBlock((round(i[1]), round(i[2]), round(i[0])), "minecraft:stone")

        print('保存schem文件')
        schem.save("./", filename, mcschematic.Version.JE_1_20_1)
