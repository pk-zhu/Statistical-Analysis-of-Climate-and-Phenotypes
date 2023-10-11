import pandas as pd
import os
import re
import statsmodels.api as sm
from statsmodels.formula.api import ols

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

# 进行多元回归分析
phenotype_columns = type_data.columns[2:]  # 从第三列到最后一列的所有列
environment_columns = env_data.columns[1:-1]  # 从第二列到倒数第二列的所有列

# 选中特定环境变量
print (environment_columns)
environment_columns = ['Latitude', 'Annual_Precipitation', 'Sunshine_Hours', 'Humidity', 'Source_Location_Distance']
# 创建一个空的 DataFrame 以存储回归分析结果
regression_results = pd.DataFrame(columns=['Phenotype', 'Environment', 'Coefficient', 'p-value', 'R-squared'])

for phenotype_column in phenotype_columns:
    print(f"正在进行多元回归分析，以 {phenotype_column} 作为因变量:")

    for environment_column in environment_columns:
        print(f"环境因子列: {environment_column}")

        # 构建多元回归模型
        formula = f"{phenotype_column} ~ {environment_column}"
        model = ols(formula=formula, data=merged_data).fit()

        # 提取回归系数、p值和R-squared
        coefficient = model.params[1]
        p_value = model.pvalues[1]
        r_squared = model.rsquared

        # 输出回归分析结果
        print(f"{environment_column} 的回归系数: {coefficient}")
        print(f"{environment_column} 的p值: {p_value}")
        print(f"{environment_column} 的R-squared: {r_squared}")
        print("=" * 50 + "\n")

        # 将结果添加到DataFrame
        regression_results = regression_results.append({'Phenotype': phenotype_column,
                                                        'Environment': environment_column,
                                                        'Coefficient': coefficient,
                                                        'p-value': p_value,
                                                        'R-squared': r_squared}, ignore_index=True)

# 导出回归分析结果到CSV文件
regression_results.to_csv("regression_results.csv", index=False)
print("多元回归分析结果已导出到文件: regression_results.csv")
