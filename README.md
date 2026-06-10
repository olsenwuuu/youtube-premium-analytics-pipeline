# YouTube Premium Analytics Pipeline

An end-to-end modern data engineering and product analytics pipeline designed to ingest raw user activity logs, transform them into high-value analytical marts using dbt, and enforce rigorous data governance and quality constraints. 

This project demonstrates how data architecture directly answers strategic business questions regarding user value, platform engagement, feature preferences, and customer churn.

---

## 🎯 Strategic Business Questions Answered

The data pipeline and downstream analytical layers were engineered specifically to provide the business logic necessary to answer four critical product growth questions:

1. **Subscription Value:** Are premium users getting enough value from their subscription?

2. **Daily Engagement Trends:** What are the daily streaming trends over time?

3. **Hardware Preferences:** Which devices are preferred based on plan type?

4. **Retention and Churn Risk:** Which subscriptions are stable and which are at risk of churn?

---

## 🏗️ Architecture & Data Flow

The pipeline is structured across a decoupled, modern data stack pattern:
1. **Ingestion & Database Loading:** Raw JSON user activity records (`raw_activity_logs.json`) and subscription data are processed and loaded via Python/Pandas into a local SQLite data warehouse instance.
2. **Data Cataloging (dbt Sources):** Raw tables are registered into `sources.yml` to decouple the underlying database architecture from transformation logic and build automated data lineage.
3. **Dimensional Modeling (Marts):** Transformations are written in optimized SQL (`fct_streaming_summary.sql`) to aggregate granular streaming events into an enterprise-ready production mart.

---

## 🧪 Data Quality, Governance & Testing

To ensure absolute pipeline reliability and protect downstream metrics, this project implements a strict data governance framework within dbt:

* **Composite Key Uniqueness:** Enforces entity integrity on `fct_streaming_summary` by testing the true grain of the data model (`user_id` + `activity_date`), ensuring zero duplicate metric inflation.
* **Categorical Constraints (`accepted_values`):** Hardens business definitions by validating that fields like `plan_type` (`Individual`, `Family`, `Student`) and `account_status` (`Active`, `Canceled`) never ingest corrupted or drifted variations.
* **Null Pointer Prevention:** Guarantees comprehensive reporting by enforcing `not_null` criteria across all primary tracking keys and dimensions.
* **Decoupled Data Lineage:** Leverages dbt source abstraction (`{{ source() }}`) to map visual data flows from raw landing areas to final analytics tables, making the pipeline fully portable to enterprise warehouses like Snowflake or BigQuery.

---

## 🚀 How to Run Locally

### 1. Database Setup
Execute the ingestion notebooks to seed the SQLite warehouse:
```bash
# Run database loading notebook to process raw JSON/CSV inputs
# (Outputs: data/streaming_warehouse.db)
jupyter nbconvert --to notebook --execute notebooks/02_database_loading.ipynb
