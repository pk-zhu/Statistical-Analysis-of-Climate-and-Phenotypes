import pandas as pd
import os
import re

# 设置工作路径
# 获取当前脚本的目录，并转到其父目录
script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)
os.chdir(parent_directory)

# 创建工作目录 "5.LSD"（如果不存在），并将工作路径切换到该目录
work_directory = os.path.join(parent_directory, "5.Kruskal-Wallis")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取数据
type_path = os.path.join(parent_directory, "1.data_qc", "filtered.csv")
type_data = pd.read_csv(type_path)

# 读取聚类结果
cluster_path = os.path.join(work_directory, "cluster.csv")
cluster_data = pd.read_csv(cluster_path)

# 列名转换函数
def clean_column_name(column_name):
    # 清理列名：去掉括号内的内容，将空格替换为下划线，并删除结尾的下划线
    cleaned_name = re.sub(r'\([^)]*\)', '', column_name).replace(" ", "_")
    if cleaned_name.endswith("_"):
        cleaned_name = cleaned_name[:-1]
    return cleaned_name

# 应用列名清理函数，将列名转为合适的格式
type_data.columns = [clean_column_name(col) for col in type_data.columns]

# 合并数据集
# 使用 "source" 列将两个数据集合并
merged_data = pd.merge(type_data, cluster_data, on="source")


# 定义环境因子和表型的列名
environment_factors = cluster_data.columns[1:]
phenotypes = type_data.columns[2:]


# 创建一个空的数据框，用于存储结果
result_df = pd.DataFrame()


# 循环遍历每种环境因子作为分组依据
for factor in environment_factors:
    # 获取分组信息
    groups = cluster_data[factor].unique()

    # 循环遍历每个分组
    for group in groups:
        group_name = f"{factor}_{group}"  # 使用分组值和环境因子名作为列名
        group_data = type_data[type_data['source'].isin(cluster_data[cluster_data[factor] == group]['source'])]
        group_data = group_data.groupby('source').mean()
        group_mean = group_data.mean()
        result_df[group_name] = group_mean

# 输出结果表格
result_df = result_df.iloc[1:]
result_df.index = type_data.columns[2:]  # 行名为不同表型
result_df.to_csv('result_table.csv')