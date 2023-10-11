import pandas as pd
import os

# 设置工作路径

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建目录路径
work_directory = os.path.join(parent_directory, "4.ANOVA")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取文件件
type_path = os.path.join(parent_directory, "2.Shapiro-Wilk_Test", "processed_data.csv")
type_data = pd.read_csv("..\\2.Shapiro-Wilk_Test\\processed_data.csv")
env_path = os.path.join(parent_directory, "data", "env.csv")
env_data = pd.read_csv(env_path)

# 列名转换函数
import re

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

# 创建一个空数据框来存储合并后的结果
merged_result = pd.DataFrame()

# 循环遍历每个表型数据列
for phenotype_column in phenotype_columns:
    print(f"正在分析环境数据对 {phenotype_column} 的影响:")

    # 循环遍历每个环境数据列
    for environment_column in environment_columns:
        print(f"环境数据列: {environment_column}")
        
        
        # 构建多因素方差分析模型
        formula = f'{phenotype_column} ~ C({environment_column})'
        model = ols(formula, data=merged_data).fit()
        
        # 计算方差分析表
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        # 输出方差分析结果
        print(anova_table)
        print("\n" + "=" * 50 + "\n")  # 用于分隔不同环境数据的结果

        # 导出方差分析结果为CSV文件
        result_filename = f"result_{phenotype_column}_{environment_column}.csv"
        anova_table.to_csv(result_filename, index=False)
        print(f"方差分析结果已导出到文件: {result_filename}")

        # 将方差分析结果添加到合并结果中
        anova_table['Phenotype'] = phenotype_column
        anova_table['Environment'] = environment_column
        merged_result = pd.concat([merged_result, anova_table])

# 保存合并的结果为CSV文件
merged_result.to_csv("merged_anova_results.csv", index=False)
print("合并的方差分析结果已保存为 merged_anova_results.csv 文件")

# 移除带有空字符的行
merged_result = merged_result.dropna(subset=['Phenotype', 'Environment', 'PR(>F)'])
# 使用 pivot 表格来整理数据
pivot_table = merged_result.pivot(index='Phenotype', columns='Environment', values='PR(>F)')
# 保存整理后的表格为新的 CSV 文件
pivot_table.to_csv("pivot_anova_results.csv")
print("整理后的表格已保存为 pivot_anova_results.csv 文件")