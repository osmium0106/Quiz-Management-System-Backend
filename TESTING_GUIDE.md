# Quiz Management System Backend - Testing Guide

## Test Coverage Overview

This document provides comprehensive testing instructions for the Quiz Management System backend API.

## Prerequisites

1. **Start the application using Docker:**
   ```bash
   docker-compose up --build
   ```

2. **Verify services are running:**
   - API: http://localhost:8000/
   - Swagger UI: http://localhost:8000/swagger/
   - Database: PostgreSQL on port 5432

## Testing Tools

You can test the API using:
- **Swagger UI** (Recommended): http://localhost:8000/swagger/
- **cURL** commands (provided below)
- **Postman** (import the OpenAPI spec from /swagger.json)
- **Python requests** library

## Complete Testing Workflow

### Phase 1: Authentication Testing

#### 1.1 Register Admin User

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "email": "admin@test.com",
    "first_name": "Test",
    "last_name": "Admin",
    "password": "TestAdmin123!",
    "password_confirm": "TestAdmin123!"
  }'
```

**Expected Response:**
```json
{
  "error": false,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "testadmin",
    "email": "admin@test.com",
    "first_name": "Test",
    "last_name": "Admin",
    "full_name": "Test Admin",
    "is_quiz_admin": true
  },
  "status_code": 201
}
```

#### 1.2 Login Admin User

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "password": "TestAdmin123!"
  }'
```

**Expected Response:**
```json
{
  "error": false,
  "message": "Login successful",
  "data": {
    "user": {...},
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "status_code": 200
}
```

**Save the access_token for subsequent requests!**

#### 1.3 Get User Profile

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Phase 2: Quiz Management Testing

#### 2.1 Create a Quiz

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Programming Quiz",
    "description": "Test your Python programming knowledge",
    "time_limit": 30,
    "passing_score": 70,
    "show_results_immediately": true,
    "allow_retakes": false,
    "max_attempts": 1
  }'
```

**Expected Response:**
```json
{
  "error": false,
  "message": "Success",
  "data": {
    "id": 1,
    "title": "Python Programming Quiz",
    "description": "Test your Python programming knowledge",
    "time_limit": 30,
    "passing_score": 70,
    "is_active": true
  },
  "status_code": 201
}
```

#### 2.2 List All Quizzes

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/admin/quizzes/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 2.3 Get Quiz Details

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/admin/quizzes/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Phase 3: Question Management Testing

#### 3.1 Add MCQ Question

**Request:**
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
    "explanation": "Python has several built-in data types.",
    "options": [
      {"option_text": "list", "is_correct": true, "order": 1},
      {"option_text": "array", "is_correct": false, "order": 2},
      {"option_text": "pointer", "is_correct": false, "order": 3},
      {"option_text": "struct", "is_correct": false, "order": 4}
    ]
  }'
```

#### 3.2 Add True/False Question

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/1/questions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Python is an interpreted language.",
    "question_type": "TRUE_FALSE",
    "order": 2,
    "points": 1,
    "is_required": true,
    "explanation": "Python code is executed line by line by the Python interpreter.",
    "options": [
      {"option_text": "True", "is_correct": true, "order": 1},
      {"option_text": "False", "is_correct": false, "order": 2}
    ]
  }'
```

#### 3.3 Add Text Question

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/1/questions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Explain the difference between a list and a tuple in Python.",
    "question_type": "TEXT",
    "order": 3,
    "points": 5,
    "is_required": true,
    "explanation": "Lists are mutable while tuples are immutable data structures."
  }'
```

#### 3.4 List Questions for Quiz

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/admin/quizzes/1/questions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Phase 4: Public Quiz Taking Testing

#### 4.1 List Public Quizzes (No Auth Required)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/public/quizzes/
```

**Expected Response:**
```json
{
  "error": false,
  "message": "Success",
  "data": {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Python Programming Quiz",
        "description": "Test your Python programming knowledge",
        "time_limit": 30,
        "total_questions": 3
      }
    ]
  }
}
```

#### 4.2 Get Quiz for Taking (No Auth Required)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/public/quizzes/1/
```

**Expected Response:**
```json
{
  "error": false,
  "message": "Success",
  "data": {
    "id": 1,
    "title": "Python Programming Quiz",
    "description": "Test your Python programming knowledge",
    "questions": [
      {
        "id": 1,
        "question_text": "Which of the following is a Python data type?",
        "question_type": "MCQ",
        "points": 2,
        "options": [
          {"id": 1, "option_text": "list", "order": 1},
          {"id": 2, "option_text": "array", "order": 2},
          {"id": 3, "option_text": "pointer", "order": 3},
          {"id": 4, "option_text": "struct", "order": 4}
        ]
      }
    ]
  }
}
```

#### 4.3 Submit Quiz Response (No Auth Required)

**Request:**
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
        "selected_option_id": 5
      },
      {
        "question_id": 3,
        "text_answer": "Lists are mutable sequences that can be modified after creation, while tuples are immutable sequences that cannot be changed once created. Lists use square brackets [] and tuples use parentheses ()."
      }
    ]
  }'
```

**Expected Response:**
```json
{
  "error": false,
  "message": "Quiz submitted successfully",
  "data": {
    "quiz_title": "Python Programming Quiz",
    "participant_name": "John Doe",
    "score": 3.00,
    "total_points": 8,
    "percentage": 37.50,
    "is_passed": false,
    "submitted_at": "2025-11-22T01:30:00Z",
    "attempt_number": 1,
    "correct_answers_count": 2,
    "total_questions_count": 3,
    "answers": [...] // Detailed answers if show_results_immediately is true
  },
  "status_code": 201
}
```

#### 4.4 Get Quiz Results (No Auth Required)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/public/results/SESSION_ID_FROM_RESPONSE/
```

### Phase 5: Admin Response Management Testing

#### 5.1 List All Responses (Admin Only)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/public/admin/responses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5.2 Get Detailed Response (Admin Only)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/public/admin/responses/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Advanced Testing Scenarios

### Test Error Handling

#### Invalid Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "invalid", "password": "wrong"}'
```

#### Unauthorized Access
```bash
curl -X GET http://localhost:8000/api/v1/admin/quizzes/
# Should return 401 Unauthorized
```

#### Invalid Quiz Submission
```bash
curl -X POST http://localhost:8000/api/v1/public/quizzes/999/submit/ \
  -H "Content-Type: application/json" \
  -d '{"participant_name": "Test", "participant_email": "test@test.com", "answers": []}'
# Should return 404 Not Found
```

### Test Data Validation

#### Invalid Question Creation
```bash
curl -X POST http://localhost:8000/api/v1/admin/quizzes/1/questions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "",
    "question_type": "MCQ",
    "options": [
      {"option_text": "Option 1", "is_correct": true},
      {"option_text": "Option 2", "is_correct": true}
    ]
  }'
# Should return validation errors
```

### Test Pagination

#### Test Quiz List Pagination
```bash
curl -X GET "http://localhost:8000/api/v1/admin/quizzes/?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test Search and Filtering

#### Search Quizzes
```bash
curl -X GET "http://localhost:8000/api/v1/admin/quizzes/?search=Python" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Expected Test Results Summary

After running all tests, you should verify:

✅ **Authentication System**
- User registration works
- Login returns valid JWT tokens
- Protected endpoints require authentication
- Token refresh works

✅ **Quiz Management**
- Admins can create, read, update, delete quizzes
- Quiz validation works correctly
- Pagination functions properly

✅ **Question Management**
- All question types (MCQ, True/False, Text) can be created
- Question validation works (correct answers, options)
- Questions are properly associated with quizzes

✅ **Public Quiz Taking**
- Public can view active quizzes without authentication
- Quiz submission works correctly
- Scoring is calculated automatically
- Results are returned properly

✅ **Response Management**
- Admins can view all responses
- Detailed response information is available
- Filtering and search work correctly

✅ **Error Handling**
- Invalid requests return proper error messages
- Authentication errors are handled correctly
- Validation errors provide clear feedback

## Performance Testing

For load testing, you can use tools like:
- Apache Bench (ab)
- wrk
- Artillery.js

Example load test:
```bash
ab -n 1000 -c 10 http://localhost:8000/api/v1/public/quizzes/
```

## API Documentation Testing

Visit these URLs to verify documentation:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- OpenAPI JSON: http://localhost:8000/swagger.json

## Security Testing

1. **Test CORS**: Try making requests from different origins
2. **Test JWT Expiry**: Wait for token expiration and test refresh
3. **Test Input Validation**: Try sending malformed data
4. **Test SQL Injection**: Try SQL injection in text fields (should be prevented)

## Troubleshooting

### Common Issues

1. **Docker not starting**: Check if ports 8000 and 5432 are available
2. **Database connection errors**: Verify PostgreSQL is running in Docker
3. **JWT errors**: Check token format and expiration
4. **Permission errors**: Ensure you're using the correct authorization header

### Debug Commands

```bash
# Check Docker logs
docker-compose logs web
docker-compose logs db

# Check running containers
docker ps

# Access Django shell
docker-compose exec web python manage.py shell

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

This completes the comprehensive testing guide for the Quiz Management System backend API.