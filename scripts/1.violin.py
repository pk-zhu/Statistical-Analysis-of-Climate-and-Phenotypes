import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt

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

# 读取数据文件
data = pd.read_csv("filtered.csv")

# 获取数据的来源列表
sources = data['source'].unique()

# 获取第三列后的所有数据列
phenotype_columns = data.columns[2:]

# 设置标题字体大小和风格
sns.set(font_scale=3.5)  # 设置标题字体大小
sns.set_style("whitegrid")  # 设置Seaborn样式

# 遍历每一列数据，绘制小提琴图
for column in phenotype_columns:
    # 创建小提琴图
    plt.figure(figsize=(32, 21))
    ax = sns.violinplot(x='source', \
                        y=column, data=data, inner=None, \
                        saturation=1, \
                        width=1, linewidth=0)

    # 使用stripplot或swarmplot来显示数据点
    sns.stripplot(x='source', y=column, data=data, color='black', size=4, ax=ax)
            
    # 设置图标题和轴标签
    plt.title(f"{column}", fontsize=50, y=1.05)
    plt.xlabel("Source", fontsize=40, labelpad=10)
    plt.ylabel("")
    plt.xticks(rotation=30)
    # 生成文件名并保存图像
    output_dir = "violin_plots"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"violinplot_{column}.png")
    plt.savefig(output_file)
    
    output_file_pdf = os.path.join(output_dir, f"violinplot_{column}.pdf")
    plt.savefig(output_file_pdf, format='pdf')
    # 关闭图形窗口
    plt.close()

print("Violin plots generated and saved in the 'violin_plots' directory.")
