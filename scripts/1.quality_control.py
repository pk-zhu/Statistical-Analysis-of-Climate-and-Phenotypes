import pandas as pd
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建 "1.data_qc" 目录路径
work_directory = os.path.join(parent_directory, "1.data_qc")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取数据
file_path = os.path.join(parent_directory, "data", "raw.csv")
data = pd.read_csv(file_path)

# 获取数据的来源列表
sources = data['source'].unique()

# 创建一个DataFrame来存储过滤后的数据
filtered_data = pd.DataFrame(columns=data.columns)

# 获取第三列后的所有数据列作为表型数据
phenotype_columns = data.columns[2:]

# 遍历每个来源
for source in sources:
    # 获取当前来源的数据
    source_data = data[data['source'] == source]
    
    # 遍历每个样本
    for _, row in source_data.iterrows():
        # 初始化一个标志，用于指示是否删除当前样本
        should_delete = False
        
        # 遍历每种表型列
        for column in phenotype_columns:
            # 计算平均值和标准差
            mean_value = source_data[column].mean()
            std_dev = source_data[column].std()
            
            # 检查是否有任何一个表型超出与平均值相差大于3个标准差
            if abs(row[column] - mean_value) > 3 * std_dev:
                should_delete = True
                break  # 如果有一个表型超出3个标准差，就不需要再检查其他表型了
        
        # 如果不需要删除当前样本，则将其添加到filtered_data中
        if not should_delete:
            filtered_data = filtered_data.append(row, ignore_index=True)

# 使用drop_duplicates()函数去除filtered_data中的重复行
filtered_data = filtered_data.drop_duplicates()

# 导出过滤后的数据到 "filtered.csv" 文件
filtered_data.to_csv("filtered.csv", index=False)

print("Filtered data saved to 'filtered.csv'.")
