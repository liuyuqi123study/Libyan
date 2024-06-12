import pandas as pd
import jieba
import csv
from bert_serving.client import BertClient
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

data=pd.read_csv("Herong.csv").astype(str)
content=data['留言内容']
#对留言内容进行分词
sentence_cut=[jieba.lcut(line) for line in content]
stopwords=pd.read_csv("stopwords.txt",header=None,quoting=csv.QUOTE_NONE,delimiter='\t')
#转换为列表形式
stopwords=stopwords[0].tolist()
not_stopwords=[[word for word in line if word not in stopwords and len(word)>1] for line in sentence_cut]
#将二维列表转换为一维列表
corpus=[i for item in not_stopwords for i in item]
print(corpus[0])
bc=BertClient()
vectors=bc.encode(corpus)

#利用bert_serving进行文本向量化
#对向量化的结果进行PCA降维
vectors_=PCA.fit_transform(vectors)

#利用kmeans进行聚类
y_=KMeans.fit_predict(vectors_)
plt.rcParams['font.sans-serif']=['SimHei']
plt.scatter(vectors_[:,0],vectors_[:,1],c=y_)
for i in range(len(corpus)):
    plt.annotate(s=corpus[i],xy=(vectors_[:,0][i],vectors_[:,1][i]),xytext=(vectors_[:,0][i]+0.1,vectors_[:,1][i]+0.1))
plt.show()