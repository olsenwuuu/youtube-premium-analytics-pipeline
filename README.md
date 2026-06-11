# YouTube Premium Analytics Pipeline

An end-to-end modern data engineering and product analytics pipeline designed to ingest raw user activity logs, transform them into high-value analytical marts using dbt, and enforce rigorous data governance and quality constraints. 

This project demonstrates how data architecture directly answers strategic business questions regarding user value, platform engagement, feature preferences, and customer churn.

---

## 🎯 Strategic Business Questions Answered

The data pipeline and downstream analytical layers were engineered specifically to provide the business logic necessary to answer four critical product growth questions:

### 1. Subscription Value: Are premium users getting enough value?
**Yes.** Active subscribers across all tiers maintain a steady average session length of **~50 minutes**. **Student plans** drive the highest platform engagement, averaging **50.5 minutes** per session, proving that the discounted tier attracts highly engaged, loyal users.

### 2. Daily Engagement Trends: What are the streaming trends over time?
**Highly Stable.** Platform consumption is utility-driven and flat across all seven days of the week. Individual plans consistently generate **~90k–93k minutes daily**, showing no major traffic drops or spikes between weekdays and weekends.

### 3. Hardware Preferences: Which devices are preferred based on plan type?
**Mobile First.** Mobile is indisputably the dominant device type across all plans, handling more volume than Desktop and TV combined. The **Individual Tier on Mobile** is the primary engine of the platform, generating over **400,000 minutes** streamed.

### 4. Retention and Churn Risk: Which segment is stable and which is at risk?
**Stable:** The **Individual plan** is the most stable segment, sustaining the lowest relative churn rate at **24.37%**. 
**At Risk:** The **Student plan** exhibits the highest churn rate on the platform at **29.00%**, closely followed by the Family plan at **26.88%**.

---

## 🏗️ Architecture & Data Flow

The pipeline is structured across a decoupled, modern data stack pattern:

![Data Lineage Graph](lineage_graph.png)

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
# Process raw JSON/CSV inputs to output data/streaming_warehouse.db
jupyter nbconvert --to notebook --execute notebooks/02_database_loading.ipynb