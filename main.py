import sys
from pyspark.sql import SparkSession
from scripts.bronze import fetch_api_data
from scripts.silver import process_silver
from scripts.gold import process_gold

def main():
    # Spark Session initialization
    spark = SparkSession.builder \
        .appName("BeesBreweryPipeline") \
        .getOrCreate()

    print("--- Pipeline Started ---")

    try:
        # Layer orchestration
        bronze_file = fetch_api_data() 
        process_silver(spark, bronze_file)
        process_gold(spark, "data/silver/breweries_partitioned")

        print("--- Pipeline Finished Successfully! ---")

    except Exception as e:
        print(f"Execution Failure: {e}")
        sys.exit(1)

    finally:
        spark.stop()

if __name__ == "__main__":
    main()