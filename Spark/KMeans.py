import findspark

findspark.init()
from pyspark.sql import SparkSession
# from pyspark.ml.clustering import KMeans
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans


log_file = '../spider/bilibili/allc.csv'

spark = SparkSession.builder.appName('test').master('local[*]').getOrCreate()
sc = spark.sparkContext
log_data = sc.textFile(log_file).cache()

stop_word_path = "stop_word.txt"
with open(stop_word_path, "r", encoding='utf-8') as f:
    stop_words = [line.strip() for line in f]

log_data = log_data.map(lambda x: jieba.lcut(x.split(",")[-1].strip()))
log_data = log_data.map(lambda x: " ".join(x))
print(log_data.collect())

countVectorizer = CountVectorizer(stop_words=stop_words, analyzer="word")
count_v = countVectorizer.fit_transform(log_data.collect()[:10000])
textsss = log_data.collect()

tfidfTransformer = TfidfTransformer()
tfidf = tfidfTransformer.fit_transform(count_v)

clf = KMeans()
y = clf.fit_predict(tfidf.toarray())
# print(y)

result = {}
for text_idx, lable_idx in enumerate(y):
    key = "cluster_{}".format(lable_idx)
    if key not in result:
        result[key] = [text_idx]
    else:
        result[key].append(text_idx)
for clu_k, clu_v in result.items():
    print("\n", "~"*170)
    print(clu_k)
    print(clu_v)

    for i in clu_v:
        print(textsss[i])



