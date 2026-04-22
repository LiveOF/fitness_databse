import sqlite3
import psycopg2

# Configuration for the Bank PostgreSQL database
PG_DB = "bank_db"
PG_USER = "postgres"
PG_PASSWORD = "password123"  # Ensure this matches your local PostgreSQL password
PG_HOST = "localhost"
PG_PORT = "5432"

# Configuration for the local Fitness SQLite database
SQLITE_DB = "fitness_db.sqlite"

def setup_fitness_db():
    """Initializes the independent SQLite database for the fitness club."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # 1. Create the memberships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memberships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # 2. Create the purchases table to track membership buying status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_bank_account_id INTEGER NOT NULL,
            membership_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Insert some dummy memberships if the table is empty
    cursor.execute('SELECT COUNT(*) FROM memberships')
    if cursor.fetchone()[0] == 0:
        dummy_memberships = [
            ('Bronze Plan', 30.00),
            ('Silver Plan', 60.00),
            ('Gold VIP Plan', 120.00)
        ]
        cursor.executemany('''
            INSERT INTO memberships (name, price) VALUES (?, ?)
        ''', dummy_memberships)
    
    conn.commit()
    conn.close()

def buy_membership(user_bank_account_id, fitness_club_bank_account_id, membership_id):
    """
    Acts as a bridge between the fitness DB and the bank DB. 
    It processes a membership purchase by requesting a transaction from the bank.
    """
    sqlite_conn = None
    pg_conn = None
    purchase_id = None
    
    try:
        # Step 1: Connect to Fitness DB and fetch the membership price
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_cursor = sqlite_conn.cursor()
        
        sqlite_cursor.execute("SELECT name, price FROM memberships WHERE id = ?", (membership_id,))
        membership = sqlite_cursor.fetchone()
        
        if not membership:
            print("Error: Membership not found.")
            return
        
        mem_name, price = membership
        print(f"\nAttempting to buy '{mem_name}' for ${price} (User Account: {user_bank_account_id})...")
        
        # Step 2: Create a 'pending' purchase record in the Fitness DB
        sqlite_cursor.execute('''
            INSERT INTO purchases (user_bank_account_id, membership_id, status)
            VALUES (?, ?, 'pending')
        ''', (user_bank_account_id, membership_id))
        purchase_id = sqlite_cursor.lastrowid
        sqlite_conn.commit()
        
        # Step 3: Connect to the external PostgreSQL Bank DB
        pg_conn = psycopg2.connect(
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        pg_conn.autocommit = True  # Required for calling stored procedures containing COMMIT
        pg_cursor = pg_conn.cursor()
        
        # Fetch the initial balance of the fitness club to verify if payment arrives
        pg_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (fitness_club_bank_account_id,))
        initial_balance_row = pg_cursor.fetchone()
        initial_balance = initial_balance_row[0] if initial_balance_row else 0
        
        # Call the `make_payment` stored procedure in PostgreSQL
        pg_cursor.execute("CALL make_payment(%s, %s, %s)", 
                          (user_bank_account_id, fitness_club_bank_account_id, price))
        
        # Read the new balance to confirm the transaction was successful 
        # (since `make_payment` suppresses runtime errors and logs them internally)
        pg_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (fitness_club_bank_account_id,))
        new_balance_row = pg_cursor.fetchone()
        new_balance = new_balance_row[0] if new_balance_row else 0
        
        # Step 4: Update status in Fitness DB based on transaction outcome
        if new_balance > initial_balance:
            sqlite_cursor.execute("UPDATE purchases SET status = 'completed' WHERE id = ?", (purchase_id,))
            print(f"-> Success! Payment cleared. '{mem_name}' purchased.")
        else:
            sqlite_cursor.execute("UPDATE purchases SET status = 'failed' WHERE id = ?", (purchase_id,))
            print("-> Failed: Payment was rejected by the bank (e.g. insufficient funds).")
            
        sqlite_conn.commit()

    except Exception as e:
        print(f"-> System Error encountered during purchase: {e}")
        # Make sure we mark the transaction as failed in the local DB if an actual crash happens
        if sqlite_conn and purchase_id:
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute("UPDATE purchases SET status = 'failed' WHERE id = ?", (purchase_id,))
            sqlite_conn.commit()
            
    finally:
        # Step 5: Always ensure clean disconnection from both databases
        if sqlite_conn:
            sqlite_conn.close()
        if pg_conn:
            pg_conn.close()

if __name__ == '__main__':
    print("Initializing Fitness Database system...")
    setup_fitness_db()
    
    # We assume Test Accounts are already created in Postgres database via the bank_setup.sql:
    # User 1 has sufficient funds, User 3 has very low funds. Account 2 is our Fitness Club.
    
    # Test 1: Successful purchase (Basic Plan = $30.00)
    print("\n--- TEST 1: Successful Transaction ---")
    buy_membership(user_bank_account_id=1, fitness_club_bank_account_id=2, membership_id=1)
    
    # Test 2: Failed purchase due to bank restrictions (Gold VIP Plan = $120.00)
    print("\n--- TEST 2: Failed Transaction (Insufficient Funds) ---")
    buy_membership(user_bank_account_id=3, fitness_club_bank_account_id=2, membership_id=3)
