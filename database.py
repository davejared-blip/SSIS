import pandas as pd
import os

def load_students(csv_file):
    """Loads students from a CSV file and ensures required columns exist."""
    required_columns = [
        "First Name",
        "Last Name",
        "ID Number",
        "Age",
        "Year Level",
        "Gender",
        "College",
        "College Code",
        "Program",
        "Program Code"
    ]
    try:
        df = pd.read_csv(csv_file, dtype=str)
        
        # error checking
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        return df
    except (FileNotFoundError, ValueError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=required_columns)

def save_students(df, csv_file):
    """Safely saves student data, preventing file corruption."""
    temp_file = csv_file + ".tmp"
    try:
        df.to_csv(temp_file, index=False)
        os.replace(temp_file, csv_file)
    except Exception as e:
        print(f"Error saving students: {e}")

def extract_colleges_programs(csv_file):
    """Extracts valid colleges and programs dynamically from the student CSV."""
    df = load_students(csv_file)
    
    college_dict = {}
    program_dict = {}
    
    for _, row in df.iterrows():
        college = str(row["College"]).strip() if pd.notna(row["College"]) else ""
        program = str(row["Program"]).strip() if pd.notna(row["Program"]) else ""

        if college and program:
            college_dict.setdefault(college, set()).add(program)
            program_dict[program] = program  
    
    return {k: list(v) for k, v in college_dict.items()}, program_dict
