import re
import os
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import HashingTF, IDF
from pyspark.ml.feature import Tokenizer
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, udf, col
from pyspark.sql.types import *

sc = SparkSession.builder \
    .master('local[*]') \
    .config("spark.driver.memory", "15g") \
    .config("spark.sql.shuffle.partitions", 6) \
    .config("spark.executor.memory", '12g') \
    .appName('MovieGenrePrediction') \
    .getOrCreate()

sqlContext = SQLContext(sc)

df = (sqlContext.read
      .format("com.databricks.spark.csv")
      .options(header='true', inferschema='true', quote='"', delimiter=',', escape='"')
      .load(r"train.csv"))

def clean_text(text):
    text = text.lower()
    text = re.sub("\'", "", text)
    text = re.sub('[°-°|\â€:,;!@#$%^&*()0123456789-_`“†✠.•”’—{}]', '', text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = ' '.join(text.split())
    return text

def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

def isGenreAvailable(x, genre):
    a = 0
    if x is not None:
        if genre in x:
            a = 1
    return a

def add_column(column_name, dataframe, op_udf):
    for column in dataframe.columns:
        if column == column_name:
            return op_udf(column)

#Get the list of genres
def genre_lst():
    genres = []
    df = (sqlContext.read
          .format("com.databricks.spark.csv")
          .options(header='true', inferschema='true', quote='"', delimiter=',', escape='"')
          .load(r"mapping.csv"))

    data = df.select(col("0").alias("genre"))
    for row in data.rdd.collect():
        genres.append(row['genre'])
    return genres


# Cleaning Text - Postprocessing.
clean_text_using_udf = udf(lambda x: clean_text(x), StringType())
new_df = df.select(
    *[clean_text_using_udf(column).alias('plot') if column == 'plot' else column for column in df.columns])

# Removing Stop words.
stop_words = {'there', 'mustn', 'only', 'more', 'doesn', 'this', 'up', 'her', 'off', 'having', 'after', 'ourselves', 'each', 't', 'couldn', 'isn', 'by', "isn't", 'hers', 'shan', 'about', 'can', "wasn't", 'below', 'over', 'further', 'me', 'myself', 'as', "mightn't", "shouldn't", 're', 'we', 'where', 'of', 'needn', "she's", 'on', 'them', 'most', 'in', 'than', 'too', 'mightn', 'won', 'during', 'don', 'he', 'that', 'these', 'their', 'd', 'our', 'o', "wouldn't", 'with', 'no', 'm', 'yourselves', "doesn't", 'before', 'few', 'weren', 'again', 'while', 'its', 'themselves', 'such', 'wouldn', 'were', 'be', 'my', 'against', 'are', 'am', 'who', 'between', 'some', 'not', "shan't", 'ma', 'nor', 'aren', 'now', 'your', 'wasn', 'whom', 'down', 'why', 'which', 'being', 'they', 'very', "that'll", "it's", 'herself', 'an', 'and', "you'll", 'from', "should've", 'the', 'has', 'himself', 'it', 'above', "you'd", 'she', 'under', 'itself', 'then', 'own', 'any', 'yours', 'those', 'haven', 'hasn', "didn't", 'because', 'both', 'y', "couldn't", 'i', 'did', "hadn't", 'so', "you're", 'do', 'all', "needn't", 'when', "haven't", 'him', 'if', 'doing', 'been', 'but', 'was', 'at', "you've", 'other', 'his', 'should', 'or', "mustn't", "won't", 'once', 'theirs', 've', 'is', "aren't", 'have', "weren't", 's', "hasn't", 'into', 'out', 'same', "don't", 'will', 'didn', 'yourself', 'hadn', 'll', 'until', 'had', 'ain', 'for', 'through', 'a', 'does', 'just', 'shouldn', 'ours', 'how', 'what', 'here', 'to', 'you'}

remove_stopwords_from_plot = udf(lambda x: remove_stopwords(x), StringType())
df_with_stop_words_removed = new_df.select(
    *[remove_stopwords_from_plot(column).alias('plot') if column == 'plot' else column for column in df.columns])

genre_list =[]
for genre in genre_lst():
  genre = genre.replace(" ", "_")
  genre = genre.replace("/", "_")
  genre = genre.replace("-", "_")
  genre_list.append(genre)

for genre in genre_list:
    genre_name = genre.replace(" ", "_")
    map_df_udf = udf(lambda x: isGenreAvailable(x, genre), StringType())
    df_with_stop_words_removed = df_with_stop_words_removed.withColumn("genre_" + genre_name, lit(
        add_column('genre', df_with_stop_words_removed, map_df_udf)))
    df_with_stop_words_removed = df_with_stop_words_removed.withColumn("genre_" + genre_name,
                                                                       df_with_stop_words_removed[
                                                                           "genre_" + genre_name].cast(IntegerType()))

# Tokenizer and Hashing
tokenizer = Tokenizer(inputCol="plot", outputCol="word_plot")
wordsData = tokenizer.transform(df_with_stop_words_removed)

# HashingTF
hashingTF = HashingTF(numFeatures=5000, inputCol="word_plot", outputCol="rawFeatures")
featurizedData = hashingTF.transform(wordsData)

#TF-IDF
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

# Applying on Test Data
test_df = (sqlContext.read
           .format("com.databricks.spark.csv")
           .options(header='true', inferschema='true', quote='"', delimiter=',', escape='"')
           .load(r"test.csv"))

test_new_df = test_df.select(
    *[clean_text_using_udf(column).alias('plot') if column == 'plot' else column for column in test_df.columns])
test_df_with_stop_words_removed = test_new_df.select(
    *[remove_stopwords_from_plot(column).alias('plot') if column == 'plot' else column for column in
      test_new_df.columns])

test_tokenizer = Tokenizer(inputCol="plot", outputCol="word_plot")
test_wordsData = test_tokenizer.transform(test_df_with_stop_words_removed)

# Hashing TF on Test
test_hashingTF = HashingTF(numFeatures=5000, inputCol="word_plot", outputCol="rawFeatures")
test_featurizedData = test_hashingTF.transform(test_wordsData)

#TF-IDF on Test
test_idf = IDF(inputCol="rawFeatures", outputCol="features")
test_idfModel = test_idf.fit(test_featurizedData)
test_rescaledData = test_idfModel.transform(test_featurizedData)

if os.path.exists("_model_part2/"):
    test_predictions = []
    for i in range(0, len(genre_list)):
        genre_name = genre_list[i].replace(" ", "_")
        model_load = LogisticRegressionModel.load("_model_part2/model_"+genre_name)
        predictions = model_load.transform(test_rescaledData)
        pred = predictions.select(col("prediction").alias("prediction_" + genre_name), col('movie_id'))
        test_predictions.append(pred)
else:
    test_predictions = []
    train = rescaledData
    for i in range(0, len(genre_list)):
        genre_name = genre_list[i].replace(" ", "_")
        lr = LogisticRegression(maxIter=1000, featuresCol='features', labelCol='genre_' + genre_name)
        model = lr.fit(train)
        model.save(r"_model_part2/model_"+genre_name)
        predictions = model.transform(test_rescaledData)
        pred = predictions.select(col("prediction").alias("prediction_" + genre_name), col('movie_id'))
        test_predictions.append(pred)

test_data = test_rescaledData
for pred in test_predictions:
    test_data = test_data.join(pred, how='inner', on=['movie_id'])

sql_str = ''
for genre in genre_list:
    genre_name = "prediction_" + genre.replace(" ", "_") + ", "
    sql_str += genre_name

test_data.registerTempTable("test_sql")
test_pred = sqlContext.sql("SELECT movie_id, CONCAT(REPLACE(prediction_Drama,'.0',' '),REPLACE(prediction_Comedy,'.0',' '),REPLACE(prediction_Romance_Film,'.0',' '),REPLACE(prediction_Thriller,'.0',' '),REPLACE(prediction_Action,'.0',' '),REPLACE(prediction_World_cinema,'.0',' '),REPLACE(prediction_Crime_Fiction,'.0',' '),REPLACE(prediction_Horror,'.0',' '),REPLACE(prediction_Black_and_white,'.0',' '),REPLACE(prediction_Indie,'.0',' '),REPLACE(prediction_Action_Adventure,'.0',' '),REPLACE(prediction_Adventure,'.0',' '),REPLACE(prediction_Family_Film,'.0',' '),REPLACE(prediction_Short_Film,'.0',' '),REPLACE(prediction_Romantic_drama,'.0',' '),REPLACE(prediction_Animation,'.0',' '),REPLACE(prediction_Musical,'.0',' '),REPLACE(prediction_Science_Fiction,'.0',' '),REPLACE(prediction_Mystery,'.0',' '),REPLACE(prediction_Romantic_comedy,'.0',' ')) AS predictions FROM test_sql")
test_pred.show()
test_pred.coalesce(1).write.csv('final_predictions_TFIDF.csv',header=True)