# D2C Skincare E-commerce Ingestion and Analytics Pipeline

##  Project Overview
This project delivers a production-grade, end-to-end data engineering pipeline designed to ingest flat-file transactional logs from a Direct-to-Consumer (D2C) Skincare E-commerce ecosystem. The system automates data extraction, sanitization, and relational normalization into a 3-table **Star Schema** data warehouse using MySQL. 

To transition this from a manual script into an enterprise data platform, the pipeline is fully **containerized using Docker** and **orchestrated via Apache Airflow**, ensuring high availability, environment isolation, and automated workflow scheduling.

---

##  Project Architecture & Directory Layout
The repository utilizes a decoupled modular layout separating pipeline orchestration orchestration (`app/` / `dags/`), relational definitions (`sql/`), and infrastructure configuration files.

```text
skincare_pipeline_project/
├── app/
│   ├── __init__.py
│   ├── extract.py      # Ingests raw flat-file CSV profiles using Pandas
│   ├── transform.py    # Standardizes text, manages missing attributes, and normalizes schema
│   ├── load.py         # Manages SQLAlchemy connection strings to the warehouse
│   └── main.py         # Baseline script entry-point orchestrator
├── data/
│   └── skincare_dataset.csv  # Raw Kaggle D2C dataset (git-ignored)
├── sql/
│   ├── schema.sql      # MySQL DDL data definitions (Constraints, Keys, Indexes)
│   └── queries.sql     # Complex OLAP analytical business intelligence queries
├── dags/
│   └── skincare_dag.py # Apache Airflow Directed Acyclic Graph definitions
├── .gitignore          # Safeguards physical raw assets from remote version control
├── docker-compose.yaml # Coordinates Docker containers (Airflow Webserver, Scheduler, MySQL)
├── Dockerfile          # Custom blueprint building the isolated Python runtime environment
├── README.md           # Master platform system documentation
└── requirements.txt    # Python third-party dependency manifest
 Database Schema Design
The target analytical storage architecture organizes raw rows into a optimized relational Star Schema designed to accelerate Read-heavy Analytical (OLAP) processing.

Data Models:
dim_customers (Dimension Table): Captures customer demographic and signup profiles. Enforces data cleanliness with an explicit age boundary validation check constraint (chk_age).

dim_products (Dimension Table): Stores structural retail properties including specific classifications and skin-type targets.

fact_orders (Fact Table): Tracks operational point-of-sale transactional metrics linked directly to core dimension keys. Built with an optimized chronological database index (idx_orders_date) for fast time-series partitioning.

 Pipeline Orchestration & Containerization
 Infrastructure Isolation (Docker)
The entire ecosystem is containerized to guarantee environment reproducibility. This eliminates the "it works on my machine" problem by deploying:

A dedicated MySQL Container acting as the target data warehouse.

Airflow Containers hosting the orchestration engine, web UI dashboard, and worker runtimes securely isolated from the host machine operating system.

 Workflow Automation (Apache Airflow)
Rather than executing scripts sequentially in a single risk-prone run, execution is broken down into a structured Directed Acyclic Graph (DAG). This guarantees:

Modular Failure Points: If a data load fails due to network latency, the extraction phase does not need to re-run.

Automated Retry Policies: Configured with robust handling exceptions to automatically retry tasks after an outage.

Visual Visibility: Full access to status monitors through the Airflow Web UI dashboard.

Plaintext
[extract_raw_csv] ──► [transform_clean_data] ──► [load_to_mysql_warehouse]
 Step-by-Step Setup and Execution
1. Prerequisite Environments
Ensure your machine has the following foundational services running locally:

Docker Desktop

Git

2. Dataset Positioning
Download the raw spreadsheet asset from Kaggle (kaushalvyas16/d2c-skincare-e-commerce-analytics-dataset).

Extract the archive zip file, rename the raw CSV sheet to skincare_dataset.csv, and move it directly into your local data/ folder directory.

3. Deploying the Platform Architecture
Launch the containerized environment using Docker. Open your terminal window inside your root project folder and run:

Bash
# Build custom images and spin up the environment in detached mode
docker-compose up --build -d
This single command automatically spins up the MySQL server, provisions the skincare_db schema, builds the internal target table layout from schema.sql, and launches the Apache Airflow portal.

4. Running the Pipeline Engine
Open your browser and navigate to the Airflow Interface at http://localhost:8080.

Locate the pipeline named d2c_skincare_etl_pipeline.

Toggle the DAG switch to Active and trigger the workflow manually (or let it run on its automated schedule).

 Analytical Data Intelligence
Once the Airflow interface registers a successful workflow log trail, navigate to your database environment or query utility tool and run the scripts available inside sql/queries.sql to generate insights across these 5 business vectors:

Category Volume Aggregations: Aggregates order velocities and overall margins across distinct product lineups.

Skin-Concern Segments: Joins user demographics to skin targeting attributes to map consumer buying indicators.

Marketing Channel Efficiency: Calculates specific customer acquisition value performance filtered via explicit HAVING threshold boundaries.

Time-Series Revenue Vectors: Generates historical, chronological month-over-month performance trends.

Geographical Window Groupings: Employs advanced window function mechanics (DENSE_RANK() OVER) to identify and isolate the top 3 high-value VIP patrons across individual regions.
