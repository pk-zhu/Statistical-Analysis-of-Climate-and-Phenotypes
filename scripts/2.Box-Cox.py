import pandas as pd
from scipy.stats import boxcox
import numpy as np
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建 "1.data_qc" 目录路径
work_directory = os.path.join(parent_directory, "2.Shapiro-Wilk_Test")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取CSV文件
file_path = os.path.join(parent_directory, "1.data_qc", "filtered.csv")
data = pd.read_csv(file_path)

# 获取表型数据的列
phenotype_columns = data.columns[2:]

# 创建一个空的DataFrame来存储处理后的数据
processed_data = data.copy()

# 逐列进行Box-Cox变换
for phenotype in phenotype_columns:
    # 提取当前表型数据列的值
    phenotype_data = data[phenotype]
    
    # 执行Box-Cox变换，并自动估计最佳lambda值
    transformed_data, lambda_param = boxcox(phenotype_data)
    
    # 将变换后的数据替换原始数据列
    processed_data[phenotype] = transformed_data
    
    print(f"对 {phenotype} 应用了 Box-Cox 变换，估计的 lambda 值为 {lambda_param:.3f}")

# 将处理后的数据保存到新的CSV文件
processed_data.to_csv('processed_data.csv', index=False)

print("数据处理完成，已保存到 processed_data.csv 文件中。")
