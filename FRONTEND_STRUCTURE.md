# Quiz Management System - Complete Backend Structure for Frontend Development

## System Overview
A Django REST Framework backend providing complete quiz management functionality with JWT authentication, admin panel, and public quiz-taking capabilities.

## Base URLs
- **Local Development**: http://localhost:8000
- **API Base**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/swagger/

## Authentication System

### JWT Authentication Flow
1. **Register/Login** → Get access_token & refresh_token
2. **Use access_token** in Authorization header: `Bearer <token>`
3. **Refresh token** when access_token expires
4. **Logout** to blacklist tokens

### Default Admin Credentials
- Username: `admin`
- Password: `admin123`

## Complete API Structure

### 1. Authentication Endpoints (`/api/v1/auth/`)

#### POST `/api/v1/auth/register/`
**Purpose**: Register new admin user
**Auth Required**: No
**Request Body**:
```json
{
  "username": "string",
  "email": "email",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "password_confirm": "string"
}
```
**Response**:
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
    "is_quiz_admin": true,
    "date_joined": "2025-11-22T01:30:00Z"
  },
  "status_code": 201
}
```

#### POST `/api/v1/auth/login/`
**Purpose**: Login and get JWT tokens
**Auth Required**: No
**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
**Response**:
```json
{
  "error": false,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@test.com",
      "first_name": "Admin",
      "last_name": "User",
      "full_name": "Admin User",
      "is_quiz_admin": true
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  },
  "status_code": 200
}
```

#### POST `/api/v1/auth/logout/`
**Purpose**: Logout and blacklist refresh token
**Auth Required**: Yes
**Request Body**:
```json
{
  "refresh_token": "string"
}
```

#### POST `/api/v1/auth/token/refresh/`
**Purpose**: Refresh access token
**Auth Required**: No
**Request Body**:
```json
{
  "refresh": "refresh_token_string"
}
```

#### GET/PUT `/api/v1/auth/profile/`
**Purpose**: Get or update user profile
**Auth Required**: Yes
**GET Response**:
```json
{
  "error": false,
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@test.com",
    "first_name": "Admin",
    "last_name": "User",
    "full_name": "Admin User",
    "is_quiz_admin": true,
    "date_joined": "2025-11-22T01:30:00Z",
    "last_login": "2025-11-22T02:00:00Z"
  }
}
```

#### POST `/api/v1/auth/change-password/`
**Purpose**: Change user password
**Auth Required**: Yes
**Request Body**:
```json
{
  "old_password": "string",
  "new_password": "string",
  "new_password_confirm": "string"
}
```

### 2. Admin Quiz Management (`/api/v1/admin/`)

#### GET `/api/v1/admin/quizzes/`
**Purpose**: List all quizzes with pagination
**Auth Required**: Yes
**Query Parameters**: 
- `page`: Page number (default: 1)
- `search`: Search in title/description
- `ordering`: Sort by `created_at`, `title`, `total_questions` (prefix with `-` for desc)

**Response**:
```json
{
  "error": false,
  "data": {
    "count": 10,
    "next": "http://localhost:8000/api/v1/admin/quizzes/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Python Programming Quiz",
        "description": "Test your Python knowledge",
        "created_by_name": "Admin User",
        "time_limit": 30,
        "is_active": true,
        "passing_score": 70,
        "allow_retakes": false,
        "max_attempts": 1,
        "total_questions": 5,
        "total_points": 10,
        "total_responses": 3,
        "created_at": "2025-11-22T01:30:00Z"
      }
    ]
  }
}
```

#### POST `/api/v1/admin/quizzes/`
**Purpose**: Create new quiz
**Auth Required**: Yes
**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "time_limit": 30,
  "is_active": true,
  "passing_score": 70,
  "show_results_immediately": true,
  "allow_retakes": false,
  "max_attempts": 1
}
```

#### GET `/api/v1/admin/quizzes/{id}/`
**Purpose**: Get detailed quiz with all questions
**Auth Required**: Yes
**Response**:
```json
{
  "error": false,
  "data": {
    "id": 1,
    "title": "Python Programming Quiz",
    "description": "Test your Python knowledge",
    "created_by": 1,
    "created_by_name": "Admin User",
    "time_limit": 30,
    "is_active": true,
    "passing_score": 70,
    "show_results_immediately": true,
    "allow_retakes": false,
    "max_attempts": 1,
    "total_questions": 3,
    "total_points": 8,
    "total_responses": 2,
    "created_at": "2025-11-22T01:30:00Z",
    "updated_at": "2025-11-22T01:35:00Z",
    "questions": [
      {
        "id": 1,
        "question_text": "Which of the following is a Python data type?",
        "question_type": "MCQ",
        "order": 1,
        "points": 2,
        "is_required": true,
        "explanation": "Python has several built-in data types.",
        "created_at": "2025-11-22T01:32:00Z",
        "options": [
          {
            "id": 1,
            "option_text": "list",
            "is_correct": true,
            "order": 1
          },
          {
            "id": 2,
            "option_text": "array",
            "is_correct": false,
            "order": 2
          }
        ]
      }
    ]
  }
}
```

#### PUT/PATCH `/api/v1/admin/quizzes/{id}/`
**Purpose**: Update quiz
**Auth Required**: Yes
**Request Body**: Same as POST

#### DELETE `/api/v1/admin/quizzes/{id}/`
**Purpose**: Delete quiz
**Auth Required**: Yes

### 3. Question Management

#### GET `/api/v1/admin/quizzes/{quiz_id}/questions/`
**Purpose**: List questions for a quiz
**Auth Required**: Yes

#### POST `/api/v1/admin/quizzes/{quiz_id}/questions/`
**Purpose**: Add question to quiz
**Auth Required**: Yes

**MCQ Question Example**:
```json
{
  "question_text": "Which of the following is a Python data type?",
  "question_type": "MCQ",
  "order": 1,
  "points": 2,
  "is_required": true,
  "explanation": "Python has several built-in data types.",
  "options": [
    {"option_text": "list", "is_correct": true, "order": 1},
    {"option_text": "array", "is_correct": false, "order": 2},
    {"option_text": "pointer", "is_correct": false, "order": 3}
  ]
}
```

**True/False Question Example**:
```json
{
  "question_text": "Python is an interpreted language.",
  "question_type": "TRUE_FALSE",
  "order": 2,
  "points": 1,
  "is_required": true,
  "explanation": "Python code is executed by the interpreter.",
  "options": [
    {"option_text": "True", "is_correct": true, "order": 1},
    {"option_text": "False", "is_correct": false, "order": 2}
  ]
}
```

**Text Question Example**:
```json
{
  "question_text": "Explain the difference between a list and tuple.",
  "question_type": "TEXT",
  "order": 3,
  "points": 5,
  "is_required": true,
  "explanation": "Lists are mutable, tuples are immutable."
}
```

#### GET/PUT/PATCH/DELETE `/api/v1/admin/questions/{id}/`
**Purpose**: Manage individual questions
**Auth Required**: Yes

### 4. Public Quiz Taking (`/api/v1/public/`)

#### GET `/api/v1/public/quizzes/`
**Purpose**: List active quizzes for public
**Auth Required**: No
**Response**:
```json
{
  "error": false,
  "data": {
    "count": 3,
    "results": [
      {
        "id": 1,
        "title": "Python Programming Quiz",
        "description": "Test your Python knowledge",
        "time_limit": 30,
        "total_questions": 5
      }
    ]
  }
}
```

#### GET `/api/v1/public/quizzes/{id}/`
**Purpose**: Get quiz for taking (without correct answers)
**Auth Required**: No
**Response**:
```json
{
  "error": false,
  "data": {
    "id": 1,
    "title": "Python Programming Quiz",
    "description": "Test your Python knowledge",
    "time_limit": 30,
    "passing_score": 70,
    "show_results_immediately": true,
    "allow_retakes": false,
    "max_attempts": 1,
    "total_questions": 3,
    "total_points": 8,
    "questions": [
      {
        "id": 1,
        "question_text": "Which of the following is a Python data type?",
        "question_type": "MCQ",
        "order": 1,
        "points": 2,
        "is_required": true,
        "options": [
          {
            "id": 1,
            "option_text": "list",
            "order": 1
          },
          {
            "id": 2,
            "option_text": "array",
            "order": 2
          }
        ]
      }
    ]
  }
}
```

#### POST `/api/v1/public/quizzes/{id}/submit/`
**Purpose**: Submit quiz responses
**Auth Required**: No
**Request Body**:
```json
{
  "participant_name": "John Doe",
  "participant_email": "john@example.com",
  "answers": [
    {
      "question_id": 1,
      "selected_option_id": 1
    },
    {
      "question_id": 2,
      "selected_option_id": 3
    },
    {
      "question_id": 3,
      "text_answer": "Lists are mutable while tuples are immutable..."
    }
  ]
}
```

**Response**:
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
    "submitted_at": "2025-11-22T02:00:00Z",
    "attempt_number": 1,
    "correct_answers_count": 2,
    "total_questions_count": 3,
    "answers": [
      {
        "question_text": "Which of the following is a Python data type?",
        "question_type": "MCQ",
        "selected_option_text": "list",
        "text_answer": "",
        "is_correct": true,
        "points_earned": 2.00,
        "correct_option_text": "list",
        "explanation": "Python has several built-in data types."
      }
    ]
  },
  "status_code": 201
}
```

#### GET `/api/v1/public/results/{session_id}/`
**Purpose**: Get quiz results by session ID
**Auth Required**: No

### 5. Admin Response Management

#### GET `/api/v1/public/admin/responses/`
**Purpose**: List all quiz responses for admin
**Auth Required**: Yes
**Query Parameters**: 
- `page`: Page number
- `search`: Search by participant name/email/quiz title
- `ordering`: Sort by `submitted_at`, `score`, `percentage`

**Response**:
```json
{
  "error": false,
  "data": {
    "count": 15,
    "results": [
      {
        "id": 1,
        "quiz_title": "Python Programming Quiz",
        "participant_name": "John Doe",
        "participant_email": "john@example.com",
        "score": 6.00,
        "total_points": 8,
        "percentage": 75.00,
        "is_passed": true,
        "submitted_at": "2025-11-22T02:00:00Z",
        "attempt_number": 1,
        "correct_answers_count": 3,
        "total_questions_count": 3
      }
    ]
  }
}
```

#### GET `/api/v1/public/admin/responses/{id}/`
**Purpose**: Get detailed response with all answers
**Auth Required**: Yes

## Data Models Structure

### User Model
```typescript
interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  is_quiz_admin: boolean;
  date_joined: string;
  last_login: string;
}
```

### Quiz Model
```typescript
interface Quiz {
  id: number;
  title: string;
  description: string;
  created_by: number;
  created_by_name: string;
  time_limit: number; // minutes, 0 = no limit
  is_active: boolean;
  passing_score: number; // percentage 0-100
  show_results_immediately: boolean;
  allow_retakes: boolean;
  max_attempts: number;
  total_questions: number;
  total_points: number;
  total_responses: number;
  created_at: string;
  updated_at: string;
  questions?: Question[]; // Only in detail view
}
```

### Question Model
```typescript
type QuestionType = 'MCQ' | 'TRUE_FALSE' | 'TEXT';

interface Question {
  id: number;
  quiz: number;
  question_text: string;
  question_type: QuestionType;
  order: number;
  points: number;
  is_required: boolean;
  explanation: string;
  created_at: string;
  options: MCQOption[]; // Only for MCQ and TRUE_FALSE
}
```

### MCQOption Model
```typescript
interface MCQOption {
  id: number;
  question: number;
  option_text: string;
  is_correct: boolean; // Only visible to admin
  order: number;
}
```

### QuizResponse Model
```typescript
interface QuizResponse {
  id: number;
  quiz: number;
  quiz_title: string;
  participant_name: string;
  participant_email: string;
  session_id: string;
  score: number;
  total_points: number;
  percentage: number;
  is_passed: boolean;
  time_taken: string; // Duration
  started_at: string;
  submitted_at: string;
  is_completed: boolean;
  attempt_number: number;
  correct_answers_count: number;
  total_questions_count: number;
  answers: Answer[];
}
```

### Answer Model
```typescript
interface Answer {
  question_text: string;
  question_type: QuestionType;
  selected_option_text: string;
  text_answer: string;
  is_correct: boolean;
  points_earned: number;
  correct_option_text: string;
  explanation: string;
}
```

## Frontend Requirements & Features

### 1. Admin Dashboard Features Needed:
- **Login/Register Forms**
- **Dashboard Overview** (total quizzes, responses, etc.)
- **Quiz Management**:
  - Quiz list with search/filter/pagination
  - Create/Edit quiz form
  - Quiz details view
  - Delete confirmation
- **Question Management**:
  - Add different question types (MCQ, True/False, Text)
  - Question list for each quiz
  - Edit/Delete questions
  - Reorder questions
- **Response Analytics**:
  - Response list with filters
  - Detailed response view
  - Basic statistics
- **Profile Management**
- **Logout functionality**

### 2. Public Quiz Taking Features Needed:
- **Quiz List Page** (available quizzes)
- **Quiz Taking Interface**:
  - Question navigation
  - Timer (if time limit set)
  - Progress indicator
  - Answer validation
  - Participant info form
- **Results Page**:
  - Score display
  - Correct/incorrect answers (if enabled)
  - Explanations
  - Session-based result access

### 3. Technical Requirements:
- **Authentication**: JWT token management with auto-refresh
- **Error Handling**: Standardized error responses
- **Loading States**: For all API calls
- **Responsive Design**: Mobile-friendly
- **Form Validation**: Client-side validation matching backend
- **State Management**: For user session, quiz data, etc.

## Error Response Format
All errors follow this standard format:
```json
{
  "error": true,
  "message": "Error description",
  "details": {
    "field": ["Specific error message"]
  },
  "status_code": 400
}
```

## CORS Configuration
The backend is configured to accept requests from:
- `http://localhost:3000` (React default)
- `http://127.0.0.1:3000`

## Environment Variables for Frontend
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
REACT_APP_BACKEND_URL=http://localhost:8000
```

## Pagination Format
All paginated endpoints return:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/admin/quizzes/?page=3",
  "previous": "http://localhost:8000/api/v1/admin/quizzes/?page=1",
  "results": []
}
```

## Recommended Frontend Tech Stack
- **React** with TypeScript
- **React Router** for navigation
- **Axios** for API calls
- **React Hook Form** for form handling
- **React Query/SWR** for data fetching
- **Tailwind CSS/Material-UI** for styling
- **Zustand/Context API** for state management

This complete structure provides everything needed to build a comprehensive frontend for the Quiz Management System!