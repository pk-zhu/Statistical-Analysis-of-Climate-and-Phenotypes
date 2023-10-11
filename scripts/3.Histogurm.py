import pandas as pd
import matplotlib.pyplot as plt
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建 "1.data_qc" 目录路径
work_directory = os.path.join(parent_directory, "3.PCA_env")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取CSV文件
file_path = os.path.join(parent_directory, "data", "env.csv")
data = pd.read_csv(file_path)

# 获取列名列表
columns = data.columns

# 遍历每一列环境数据并绘制直方图
for col in columns[1:-1]:  # 忽略第一列（样品来源）和最后一列（样本容量）
    plt.figure(figsize=(8, 6))  # 设置图形大小
    plt.hist(data[col], bins=20, edgecolor='k')  # 绘制直方图，bins可根据需要调整
    plt.xlabel(col, fontsize=16)  # 设置X轴标签
    plt.ylabel('Frequency', fontsize=16)  # 设置Y轴标签
    plt.title(f'Histogram of {col}', fontsize=25, y=1.05)  # 设置图标题
    plt.grid(True)  # 添加网格线

    plt.savefig(f'Histogram of {col}.pdf')
    plt.savefig(f'Histogram of {col}.jpg')
    plt.close()  # 关闭图形，以便下一次迭代