-- test_run.sql
-- This script tests all database functions of the Bank System

-- 1. Create test accounts (using "owner_name" per the updated requirement)
INSERT INTO accounts (id, owner_name, balance) 
VALUES 
    (1, 'User 1: Alice (Funded)', 10000.00),
    (2, 'Account 2: Fitness Club', 500.00),
    (3, 'User 3: Charlie (Low funds)', 50.00)
ON CONFLICT (id) DO NOTHING;

-- 2. Successful transaction: Alice pays the Fitness Club 2000
CALL make_payment(1, 2, 2000.00);

-- 3. Failed transaction: Charlie tries to transfer more than his balance
CALL make_payment(3, 2, 50000.00);

-- 4. Failed transaction: Attempt to transfer a negative amount
CALL make_payment(1, 2, -100.00);

-- 5. Loan Test: Charlie takes a loan of 1200 at 5% for 12 months
INSERT INTO loans (id, account_id, total_amount, interest_rate, duration_months, start_date) 
VALUES (1, 3, 1200.00, 5.00, 12, CURRENT_DATE)
ON CONFLICT (id) DO NOTHING;

-- Clear old schedules if they exist to avoid duplication
DELETE FROM loan_schedules WHERE loan_id = 1;

-- 6. Generate the payment schedule for the loan
CALL generate_loan_schedule(1);

-- ==========================================
-- OUTPUT RESULTS (Verification)
-- ==========================================

\echo '--- ACCOUNTS (All current balances) ---'
SELECT * FROM accounts;

\echo '--- TRANSACTIONS (Successful transfers log) ---'
SELECT * FROM transactions;

\echo '--- ERROR LOGS (Failed transfers track) ---'
SELECT * FROM error_logs;

\echo '--- LOAN SCHEDULE (Charlie''s first 3 months) ---'
SELECT * FROM loan_schedules WHERE loan_id = 1 LIMIT 3;
