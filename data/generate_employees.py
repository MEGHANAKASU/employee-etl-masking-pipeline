import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# ── CONFIG ──────────────────────────────────────────
NUM_EMPLOYEES = 200
OUTPUT_PATH = "data/raw_employees.csv"

# ── REFERENCE DATA ──────────────────────────────────
DEPARTMENTS = ["Engineering", "Finance", "HR", "Marketing", "Operations", "Legal", "Sales"]
JOB_TITLES = {
    "Engineering": ["Software Engineer", "Data Engineer", "DevOps Engineer", "ML Engineer"],
    "Finance": ["Financial Analyst", "Accountant", "CFO", "Budget Analyst"],
    "HR": ["HR Manager", "Recruiter", "HR Analyst", "Compensation Analyst"],
    "Marketing": ["Marketing Manager", "Content Analyst", "SEO Specialist", "Brand Manager"],
    "Operations": ["Operations Manager", "Supply Chain Analyst", "Logistics Coordinator"],
    "Legal": ["Legal Counsel", "Compliance Officer", "Paralegal"],
    "Sales": ["Sales Manager", "Account Executive", "Sales Analyst", "BDR"]
}
LOCATIONS = ["New York", "Chicago", "Houston", "Los Angeles", "Seattle",
             "San Francisco", "Miami", "Dallas", "Boston", "Phoenix"]
EMPLOYMENT_STATUS = ["Active", "Active", "Active", "Active", "Inactive", "On Leave"]
PERFORMANCE_RATINGS = ["Exceeds Expectations", "Meets Expectations",
                        "Below Expectations", "Outstanding"]

# ── GENERATE EMPLOYEES ───────────────────────────────
def generate_employees(n):
    employees = []
    start_date = datetime(2018, 1, 1)

    for i in range(1, n + 1):
        department = random.choice(DEPARTMENTS)
        job_title = random.choice(JOB_TITLES[department])

        # Salary based on department
        if department in ["Engineering", "Finance", "Legal"]:
            salary = round(random.uniform(90000, 180000), 2)
        elif department in ["Marketing", "Operations"]:
            salary = round(random.uniform(60000, 120000), 2)
        else:
            salary = round(random.uniform(50000, 100000), 2)

        # Hire date
        days_offset = random.randint(0, 2000)
        hire_date = start_date + timedelta(days=days_offset)

        # Introduce some NULLs for DQ testing
        ssn = fake.ssn() if random.random() > 0.03 else None
        salary = salary if random.random() > 0.04 else None
        email = fake.company_email() if random.random() > 0.02 else None

        employees.append({
            "employee_id": f"EMP{str(i).zfill(5)}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,                          # SENSITIVE — will be masked
            "phone": fake.phone_number(),            # SENSITIVE — will be masked
            "ssn": ssn,                              # SENSITIVE — will be masked
            "date_of_birth": fake.date_of_birth(
                minimum_age=22, maximum_age=65
            ).strftime("%Y-%m-%d"),                  # SENSITIVE — will be masked
            "salary": salary,                        # SENSITIVE — will be masked
            "department": department,
            "job_title": job_title,
            "location": random.choice(LOCATIONS),
            "hire_date": hire_date.strftime("%Y-%m-%d"),
            "employment_status": random.choice(EMPLOYMENT_STATUS),
            "performance_rating": random.choice(PERFORMANCE_RATINGS),
            "manager_id": f"EMP{str(random.randint(1, 50)).zfill(5)}"
        })

    return pd.DataFrame(employees)

# ── MAIN ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  EMPLOYEE ETL — DATA GENERATION")
    print("=" * 55)

    print(f"\nGenerating {NUM_EMPLOYEES} employee records...")
    employees_df = generate_employees(NUM_EMPLOYEES)
    employees_df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Generated {len(employees_df)} employees → {OUTPUT_PATH}")
    print(f"\nSensitive fields included:")
    print(f"  🔴 SSN — {employees_df['ssn'].notna().sum()} records")
    print(f"  🔴 Email — {employees_df['email'].notna().sum()} records")
    print(f"  🔴 Phone — {employees_df['phone'].notna().sum()} records")
    print(f"  🔴 Date of Birth — {employees_df['date_of_birth'].notna().sum()} records")
    print(f"  🔴 Salary — {employees_df['salary'].notna().sum()} records")
    print(f"\nNULLs for DQ testing:")
    print(f"  SSN NULLs: {employees_df['ssn'].isna().sum()}")
    print(f"  Email NULLs: {employees_df['email'].isna().sum()}")
    print(f"  Salary NULLs: {employees_df['salary'].isna().sum()}")
    print(f"\nDepartment breakdown:")
    print(employees_df["department"].value_counts().to_string())
    print(f"\nSample data (first 3 rows):")
    print(employees_df[["employee_id", "first_name", "last_name",
                          "department", "salary", "employment_status"]].head(3))

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    main()