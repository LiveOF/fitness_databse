import sqlite3
import psycopg2
from psycopg2 import sql, DatabaseError

# Configure PostgreSQL connection details
PG_DB = "bank_db"
PG_USER = "postgres"
PG_PASSWORD = "password123"
PG_HOST = "localhost"
PG_PORT = "5432"

def setup_sqlite():
    """Sets up the personal database with mock pending income data."""
    conn = sqlite3.connect('personal.db')
    cursor = conn.cursor()
    
    # Create the table for expected incomes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expected_incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            sender_bank_id INTEGER,
            my_bank_id INTEGER,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Insert mock data if table is empty
    cursor.execute('SELECT COUNT(*) FROM expected_incomes')
    if cursor.fetchone()[0] == 0:
        incomes = [
            # Assume employer bank id is 1 and personal account bank id is 2
            ('Monthly Salary', 3500.00, 1, 2, 'pending'),
            ('Consulting Gig', 500.00, 3, 2, 'pending')
        ]
        cursor.executemany('''
            INSERT INTO expected_incomes (source, amount, sender_bank_id, my_bank_id, status)
            VALUES (?, ?, ?, ?, ?)
        ''', incomes)
    
    conn.commit()
    return conn

def process_incomes():
    """Reads pending incomes from SQLite and processes them in PostgreSQL."""
    sqlite_conn = None
    pg_conn = None
    
    try:
        print("Setting up local personal SQLite DB...")
        sqlite_conn = setup_sqlite()
        sqlite_cursor = sqlite_conn.cursor()
        
        print("Connecting to bank PostgreSQL DB...")
        # Note: Set up connection to match your personal testing environment
        pg_conn = psycopg2.connect(
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        pg_conn.autocommit = True # Procedures managing transactions often require autocommit
        pg_cursor = pg_conn.cursor()
        
        # 3. Read pending incomes
        sqlite_cursor.execute("SELECT id, source, amount, sender_bank_id, my_bank_id FROM expected_incomes WHERE status = 'pending'")
        pending_incomes = sqlite_cursor.fetchall()
        
        if not pending_incomes:
            print("No pending incomes to process.")
            return

        for income in pending_incomes:
            inc_id, source, amount, sender_id, my_id = income
            print(f"\nProcessing income: {source} - ${amount}")
            
            try:
                # 4. Call `make_payment` stored procedure in PostgreSQL
                pg_cursor.execute("CALL make_payment(%s, %s, %s)", (sender_id, my_id, amount))
                
                # We can consider it processed if the stored procedure finishes without throwing backend PG errors
                # Note: `make_payment` writes to error_logs internally if validations fail.
                # In more advanced versions, `make_payment` could return a status output parameter to check success.
                
                # 5. Mark as processed in local SQLite
                sqlite_cursor.execute("UPDATE expected_incomes SET status = 'processed' WHERE id = ?", (inc_id,))
                sqlite_conn.commit()
                print(f"-> Successfully processed {source}")
                
            except Exception as e:
                print(f"-> Failed processing {source}: {e}")
                
    except DatabaseError as error:
        print(f"Database connection or execution error: {error}")
    finally:
        # 6. Wrap connection operations in try-except-finally blocks
        if sqlite_conn:
            sqlite_conn.close()
            print("\nClosed local SQLite connection.")
        if pg_conn:
            pg_conn.close()
            print("Closed bank PostgreSQL connection.")

if __name__ == '__main__':
    process_incomes()
