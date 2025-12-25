import pandas as pd
from typing import Tuple, List, Dict, Any
from .validator import RawMember, RawMember
from .normalizer import normalize_name, standardize_date
from pydantic import ValidationError

def load_and_process_data(file_path: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Loads CSV, normalizes, and validates data.
    Returns (valid_records, errors)
    """
    try:
        # Load Raw CSV
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return [], [{"error": "File not found"}]
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return [], [{"error": str(e)}]

    valid_records = []
    errors = []

    # Iterate row by row
    for index, row in df.iterrows():
        # 1. basic cleaning
        raw_data = row.to_dict()
        
        # 2. Normalize
        # Flexible column mapping
        raw_name = raw_data.get("Full Name") or raw_data.get("member_name")
        raw_email = raw_data.get("Email Address")
        raw_date_joined = raw_data.get("Date Joined") 
        raw_bio = raw_data.get("Bio_or_comment") or raw_data.get("bio_or_comment")
        raw_last_activity = raw_data.get("Last Activity") or raw_data.get("last_active_date")

        normalized_name = normalize_name(raw_name)
        # We don't have date joined in some CSVs, maybe use last_active as proxy or leave None
        normalized_date = standardize_date(raw_date_joined)
        normalized_last_active = standardize_date(raw_last_activity)
        
        # Capture context for error logging
        record_context = {
            "row_index": index + 2, 
            "raw_name": raw_name,
            "raw_email": raw_email
        }

        if not normalized_name:
            errors.append({**record_context, "error": "Invalid Name"})
            continue
        
        # If Date Joined is mandatory, failure. If optional, ignore.
        # Requirement: "Normalize names and standardize dates (flagging invalid entries)".
        # Doesn't explicitly say Date Joined is mandatory.
        
        # 3. Construct candidate dict for validation
        candidate = {
            "Full Name": normalized_name,
            "Email Address": raw_email,
            "Date Joined": normalized_date,
            "Bio_or_comment": raw_bio,
            "Last Activity": normalized_last_active
        }

        # 4. Validate with Pydantic
        try:
            member = RawMember(**candidate)
            # Create a clean dict for downstream
            clean_record = member.model_dump(by_alias=False)
            # Override with normalized values explicitly if needed, but Pydantic holds them if passed
            # We already passed normalized values to the model.
            
            # Additional logic: 'clean_record' now keys by field name in model?
            # Pydantic V2 model_dump: if by_alias=False, uses attribute names (full_name).
            
            valid_records.append(clean_record)
            
        except ValidationError as e:
            # Format Pydantic errors
            metrics = []
            for err in e.errors():
                metrics.append(f"{err['loc'][0]}: {err['msg']}")
            
            errors.append({
                **record_context, 
                "error": "; ".join(metrics)
            })

    return valid_records, errors
