-- PART 1: PostgreSQL Banking System Setup
-- bank_setup.sql

-- 1. Accounts Table
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    balance NUMERIC(15, 2) NOT NULL DEFAULT 0.00
);

-- 2. Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    from_account INT REFERENCES accounts(id),
    to_account INT REFERENCES accounts(id),
    amount NUMERIC(15, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Error Logs Table
CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    error_message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Loans and Loan Schedules Tables
CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(id),
    total_amount NUMERIC(15, 2) NOT NULL,
    interest_rate NUMERIC(5, 2) NOT NULL,
    duration_months INT NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS loan_schedules (
    id SERIAL PRIMARY KEY,
    loan_id INT REFERENCES loans(id),
    payment_number INT NOT NULL,
    payment_date DATE NOT NULL,
    amount_due NUMERIC(15, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending'
);

-- 5. Stored Procedure: generate_loan_schedule
CREATE OR REPLACE PROCEDURE generate_loan_schedule(p_loan_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_duration INT;
    v_total_amount NUMERIC;
    v_interest_rate NUMERIC;
    v_monthly_payment NUMERIC;
    v_start_date DATE;
BEGIN
    -- Fetch loan details
    SELECT duration_months, total_amount, interest_rate, start_date
    INTO v_duration, v_total_amount, v_interest_rate, v_start_date
    FROM loans WHERE id = p_loan_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Loan ID % not found', p_loan_id;
    END IF;

    -- Calculate simple monthly payment (amount + total flat interest) / months
    v_monthly_payment := (v_total_amount * (1 + (v_interest_rate / 100.0))) / v_duration;

    -- Generate actual schedule
    FOR i IN 1..v_duration LOOP
        INSERT INTO loan_schedules (loan_id, payment_number, payment_date, amount_due)
        VALUES (p_loan_id, i, v_start_date + (i || ' month')::interval, v_monthly_payment);
    END LOOP;
    
    COMMIT;
END;
$$;

-- 6. Stored Procedure: make_payment
CREATE OR REPLACE PROCEDURE make_payment(p_sender_id INT, p_receiver_id INT, p_pay_amount NUMERIC)
LANGUAGE plpgsql
AS $$
DECLARE
    v_sender_balance NUMERIC;
BEGIN
    -- Validation 1: Amount must be positive
    IF p_pay_amount <= 0 THEN
        ROLLBACK;
        INSERT INTO error_logs (error_message) VALUES ('Payment failed: Amount must be greater than 0');
        COMMIT;
        RETURN;
    END IF;

    -- Validation 2: Sender and receiver must not be the same
    IF p_sender_id = p_receiver_id THEN
        ROLLBACK;
        INSERT INTO error_logs (error_message) VALUES ('Payment failed: Sender and receiver cannot be the same');
        COMMIT;
        RETURN;
    END IF;

    -- Lock the sender's row for transaction safety to prevent race conditions
    SELECT balance INTO v_sender_balance FROM accounts WHERE id = p_sender_id FOR UPDATE;

    IF v_sender_balance IS NULL THEN
        ROLLBACK;
        INSERT INTO error_logs (error_message) VALUES ('Payment failed: Sender account does not exist');
        COMMIT;
        RETURN;
    END IF;

    -- Validation 3: Check sufficient balance
    IF v_sender_balance < p_pay_amount THEN
        ROLLBACK;
        -- Incorporate details directly to the log
        INSERT INTO error_logs (error_message) VALUES ('Payment failed: Insufficient balance for Account ' || p_sender_id);
        COMMIT;
        RETURN;
    END IF;

    -- Ensure receiver exists before proceeding
    IF NOT EXISTS (SELECT 1 FROM accounts WHERE id = p_receiver_id FOR UPDATE) THEN
        ROLLBACK;
        INSERT INTO error_logs (error_message) VALUES ('Payment failed: Receiver account does not exist');
        COMMIT;
        RETURN;
    END IF;

    -- Successful validations, deduct & add
    UPDATE accounts SET balance = balance - p_pay_amount WHERE id = p_sender_id;
    UPDATE accounts SET balance = balance + p_pay_amount WHERE id = p_receiver_id;

    -- Record transaction
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (p_sender_id, p_receiver_id, p_pay_amount);

    -- Commit the main transaction
    COMMIT;
END;
$$;
