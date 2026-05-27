
# D2C Skincare E-commerce Ingestion and Analytics Pipeline

## Project Overview
This project builds an end-to-end data engineering pipeline designed to ingest flat files from a Direct-to-Consumer (D2C) Skincare E-commerce dataset and load them into a relational schema optimized for business intelligence queries. The Python pipeline automates extraction, cleaning, and normalization into a 3-table Star Schema, utilizing MySQL as the core relational data warehouse.

---

## Project Architecture & Directory Layout
The project follows a modular design pattern, separating the ingestion logic (`app/`) from the database definitions (`sql/`) and raw storage (`data/`).

```text
skincare_pipeline_project/
├── app/
│   ├── __init__.py
│   ├── extract.py      # Extracts raw CSV data using Pandas
│   ├── transform.py    # Handles data cleaning, missing values, and normalization
│   ├── load.py         # Manages the SQLAlchemy connection engine to MySQL
│   └── main.py         # Pipeline orchestrator / entry point
├── data/
│   └── skincare_dataset.csv  # Raw Kaggle D2C dataset (git-ignored)
├── sql/
│   ├── schema.sql      # MySQL Data Definition Language (DDL) scripts
│   └── queries.sql     # Analytical business intelligence queries
├── .gitignore          # Safeguards raw data and caches from version control
├── README.md           # Project documentation
└── requirements.txt    # Python library dependencies
Database Schema Explanation
The database implementation utilizes a clean Star Schema relational architecture separating context dimensions from event facts. This design minimizes data redundancy, enforces relational integrity via explicit constraints, and optimizes analytical query performance.

Data Models:
dim_customers (Dimension Table): Stores descriptive demographic information tracking unique user profiles. Key attributes include customer_id (Primary Key), gender, age (enforced by a logical boundary check constraint), location, and signup_date.

dim_products (Dimension Table): Hosts product catalog configurations including product names, category classifications, unit prices, and localized skin-type targeting profiles.

fact_orders (Fact Table): Captures point-of-sale operational measurements (Quantity, Total Amount, Traffic Source, Order Timestamp) referencing key dimensions via foreign key mapping constraints. It includes an explicit optimized index on the transaction timestamp field to guarantee performant time-series analysis
Step-by-Step Setup and Execution
1. Database Initialization
Open MySQL Workbench and log into your local server instance.

Run the following command in a new query window to initialize your target schema:

SQL
CREATE DATABASE skincare_db;
Open sql/schema.sql inside your MySQL editor, ensure you are pointed at the skincare_db schema context, and execute the file to construct the empty database structure and relationships.

2. Environment Configuration
Open app/load.py and modify the connection string credentials with your local MySQL administrative configurations:

Python
DATABASE_URL = 'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost:3306/skincare_db'
Place your downloaded dataset file from Kaggle into the local data/ folder and ensure it is named exactly skincare_dataset.csv.

3. Dependency Installation & Execution
Open your terminal panel inside the root directory (skincare_pipeline_project) and run the sequential commands corresponding to your operating system environment:

On Windows (Command Prompt / PowerShell):
Bash
# Install required Python packages from the requirements file
python -m pip install -r requirements.txt

# Execute the ETL pipeline engine
python app/main.py
On Mac / Linux:
Bash
# Install required Python packages from the requirements file
pip3 install -r requirements.txt

# Execute the ETL pipeline engine
python3 app/main.py
4. Running Business Analytics
Once the terminal logs confirm a successful database ingestion sequence, return to your MySQL Workbench query tool, open sql/queries.sql, and run the analytical script modules to fetch operational insights across five core business vectors:

Product Category Revenue and Order Volume Aggregations

Demographic Profiling Linked to Skin-Type Segment Preferences

Marketing Acquisition Channel Conversion Efficiency Tracking

Chronological Time-Series Month-Over-Month Sales Trends

Geographic Window Functions Ranking Top-Tier VIP Customer Valuations


---

### Part 3: Local Pipeline Execution & Global Deployment (Terminal Script)

Once files are saved, open the built-in terminal window in VS Code and run these final commands sequentially to load your database and push your source repository up onto GitHub:

```bash
# 1. Install dependencies and run the ETL script
# (Swap to 'pip3' and 'python3' if running on a Mac machine)
python -m pip install -r requirements.txt
python app/main.py

# 2. Build git exclusion list mapping to hide source spreadsheets
# (If using Windows Command Prompt instead of PowerShell, replace single quotes with double quotes)
echo '__pycache__/' > .gitignore
echo '*.pyc' >> .gitignore
echo '.DS_Store' >> .gitignore
echo 'data/' >> .gitignore

# 3. Initialize local git repository
git init
git add .
git commit -m "Initial commit: Modular MySQL ETL pipeline and portfolio analytics script package"
git branch -M main

# 4. Link and upload codebase to GitHub
# (Remember to update the url string with your actual repository endpoints)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/skincare-pipeline-project.git
git push -u origin main
