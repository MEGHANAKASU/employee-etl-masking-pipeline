from google.cloud import storage
import os

# ── CONFIG ──────────────────────────────────────────
PROJECT_ID = "crested-polygon-490400-s2"
BUCKET_NAME = "employee-etl-bucket-meghana-2"
LOCAL_FILE = "data/raw_employees.csv"
GCS_DESTINATION = "raw/raw_employees.csv"

# ── CREATE BUCKET ────────────────────────────────────
def create_bucket():
    client = storage.Client(project=PROJECT_ID)
    try:
        bucket = client.create_bucket(BUCKET_NAME, location="US")
        print(f"✅ Bucket created: {BUCKET_NAME}")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Bucket already exists: {BUCKET_NAME}")
        else:
            print(f"❌ Bucket error: {e}")

# ── UPLOAD FILE ──────────────────────────────────────
def upload_file():
    client = storage.Client(project="crested-polygon-490400-s2")
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(GCS_DESTINATION)
    blob.upload_from_filename(LOCAL_FILE)
    print(f"✅ Uploaded {LOCAL_FILE} → gs://{BUCKET_NAME}/{GCS_DESTINATION}")

# ── MAIN ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  EMPLOYEE ETL — UPLOAD TO GCS")
    print("=" * 55)

    print(f"\nCreating GCS bucket...")
    create_bucket()

    print(f"\nUploading raw employee data...")
    upload_file()

    print(f"\n✅ Data available at:")
    print(f"   gs://{BUCKET_NAME}/{GCS_DESTINATION}")
    print(f"\nCheck in GCS Console:")
    print(f"   https://console.cloud.google.com/storage/browser/{"employee-etl-bucket-meghana-2-2"}")
if __name__ == "__main__":
    main()