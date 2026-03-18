# BEES Data Engineering Case - Open Brewery DB

This project implements a scalable data pipeline using the Medallion Architecture (Bronze, Silver, and Gold) to process information from the Open Brewery DB API.

---

## 🛠️ Tech Stack

* Python 3
* Apache Spark (PySpark)
* Docker & Docker Compose
* Parquet (Columnar Storage Format)

## 🛡️ Technical Approach & Design Decisions
This project was architected to demonstrate a production-ready Data Engineering pipeline, focusing on the following core principles:

Data Quality & Integrity: To mitigate risks associated with raw API data, the Silver Layer implements strict schema enforcement and data cleansing. Using the Parquet format ensures data types are preserved and optimized for downstream consumption, preventing "data drift."

Strategic Aggregation: Business logic is centralized in the Gold Layer. Instead of scattered queries, I implemented specific aggregations (e.g., breweries by type and location) to provide a single source of truth for analytical metrics, ensuring consistency across reports.

Scalability & Partitioning: The pipeline is designed to handle high volumes by utilizing partitioning strategies. This optimizes query performance and reduces cloud infrastructure costs by limiting the amount of data scanned during transformations.

Reliable Workflow: The repository structure follows modular engineering standards, facilitating collaboration and version control (Git). This architecture allows for clear traceability and easy rollbacks, ensuring a stable production environment.

## 🏗️ Project Architecture

The pipeline is structured into three logical layers:

1. Bronze (Raw): Ingests raw data from the API in JSON format using a resilient ingestion script.
2. Silver (Curated): Performs data cleaning, deduplication, and standardization. Data is stored in Parquet format and partitioned by location.
3. Gold (Analytical): Final data aggregation for business value, providing a view of brewery counts by type and location.

## 🚀 Technical Decisions & Resilience

### 1. Programmatic Orchestration
I chose not to use external orchestration tools such as Apache Airflow or Mage.ai for this challenge. The goal was to maintain a lightweight, portable, and easy-to-run solution. The flow is handled programmatically via a modularized main.py script, ensuring proper sequencing and error handling without the overhead of a complex infrastructure. The code is modular, allowing for future integration into tools like Airflow by importing existing functions into operators.

### 2. Infrastructure Resilience (API Ingestion)
I deliberately replaced unpredictable while True loops with a controlled for loop combined with a maximum page limit (max_pages). This implementation ensures the process is finite and safe for the infrastructure. Additionally, the logic includes an early-exit condition that breaks the loop immediately if the API returns an empty dataset, preventing unnecessary requests and resource exhaustion.

### 3. Technical Deep Dive: Silver Layer Transformations
The Silver layer ensures the data is reliable and optimized for analysis through the following operations:

* Schema Enforcement & Type Casting: Utilization of Spark’s withColumn and cast functions to ensure numerical fields and timestamps follow a strict schema, preventing type mismatches.
* Data Sanitization: Application of dropDuplicates based on the unique id and filtering out records missing critical business keys to ensure dataset integrity.
* Data Standardization: String cleaning and standardization to ensure consistency in categorical fields.
* Optimization via Partitioning: The data is persisted using the partitionBy("state_province") method. This implements Partition Pruning, allowing Spark to read only the relevant directories when queries filter by state, reducing I/O overhead.
* Storage Format: Persisted in Parquet format to leverage columnar storage and Snappy compression.

---

## 📈 Monitoring, Logging, and Alerting Strategy

The pipeline follows a production-grade observability approach:

* Structured Logging: Every step of the pipeline generates detailed logs using the Python logging library, allowing for tracking of data volume and execution time.
* Error Alerting: The pipeline is wrapped in a high-level try-except block. In a production cloud environment, this structure is designed to trigger notifications or alarms (such as SNS, Slack, or CloudWatch) upon failure.
* Data Integrity Monitoring: The process monitors the count of records ingested versus processed. If the API returns zero records or a significant drop is detected, a critical alert is logged for intervention.

---

## 🔧 How to Run

Ensure you have Docker installed and running. In the project root, run the following command:

```bash
docker-compose up --build