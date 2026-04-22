-- test_run.sql
-- Этот скрипт проверяет все функции базы данных банка

-- 1. Создаем тестовые аккаунты
INSERT INTO accounts (id, name, balance) 
VALUES 
    (1, 'Alice (Employer)', 10000.00),
    (2, 'Bob (Employee)', 500.00),
    (3, 'Charlie (Student)', 50.00)
ON CONFLICT (id) DO NOTHING;

-- 2. Успешная транзакция: Алиса платит Бобу 2000
CALL make_payment(1, 2, 2000.00);

-- 3. Провальная транзакция: Боб пытается перевести больше, чем у него есть
CALL make_payment(2, 3, 50000.00);

-- 4. Провальная транзакция: Попытка перевести отрицательную сумму
CALL make_payment(1, 3, -100.00);

-- 5. Тест кредита: Чарли берет кредит на 1200 под 5% на 12 месяцев
INSERT INTO loans (id, account_id, total_amount, interest_rate, duration_months, start_date) 
VALUES (1, 3, 1200.00, 5.00, 12, CURRENT_DATE)
ON CONFLICT (id) DO NOTHING;

-- Очистка старых графиков, если они были, чтобы не дублировать
DELETE FROM loan_schedules WHERE loan_id = 1;

-- 6. Генерируем график платежей по кредиту
CALL generate_loan_schedule(1);

-- ==========================================
-- ВЫВОД РЕЗУЛЬТАТОВ (Проверка работоспособности)
-- ==========================================

\echo '--- ACCOUNTS (Счета) ---'
SELECT * FROM accounts;

\echo '--- TRANSACTIONS (Успешные переводы) ---'
SELECT * FROM transactions;

\echo '--- ERROR LOGS (Ошибки при переводах) ---'
SELECT * FROM error_logs;

\echo '--- LOAN SCHEDULE (График платежей для Чарли - первые 3 месяца) ---'
SELECT * FROM loan_schedules WHERE loan_id = 1 LIMIT 3;
