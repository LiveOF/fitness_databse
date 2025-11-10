# API Testing Examples

This document provides examples for testing all API endpoints.

## Base URL

```
http://localhost:3000
```

## Testing with cURL

### 1. Health Check

```bash
curl http://localhost:3000/health
```

**Expected Response:**
```json
{
  "status": "OK",
  "timestamp": "2024-11-10T17:00:00.000Z"
}
```

---

### 2. Members Endpoints

#### Get All Members
```bash
curl http://localhost:3000/api/members
```

#### Get Specific Member
```bash
curl http://localhost:3000/api/members/1
```

#### Create New Member
```bash
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alex",
    "last_name": "Johnson",
    "email": "alex.johnson@email.com",
    "phone": "+1-555-0100",
    "date_of_birth": "1993-06-15",
    "gender": "M",
    "address": "789 Maple Ave, NY",
    "emergency_contact": "Sarah Johnson",
    "emergency_phone": "+1-555-0101",
    "registration_date": "2024-11-10"
  }'
```

#### Update Member
```bash
curl -X PUT http://localhost:3000/api/members/1 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "+1-555-0001",
    "date_of_birth": "1990-05-15",
    "gender": "M",
    "address": "100 First St, NY",
    "emergency_contact": "Jane Doe",
    "emergency_phone": "+1-555-0002"
  }'
```

#### Get Member's Memberships
```bash
curl http://localhost:3000/api/members/1/memberships
```

#### Get Member's Attendance
```bash
curl http://localhost:3000/api/members/1/attendance
```

---

### 3. Trainers Endpoints

#### Get All Trainers
```bash
curl http://localhost:3000/api/trainers
```

#### Get Specific Trainer
```bash
curl http://localhost:3000/api/trainers/1
```

#### Get Trainer's Schedule
```bash
curl http://localhost:3000/api/trainers/1/schedule
```

#### Create New Trainer
```bash
curl -X POST http://localhost:3000/api/trainers \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Lisa",
    "last_name": "Anderson",
    "email": "lisa.a@fitlife.com",
    "phone": "+1-555-2001",
    "specialization": "Nutrition & Wellness",
    "certification": "ACE-CPT, Precision Nutrition",
    "hire_date": "2024-01-15",
    "club_id": 1
  }'
```

---

### 4. Clubs Endpoints

#### Get All Clubs
```bash
curl http://localhost:3000/api/clubs
```

#### Get Specific Club
```bash
curl http://localhost:3000/api/clubs/1
```

#### Get Club's Trainers
```bash
curl http://localhost:3000/api/clubs/1/trainers
```

#### Get Club's Members
```bash
curl http://localhost:3000/api/clubs/1/members
```

#### Create New Club
```bash
curl -X POST http://localhost:3000/api/clubs \
  -H "Content-Type: application/json" \
  -d '{
    "club_name": "FitLife Queens",
    "address": "999 Queens Blvd, Queens, NY 11375",
    "phone": "+1-718-555-0200",
    "email": "queens@fitlife.com",
    "opening_hours": "Mon-Fri: 5AM-11PM, Sat-Sun: 7AM-9PM"
  }'
```

---

### 5. Memberships Endpoints

#### Get All Memberships
```bash
curl http://localhost:3000/api/memberships
```

#### Get Active Memberships Only
```bash
curl http://localhost:3000/api/memberships/active
```

#### Get Specific Membership
```bash
curl http://localhost:3000/api/memberships/1
```

#### Create New Membership
```bash
curl -X POST http://localhost:3000/api/memberships \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "club_id": 1,
    "membership_type": "Premium",
    "start_date": "2024-11-10",
    "end_date": "2025-11-10",
    "price": 899.99,
    "status": "Active"
  }'
```

#### Update Membership
```bash
curl -X PUT http://localhost:3000/api/memberships/1 \
  -H "Content-Type: application/json" \
  -d '{
    "membership_type": "VIP",
    "start_date": "2024-01-15",
    "end_date": "2025-01-15",
    "price": 1499.99,
    "status": "Active"
  }'
```

---

### 6. Workouts Endpoints

#### Get All Workout Types
```bash
curl http://localhost:3000/api/workouts/types
```

#### Get Full Workout Schedule
```bash
curl http://localhost:3000/api/workouts/schedule
```

#### Get Upcoming Workouts
```bash
curl http://localhost:3000/api/workouts/schedule/upcoming
```

#### Get Specific Schedule
```bash
curl http://localhost:3000/api/workouts/schedule/1
```

#### Create New Workout Type
```bash
curl -X POST http://localhost:3000/api/workouts/types \
  -H "Content-Type: application/json" \
  -d '{
    "workout_name": "Zumba Dance",
    "description": "High-energy dance fitness workout",
    "duration_minutes": 55,
    "difficulty_level": "Beginner",
    "max_participants": 30
  }'
```

#### Create New Workout Schedule
```bash
curl -X POST http://localhost:3000/api/workouts/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "workout_type_id": 1,
    "trainer_id": 1,
    "club_id": 1,
    "schedule_date": "2024-11-15",
    "start_time": "18:00:00",
    "end_time": "18:45:00",
    "available_spots": 20
  }'
```

---

### 7. Attendance Endpoints

#### Get All Attendance Records
```bash
curl http://localhost:3000/api/attendance
```

#### Get Attendance for Specific Schedule
```bash
curl http://localhost:3000/api/attendance/schedule/1
```

#### Create Attendance Record (Check-in)
```bash
curl -X POST http://localhost:3000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "schedule_id": 1,
    "member_id": 1,
    "status": "Present"
  }'
```

#### Update Attendance Status
```bash
curl -X PUT http://localhost:3000/api/attendance/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Absent"
  }'
```

#### Delete Attendance (Cancel Check-in)
```bash
curl -X DELETE http://localhost:3000/api/attendance/1
```

---

## Testing with JavaScript (Fetch API)

### Get All Members
```javascript
fetch('http://localhost:3000/api/members')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Create New Member
```javascript
fetch('http://localhost:3000/api/members', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'Test',
    last_name: 'User',
    email: 'test@example.com',
    phone: '+1-555-9999',
    date_of_birth: '1995-03-20',
    gender: 'F',
    address: '123 Test Ave',
    emergency_contact: 'Emergency User',
    emergency_phone: '+1-555-9998',
    registration_date: '2024-11-10'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Get Upcoming Workouts
```javascript
fetch('http://localhost:3000/api/workouts/schedule/upcoming')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

## Testing with Python (requests library)

```python
import requests

# Base URL
base_url = 'http://localhost:3000'

# Get all members
response = requests.get(f'{base_url}/api/members')
print(response.json())

# Create new member
new_member = {
    'first_name': 'Python',
    'last_name': 'Tester',
    'email': 'python@test.com',
    'phone': '+1-555-7777',
    'date_of_birth': '1991-12-25',
    'gender': 'M',
    'address': '456 Code St',
    'emergency_contact': 'Emergency',
    'emergency_phone': '+1-555-7776',
    'registration_date': '2024-11-10'
}
response = requests.post(f'{base_url}/api/members', json=new_member)
print(response.json())

# Get upcoming workouts
response = requests.get(f'{base_url}/api/workouts/schedule/upcoming')
print(response.json())
```

---

## Common Response Formats

### Success Response
```json
{
  "success": true,
  "data": { /* ... data object ... */ }
}
```

### Success with List
```json
{
  "success": true,
  "count": 5,
  "data": [ /* ... array of objects ... */ ]
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here"
}
```

### Created Response
```json
{
  "success": true,
  "message": "Resource created successfully",
  "data": { "id": 123 }
}
```

---

## Expected HTTP Status Codes

- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST (resource created)
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
