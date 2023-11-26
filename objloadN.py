"""
Load and pack *.obj files
加载和打包.obj文件数据
---
IDLE:VS CODE
Python Version:3.11.5
@PuiChing Memory
"""

import re
from rich.progress import track
import rich.progress

class OBJN:
	'''
	OBJ文件对象
	---
	从文件加载:__init__ or open() \n
	导出数据:Exp_V()
	'''
	def __init__(self, path: str) -> "OBJN":
		self.path = path
		with rich.progress.open(path,encoding='utf-8') as file:
			self._temp_data = file.readlines()

		self._Analyze()
	
	def Open(self, path):
		pass

	def _Analyze(self):

		
		self._enc_data = []

		# 过滤无关字符
		for i in self._temp_data:
			if i[0]== '#':
				continue 
			if i == '\n':
				continue

			self._enc_data.append(i)

		##print(self._enc_data)

	def Exp_V(self) -> list:
		'''
		导出数据
		---
		list[0] = v_list #顶点列表\n
		list[1] = vn_list #法向量列表\n
		list[2] = f_list #面列表
		'''
		#_exp_data = []
		_exp_v = []
		_exp_vn = []
		_exp_f = []

		for i in track(self._enc_data,description='分析点v数据'):
			# 使用正则表达式提取以"v"开头的行  
			vertices = re.findall(r"v\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)", i)  
			
			# 遍历提取到的顶点数据  
			for vertex in vertices:  
				x, y, z = vertex  # 将每行的数据分为三份
				_exp_v.append([float(x),float(y),float(z)])
		
		
		for i in track(self._enc_data,description='分析vn数据'):
			# 使用正则表达式提取以"vn"开头的行  
			vertices = re.findall(r"vn\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)", i)  
			
			# 遍历提取到的顶点数据  
			for vertex in vertices:  
				x, y, z = vertex  # 将每行的数据分为三份
				_exp_vn.append([float(x),float(y),float(z)])
		
		#print(_exp_vn)


		for i in track(self._enc_data,description='分析面f数据'):
			# 使用正则表达式提取以"f"开头的行
			#matches = re.findall( r"f (\d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+)" , i, re.MULTILINE)
			matches = re.findall(  r"f (\d+/\d+/\d+ \d+/\d+/\d+ \d+/\d+/\d+)" , i, re.MULTILINE)
			# 将找到的匹配项保存到列表中

			for match in matches:
				int_list = [[int(i) for i in match.split(' ')[i].split('/')] for i in range(len(match.split(' ')))]
				_exp_f.append(int_list)
				

		return [_exp_v,_exp_vn,_exp_f]



if __name__ == "__main__":
	#Object = OBJN("./3dobj/lite/lite.obj")
	#result = Object.Exp_V()
	#print(result[2])

	Object = OBJN("out.obj")
	result = Object.Exp_V()
	#print(result[2])