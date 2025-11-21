# Quiz Management System Backend - API Documentation

## Overview
This is a comprehensive Django REST Framework backend for a Quiz Management System that provides:
- Admin authentication and quiz management
- Public quiz-taking functionality
- Real-time scoring and results
- Comprehensive API documentation with Swagger

## Quick Start

### Using Docker (Recommended)

1. **Clone and start the application:**
   ```bash
   git clone <repository-url>
   cd Quiz-Management-System-Backend
   docker-compose up --build
   ```

2. **Access the application:**
   - API Base URL: http://localhost:8000/api/v1/
   - Swagger Documentation: http://localhost:8000/swagger/
   - ReDoc Documentation: http://localhost:8000/redoc/
   - Django Admin: http://localhost:8000/admin/

3. **Default Admin Credentials:**
   - Username: `admin`
   - Password: `admin123`

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database and update .env file**

3. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Start server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints
- `POST /api/v1/auth/register/` - Register new admin user
- `POST /api/v1/auth/login/` - Login and get JWT tokens
- `POST /api/v1/auth/logout/` - Logout (blacklist token)
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `GET/PUT /api/v1/auth/profile/` - Get/Update user profile
- `POST /api/v1/auth/change-password/` - Change password

### Admin Quiz Management
- `GET /api/v1/admin/quizzes/` - List all quizzes (paginated)
- `POST /api/v1/admin/quizzes/` - Create new quiz
- `GET /api/v1/admin/quizzes/{id}/` - Get quiz details
- `PUT /api/v1/admin/quizzes/{id}/` - Update quiz
- `DELETE /api/v1/admin/quizzes/{id}/` - Delete quiz
- `GET /api/v1/admin/quizzes/{quiz_id}/questions/` - List questions
- `POST /api/v1/admin/quizzes/{quiz_id}/questions/` - Add question
- `GET /api/v1/admin/questions/{id}/` - Get question details  
- `PUT /api/v1/admin/questions/{id}/` - Update question
- `DELETE /api/v1/admin/questions/{id}/` - Delete question

### Public Quiz Taking
- `GET /api/v1/public/quizzes/` - List available quizzes
- `GET /api/v1/public/quizzes/{id}/` - Get quiz for taking
- `POST /api/v1/public/quizzes/{id}/submit/` - Submit quiz responses
- `GET /api/v1/public/results/{session_id}/` - Get quiz results

### Admin Response Management
- `GET /api/v1/public/admin/responses/` - List all responses
- `GET /api/v1/public/admin/responses/{id}/` - Get detailed response

## Question Types Supported

### 1. Multiple Choice Questions (MCQ)
```json
{
  "question_text": "What is the capital of France?",
  "question_type": "MCQ",
  "points": 2,
  "options": [
    {"option_text": "London", "is_correct": false, "order": 1},
    {"option_text": "Paris", "is_correct": true, "order": 2},
    {"option_text": "Berlin", "is_correct": false, "order": 3},
    {"option_text": "Madrid", "is_correct": false, "order": 4}
  ]
}
```

### 2. True/False Questions
```json
{
  "question_text": "Python is a programming language.",
  "question_type": "TRUE_FALSE",
  "points": 1,
  "options": [
    {"option_text": "True", "is_correct": true, "order": 1},
    {"option_text": "False", "is_correct": false, "order": 2}
  ]
}
```

### 3. Text Questions
```json
{
  "question_text": "Explain the concept of inheritance in OOP.",
  "question_type": "TEXT",
  "points": 5,
  "explanation": "Answer should cover basic inheritance concepts..."
}
```

## Sample API Usage

### 1. Admin Registration and Login

**Register Admin:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "quiz_admin",
    "email": "admin@example.com",
    "first_name": "Quiz",
    "last_name": "Admin",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "quiz_admin",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "error": false,
  "message": "Login successful",
  "data": {
    "user": {...},
    "access_token": "eyJ0eXAiOiJKV1Q...",
    "refresh_token": "eyJ0eXAiOiJKV1Q..."
  }
}
```

### 2. Create a Quiz

```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Basics Quiz",
    "description": "Test your knowledge of Python fundamentals",
    "time_limit": 30,
    "passing_score": 70,
    "show_results_immediately": true,
    "allow_retakes": false,
    "max_attempts": 1
  }'
```

### 3. Add Questions to Quiz

**MCQ Question:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/1/questions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Which of the following is a Python data type?",
    "question_type": "MCQ",
    "order": 1,
    "points": 2,
    "is_required": true,
    "explanation": "Python has several built-in data types including lists, tuples, and dictionaries.",
    "options": [
      {"option_text": "list", "is_correct": true, "order": 1},
      {"option_text": "array", "is_correct": false, "order": 2},
      {"option_text": "pointer", "is_correct": false, "order": 3}
    ]
  }'
```

### 4. Take a Quiz (Public)

**Get Quiz:**
```bash
curl http://localhost:8000/api/v1/public/quizzes/1/
```

**Submit Response:**
```bash
curl -X POST http://localhost:8000/api/v1/public/quizzes/1/submit/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_name": "John Doe",
    "participant_email": "john@example.com",
    "answers": [
      {
        "question_id": 1,
        "selected_option_id": 1
      },
      {
        "question_id": 2,
        "text_answer": "Object-oriented programming allows code reuse through inheritance..."
      }
    ]
  }'
```

## Features

### Core Features
- ✅ JWT Authentication for admins
- ✅ Complete quiz CRUD operations
- ✅ Multiple question types (MCQ, True/False, Text)
- ✅ Public quiz taking without authentication
- ✅ Automatic scoring and results
- ✅ Pagination on all list endpoints
- ✅ Comprehensive error handling
- ✅ Swagger/OpenAPI documentation

### Quiz Management Features
- ✅ Time limits for quizzes
- ✅ Passing score configuration
- ✅ Retake policies
- ✅ Maximum attempts control
- ✅ Show/hide results immediately
- ✅ Question ordering and points
- ✅ Optional explanations for questions

### Response Management
- ✅ Track participant responses
- ✅ Calculate scores automatically
- ✅ Session-based result retrieval
- ✅ Admin response analytics
- ✅ Attempt tracking for retakes

## Database Schema

The system uses the following main models:

- **User**: Custom user model for admin authentication
- **Quiz**: Main quiz configuration and metadata  
- **Question**: Questions with different types and options
- **MCQOption**: Options for MCQ and True/False questions
- **QuizResponse**: Participant responses and scoring
- **Answer**: Individual question answers

## Error Handling

All API endpoints return standardized error responses:

```json
{
  "error": true,
  "message": "Error description",
  "details": {...},
  "status_code": 400
}
```

Success responses follow this format:
```json
{
  "error": false,
  "message": "Success message",
  "data": {...},
  "status_code": 200
}
```

## Security Features

- JWT-based authentication for admins
- Token refresh mechanism  
- Password validation and hashing
- CORS configuration for frontend integration
- Input validation and sanitization
- SQL injection protection (Django ORM)
- Permission-based access control

## Performance Features

- Database query optimization
- Pagination on all list views
- Efficient scoring calculations
- Proper database indexing
- Static file serving configuration

## Testing

The system includes comprehensive test coverage. Run tests with:

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Docker Production Deployment

1. Update environment variables in `.env`
2. Set `DEBUG=False` for production
3. Configure proper database credentials
4. Use production-ready web server (gunicorn)
5. Set up reverse proxy (nginx)
6. Configure SSL certificates

### Environment Variables

Required environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=quiz_management_db
DB_USER=quiz_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Support

For questions or issues:
1. Check the Swagger documentation at `/swagger/`
2. Review the API examples above
3. Check the Django logs for detailed error information
4. Ensure all required environment variables are set

## Next Steps

If you had more time, consider implementing:
- Advanced analytics and reporting
- Quiz categories and tagging
- File upload support for questions
- Email notifications for results
- Advanced permission system
- Caching for better performance
- Real-time quiz sessions
- Mobile-optimized endpoints