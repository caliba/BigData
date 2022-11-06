import re

import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
import jieba

log_file = '../spider/bilibili/alldanmu.csv'

spark = SparkSession.builder.appName('test').master('local[*]').getOrCreate()
sc = spark.sparkContext
log_data = sc.textFile(log_file).cache()

log_data = log_data.map(lambda x: jieba.lcut(x.split(",")[-1].strip().lower()))
log_data = log_data.map(lambda x: sorted(list(set(x)), key=x.index))  # 去重
danmu_content = log_data.collect()
df = []
i = 0
for d in danmu_content:
    line = []
    for w in d:
        if re.search(r"[a-zA-Z]+", w) is not None:
            line.append(w)
    if len(line) != 0:
        df.append([line])
        i += 1

# print(df)
df = spark.createDataFrame(df, ["items"])
fpGrowth = FPGrowth(itemsCol="items", minSupport=0.0001)

model = fpGrowth.fit(df)

model.freqItemsets.show()

model.associationRules.show()

# model.transform(df).show()
