import os
import psycopg2
from dotenv import load_dotenv

# Load enterprise environment parameters from disk
load_dotenv()

def seed_database():
    # Establish network connection socket directly to the PostgreSQL Docker container
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "datapulse_admin"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "datapulse_warehouse")
    )
    cursor = conn.cursor()
    
    # Create the raw unstructured enterprise ingestion staging schema
    cursor.execute("""
        DROP TABLE IF EXISTS raw_workforce_logs;
        CREATE TABLE raw_workforce_logs (
            log_id SERIAL PRIMARY KEY,
            employee_name VARCHAR(100),
            department VARCHAR(50),
            assigned_hours INT,
            shift_notes TEXT,
            last_certification_date DATE
        );
    """)
    
    # Inject diverse high-fidelity sample records mimicking operational edge cases
    mock_data = [
        ('Alice Smith', 'Operations', 48, 'Completed consecutive overnight tactical shifts without standard depot cooldown period.', '2025-06-15'),
        ('Bob Jones', 'Customer Experience', 35, 'Standard daytime customer onboarding workflows.', '2026-02-10'),
        ('Charlie Brown', 'Fleet Deployment', 52, 'Assigned to extended vehicle recovery operations; compliance certification has lapsed past 12-month limit.', '2024-05-20'),
        ('Dana White', 'Operations', 40, 'Normal operational routines monitored with no active warnings.', '2026-07-01')
    ]
    
    cursor.executemany("""
        INSERT INTO raw_workforce_logs (employee_name, department, assigned_hours, shift_notes, last_certification_date)
        VALUES (%s, %s, %s, %s, %s);
    """, mock_data)
    
    conn.commit()
    print("🚀 Local Data Warehouse initialized and seeded successfully with 4 employee logging profiles!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_database()

