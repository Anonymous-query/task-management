# Task Manager API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, enterprise-grade Task Manager API built with FastAPI, featuring robust authentication, role-based access control, and production-ready architecture. Designed with 10+ years of development best practices in mind.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, authentication, and profile management
- **Task Management**: Full CRUD operations with status tracking
- **Role-Based Access Control**: User and Admin roles with appropriate permissions
- **JWT Authentication**: Secure token-based authentication system
- **Data Validation**: Comprehensive input validation using Pydantic

### Security Features
- 🔐 **JWT Token Authentication** with expiration handling
- 🔒 **Password Hashing** using bcrypt with salt
- 👥 **Role-Based Permissions** (User/Admin access levels)
- 🛡️ **Input Validation** and sanitization
- 🚫 **Rate Limiting** to prevent API abuse
- 🔒 **Security Headers** (XSS, CSRF, HSTS protection)

### Enterprise Features
- 📊 **Database Migrations** with Alembic
- 🐳 **Docker Support** with docker-compose
- 📝 **Comprehensive Logging** with structured JSON logs
- 🧪 **Test Coverage** with pytest
- 📖 **API Documentation** with automatic OpenAPI/Swagger
- ⚡ **Performance Optimization** with caching and connection pooling

## 🏗️ Architecture

```
task_manager/
├── app/
│   ├── api/            # API route handlers
│   ├── core/           # Core functionality (config, security, database)
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic layer
│   └── main.py         # FastAPI application entry point
├── tests/              # Comprehensive test suite
├── alembic/           # Database migration files
├── docker-compose.yml # Multi-container Docker setup
└── requirements.txt   # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/task-management.git
   cd task-management
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database**
   ```sql
   CREATE DATABASE task_manager;
   CREATE USER 'taskuser'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON task_manager.* TO 'taskuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Setup

```bash
# Build and run with docker-compose
docker-compose up --build

# The API will be available at http://localhost:8000
```

## 📖 API Usage

### Authentication

#### Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "john_doe",
    "password": "securepassword123"
  }'
```

### Task Management

#### Create a task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "pending"
  }'
```

#### Get all tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Update a task
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## 🔐 Access Control

### User Roles

- **User**: Can manage only their own tasks
- **Admin**: Can manage all users and tasks

### Permissions Matrix

| Action | User | Admin |
|--------|------|-------|
| Create own tasks | ✅ | ✅ |
| View own tasks | ✅ | ✅ |
| Edit own tasks | ✅ | ✅ |
| Delete own tasks | ✅ | ✅ |
| View all tasks | ❌ | ✅ |
| Manage users | ❌ | ✅ |

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `role`: User role (user/admin)
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Tasks Table
- `id`: Primary key
- `title`: Task title
- `description`: Task description
- `status`: Task status (pending/in_progress/completed/cancelled)
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Timestamps

## 🔧 Configuration

### Environment Variables

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/task_manager
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Production Deployment

1. **Set secure environment variables**
2. **Use HTTPS in production**
3. **Configure proper CORS settings**
4. **Set up database connection pooling**
5. **Enable proper logging and monitoring**

## 🚀 Production Deployment

### Using Docker

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With load balancer
docker-compose -f docker-compose.prod.yml --scale app=3 up -d
```

### Using Gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run code formatting
black app/ tests/

# Run linting
flake8 app/ tests/

# Run type checking
mypy app/
```

## 📝 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`

## 🔍 Monitoring and Logging

- **Health Check**: `GET /health`
- **Structured JSON Logging**: All requests and errors are logged
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Comprehensive error handling and reporting

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker & Docker Compose
- **Documentation**: Automatic OpenAPI/Swagger

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database ORM by [SQLAlchemy](https://www.sqlalchemy.org/)
- Security implementations following OWASP guidelines
- Inspired by enterprise-grade API development practices

## 📞 Support

If you have any questions or run into issues, please:
1. Check the [Issues](https://github.com/yourusername/task-manager-api/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Made with ❤️ and Python**
