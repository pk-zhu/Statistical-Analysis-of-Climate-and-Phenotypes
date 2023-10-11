import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建路径
work_directory = os.path.join(parent_directory, "3.PCA_env")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取CSV文件
file_path = os.path.join(parent_directory, "data", "env.csv")
data = pd.read_csv(file_path)

# 提取环境数据列（第二列到倒数第二列）
X = data.iloc[:, 1:-1].values

# 标准化数据
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# 创建PCA模型，假设你希望保留所有主成分
pca = PCA()

# 拟合PCA模型
pca.fit(X_std)

# 获取主成分的方差解释比例
explained_variance_ratio = pca.explained_variance_ratio_

# 绘制方差解释比例的累积图
cumulative_explained_variance = np.cumsum(explained_variance_ratio)
plt.plot(range(1, len(cumulative_explained_variance) + 1), cumulative_explained_variance, marker='o', linestyle='-')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Cumulative Explained Variance vs. Number of Principal Components')

# 保存累积方差解释比例图为PDF和JPG文件
plt.savefig('pca_plot.pdf')
plt.savefig('pca_plot.jpg')

# 根据需要选择主成分数量
num_components = 2  # 假设选择前两个主成分

# 应用PCA变换
X_pca = pca.transform(X_std)[:, :num_components]

# 添加样品来源列作为新的一列
sample_source = data.iloc[:, 0].values
X_pca = np.column_stack((sample_source, X_pca))

# 创建新的DataFrame
columns = ['Sample Source'] + [f'PC{i}' for i in range(1, num_components + 1)]
pca_df = pd.DataFrame(X_pca, columns=columns)

# 打印包含主成分的新DataFrame
print(pca_df)

# 创建样本来源到颜色的映射字典
# 创建样本来源到颜色的映射字典
source_to_color = {
    'FJAX': 'red',
    'FJHA': 'blue',
    'FJSM': 'green',
    'FJMQ': 'orange',
    'FJSH': 'purple',
    'FJXY': 'cyan',
    'FJYC': 'magenta',
    'FJYT': 'yellow',
    'FJCD': 'brown',
    'GDNL': 'pink',
    'GXDMS': 'lime',
    'GXGY': 'teal',
    'GXJX': 'olive',
    'CQJJ': 'gray'
}

# 根据样本来源获取对应颜色的列表
colors = [source_to_color.get(source, 'black') for source in sample_source]
# 绘制PCA散点图
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 1], X_pca[:, 2], c=colors, marker='o', alpha=0.7)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Scatter Plot')

# 在每个数据点旁边标上 sample_source 的名字
for i, source in enumerate(sample_source):
    plt.annotate(source, (X_pca[i, 1], X_pca[i, 2]), fontsize=8, alpha=0.8, xytext=(5, 5), textcoords='offset points')

# 移除颜色条
plt.colorbar(scatter, ax=plt.gca(), label='Sample Source').remove()


# 保存PCA散点图为PDF和JPG文件
plt.savefig('pca_scatter.pdf')
plt.savefig('pca_scatter.jpg')


