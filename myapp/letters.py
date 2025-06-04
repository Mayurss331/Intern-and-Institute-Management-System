import subprocess
from datetime import datetime, timedelta
import pandas as pd
import pdfkit
import os
from django.conf import settings

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
options = {
    'enable-local-file-access': '',
    'page-width': 210,
    'page-height': 270,
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm'
}

def create_internship_offer_letter(full_name='', email='', last_batch='', Id='', role='', date=''):
    """
    Creates an internship offer letter as a PDF file in the static/Offer folder.

    Args:
        full_name (str): Full name of the candidate.
        email (str): Candidate's email address.
        last_batch (int): Last batch number from the CSV file.
        Id (int): Unique ID for the candidate.
        role (str): Internship role.
        date (str): Internship start date in YYYY-MM-DD format.

    Returns:
        str: The name of the generated PDF file.
    """

    # Split name into first and last
    name_list = full_name.split(" ")
    first_name = name_list[0]
    last_name = name_list[1] if len(name_list) > 1 else ""

    # Increment batch number
    new_batch = last_batch + 1

    # Generate internship ID
    current_year = str(datetime.now().year)
    intern_id = f"ELE{new_batch:02}{Id:02}{current_year}"

    # Path to candidates CSV in static/
    csv_file = os.path.join(settings.BASE_DIR, 'static', 'Candidates.csv')

    # Prepare new candidate data
    new_data = {
        'First Name': [first_name],
        'Last Name': [last_name],
        'Email': [email],
        'Batch': [new_batch],
        'Id': [Id],
        'Intern Id': [intern_id]
    }

    # Append new data to CSV
    new_entry_df = pd.DataFrame(new_data)
    new_entry_df.to_csv(csv_file, mode='a', header=False, index=False)

    # Format dates
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%d-%m-%Y')
    join_date_obj = date_obj + timedelta(days=7)
    join_date = join_date_obj.strftime('%d-%m-%Y')

    # Read role descriptions CSV from static/
    csv_path = os.path.join(settings.BASE_DIR, 'static', 'role_descriptions.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    result = df[df["role"] == role]

    if result.empty:
        return "Role not found."

    role_para = result.iloc[0]["description"]

    # Replace placeholders in HTML template
    replacements = {
        "{{candidatename}}": full_name,
        "{{internshipid}}": intern_id,
        "{{changedate}}": formatted_date,
        "{{joindate}}": join_date,
        "{{internshiprole}}": role,
        "{{rolepara}}": role_para
    }

    # Save modified HTML content in static/
    html_file = os.path.join(settings.BASE_DIR, 'static', 'offer-template.html')
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
        for key, value in replacements.items():
            html_content = html_content.replace(key, value)

    replaced_html_file = os.path.join(settings.BASE_DIR, 'static', 'offer_letter_temp.html')
    with open(replaced_html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)


    # Ensure the Offer directory exists inside static/
    output_directory = os.path.join(settings.BASE_DIR, 'static', 'offers')
    os.makedirs(output_directory, exist_ok=True)

    output_pdf = f"{output_directory}\\{replacements['{{candidatename}}'].replace(' ', '_')}_offer_letter.pdf"
    pdfkit.from_file(replaced_html_file, output_pdf, configuration=config, options=options)
    os.remove(replaced_html_file)
    return output_pdf
