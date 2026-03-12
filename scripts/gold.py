def process_gold(spark, input_path):
    df_silver = spark.read.parquet(input_path)
    # Agregação final solicitada 
    gold_df = df_silver.groupBy("brewery_type", "state_province", "city") \
        .count() \
        .withColumnRenamed("count", "brewery_qty")
    
    gold_df.write.mode("overwrite").parquet("data/gold/brewery_aggregation")