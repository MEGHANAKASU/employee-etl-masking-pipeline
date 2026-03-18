# Employee ETL Masking Pipeline
**By Meghana Kasu | Visualization Analyst S1**

## Overview
End-to-end Employee ETL pipeline using Cloud Data Fusion,
GCS, Wrangler data masking and BigQuery.

## Sensitive Fields Masked
- SSN
- Email
- Phone
- Salary
- Date of Birth

## Tools Used
- Python + Faker
- Google Cloud Storage
- Cloud Data Fusion + Wrangler
- BigQuery
- Looker Studio

## How to Run
pip install -r requirements.txt
python3 data/generate_employees.py
python3 data/upload_to_gcs.py