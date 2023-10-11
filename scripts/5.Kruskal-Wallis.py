
# 导入所需的库
import pandas as pd  # 用于数据处理
import os  # 用于处理文件路径和目录
import re  # 用于正则表达式操作
from scipy.stats import kruskal


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
# 从 "2.Shapiro-Wilk_Test" 目录读取数据到 type_data
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

phenotype_columns = type_data.columns[2:]  # 从第三列开始，因为前两列可能是标识符
environment_columns = cluster_data.columns[1:]  # 排除第一列和最后一列，可能是标识符和不需要的列










# 存储每个环境组的表型数据
environment_groups = []

kruskal_results = []

# 遍历每一列环境数据
for column in environment_columns:
    unique_values = merged_data[column].unique()  # 获取唯一的环境数据值
    environment_group_data = []  # 存储每个环境值对应的表型数据
    for value in unique_values:
        subset = merged_data[merged_data[column] == value]
        environment_group_data.append({
            "Environment": value,
            "Phenotype_Data": subset[phenotype_columns]
        })
    
    # 执行Kruskal-Wallis检验比较不同环境组的表型数据
    for i, group1 in enumerate(environment_group_data):
        for j, group2 in enumerate(environment_group_data):
            if i < j:
                h_statistic, p_value = kruskal(group1["Phenotype_Data"], group2["Phenotype_Data"])
                environment1 = group1["Environment"]
                environment2 = group2["Environment"]
                kruskal_results.append({
                    "Environment_Column": column,  # 添加环境数据列名
                    "Environment1": environment1,
                    "Environment2": environment2,
                    "H-Statistic": h_statistic,
                    "p-value": p_value,
                    "Phenotype_Columns": ', '.join(phenotype_columns)  # 添加 Phenotype_Data 列名
                })

# 创建包含所有结果的DataFrame
kruskal_df = pd.DataFrame(kruskal_results)
kruskal_df.to_csv("kruskal_results.csv", index=False)








# 创建一个新的 DataFrame，将多列中的元素对应起来
new_rows = []

for index, row in kruskal_df.iterrows():
    for i, p_value in enumerate(row["p-value"]):
        new_row = {
            "Environment_Column": row["Environment_Column"],
            "Environment1": row["Environment1"],
            "Environment2": row["Environment2"],
            "H-Statistic": row["H-Statistic"][i],
            "p-value": p_value,
            "Phenotype_Column": row["Phenotype_Columns"].split(", ")[i]
        }
        new_rows.append(new_row)

# 创建新的 DataFrame，包含对应的元素
new_df = pd.DataFrame(new_rows)

# 输出到 CSV 文件
new_df.to_csv("final_results.csv", index=False)