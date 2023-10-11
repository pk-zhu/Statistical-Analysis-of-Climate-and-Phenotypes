import pandas as pd
import os
import re
from scipy.stats import chi2_contingency, fisher_exact

# 设置工作路径

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建目录路径
work_directory = os.path.join(parent_directory, "8.Contingency-Table-Test")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取数据文件
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
phenotype_columns = type_data.columns[2:]  # 从第三列到最后一列的所有列
environment_columns = env_data.columns[1:-1]  # 从第二列到倒数第二列的所有列

# 合并数据集，使用样品来源作为连接关键字
merged_data = pd.merge(type_data, env_data, on="source")

# 初始化结果存储
result_data = []

# 遍历PhenotypeColumnName和CategoricalVariableColumn组合执行列联表检验
for phenotype_column in phenotype_columns:
    for categorical_variable_column in environment_columns:
        # 执行列联表检验
        crosstab = pd.crosstab(merged_data[phenotype_column], merged_data[categorical_variable_column])

        # 执行卡方检验
        chi2_stat, p_value, dof, expected = chi2_contingency(crosstab)

        # 执行Fisher's精确检验（如果样本较小或有预期的频次小于5）
        # fisher_result = fisher_exact(crosstab)

        # 根据p-value进行统计显著性检验
        alpha = 0.05  # 设置显著性水平
        if p_value < alpha:
            correlation = "Significant correlation"
        else:
            correlation = "No significant correlation"

        # 存储结果
        result_data.append({
            'PhenotypeColumnName': phenotype_column,
            'CategoricalVariableColumn': categorical_variable_column,
            'ChiSquareStatistic': chi2_stat,
            'PValue': p_value,
            'Correlation': correlation
        })

# 将结果转换为DataFrame
result_df = pd.DataFrame(result_data)

# 导出列联表检验结果到CSV文件
result_df.to_csv("contingency_table_results.csv", index=False)
print("列联表检验结果已导出到文件: contingency_table_results.csv")