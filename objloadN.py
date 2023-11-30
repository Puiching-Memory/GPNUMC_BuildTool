"""
Load and pack *.obj files
加载和打包.obj文件数据
---
#不支持:
四点面
O(分组)
S
*.mtl

IDLE:VS CODE
Python Version:3.11.5/3.10.11/
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
	def __init__(self, *path: str) -> "OBJN":
		self._enc_data = []

		if path != ():
			self.Open(path[0])
	
	def Open(self, path:str):
		self.path = path
		self._enc_data = []
		with rich.progress.open(path,encoding='utf-8') as file:
			# 过滤无关字符
			for i in file.readlines():
				if i[0]== '#':
					continue 
				if i == '\n':
					continue

				self._enc_data.append(i)


	def Exp_V(self) -> list:
		'''
		导出数据
		---
		list[0] = v_list #顶点列表\n
		list[1] = vn_list #法向量列表\n
		list[2] = f_list #面列表
		'''
		if self._enc_data == []:
			raise IndexError('导出错误:数据未载入,先调用Open(path)')

		_exp_v = []
		_exp_vn = []
		_exp_f = []
		_exp_vt = []

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
	Object = OBJN()
	#Object.Open('3.obj')
	result = Object.Exp_V()
	#print(result[2])