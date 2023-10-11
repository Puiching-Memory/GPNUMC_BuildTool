"""
Load and pack *.obj files
加载和打包.obj文件数据
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""

import re

class OBJN:
    def __init__(self, path: str) -> "OBJN":
        self.path = path
        self._obj = open(path,encoding='utf-8')
        self._Analyze()
    
    def Open(self, path):
        pass

    def _Analyze(self):

        self._temp_data = self._obj.readlines()
        self._enc_data = []

        # 过滤无关字符
        for i in self._temp_data:
            if i[0]== '#':
                continue 
            if i == '\n':
                continue

            self._enc_data.append(i)

        ##print(self._enc_data)

    def Exp_V(self):
        _exp_data = []

        for i in self._enc_data:
            # 使用正则表达式提取以"v"开头的行  
            vertices = re.findall(r"v\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)", i)  
            
            # 遍历提取到的顶点数据  
            for vertex in vertices:  
                x, y, z = vertex  # 将每行的数据分为三份
                _exp_data.append([float(x),float(y),float(z)])
        

        return _exp_data



if __name__ == "__main__":
    Object = OBJN("./3dobj/lite.obj")
    print(Object.Exp_V())