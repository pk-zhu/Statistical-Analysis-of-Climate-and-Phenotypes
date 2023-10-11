import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast  # 导入 ast 模块
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建目录路径
work_directory = os.path.join(parent_directory, "6.correlation")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)
# 读取 CSV 文件
df = pd.read_csv('correlation_result_matrix.csv')
# print (df)
# 提取变量名和因子名
variables = df.iloc[1:, 0]
# print (variables)
factors = df.columns[1:]
# print (factors)

# 提取相关性和 p 值数据
# 从 DataFrame 中提取相关性和 p 值数据
correlation_values = df.iloc[1:, 1:].apply(lambda x: x.iloc[0])
print(correlation_values)
p_values = df.iloc[1:, 1:].apply(lambda x: x[1])
print(p_values)
# 对 p 值应用对数运算并处理无效值
p_values = np.array([float(x[1]) for x in df.iloc[:, 1:]])
log10_p_values = np.where(np.isfinite(p_values), -np.log10(p_values), 0.0)

# 将 correlation_values 数组展平为 1D 数组
correlation_values_flat = correlation_values.flatten()

# 定义标记的大小
marker_size = 50

# 创建散点图
plt.figure(figsize=(10, 6))
scatter = plt.scatter(variables.repeat(len(factors)), factors.repeat(len(variables)), c='blue', s=marker_size, cmap='coolwarm', alpha=0.7)

# 添加颜色条
plt.colorbar(scatter, label='Correlation')

# 设置标题和标签
plt.title('Correlation and Significance Visualization')
plt.xlabel('Variables')
plt.ylabel('Factors')

# 为相关性和 p 值添加标签
for i in range(len(factors)):
    for j in range(len(variables)):
        correlation_label = f'{correlation_values[i][j]:.2f}'
        p_value_label = f'({p_values[i][j]:.2e})'
        plt.text(variables[j], factors[i], f'{correlation_label}\n{p_value_label}', ha='center', va='center', fontsize=8, color='black')

# 显示图表
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()