import sqlite3
import psycopg2

# Configuration for the external Bank DB (PostgreSQL)
PG_DB = "bank_db"
PG_USER = "postgres"
PG_PASSWORD = "123123"  # <-- Please change this to your actual password before running!
PG_HOST = "localhost"
PG_PORT = "5432"

# Configuration for the independent Fitness Club DB (SQLite)
SQLITE_DB = "fitness_db.sqlite"

def setup_fitness_db():
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # 1. Create the independent services table (memberships & training)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fitness_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # 2. Create the purchases table to track logic internally
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_bank_account_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    # Insert some dummy services if the table is empty
    cursor.execute('SELECT COUNT(*) FROM fitness_services')
    if cursor.fetchone()[0] == 0:
        dummy_services = [
            ('Bronze Membership Plan', 30.00),
            ('Gold VIP Membership Plan', 120.00),
            ('1-on-1 Personal Training Session', 50.00),
            ('Group Yoga Class', 15.00)
        ]
        cursor.executemany('''
            INSERT INTO fitness_services (name, price) VALUES (?, ?)
        ''', dummy_services)
    
    conn.commit()
    conn.close()

def buy_fitness_service(user_bank_account_id, fitness_club_bank_account_id, service_id):
    """
    Acts as an API bridge. It connects to the Fitness system, then calls the external 
    Banking system to secure funds, and then returns to the Fitness system to update statuses.
    """
    sqlite_conn = None
    pg_conn = None
    purchase_id = None
    
    try:
        # ---> STEP 1: Interact with FITNESS SYSTEM
        print(f"\n[1/5] [FITNESS SYSTEM] Checking requested service ID {service_id}...")
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_cursor = sqlite_conn.cursor()
        
        sqlite_cursor.execute("SELECT name, price FROM fitness_services WHERE id = ?", (service_id,))
        service = sqlite_cursor.fetchone()
        
        if not service:
            print("[!] [FITNESS SYSTEM] Error: Service not found.")
            return
        
        serv_name, price = service
        print(f"[2/5] [FITNESS SYSTEM] Found '{serv_name}'. Price: ${price}.")
        print(f"      -> Injecting Purchase Order with status 'PENDING'...")
        
        sqlite_cursor.execute('''
            INSERT INTO purchases (user_bank_account_id, service_id, status)
            VALUES (?, ?, 'pending')
        ''', (user_bank_account_id, service_id))
        purchase_id = sqlite_cursor.lastrowid
        sqlite_conn.commit()
        print(f"      -> OK! Purchase Order #{purchase_id} secured.")
        
        # ---> STEP 2: Establish BRIDGE to BANK SYSTEM
        print(f"[3/5] [API BRIDGE] Connecting to external Banking Network (PostgreSQL)...")
        pg_conn = psycopg2.connect(
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT
        )
        pg_conn.autocommit = True
        pg_cursor = pg_conn.cursor()
        
        # Fetch the club's current balance to verify transaction completion
        pg_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (fitness_club_bank_account_id,))
        initial_balance_row = pg_cursor.fetchone()
        initial_balance = initial_balance_row[0] if initial_balance_row else 0
        
        print(f"[4/5] [BANK SYSTEM] Initiating secure transaction via 'make_payment' procedure...")
        print(f"      -> Requesting transfer of ${price} from Account ID {user_bank_account_id} to Account ID {fitness_club_bank_account_id}.")
        
        # Execute Stored Procedure
        pg_cursor.execute("CALL make_payment(%s, %s, %s)", 
                          (user_bank_account_id, fitness_club_bank_account_id, price))
        
        # Verify if payment actually deposited
        pg_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (fitness_club_bank_account_id,))
        new_balance_row = pg_cursor.fetchone()
        new_balance = new_balance_row[0] if new_balance_row else 0
        
        # ---> STEP 3: Return to FITNESS SYSTEM with the result
        if new_balance > initial_balance:
            print(f"[5/5] [BANK SYSTEM] Transaction CLEARED! Funds transferred securely.")
            print(f"      [FITNESS SYSTEM] Updating Purchase #{purchase_id} status to 'COMPLETED'.")
            sqlite_cursor.execute("UPDATE purchases SET status = 'completed' WHERE id = ?", (purchase_id,))
        else:
            print(f"[5/5] [BANK SYSTEM] Transaction DECLINED! (Possible insufficient funds. Check bank error logs).")
            print(f"      [FITNESS SYSTEM] Updating Purchase #{purchase_id} status to 'FAILED'. User must try again.")
            sqlite_cursor.execute("UPDATE purchases SET status = 'failed' WHERE id = ?", (purchase_id,))
            
        sqlite_conn.commit()

    except Exception as e:
        print(f"[X] CRITICAL ERROR: Database Connection Failed.\nDetails: {e}")
        if sqlite_conn and purchase_id:
            print(f"      [FITNESS SYSTEM] Forcing Purchase #{purchase_id} status to 'FAILED' due to crash.")
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute("UPDATE purchases SET status = 'failed' WHERE id = ?", (purchase_id,))
            sqlite_conn.commit()
            
    finally:
        # Step 4: Always ensure clean disconnection from both databases
        if sqlite_conn:
            sqlite_conn.close()
        if pg_conn:
            pg_conn.close()

if __name__ == '__main__':
    print("======== FITNESS DB & BANK DB API INTEGRATION ========")
    setup_fitness_db()
    
    # We assume Test Accounts are already created in Postgres via 'test_run.sql'
    # Account 1: Alice (Rich), Account 2: Fitness Club, Account 3: Charlie (Poor)
    
    # Test 1: Successful purchase of a membership
    print("\n--- TEST 1: Alice buys a Bronze Membership ---")
    # Alice = 1, Fitness club = 2, service 1 = Bronze Membership ($30.00)
    buy_fitness_service(user_bank_account_id=1, fitness_club_bank_account_id=2, service_id=1)
    
    # Test 2: Successful purchase of Personal Training
    print("\n--- TEST 2: Alice books a 1-on-1 Personal Training Session ---")
    # Alice = 1, Fitness club = 2, service 3 = Personal Training ($50.00)
    buy_fitness_service(user_bank_account_id=1, fitness_club_bank_account_id=2, service_id=3)
    
    # Test 3: Failed purchase due to bank restrictions
    print("\n--- TEST 3: Charlie tries to buy a VIP Membership (Insufficient Funds) ---")
    # Charlie = 3 (has only $50.00), Fitness club = 2, service 2 = VIP ($120.00)
    buy_fitness_service(user_bank_account_id=3, fitness_club_bank_account_id=2, service_id=2)
