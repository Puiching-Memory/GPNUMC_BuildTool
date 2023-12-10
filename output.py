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
from concurrent import futures
#import open3d
#import math
import time
from rich.progress import track

mc_block = {
    "minecraft:white_concrete": (205, 210, 211),
    "minecraft:light_gray_concrete": (124, 124, 114),
    "minecraft:gray_concrete": (54, 57, 61),
    "minecraft:black_concrete": (8, 10, 15),
    "minecraft:brown_concrete": (96, 59, 31),
    "minecraft:red_concrete": (141, 33, 33),
    "minecraft:orange_concrete": (222, 96, 0),
    "minecraft:yellow_concrete": (238, 173, 21),
    "minecraft:lime_concrete": (94, 168, 25),
    "minecraft:green_concrete": (72, 91, 36),
    "minecraft:cyan_concrete": (21, 119, 136),
    "minecraft:light_blue_concrete": (35, 134, 195),
    "minecraft:blue_concrete": (44, 46, 142),
    "minecraft:purple_concrete": (99, 31, 154),
    "minecraft:magenta_concrete": (165, 46, 155),
    "minecraft:pink_concrete": (210, 99, 140),
    "minecraft:bamboo_planks": (197, 176, 82),
    "minecraft:stripped_oak_wood": (177, 143, 85),
    "minecraft:stripped_jungle_wood": (171, 132, 84),
    "minecraft:stripped_birch_wood": (196, 175, 118),
    "minecraft:stripped_acacia_wood": (173, 92, 59),
    "minecraft:stripped_mangrove_wood": (119, 54, 47),
    "minecraft:stripped_dark_oak_wood": (71, 56, 35),
    "minecraft:stripped_cherry_wood": (214, 144, 148),
    "minecraft:packed_mud": (142, 107, 80),
    "minecraft:polished_deepslate": (65, 65, 66),
    "minecraft:polished_andesite": (123, 126, 126),
    "minecraft:stone": (124, 124, 124),
    "minecraft:smooth_stone": (154, 154, 154),
    "minecraft:polished_granite": (148, 102, 85),
    "minecraft:polished_diorite": (177, 177, 178),
    "minecraft:polished_blackstone": (50, 45, 53),
    "minecraft:nether_bricks": (47, 23, 27),
    "minecraft:netherrack": (98, 38, 38),
    "minecraft:end_stone": (220, 223, 159),
    "minecraft:dark_prismarine": (44, 71, 60),
    "minecraft:prismarine_bricks": (86, 156, 139),
    "minecraft:smooth_red_sandstone": (181, 97, 31),
    "minecraft:smooth_sandstone": (223, 214, 170),
    "minecraft:iron_block": (214, 214, 214),
    "minecraft:purpur_block": (159, 115, 159),
    "minecraft:redstone_block": (182, 25, 5),
    "minecraft:emerald_block": (42, 194, 81),
    "minecraft:lapis_block": (29, 64, 137),
    "minecraft:diamond_block": (81, 228, 221),
    "minecraft:netherite_block": (61, 55, 58),
    "minecraft:quartz_block": (223, 227, 218),
    "minecraft:quartz_block": (223, 227, 218),
}

class SchemN:
    def __init__(self, v: list, vn: list,vt:list, f: list,mtllib:object,strc) -> None:
        self.v = v  # 顶点列表
        self.f = f  # 面列表
        self.vn = vn  # 法向量列表
        self.vt = vt # uv坐标列表
        self.mtllib = mtllib #mtl对象
        self.strc = strc #f对应mtl分组结构
        self.f_v = []  # 面对应的点索引列表
        self.f_uv = []  # 面对应的uv纹理坐标索引列表
        self.f_vn = []  # 面对应的法向量索引列表
        self.points = [] # 点云坐标列表
        

        #mp.Manager().list()

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

        #self.GenerateFace()  # 计算




    def GenerateFace(self):
        task_face = []
        for i in track(range(0,len(self.f)-1),description='生成任务列表'):
            VN = self.vn[self.f_vn[i][0]-1]
            A = self.v[self.f_v[i][0]-1]
            B = self.v[self.f_v[i][1]-1]
            C = self.v[self.f_v[i][2]-1]
            task_face.append([A,B,C])

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

            #TODO:多进程内存共享
            #self.mp_center(self.point_liner_inset,(A,B,C))
            #self.point_liner_inset(A,B,C)

        #self.points = np.unique(self.points)
        #print(self.points)
        #print(task_face)
        print('task_point:',len(task_face))
        print('frame:',len(self.f))
        self.points = mp_center(point_liner_inset,task_face)
        print('generate_point:',len(self.points))
        #self.point_liner_inset(A,B,C)


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
        for i in track(self.points,description='生成schem文件'):
            schem.setBlock((round(i[1]), round(i[2]), round(i[0])), "minecraft:stone")
        

        #print('着色中')
        current = 0
        padding = 0
        img_index = 0
        #print(self.strc)
        for i,i2 in track(zip(self.f_uv,self.f_v),description='着色中'):
            #print(i,i2)
            current = current + 1
            #print(i)
            for i999 in self.strc:
                padding = padding + i999
                if current <= padding:
                    break
                img_index = img_index + 1

            #print(current,padding,img_index)           
            
            for i12,i22 in zip(i,i2):
                #print(i2,i22)
                #print(self.vt[i2-1])
                try:
                    re = self.mtllib.get_pixel(img_index-1,self.vt[i12-1][0],self.vt[i12-1][1])
                except Exception as error:
                    #print(error,'skip')
                    break
                be = self.v[i22-1]
                #print(re,be)



                rsumm = 999
                tar_block = ""
                for i in mc_block.keys():
                    # mc_block[i]
                    summ = 0
                    for c1, c2 in zip(re, mc_block[i]):
                        summ = summ + abs(c1 - c2)

                    if summ < rsumm:
                        rsumm = summ
                        tar_block = i

                ##print(tar_block)

                #schem.setBlock((x, 0, y), tar_block)

                schem.setBlock((round(be[1]), round(be[2]), round(be[0])), tar_block)

        print('保存schem文件')
        schem.save("./", filename, mcschematic.Version.JE_1_20_1)

def point_liner_inset(*kargs):
        """
        线性点插值
        ---
        """
        maxinsert = 1 #动态点插值阈值,大于则忽略
        inserttimes = 2 #点插值阶数
        #print('Point:',kargs)
        PointA = kargs[0][0]
        PointB = kargs[0][1]
        PointC = kargs[0][2]
        points = []
        points.append(PointA)
        points.append(PointB)
        points.append(PointC)

        for t in range(0,inserttimes):
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
                    while np.linalg.norm(arrAB/scale) > maxinsert:
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
        #self.points.extend(re)
        return re

def mp_center(fun,*kargs):
    '''
    多进程管理器
    ---
    fun:function()\n
    *kargs:待处理数据,不要当作形式参数!
    '''
    
    result = []
    NUMBER_OF_PROCESSES = mp.cpu_count()
    #NUMBER_OF_PROCESSES = 3
    CHUNKSIZE = max(1,int(len(*kargs)/NUMBER_OF_PROCESSES))
    print('Using Core:',NUMBER_OF_PROCESSES,"Chunksize:",CHUNKSIZE)
    
    #print('*kargs:',*kargs)
    t1 = time.time()
    with futures.ProcessPoolExecutor(NUMBER_OF_PROCESSES) as executor:
        res = executor.map(fun,*kargs,chunksize=CHUNKSIZE)
    #print("----print result----")
    print('used time:',time.time()-t1)
    for r in res:
        #print(r)
        result.extend(r)

    return result