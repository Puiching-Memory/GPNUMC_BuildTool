import re  
  
# 输入的文本  
text = """  
vt 0.625000 0.000000  
vt 0.375000 0.250000  
vt 0.375000 0.000000  
vt 0.625000 0.250000  
"""  
  
# 使用正则表达式提取 vt 行，并将它们转换为 [x, y] 的列表形式  
pattern = r'vt (\d+\.\d+)\s(\d+\.\d+)'  
matches = re.findall(pattern, text)  
  
# 打印结果  
for match in matches:  
    print(match)  # 输出：[x, y] 的列表，例如：[0.625, 0.0], [0.375, 0.25], [0.375, 0.0], [0.625, 0.25]