import pandas as pd
import os
from scipy.stats import pearsonr, spearmanr
import re

# 设置工作路径

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

# 读取文件件
type_path = os.path.join(parent_directory, "1.data_qc", "filtered.csv")
type_data = pd.read_csv("..\\2.Shapiro-Wilk_Test\\processed_data.csv")
env_path = os.path.join(parent_directory, "data", "env.csv")
env_data = pd.read_csv(env_path)

# 列名转换函数
def clean_column_name(column_name):
    # 删除括号及其内部的内容，同时删除空格
    cleaned_name = re.sub(r'\([^)]*\)', '', column_name).replace(" ", "_")
    if cleaned_name.endswith("_"):
        cleaned_name = cleaned_name[:-1]

    return cleaned_name

# 为表型数据和环境数据的列名应用列名转换
type_data.columns = [clean_column_name(col) for col in type_data.columns]
env_data.columns = [clean_column_name(col) for col in env_data.columns]

# 合并数据集，使用样品来源作为连接关键字
merged_data = pd.merge(type_data, env_data, on="source")

# 进行多因素方差分析，导入库
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 表型数据列
phenotype_columns = type_data.columns[2:]  # 从第三列到最后一列的所有列
# 环境数据列
environment_columns = env_data.columns[1:-1]  # 从第二列到倒数第二列的所有列

# 创建一个空的 DataFrame 以存储结果
correlation_results = pd.DataFrame(columns=['Phenotype', 'Environment', 'Correlation', 'p-value'])
p_value_results = pd.DataFrame(index=phenotype_columns, columns=environment_columns)
correlation_values_results = pd.DataFrame(index=phenotype_columns, columns=environment_columns)

for phenotype_column in phenotype_columns:
    print(f"正在分析环境数据对 {phenotype_column} 的影响:")

    for environment_column in environment_columns:
        print(f"环境数据列: {environment_column}")
        
        # Calculate correlation and p-value
        correlation_method = 'spearman'  # You can change this to 'pearson' if needed
        if correlation_method == 'pearson':
            correlation, p_value = pearsonr(merged_data[phenotype_column], merged_data[environment_column])
        elif correlation_method == 'spearman':
            correlation, p_value = spearmanr(merged_data[phenotype_column], merged_data[environment_column])
        
        # Output correlation analysis result
        print(f"{correlation_method.capitalize()}相关系数: {correlation}")
        print(f"p-value: {p_value}")
        print("=" * 50 + "\n")
        
        # Append the result to DataFrames
        correlation_results = correlation_results.append({'Phenotype': phenotype_column,
                                                          'Environment': environment_column,
                                                          'Correlation': correlation,
                                                          'p-value': p_value}, ignore_index=True)
        p_value_results.at[phenotype_column, environment_column] = p_value
        correlation_values_results.at[phenotype_column, environment_column] = correlation

# Export correlation analysis results to a CSV file
correlation_results.to_csv("correlation_results.csv", index=False)
print("相关性分析结果已导出到文件: correlation_results.csv")

# Export p-value results to a CSV file with Phenotype as the index
p_value_results.to_csv("p_value.csv", index_label="Phenotype")
print("p值结果已导出到文件: p_value.csv")

# Export correlation coefficients results to a CSV file with both Phenotype and Environment columns
correlation_values_results.to_csv("correlation_value.csv", index_label="Phenotype")
print("相关性系数已导出到文件: correlation_value.csv")