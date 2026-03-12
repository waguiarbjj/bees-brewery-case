# BEES Data Engineering Case - Open Brewery DB

This project implements a scalable data pipeline using the Medallion Architecture (Bronze, Silver, and Gold) to process information from the Open Brewery DB API.

---

## 🛠️ Tech Stack

* **Python 3**
* **Apache Spark (PySpark)**
* **Docker & Docker Compose**
* **Parquet** (Columnar Storage Format)

---

## 🏗️ Project Architecture

The pipeline is structured into three logical layers:

1.  **Bronze (Raw):** Ingests raw data from the API in JSON format.
2.  **Silver (Curated):** Cleans, deduplicates, and stores data in Parquet format, with partitioning by location (`state_province`).
3.  **Gold (Analytical):** Final data aggregation for business value (brewery count by type and location).

---

## 🚀 Technical Decisions & Resilience

### 1. Programmatic Orchestration (No external tools)
I chose not to use external orchestration tools (such as Apache Airflow or Mage.ai) for this challenge. The goal was to keep the solution lightweight, portable, and easy to run ("One-Click Run"). 

The data flow orchestration is handled programmatically via a modularized `main.py` script, ensuring proper sequencing and error handling without the overhead of a complex DAG infrastructure for this scope. I kept the code modular so that, if scaling to Airflow is required in the future, the existing functions can be easily imported into Airflow operators without rewriting logic.

### 2. Scalability with PySpark
Unlike Pandas, PySpark was chosen for its distributed processing capabilities. This ensures the pipeline is ready to handle large data volumes (Big Data) following Data Engineering best practices.

### 3. Safety and Stability
* **Controlled Pagination:** I deliberately replaced unpredictable `while True` loops with a controlled `for` loop combined with a maximum page limit (`max_pages`). This implementation ensures the process is finite and safe. Additionally, the logic includes an early-exit condition that breaks the loop immediately if the API returns an empty dataset, preventing unnecessary requests and resource exhaustion.
* **Storage Performance:** Using partitioned Parquet in the Silver layer optimizes read performance and reduces storage costs.

---

## 🔧 How to Run

Ensure you have Docker installed and running. In the project root, run the following command:

```bash
docker-compose up --build