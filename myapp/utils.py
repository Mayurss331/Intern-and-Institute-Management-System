import pandas as pd
from .models import Application

def process_excel(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")

    # Rename columns to match Django model fields
    df.columns = [
        "role", "timestamp", "first_name", "last_name", "email", "phone_number", "resume",
        "source", "gender", "date_of_birth", "domicile_state", "current_location",
        "citizenship", "postgraduate_degree", "postgraduate_stream",
        "postgraduate_passing_year", "undergraduate_degree", "undergraduate_stream",
        "undergraduate_passing_year", "college_name", "score_above_60",
        "standing_arrears", "coding_languages", "currently_working", "company_name",
        "ctc_or_stipend", "designation", "open_to_relocate", "passport_photo"
    ]

    # Remove whitespace from column names
    df.columns = df.columns.str.strip()

    # Convert date fields to string format
    df["timestamp"] = df["timestamp"].astype(str)  
    df["date_of_birth"] = df["date_of_birth"].astype(str)  

    # Convert passing years to integers (handling NaN values)
    df["postgraduate_passing_year"] = pd.to_numeric(df["postgraduate_passing_year"], errors="coerce").fillna(0).astype(int)
    df["undergraduate_passing_year"] = pd.to_numeric(df["undergraduate_passing_year"], errors="coerce").fillna(0).astype(int)

    # ✅ Convert Boolean fields properly (replace NaN with False)
    boolean_fields = ["score_above_60", "standing_arrears", "currently_working", "open_to_relocate"]
    for field in boolean_fields:
        df[field] = df[field].fillna(False).astype(bool)

    # ✅ Ensure `resume` and `passport_photo` are valid file paths (convert NaN to empty string)
    df["resume"] = df["resume"].fillna("").astype(str)
    df["passport_photo"] = df["passport_photo"].fillna("").astype(str)

    # Iterate through each row and insert data if email is not already present
    for _, row in df.iterrows():
        email = row["email"]

        # Check if the email already exists
        if not Application.objects.filter(email=email).exists():
            Application.objects.create(
                role=row["role"],
                timestamp=row["timestamp"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone_number=row["phone_number"],
                resume=row["resume"],  
                source=row["source"],
                gender=row["gender"],
                date_of_birth=row["date_of_birth"],
                domicile_state=row["domicile_state"],
                current_location=row["current_location"],
                citizenship=row["citizenship"],
                postgraduate_degree=row["postgraduate_degree"],
                postgraduate_stream=row["postgraduate_stream"],
                postgraduate_passing_year=row["postgraduate_passing_year"],
                undergraduate_degree=row["undergraduate_degree"],
                undergraduate_stream=row["undergraduate_stream"],
                undergraduate_passing_year=row["undergraduate_passing_year"],
                college_name=row["college_name"],
                score_above_60=row["score_above_60"],
                standing_arrears=row["standing_arrears"],
                coding_languages=row["coding_languages"],
                currently_working=row["currently_working"],
                company_name=row["company_name"],
                ctc_or_stipend=row["ctc_or_stipend"],
                designation=row["designation"],
                open_to_relocate=row["open_to_relocate"],
                passport_photo=row["passport_photo"]  # ✅ Now always a valid string
            )
            print(f"Inserted: {email}")
        else:
            print(f"Duplicate email found: {email}, skipping insertion.")
    