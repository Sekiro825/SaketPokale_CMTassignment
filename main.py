import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.etl.loader import load_and_process_data

def main():
    print("Running Volunteer-First OS ETL...")
    # Check for file in data/ or data/raw/
    if os.path.exists("data/members_raw.csv"):
        raw_path = "data/members_raw.csv"
    else:
        raw_path = "data/raw/members_raw.csv"
    
    print(f"Reading from: {raw_path}")
    
    valid, errors = load_and_process_data(raw_path)
    
    print(f"Processed {len(valid)} valid records.")
    print(f"Found {len(errors)} errors.")
    
    if valid:
        print("\n--- Starting AI Enrichment ---")
        from src.enrichment.processor import EnrichmentProcessor
        processor = EnrichmentProcessor()
        enriched_data = processor.process_batch(valid)
        
        print(f"Enriched {len(enriched_data)} records.")
        print("Sample Enriched Record:")
        print(enriched_data[0])
        
        # Persistence
        print("\n--- Saving to Database ---")
        try:
            from src.persistence.database import init_db, get_db, save_enriched_data
            
            init_db()
            db = next(get_db())
            try:
                save_enriched_data(db, enriched_data)
                print("Data saved successfully to volunteer_data.db")
            finally:
                db.close()
        except ImportError:
            print("WARNING: SQLAlchemy not found. Skipping persistence step.")
    
    if errors:
        print("\nSample Error:")
        print(errors[0])


if __name__ == "__main__":
    main()
