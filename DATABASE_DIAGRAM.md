# Database Schema Diagram - Fitness Club System

## Entity Relationship Diagram (Text Format)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLUBS                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ PK  club_id           INT                                                   │
│     club_name         VARCHAR(100)                                          │
│     address           VARCHAR(255)                                          │
│     phone             VARCHAR(20)                                           │
│     email             VARCHAR(100)                                          │
│     opening_hours     VARCHAR(100)                                          │
│     created_at        TIMESTAMP                                             │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         │ 1:N
         ├───────────────────────────────────────────────────────────────┐
         │                                                               │
         │                                                               ▼
         │                                                    ┌──────────────────────────┐
         │                                                    │      TRAINERS            │
         │                                                    ├──────────────────────────┤
         │                                                    │ PK  trainer_id    INT    │
         │                                                    │     first_name    VARCHAR│
         │                                                    │     last_name     VARCHAR│
         │                                                    │     email         VARCHAR│
         │                                                    │     phone         VARCHAR│
         │                                                    │     specialization VARCHAR│
         │                                                    │     certification VARCHAR│
         │                                                    │     hire_date     DATE   │
         │                                                    │ FK  club_id       INT    │
         │                                                    │     created_at    TIMESTAMP│
         │                                                    └──────────────────────────┘
         │                                                               │
         │ 1:N                                                          │ 1:N
         │                                                               │
         ▼                                                               │
┌──────────────────────────────────────────┐                            │
│        MEMBERSHIPS                       │                            │
├──────────────────────────────────────────┤                            │
│ PK  membership_id       INT              │                            │
│ FK  member_id           INT              │◄───────────────┐           │
│ FK  club_id             INT              │                │           │
│     membership_type     ENUM             │                │           │
│     start_date          DATE             │                │           │
│     end_date            DATE             │                │           │
│     price               DECIMAL          │                │           │
│     status              ENUM             │                │           │
│     created_at          TIMESTAMP        │                │           │
└──────────────────────────────────────────┘                │           │
                                                            │ N:1       │
                                                            │           │
                                             ┌──────────────────────────────────┐
                                             │         MEMBERS                  │
                                             ├──────────────────────────────────┤
                                             │ PK  member_id        INT         │
                                             │     first_name       VARCHAR     │
                                             │     last_name        VARCHAR     │
                                             │     email            VARCHAR     │
                                             │     phone            VARCHAR     │
                                             │     date_of_birth    DATE        │
                                             │     gender           ENUM        │
                                             │     address          VARCHAR     │
                                             │     emergency_contact VARCHAR     │
                                             │     emergency_phone  VARCHAR     │
                                             │     registration_date DATE        │
                                             │     created_at       TIMESTAMP   │
                                             └──────────────────────────────────┘
                                                            │
                                                            │ 1:N
                                                            │
         ┌──────────────────────────────────────────────────┘
         │
         │
         ▼
┌──────────────────────────────────────────┐
│         ATTENDANCE                       │
├──────────────────────────────────────────┤
│ PK  attendance_id       INT              │
│ FK  schedule_id         INT              │────────┐
│ FK  member_id           INT              │        │
│     attendance_date     TIMESTAMP        │        │
│     status              ENUM             │        │ N:1
│     created_at          TIMESTAMP        │        │
└──────────────────────────────────────────┘        │
                                                    │
                                                    ▼
                         ┌─────────────────────────────────────────────────┐
                         │         WORKOUT_SCHEDULE                        │
                         ├─────────────────────────────────────────────────┤
                         │ PK  schedule_id        INT                      │
                         │ FK  workout_type_id    INT                      │
                         │ FK  trainer_id         INT   ◄──────────────────┘ (from TRAINERS)
                         │ FK  club_id            INT   ◄──────────────────┐ (from CLUBS)
                         │     schedule_date      DATE                     │
                         │     start_time         TIME                     │
                         │     end_time           TIME                     │
                         │     available_spots    INT                      │
                         │     created_at         TIMESTAMP                │
                         └─────────────────────────────────────────────────┘
                                    │ N:1
                                    │
                                    ▼
                         ┌─────────────────────────────────────────┐
                         │      WORKOUT_TYPES                      │
                         ├─────────────────────────────────────────┤
                         │ PK  workout_type_id    INT              │
                         │     workout_name       VARCHAR          │
                         │     description        TEXT             │
                         │     duration_minutes   INT              │
                         │     difficulty_level   ENUM             │
                         │     max_participants   INT              │
                         │     created_at         TIMESTAMP        │
                         └─────────────────────────────────────────┘
```

## Relationships Summary

### One-to-Many (1:N) Relationships

1. **CLUBS → TRAINERS**
   - One club can have many trainers
   - Each trainer belongs to one club

2. **CLUBS → MEMBERSHIPS**
   - One club can have many memberships
   - Each membership is for one club

3. **CLUBS → WORKOUT_SCHEDULE**
   - One club can have many scheduled workouts
   - Each workout is at one club

4. **MEMBERS → MEMBERSHIPS**
   - One member can have many memberships (past and present)
   - Each membership belongs to one member

5. **MEMBERS → ATTENDANCE**
   - One member can have many attendance records
   - Each attendance record is for one member

6. **TRAINERS → WORKOUT_SCHEDULE**
   - One trainer can lead many scheduled workouts
   - Each workout has one trainer

7. **WORKOUT_TYPES → WORKOUT_SCHEDULE**
   - One workout type can be scheduled many times
   - Each schedule is for one workout type

8. **WORKOUT_SCHEDULE → ATTENDANCE**
   - One scheduled workout can have many attendance records
   - Each attendance is for one scheduled workout

## Key Constraints

### Primary Keys (PK)
- Each table has a unique identifier (id field)
- Auto-incrementing integer values

### Foreign Keys (FK)
- **trainers.club_id** → clubs.club_id (ON DELETE SET NULL)
- **memberships.member_id** → members.member_id (ON DELETE CASCADE)
- **memberships.club_id** → clubs.club_id (ON DELETE CASCADE)
- **workout_schedule.workout_type_id** → workout_types.workout_type_id (ON DELETE CASCADE)
- **workout_schedule.trainer_id** → trainers.trainer_id (ON DELETE CASCADE)
- **workout_schedule.club_id** → clubs.club_id (ON DELETE CASCADE)
- **attendance.schedule_id** → workout_schedule.schedule_id (ON DELETE CASCADE)
- **attendance.member_id** → members.member_id (ON DELETE CASCADE)

### Unique Constraints
- **members.email** - Each member must have a unique email
- **trainers.email** - Each trainer must have a unique email

### ENUM Fields
- **members.gender**: 'M', 'F', 'Other'
- **memberships.membership_type**: 'Basic', 'Premium', 'VIP'
- **memberships.status**: 'Active', 'Expired', 'Suspended'
- **workout_types.difficulty_level**: 'Beginner', 'Intermediate', 'Advanced'
- **attendance.status**: 'Present', 'Absent', 'Cancelled'

## Business Logic

### Cascade Deletes
When a **member** is deleted:
- All their memberships are deleted
- All their attendance records are deleted

When a **club** is deleted:
- All memberships at that club are deleted
- All scheduled workouts at that club are deleted
- Trainers at that club have their club_id set to NULL

When a **workout schedule** is deleted:
- All attendance records for that workout are deleted

### Set NULL
When a **club** is deleted:
- Trainers assigned to that club have their club_id set to NULL (they still exist but are unassigned)

## Data Flow Examples

### Member Registration Flow
```
1. Create record in MEMBERS
2. Create record in MEMBERSHIPS (linking member to club)
```

### Booking a Workout Flow
```
1. Check WORKOUT_SCHEDULE for available spots
2. Create record in ATTENDANCE (linking member to scheduled workout)
3. Decrement available_spots in WORKOUT_SCHEDULE
```

### Scheduling a Class Flow
```
1. Select WORKOUT_TYPE (existing or create new)
2. Select TRAINER
3. Select CLUB
4. Create record in WORKOUT_SCHEDULE
```

## Indexes (Recommended for Performance)

```sql
-- Foreign key indexes
CREATE INDEX idx_trainers_club ON trainers(club_id);
CREATE INDEX idx_memberships_member ON memberships(member_id);
CREATE INDEX idx_memberships_club ON memberships(club_id);
CREATE INDEX idx_schedule_trainer ON workout_schedule(trainer_id);
CREATE INDEX idx_schedule_club ON workout_schedule(club_id);
CREATE INDEX idx_schedule_type ON workout_schedule(workout_type_id);
CREATE INDEX idx_attendance_schedule ON attendance(schedule_id);
CREATE INDEX idx_attendance_member ON attendance(member_id);

-- Search/filter indexes
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_trainers_email ON trainers(email);
CREATE INDEX idx_schedule_date ON workout_schedule(schedule_date);
CREATE INDEX idx_memberships_status ON memberships(status);
```
