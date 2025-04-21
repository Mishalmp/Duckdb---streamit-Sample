import duckdb
import os

def setup_duckdb():
    print("Setting up DuckDB database...")
    
    # Path to your CSV file
    csv_file = "dataset_eventscop_financier_YYYYMM.csv"
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        return False
    
    try:
        # Connect to or create DuckDB database
        conn = duckdb.connect("financier_data.duck.db")
        
        # Create table from CSV
        conn.execute("""
        CREATE OR REPLACE TABLE financier_data AS 
        SELECT * FROM read_csv_auto(?, delim=';')
        """, [csv_file])
        
        # Verify data was loaded
        result = conn.execute("SELECT COUNT(*) FROM financier_data").fetchone()[0]
        print(f"Successfully loaded {result} records into DuckDB")
        
        # Display sample data
        print("\nSample data:")
        sample = conn.execute("SELECT * FROM financier_data LIMIT 3").fetchdf()
        print(sample)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up DuckDB: {e}")
        return False

if __name__ == "__main__":
    setup_duckdb()