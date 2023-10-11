import pandas as pd
from sklearn.cluster import KMeans
import os
import re
from sklearn.preprocessing import LabelEncoder


# 获取脚本所在目录的路径
script_directory = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录的上级目录路径
parent_directory = os.path.dirname(script_directory)
# 将上级目录路径设置为工作路径
os.chdir(parent_directory)

# 新建路径
work_directory = os.path.join(parent_directory, "5.Kruskal-Wallis")
os.makedirs(work_directory, exist_ok=True)
os.chdir(work_directory)

# 读取CSV文件
file_path = os.path.join(parent_directory, "data", "env.csv")
data = pd.read_csv(file_path)

# 列名转换函数
def clean_column_name(column_name):
    # 清理列名：去掉括号内的内容，将空格替换为下划线，并删除结尾的下划线
    cleaned_name = re.sub(r'\([^)]*\)', '', column_name).replace(" ", "_")
    if cleaned_name.endswith("_"):
        cleaned_name = cleaned_name[:-1]
    return cleaned_name

# 应用列名清理函数，将列名转为合适的格式
data.columns = [clean_column_name(col) for col in data.columns]

# 获取第二列到倒数第二列的列名
columns_to_cluster = data.columns[1:-1]

# 创建一个空的DataFrame来存储聚类结果
clustered_data = pd.DataFrame()

# 创建一个字典来存储每个分类列的标签编码器
label_encoders = {}

# # 遍历分类列并应用标签编码
# for col in columns_to_cluster:
#     label_encoder = LabelEncoder()
#     data[col] = label_encoder.fit_transform(data[col])
#     label_encoders[col] = label_encoder

# 循环处理每一列并进行聚类
for column in columns_to_cluster:
    # 选择当前列的数据
    X = data[[column]]
    
    # 数据标准化
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 确定聚类数量
    from sklearn.metrics import silhouette_score
    cluster_range = range(2, 14)
    scores = []
    for n_clusters in cluster_range:
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(X_scaled)
        score = silhouette_score(X_scaled, kmeans.labels_)
        scores.append(score)
    
    # 根据肘部法则选择最佳聚类数量，然后执行聚类
    best_n_clusters = cluster_range[scores.index(max(scores))]
    kmeans = KMeans(n_clusters=best_n_clusters)
    kmeans.fit(X_scaled)
    
    # 将聚类结果添加到clustered_data DataFrame
    clustered_data[column] = kmeans.labels_

# 反转每个分类列的标签编码，若想输出0，1则注释掉这部分
# for col, label_encoder in label_encoders.items():
#     clustered_data[col] = label_encoder.inverse_transform(clustered_data[col])





# 提取'source'列
source_column = data['source']
# 将'source'列添加到 DataFrame 的第一列
clustered_data = pd.concat([source_column, clustered_data], axis=1)
clustered_data.to_csv('cluster.csv', index=False)

labels = clustered_data['source']
clustered_data = clustered_data.drop('source', axis=1)

# Create a DataFrame to store cluster counts
cluster_counts = pd.DataFrame(columns=['Cluster'] + list(clustered_data.columns))

# Iterate over unique cluster labels
unique_clusters = clustered_data.iloc[:, 1:].values.ravel().tolist()
unique_clusters = list(set(unique_clusters))

for cluster in unique_clusters:
    cluster_counts = cluster_counts.append({'Cluster': cluster}, ignore_index=True)
    for column in clustered_data.columns[0:]:
        count = len(clustered_data[clustered_data[column] == cluster])
        cluster_counts.at[cluster_counts.index[-1], column] = count

# Transpose the cluster_counts DataFrame
cluster_counts = cluster_counts.set_index('Cluster').T.reset_index()
cluster_counts.rename(columns={'index': 'Cluster'}, inplace=True)

# Save the transposed cluster counts to a CSV file
cluster_counts.to_csv('cluster_counts.csv', index=False)

