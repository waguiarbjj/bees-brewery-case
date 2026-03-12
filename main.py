import sys
from pyspark.sql import SparkSession
from scripts.bronze import fetch_api_data
from scripts.silver import process_silver
from scripts.gold import process_gold

def main():
    # Inicializa o Spark (Preferencial para o teste) 
    spark = SparkSession.builder.appName("Bees_Case").getOrCreate()
    print("--- Pipeline Iniciado ---")
    try:
        # Orquestração das camadas [cite: 8]
        bronze_file = fetch_api_data() 
        process_silver(spark, bronze_file)
        process_gold(spark, "data/silver/breweries_partitioned")
        print("--- Pipeline Finalizado com Sucesso! ---")
    except Exception as e:
        print(f"Falha na execução: {e}") # [cite: 13]
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()