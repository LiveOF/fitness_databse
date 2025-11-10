# Setup Guide - Fitness Club Database

This guide will help you set up and run the Fitness Club Database system with the test API.

## Prerequisites

Before you begin, ensure you have the following installed:

- **MySQL Server** (version 5.7 or higher)
- **Node.js** (version 14 or higher)
- **npm** (comes with Node.js)

## Installation Steps

### 1. Clone or Download the Repository

```bash
cd /path/to/project
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required Node.js packages:
- express (web framework)
- mysql2 (MySQL database driver)
- cors (Cross-Origin Resource Sharing)
- dotenv (environment variables)

### 3. Set Up MySQL Database

#### Option A: Using MySQL Command Line

1. Log in to MySQL:
```bash
mysql -u root -p
```

2. Create the database:
```sql
CREATE DATABASE fitness_club_db;
```

3. Import the schema:
```bash
mysql -u root -p fitness_club_db < schema.sql
```

#### Option B: Using MySQL Workbench or phpMyAdmin

1. Create a new database named `fitness_club_db`
2. Import the `schema.sql` file through the GUI

### 4. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your database credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=fitness_club_db
DB_PORT=3306

API_PORT=3000
```

**Important**: Replace `your_mysql_password` with your actual MySQL root password.

### 5. Verify Database Connection

Start the API server to test the database connection:
```bash
npm start
```

If successful, you should see:
```
✓ Database connected successfully

╔═══════════════════════════════════════╗
║   Fitness Club API Server Started    ║
╠═══════════════════════════════════════╣
║   Port: 3000                          ║
║   Environment: development            ║
╚═══════════════════════════════════════╝

API available at: http://localhost:3000
```

## Using the API

Once the server is running, you can access the API at `http://localhost:3000`

### Available Endpoints

#### Root
- `GET /` - API information and available endpoints
- `GET /health` - Health check

#### Members
- `GET /api/members` - Get all members
- `GET /api/members/:id` - Get member by ID
- `GET /api/members/:id/memberships` - Get member's memberships
- `GET /api/members/:id/attendance` - Get member's attendance history
- `POST /api/members` - Create new member
- `PUT /api/members/:id` - Update member
- `DELETE /api/members/:id` - Delete member

#### Trainers
- `GET /api/trainers` - Get all trainers
- `GET /api/trainers/:id` - Get trainer by ID
- `GET /api/trainers/:id/schedule` - Get trainer's schedule
- `POST /api/trainers` - Create new trainer
- `PUT /api/trainers/:id` - Update trainer
- `DELETE /api/trainers/:id` - Delete trainer

#### Clubs
- `GET /api/clubs` - Get all clubs
- `GET /api/clubs/:id` - Get club by ID
- `GET /api/clubs/:id/trainers` - Get club's trainers
- `GET /api/clubs/:id/members` - Get club's active members
- `POST /api/clubs` - Create new club
- `PUT /api/clubs/:id` - Update club
- `DELETE /api/clubs/:id` - Delete club

#### Memberships
- `GET /api/memberships` - Get all memberships
- `GET /api/memberships/active` - Get active memberships only
- `GET /api/memberships/:id` - Get membership by ID
- `POST /api/memberships` - Create new membership
- `PUT /api/memberships/:id` - Update membership
- `DELETE /api/memberships/:id` - Delete membership

#### Workouts
- `GET /api/workouts/types` - Get all workout types
- `GET /api/workouts/schedule` - Get workout schedule
- `GET /api/workouts/schedule/upcoming` - Get upcoming workouts
- `GET /api/workouts/schedule/:id` - Get schedule by ID
- `POST /api/workouts/types` - Create workout type
- `POST /api/workouts/schedule` - Create workout schedule
- `PUT /api/workouts/schedule/:id` - Update workout schedule
- `DELETE /api/workouts/schedule/:id` - Delete workout schedule

#### Attendance
- `GET /api/attendance` - Get all attendance records
- `GET /api/attendance/schedule/:schedule_id` - Get attendance by schedule
- `POST /api/attendance` - Create attendance record (check-in)
- `PUT /api/attendance/:id` - Update attendance status
- `DELETE /api/attendance/:id` - Delete attendance record

## Testing the API

### Using cURL

Get all members:
```bash
curl http://localhost:3000/api/members
```

Get all clubs:
```bash
curl http://localhost:3000/api/clubs
```

Create a new member:
```bash
curl -X POST http://localhost:3000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "phone": "+1-555-9999",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "address": "123 Test St",
    "emergency_contact": "Emergency Contact",
    "emergency_phone": "+1-555-8888",
    "registration_date": "2024-11-10"
  }'
```

### Using Postman or Insomnia

1. Import the endpoints listed above
2. Set the base URL to `http://localhost:3000`
3. Test GET, POST, PUT, and DELETE operations

### Using Browser

Navigate to:
- `http://localhost:3000` - API documentation
- `http://localhost:3000/api/members` - View all members (JSON)
- `http://localhost:3000/api/clubs` - View all clubs (JSON)

## Development Mode

For development with auto-reload on file changes:

```bash
npm run dev
```

This requires `nodemon` which is installed as a dev dependency.

## Troubleshooting

### Database Connection Issues

If you see "Database connection failed":

1. Verify MySQL is running:
```bash
# On Linux/Mac
sudo systemctl status mysql
# or
mysql.server status

# On Windows
# Check Services for MySQL
```

2. Check your `.env` file credentials
3. Ensure the database exists:
```bash
mysql -u root -p -e "SHOW DATABASES;"
```

### Port Already in Use

If port 3000 is already in use, change `API_PORT` in `.env`:
```env
API_PORT=3001
```

### Permission Errors

If you get MySQL permission errors, ensure your user has proper privileges:
```sql
GRANT ALL PRIVILEGES ON fitness_club_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

## Sample Data

The `schema.sql` file includes sample data for testing:
- 3 fitness clubs
- 5 members
- 4 trainers
- 5 memberships
- 6 workout types
- 6 scheduled workouts
- 9 attendance records

You can use this data to test the API endpoints immediately after setup.

## Next Steps

1. Explore the API endpoints using the tools mentioned above
2. Review `SHORT.md` for detailed information about database tables
3. Modify the sample data or add your own
4. Extend the API with additional features as needed

## Support

For issues or questions:
- Check the `SHORT.md` file for database table descriptions
- Review the `schema.sql` file for database structure
- Examine the API route files in `api/routes/` for endpoint details
