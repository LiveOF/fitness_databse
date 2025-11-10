# Fitness Club Database Project

## 📌 Project Description

This is a complete database management system for fitness clubs, created based on the college_database model. The system includes all necessary components for managing:

- **Members** (club participants)
- **Trainers** (instructors)
- **Memberships** (subscriptions)
- **Clubs** (locations)
- **Workouts** (classes and sessions)
- **Attendance** (presence tracking)

## 📁 Project Structure

```
/
├── schema.sql                  # SQL database schema with test data
├── SHORT.md                    # Brief table descriptions
├── DATABASE_DIAGRAM.md         # Database schema and diagram
├── SETUP.md                    # Detailed installation guide
├── API_TESTING.md              # API testing examples
├── README.md                   # Main project documentation
├── package.json                # Node.js dependencies
├── .env.example                # Configuration example
├── .gitignore                  # Ignored files
├── index.html                  # HTML documentation
├── test-client.html            # Interactive test client
│
└── api/                        # API server
    ├── server.js               # Main server file
    ├── database.js             # Database connection
    └── routes/                 # API routes
        ├── members.js          # Member endpoints
        ├── trainers.js         # Trainer endpoints
        ├── clubs.js            # Club endpoints
        ├── memberships.js      # Membership endpoints
        ├── workouts.js         # Workout endpoints
        └── attendance.js       # Attendance endpoints
```

## 🗄️ Database Tables

### 1. **clubs**
Stores information about fitness club locations:
- Club name
- Address
- Contact information
- Operating hours

### 2. **members**
Information about club members:
- Personal data (first name, last name, email)
- Date of birth, gender
- Emergency contacts
- Registration date

### 3. **trainers**
Trainer data:
- Personal information
- Specialization (cardio, yoga, strength training, etc.)
- Certifications
- Club assignment

### 4. **memberships**
Member subscriptions:
- Membership type (Basic, Premium, VIP)
- Validity period
- Price
- Status (active/expired)

### 5. **workout_types**
Workout directory:
- Name (HIIT, Yoga, CrossFit, etc.)
- Description
- Duration
- Difficulty level
- Maximum participants

### 6. **workout_schedule**
Class schedule:
- Workout type
- Trainer
- Club
- Date and time
- Available spots

### 7. **attendance**
Attendance tracking:
- Schedule reference
- Member
- Status (present/absent)

## 🚀 Quick Start

### Requirements
- MySQL 5.7 or higher
- Node.js 14 or higher
- npm

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Create database:**
```bash
mysql -u root -p
CREATE DATABASE fitness_club_db;
exit
```

3. **Import schema:**
```bash
mysql -u root -p fitness_club_db < schema.sql
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and specify your MySQL connection data
```

5. **Start server:**
```bash
npm start
```

API will be available at: `http://localhost:3000`

## 🔌 API Endpoints

### Members
- `GET /api/members` - All members
- `GET /api/members/:id` - Specific member
- `GET /api/members/:id/memberships` - Member's memberships
- `GET /api/members/:id/attendance` - Attendance history
- `POST /api/members` - Create member
- `PUT /api/members/:id` - Update member
- `DELETE /api/members/:id` - Delete member

### Trainers
- `GET /api/trainers` - All trainers
- `GET /api/trainers/:id` - Specific trainer
- `GET /api/trainers/:id/schedule` - Trainer's schedule
- `POST /api/trainers` - Create trainer

### Clubs
- `GET /api/clubs` - All clubs
- `GET /api/clubs/:id/trainers` - Club's trainers
- `GET /api/clubs/:id/members` - Club's members
- `POST /api/clubs` - Create club

### Memberships
- `GET /api/memberships` - All memberships
- `GET /api/memberships/active` - Active memberships
- `POST /api/memberships` - Create membership

### Workouts
- `GET /api/workouts/types` - Workout types
- `GET /api/workouts/schedule` - Schedule
- `GET /api/workouts/schedule/upcoming` - Upcoming workouts
- `POST /api/workouts/schedule` - Create session

### Attendance
- `GET /api/attendance` - All records
- `POST /api/attendance` - Mark attendance
- `DELETE /api/attendance/:id` - Cancel attendance

## 🧪 Testing

### Through Browser
Open `test-client.html` in your browser for interactive API testing.

### Through cURL
```bash
# Get all members
curl http://localhost:3000/api/members

# Get upcoming workouts
curl http://localhost:3000/api/workouts/schedule/upcoming
```

### Through JavaScript
```javascript
fetch('http://localhost:3000/api/members')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📊 Test Data

The database contains ready-to-use test data:
- ✅ 3 fitness clubs
- ✅ 5 members
- ✅ 4 trainers
- ✅ 5 memberships
- ✅ 6 workout types
- ✅ 6 scheduled sessions
- ✅ 9 attendance records

## 📚 Documentation

Detailed documentation is available in the following files:

1. **SETUP.md** - Detailed installation and setup instructions
2. **SHORT.md** - Description of each table
3. **DATABASE_DIAGRAM.md** - Database schema and table relationships
4. **API_TESTING.md** - Examples for testing all API endpoints
5. **README.md** - General project information
6. **index.html** - Visual documentation (open in browser)
7. **test-client.html** - Interactive client for API testing

## 💻 Technologies

- **Database:** MySQL
- **Backend:** Node.js + Express.js
- **Database Driver:** mysql2
- **Additional:** CORS, dotenv

## 🎯 Features

✅ Complete fitness club management system
✅ Support for multiple locations
✅ Flexible membership system (Basic, Premium, VIP)
✅ Workout schedule with spot control
✅ Attendance tracking
✅ RESTful API for all operations
✅ Ready-to-use test data
✅ Detailed documentation
✅ HTML interface for testing

## 🔐 Security

⚠️ **Important:**
- Do not commit the `.env` file to repository
- Use strong passwords for the database
- In production, add authentication and authorization
- Validate all incoming data

## 📝 Notes

This project was created as a complete fitness club management system, similar to the college_database system. It includes all necessary components for working with the database through a convenient API.

All files are ready to use. To run the system, follow the instructions in the "Quick Start" section above.

## 🤝 Usage

The project can be used as:
- A ready-made system for managing a fitness club
- A template for creating your own system
- Educational material for learning Node.js + MySQL

---

**Created:** 2024  
**License:** MIT
