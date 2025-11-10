-- Fitness Club Database Schema
-- This database manages fitness clubs, members, trainers, workouts, and memberships

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS workout_schedule;
DROP TABLE IF EXISTS memberships;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS workout_types;

-- Table: clubs
-- Stores information about fitness club locations
CREATE TABLE clubs (
    club_id INT PRIMARY KEY AUTO_INCREMENT,
    club_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    opening_hours VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: members
-- Stores information about fitness club members/participants
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('M', 'F', 'Other'),
    address VARCHAR(255),
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(20),
    registration_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: trainers
-- Stores information about fitness trainers/coaches
CREATE TABLE trainers (
    trainer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100),
    certification VARCHAR(255),
    hire_date DATE NOT NULL,
    club_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE SET NULL
);

-- Table: memberships
-- Stores membership/subscription information for members
CREATE TABLE memberships (
    membership_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    club_id INT NOT NULL,
    membership_type ENUM('Basic', 'Premium', 'VIP') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status ENUM('Active', 'Expired', 'Suspended') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Table: workout_types
-- Stores different types of workouts/classes offered
CREATE TABLE workout_types (
    workout_type_id INT PRIMARY KEY AUTO_INCREMENT,
    workout_name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_minutes INT NOT NULL,
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') NOT NULL,
    max_participants INT DEFAULT 20,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: workout_schedule
-- Stores scheduled workout sessions/classes
CREATE TABLE workout_schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    workout_type_id INT NOT NULL,
    trainer_id INT NOT NULL,
    club_id INT NOT NULL,
    schedule_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    available_spots INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_type_id) REFERENCES workout_types(workout_type_id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id) ON DELETE CASCADE
);

-- Table: attendance
-- Tracks member attendance at scheduled workouts
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT NOT NULL,
    member_id INT NOT NULL,
    attendance_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Present', 'Absent', 'Cancelled') DEFAULT 'Present',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES workout_schedule(schedule_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

-- Insert sample data for testing

-- Sample clubs
INSERT INTO clubs (club_name, address, phone, email, opening_hours) VALUES
('FitLife Downtown', '123 Main Street, New York, NY 10001', '+1-212-555-0101', 'downtown@fitlife.com', 'Mon-Fri: 6AM-10PM, Sat-Sun: 8AM-8PM'),
('FitLife Uptown', '456 Park Avenue, New York, NY 10022', '+1-212-555-0102', 'uptown@fitlife.com', 'Mon-Fri: 6AM-10PM, Sat-Sun: 8AM-8PM'),
('FitLife Brooklyn', '789 Brooklyn Ave, Brooklyn, NY 11201', '+1-718-555-0103', 'brooklyn@fitlife.com', 'Mon-Sun: 24 Hours');

-- Sample members
INSERT INTO members (first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone, registration_date) VALUES
('John', 'Doe', 'john.doe@email.com', '+1-555-0001', '1990-05-15', 'M', '100 First St, NY', 'Jane Doe', '+1-555-0002', '2024-01-15'),
('Sarah', 'Smith', 'sarah.smith@email.com', '+1-555-0003', '1992-08-22', 'F', '200 Second St, NY', 'Mike Smith', '+1-555-0004', '2024-02-01'),
('Michael', 'Johnson', 'michael.j@email.com', '+1-555-0005', '1988-03-10', 'M', '300 Third St, NY', 'Lisa Johnson', '+1-555-0006', '2024-01-20'),
('Emily', 'Brown', 'emily.brown@email.com', '+1-555-0007', '1995-11-30', 'F', '400 Fourth St, NY', 'Tom Brown', '+1-555-0008', '2024-03-05'),
('David', 'Wilson', 'david.w@email.com', '+1-555-0009', '1991-07-18', 'M', '500 Fifth St, NY', 'Anna Wilson', '+1-555-0010', '2024-02-15');

-- Sample trainers
INSERT INTO trainers (first_name, last_name, email, phone, specialization, certification, hire_date, club_id) VALUES
('Alex', 'Martinez', 'alex.m@fitlife.com', '+1-555-1001', 'Cardio & HIIT', 'NASM-CPT, ACE', '2023-06-01', 1),
('Jessica', 'Lee', 'jessica.l@fitlife.com', '+1-555-1002', 'Yoga & Pilates', 'RYT-500, STOTT Pilates', '2023-07-15', 1),
('Robert', 'Taylor', 'robert.t@fitlife.com', '+1-555-1003', 'Strength Training', 'CSCS, ISSA-CFT', '2023-05-10', 2),
('Maria', 'Garcia', 'maria.g@fitlife.com', '+1-555-1004', 'CrossFit & Functional', 'CF-L2, FMS', '2023-08-01', 3);

-- Sample memberships
INSERT INTO memberships (member_id, club_id, membership_type, start_date, end_date, price, status) VALUES
(1, 1, 'Premium', '2024-01-15', '2025-01-15', 899.99, 'Active'),
(2, 1, 'Basic', '2024-02-01', '2025-02-01', 499.99, 'Active'),
(3, 2, 'VIP', '2024-01-20', '2025-01-20', 1499.99, 'Active'),
(4, 3, 'Premium', '2024-03-05', '2025-03-05', 899.99, 'Active'),
(5, 2, 'Basic', '2024-02-15', '2024-08-15', 299.99, 'Expired');

-- Sample workout types
INSERT INTO workout_types (workout_name, description, duration_minutes, difficulty_level, max_participants) VALUES
('HIIT Cardio', 'High-Intensity Interval Training for maximum calorie burn', 45, 'Intermediate', 20),
('Yoga Flow', 'Vinyasa-style yoga for flexibility and mindfulness', 60, 'Beginner', 15),
('Power Lifting', 'Advanced strength training with heavy weights', 90, 'Advanced', 10),
('Spin Class', 'Indoor cycling for cardiovascular endurance', 45, 'Intermediate', 25),
('CrossFit WOD', 'Workout of the Day - varied functional fitness', 60, 'Advanced', 15),
('Pilates Core', 'Core strengthening and flexibility training', 50, 'Beginner', 12);

-- Sample workout schedule
INSERT INTO workout_schedule (workout_type_id, trainer_id, club_id, schedule_date, start_time, end_time, available_spots) VALUES
(1, 1, 1, '2024-11-15', '07:00:00', '07:45:00', 15),
(2, 2, 1, '2024-11-15', '09:00:00', '10:00:00', 10),
(3, 3, 2, '2024-11-15', '18:00:00', '19:30:00', 8),
(4, 1, 1, '2024-11-16', '06:30:00', '07:15:00', 20),
(5, 4, 3, '2024-11-16', '17:00:00', '18:00:00', 12),
(6, 2, 1, '2024-11-17', '10:00:00', '10:50:00', 10);

-- Sample attendance records
INSERT INTO attendance (schedule_id, member_id, status) VALUES
(1, 1, 'Present'),
(1, 2, 'Present'),
(1, 3, 'Present'),
(2, 1, 'Present'),
(2, 4, 'Present'),
(3, 3, 'Present'),
(3, 5, 'Absent'),
(4, 2, 'Present'),
(5, 4, 'Present');
