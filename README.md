# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0. Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Lightweight helper libraries only** (e.g. `pandas`, `mysql-connector-python`).  
  List every dependency in **`requirements.txt`** and justify anything unusual.
- **No ORMs / auto-migration tools** – write plain SQL by hand.

---

## 1. Clone the Skeleton Repo

```bash
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ **Note:** Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```bash
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:  
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

## 2. Problem

- You are provided with a raw JSON file containing property records located in `data/`
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied `Field Config.xlsx` (in `data/`) to understand business semantics.

### Task

- **Normalize the data:**
  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer to the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

#### Deliverable:
- Write necessary Python and SQL scripts
- Place your scripts in `sql/` and `scripts/`
- The scripts should take the initial JSON to your final, normalized schema when executed
- Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**

- Python (include a `requirements.txt`)
- Use **MySQL** and SQL for all database work
- You may use any CLI or GUI for development, but the final changes must be submitted as Python/SQL scripts
- **Do not** use ORM migrations—write all SQL by hand

---

## 3. Submission Guidelines

- Edit the section at the bottom of this README with your solutions and instructions for each section.
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation
- Create a new private repo and invite the reviewer: https://github.com/mantreshjain

---

**Good luck! We look forward to your submission.**

---

## Solutions and Instructions (Filed by Candidate)

---

### 1. Database Design and Solution

**The database is normalized into six tables based on Field Config.xlsx to efficiently store property-related data:**

- **Property:** Stores core attributes like `property_title`, `address`, `tax_rate`, and `school_average`. Primary key: `property_id` (INT, AUTO_INCREMENT).
- **Leads:** Contains lead-specific data like `reviewed_status`, `net_yield`, and `irr`. Foreign key: `property_id`.
- **Taxes:** Stores tax information (`taxes`). Foreign key: `property_id`.
- **Valuation:** Holds multiple valuation records per property (e.g., `list_price`, `zestimate`). Foreign key: `property_id`.
- **HOA:** Stores multiple HOA records (e.g., `hoa`, `hoa_flag`). Foreign key: `property_id`.
- **Rehab:** Contains multiple rehab estimates (e.g., `underwriting_rehab`, `paint`). Foreign key: `property_id`.

**Design Decisions:**

- Normalized to third normal form (3NF) to eliminate redundancy and ensure data integrity.
- Used `ENUM('Yes', 'No')` for binary flags (e.g., `pool`, `hoa_flag`) to enforce consistency.
- Fields are nullable (except primary keys) to handle missing/empty JSON values (e.g., Occupancy).
- Data types (`VARCHAR`, `DECIMAL`, `INT`) align with JSON data and business semantics from Field Config.xlsx.
- Foreign keys ensure relational integrity between Property and child tables.

#### Instructions to Run and Test the Script

1. **Start the MySQL database using Docker:**

   ```bash
   docker-compose -f docker-compose.initial.yml up --build -d
   ```
   This starts the `home_db` database on `localhost:3306` with user `db_user` and password `6equj5_db_user`.

2. **Create tables using the SQL script:**

   ```bash
   Get-Content sql\create_tables.sql | mysql -h localhost -u db_user -p home_db
   ```
   Enter password: `6equj5_db_user`.
   This creates six tables: Property, Leads, Taxes, Valuation, HOA, Rehab.

3. **Verify table creation:**

   ```bash
   mysql -h localhost -u db_user -p home_db
   ```

- Explain your schema and any design decisions
- Give clear instructions on how to run and test your script

---

### 2. ETL Logic

- Outline your approach and design
- Provide instructions and code snippets for running the ETL
- List any requirements

**Approach and Design:**

The ETL script (`scripts/etl.py`) performs the following:

- **Extract:** Reads `data/fake_property_data.json` using Python’s `json` module.
- **Transform:** Uses a `get_value` function to handle missing, empty, or whitespace values, converting them to NULL. Converts data types (e.g., float for `Tax_Rate`, int for `Bed`) with error handling. Processes nested arrays (`Valuation`, `HOA`, `Rehab`) into multiple records linked by `property_id`.
- **Load:** Connects to MySQL using `mysql-connector-python`, inserts data into the six tables, and maintains foreign key relationships. Commits changes to ensure data persistence.
- Error handling includes catching JSON file errors, database connection issues, and invalid data types.
