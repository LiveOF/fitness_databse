# Fitness Club Database System

A comprehensive database system for managing fitness clubs, including members, trainers, memberships, workout schedules, and attendance tracking. This project includes a complete MySQL database schema and a RESTful API built with Node.js and Express.

## 🏋️ Features

- **Member Management**: Track member information, contact details, and emergency contacts
- **Trainer Management**: Manage trainer profiles, specializations, and certifications
- **Club Management**: Handle multiple fitness club locations
- **Membership System**: Support for different membership tiers (Basic, Premium, VIP)
- **Workout Scheduling**: Create and manage workout schedules across different clubs
- **Attendance Tracking**: Monitor member participation in scheduled workouts
- **RESTful API**: Complete API for all database operations

## 📋 Database Structure

The database includes the following tables:

1. **clubs** - Fitness club locations and information
2. **members** - Club members/participants
3. **trainers** - Fitness trainers and their qualifications
4. **memberships** - Member subscriptions and status
5. **workout_types** - Catalog of available workout classes
6. **workout_schedule** - Scheduled workout sessions
7. **attendance** - Member attendance records

For detailed information about each table, see [SHORT.md](SHORT.md).

## 🚀 Quick Start

### Prerequisites

- MySQL 5.7+
- Node.js 14+
- npm

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd 222
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up the database**
```bash
mysql -u root -p
CREATE DATABASE fitness_club_db;
exit
mysql -u root -p fitness_club_db < schema.sql
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Start the API server**
```bash
npm start
```

The API will be available at `http://localhost:3000`

For detailed setup instructions, see [SETUP.md](SETUP.md).

## 🔌 API Endpoints

### Members
- `GET /api/members` - Get all members
- `GET /api/members/:id` - Get specific member
- `POST /api/members` - Create new member
- `PUT /api/members/:id` - Update member
- `DELETE /api/members/:id` - Delete member

### Trainers
- `GET /api/trainers` - Get all trainers
- `GET /api/trainers/:id` - Get specific trainer
- `GET /api/trainers/:id/schedule` - Get trainer's schedule

### Clubs
- `GET /api/clubs` - Get all clubs
- `GET /api/clubs/:id/trainers` - Get club's trainers
- `GET /api/clubs/:id/members` - Get club's members

### Memberships
- `GET /api/memberships` - Get all memberships
- `GET /api/memberships/active` - Get active memberships
- `POST /api/memberships` - Create new membership

### Workouts
- `GET /api/workouts/types` - Get workout types
- `GET /api/workouts/schedule` - Get workout schedule
- `GET /api/workouts/schedule/upcoming` - Get upcoming workouts
- `POST /api/workouts/schedule` - Create workout session

### Attendance
- `GET /api/attendance` - Get all attendance records
- `POST /api/attendance` - Record attendance (check-in)
- `DELETE /api/attendance/:id` - Cancel check-in

## 📊 Database Schema

```
clubs (1) ────┐
              ├──> (N) trainers
              ├──> (N) memberships <──── (1) members
              └──> (N) workout_schedule
                          │
                          ├──> (1) workout_types
                          ├──> (1) trainers
                          └──> (N) attendance <──── (1) members
```

## 📝 Sample Data

The database comes pre-loaded with sample data:
- 3 fitness clubs in different locations
- 5 members with complete profiles
- 4 trainers with various specializations
- 5 memberships (active and expired)
- 6 workout types (HIIT, Yoga, CrossFit, etc.)
- 6 scheduled workouts
- 9 attendance records

## 🧪 Testing the API

### Using cURL

```bash
# Get all members
curl http://localhost:3000/api/members

# Get upcoming workouts
curl http://localhost:3000/api/workouts/schedule/upcoming

# Create a new member
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "registration_date": "2024-11-10"
  }'
```

### Using Browser

Navigate to `http://localhost:3000` to see the API documentation and available endpoints.

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup and installation guide
- **[SHORT.md](SHORT.md)** - Database table descriptions
- **[schema.sql](schema.sql)** - Complete database schema with sample data

## 🛠️ Technology Stack

- **Database**: MySQL
- **Backend**: Node.js, Express.js
- **Database Driver**: mysql2
- **Middleware**: CORS, dotenv

## 📖 Use Cases

This database system can be used for:

1. **Fitness Club Management**: Manage multiple club locations
2. **Member Registration**: Track member information and memberships
3. **Class Scheduling**: Schedule and manage workout classes
4. **Attendance Tracking**: Monitor member participation
5. **Trainer Assignment**: Assign trainers to specific classes
6. **Membership Billing**: Track membership types and expiration dates

## 🔐 Security Notes

- Never commit the `.env` file to version control
- Use strong passwords for database access
- In production, implement proper authentication and authorization
- Validate all user inputs
- Use HTTPS in production environments

## 🤝 Contributing

This is a template/example project for fitness club database management. Feel free to fork and modify it for your specific needs.

## 📄 License

MIT

## 🌐 Language Support

Documentation is available in English.

---

Built with ❤️ for fitness club management