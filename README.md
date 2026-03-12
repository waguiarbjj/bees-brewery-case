# BEES Data Engineering Case - Open Brewery DB

Este projeto implementa um pipeline de dados escalável utilizando a **Arquitetura Medallion** (Bronze, Silver e Gold) para processar informações da API Open Brewery DB.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Apache Spark (PySpark)**
* **Docker & Docker Compose**
* **Parquet** (Formato de armazenamento)

## 🏗️ Arquitetura do Projeto
O pipeline está dividido em três camadas lógicas:
1.  **Bronze (Raw):** Ingestão dos dados brutos da API em formato JSON.
2.  **Silver (Curated):** Limpeza, deduplicação e armazenamento em formato Parquet, com **particionamento por localização** (`state_province`).
3.  **Gold (Analytical):** Agregação final dos dados para entrega de valor ao negócio (contagem de cervejarias por tipo e localização).

## 🚀 Decisões Técnicas e Resiliência

### 1. Orquestração Programática (Sem ferramentas externas)
Optei por **não utilizar ferramentas de orquestração externas** (como Apache Airflow ou Mage.ai) para este desafio. O objetivo foi manter a solução leve, portável e de fácil execução ("One-Click Run"). A orquestração do fluxo de dados é feita de forma programática através de um script `main.py` modularizado, que garante o sequenciamento correto das camadas e o tratamento de erros sem a necessidade de uma infraestrutura complexa de DAGs para este escopo. Mantenho o código modular para que, se amanhã precisarmos escalar para o Airflow, basta importar as funções dos meus scripts para dentro das operadoras do Airflow sem precisar reescrever a lógica.

### 2. Escalabilidade com PySpark
Diferente do Pandas, o **PySpark** foi escolhido por sua capacidade de processamento distribuído. Isso garante que o pipeline esteja pronto para lidar com grandes volumes de dados (Big Data) seguindo as melhores práticas de Engenharia de Dados.

### 3. Segurança e Estabilidade
* **Paginação Controlada:** Substituí o uso de `while True` por laços controlados e tratamento de exceções para evitar loops infinitos e garantir a resiliência da infraestrutura durante a ingestão da API.
* **Storage Performance:** O uso de **Parquet particionado** na camada Silver otimiza a performance de leitura e reduz custos de armazenamento.

## 🔧 Como Executar
Certifique-se de ter o **Docker** instalado e rodando. Na raiz do projeto, execute:

```bash
docker-compose up --build