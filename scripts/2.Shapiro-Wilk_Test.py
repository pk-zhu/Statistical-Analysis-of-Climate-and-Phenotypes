import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import os

# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建 "1.data_qc" 目录路径
work_directory = os.path.join(parent_directory, "2.Shapiro-Wilk_Test")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取CSV文件
data = pd.read_csv('processed_data.csv')

# 获取表型数据的列
phenotype_columns = data.columns[2:]

# 创建一个空的DataFrame来存储检验结果
normality_test_results = pd.DataFrame(columns=['Phenotype', 'Test Statistic', 'P-Value'])

# 逐列进行正态性检验并绘制正态分布图
for phenotype in phenotype_columns:
    # 提取当前表型数据列的值
    phenotype_data = data[phenotype]
    
    # 执行正态性检验
    test_statistic, p_value = stats.normaltest(phenotype_data)
    
    # 绘制正态分布图
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.hist(phenotype_data, bins=20, density=True, alpha=0.6, color='b')
    plt.title(f'Histogram of {phenotype}')
    
    # 生成正态分布的随机样本
    mean, std = phenotype_data.mean(), phenotype_data.std()
    samples = np.random.normal(mean, std, size=len(phenotype_data))
    
    # 绘制正态分布曲线
    plt.subplot(1, 2, 2)
    plt.hist(samples, bins=20, density=True, alpha=0.6, color='r')
    plt.title('Normal Distribution')
    
    plt.suptitle(phenotype, fontsize=16)
    plt.tight_layout()


    pdf_filename = f'{phenotype}_normal_distribution.pdf'
    plt.savefig(pdf_filename)
    
    # 保存图形为JPEG文件
    jpg_filename = f'{phenotype}_normal_distribution.jpg'
    plt.savefig(jpg_filename, dpi=300)
    
    # 关闭图形
    plt.close()

    # 将结果添加到结果DataFrame中
    result_row = {'Phenotype': phenotype, 'Test Statistic': test_statistic, 'P-Value': p_value}
    normality_test_results = pd.concat([normality_test_results, pd.DataFrame([result_row])], ignore_index=True)


# 将结果保存到文件
normality_test_results.to_csv('normality_test_results.csv', index=False)

print("正态性检验完成，结果已保存到 normality_test_results.csv 文件中。")
