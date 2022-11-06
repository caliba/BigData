import re

import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import Row
import jieba

log_file = '../spider/bilibili/alldanmu.csv'
N = 10

spark = SparkSession.builder.appName('test').master('local[*]').getOrCreate()
sc = spark.sparkContext
log_data = sc.textFile(log_file).cache()

log_data = log_data.map(lambda x: jieba.lcut(x.split(",")[-1].strip().lower()))
danmu_content = log_data.collect()
df = []
i = 0
for d in danmu_content:
    for w in d:
        if re.search(r"[a-zA-Z]+", w) is not None:
            df.append([w])
        i += 1

df = spark.createDataFrame(df, ["items"])
df = df.groupBy("items").count().collect()
df = sorted(df, key=lambda x: x[1], reverse=True)[:N]
print(df)


