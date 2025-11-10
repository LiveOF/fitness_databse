# Short Description of Fitness Club Database Tables

## Main Tables

### 1. `clubs` (Fitness Club Locations)
**Purpose**: Stores information about different fitness club locations.

**What it stores**: Club name, address, contact information, opening hours

**Why it's needed**: Managing multiple fitness club branches in different locations.

---

### 2. `members` (Club Members/Participants)
**Purpose**: Stores information about all fitness club members.

**What it stores**: Personal data, birthdate, gender, address, emergency contacts, registration date

**Why it's needed**: Managing member database, contact information, and profiles.

---

### 3. `trainers` (Trainers/Coaches)
**Purpose**: Stores information about fitness trainers/instructors.

**What it stores**: Personal data, specialization, certifications, hire date, assigned club

**Why it's needed**: Managing trainer staff, qualifications, and club assignments.

---

### 4. `memberships` (Subscriptions)
**Purpose**: Stores membership subscription information.

**What it stores**: Member-club relationship, membership type, validity period, price, status

**Why it's needed**: Managing subscriptions, tracking active/expired memberships, revenue calculation.

---

### 5. `workout_types` (Workout Types)
**Purpose**: Directory of different workout types and classes.

**What it stores**: Workout name, description, duration, difficulty level, max participants

**Why it's needed**: Catalog of all available training programs and classes.

---

### 6. `workout_schedule` (Workout Schedule)
**Purpose**: Stores scheduled workout sessions.

**What it stores**: Workout type, trainer, club, date/time, available spots

**Why it's needed**: Planning and managing class schedules across different clubs.

---

### 7. `attendance` (Attendance Tracking)
**Purpose**: Tracks member attendance at scheduled workouts.

**What it stores**: Schedule reference, member, attendance date/time, status

**Why it's needed**: Attendance control, class popularity analytics, member activity tracking.
