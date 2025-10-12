# EduCompanion Backend

A Python Flask backend for the EduCompanion application with MongoDB integration.

## 🚀 Features

- **User Authentication**: Signup, login, and JWT-based authentication
- **User Management**: Profile updates, password changes, and account deletion
- **MongoDB Integration**: Robust database operations with proper error handling
- **RESTful API**: Clean and consistent API endpoints
- **Security**: Password hashing with bcrypt, JWT tokens, and input validation

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository
```bash
cd educompanion-backend
```

### 2. Create a virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the example environment file and configure it:
```bash
# Copy the example file
cp env.example .env

# Edit .env with your configuration
```

**Required environment variables:**
- `MONGODB_URI`: MongoDB connection string
- `MONGODB_DB`: Database name
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `SECRET_KEY`: Flask secret key

### 5. Start MongoDB
Make sure MongoDB is running on your system or use MongoDB Atlas.

## 🚀 Running the Application

### Development mode
```bash
python run.py
```

### Production mode
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
python run.py
```

The server will start on `http://localhost:5000` by default.

## 📚 API Endpoints

### Authentication Routes (`/api/auth`)

#### POST `/api/auth/signup`
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "_id": "user_id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### POST `/api/auth/login`
Authenticate user and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "_id": "user_id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access_token": "jwt_token_here"
}
```

#### GET `/api/auth/profile`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

#### POST `/api/auth/logout`
Logout user (client-side token removal).

### User Routes (`/api/user`)

#### PUT `/api/user/profile`
Update user profile (requires authentication).

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

#### DELETE `/api/user/profile`
Delete user account (soft delete, requires authentication).

#### POST `/api/user/change-password`
Change user password (requires authentication).

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword123"
}
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## 🗄️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password": "string (hashed)",
  "first_name": "string",
  "last_name": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_active": "boolean"
}
```

## 🧪 Testing

Test the API endpoints using tools like:
- Postman
- cURL
- Thunder Client (VS Code extension)

### Example cURL commands:

**Signup:**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 🚧 Project Structure

```
educompanion-backend/
├── app.py                 # Main Flask application
├── run.py                 # Application runner
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── config/               # Configuration files
│   ├── __init__.py
│   └── database.py       # Database configuration
├── models/               # Data models
│   ├── __init__.py
│   └── user.py          # User model
├── routes/               # API routes
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   └── user.py          # User management routes
└── README.md             # This file
```

## 🔧 Configuration

### MongoDB Connection
- Local MongoDB: `mongodb://localhost:27017/`
- MongoDB Atlas: `mongodb+srv://username:password@cluster.mongodb.net/`

### JWT Configuration
- Token expiration: 1 hour (3600 seconds) by default
- Customizable via environment variables

## 🚀 Next Steps

- [ ] File upload functionality
- [ ] User roles and permissions
- [ ] Email verification
- [ ] Password reset functionality
- [ ] API rate limiting
- [ ] Logging and monitoring
- [ ] Unit tests
- [ ] Docker containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
