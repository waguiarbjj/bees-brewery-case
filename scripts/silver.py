from pyspark.sql.functions import col

def process_silver(spark, input_path):
    df = spark.read.json(input_path)
    # Limpeza e Deduplicação 
    df_clean = df.dropDuplicates().filter(col("id").isNotNull())
    
    # Salvando em Parquet particionado por localização 
    df_clean.write.mode("overwrite") \
        .partitionBy("state_province") \
        .parquet("data/silver/breweries_partitioned")