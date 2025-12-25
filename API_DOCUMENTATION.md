# 📖 API Documentation - Smart To Do API

**Base URL**: `http://localhost:8000/api/v1`

This API supports **JWT Authentication** (Access + Refresh Tokens) and provides **Smart Task Management** capabilities.

---

## 🔐 Authentication

### 1. User Signup

Register a new user account.

- **Endpoint**: `POST /auth/signup`
- **Body** (JSON):

  ```json
  {
      "email": "user@example.com",
      "password": "strongpassword",
      "full_name": "Test User"
  }
  ```

- **Response**: User object (ID, email).

### 2. User Login

Authenticate to receive access and refresh tokens.

- **Endpoint**: `POST /auth/login`
- **Body** (Form Data / `x-www-form-urlencoded`):
  - `username`: `user@example.com`
  - `password`: `strongpassword`
- **Response**:

  ```json
  {
      "access_token": "eyJhbG...",
      "refresh_token": "eyJhbG...",
      "token_type": "bearer"
  }
  ```

> ⚠️ **Note**: All subsequent requests must include the header `Authorization: Bearer <your_access_token>`.

### 3. Refresh Token

Get a new access token using a valid refresh token.

- **Endpoint**: `POST /auth/refresh`
- **Endpoint**: `POST /auth/refresh`
- **Body** (JSON):

  ```json
  {
      "refresh_token": "your_refresh_token_string"
  }
  ```

- **Behavior**: Smart Rotation - A new refresh token is only issued if the current one expires in less than 5 days. Otherwise, the same token is returned.
- **Response**:

  ```json
  {
      "access_token": "new_access_token...",
      "refresh_token": "new_refresh_token...",
      "token_type": "bearer"
  }
  ```

---

## ✅ Task Management

### 4. Create a Task (Smart)

Create a new task. The system will automatically infer tags and priority if context is detected.

- **Endpoint**: `POST /tasks/`
- **Body** (JSON):

  ```json
  {
      "title": "Buy groceries for dinner",
      "description": "Milk, eggs, and bread",
      "tags": [] 
  }
  ```

- **Smart Behavior**:
  - Input: "Buy groceries"
  - Output: `tags` will automatically include `["shopping"]`.
  - Input: "Submit report ASAP"
  - Output: `priority` will automatically be set to `high`.

### 5. List Tasks

Retrieve a list of tasks with optional filtering.

- **Endpoint**: `GET /tasks/`
- **Query Parameters**:
  - `skip`: Number of records to skip (default: 0).
  - `limit`: Max records to return (default: 100).
  - `priority`: Filter by priority (`low`, `medium`, `high`).
  - `is_completed`: Filter by status (`true`, `false`).
- **Example**: `GET /tasks/?priority=high&is_completed=false`

### 6. Get Specific Task

Retrieve details of a single task.

- **Endpoint**: `GET /tasks/{task_id}`

### 7. Update Task

Update task details.

- **Endpoint**: `PUT /tasks/{task_id}`
- **Body** (JSON):

  ```json
  {
      "is_completed": true
  }
  ```

### 8. Delete Task

Permanently remove a task.

- **Endpoint**: `DELETE /tasks/{task_id}`

---

## 🚦 Error Responses

The API uses helpful error messages and standard HTTP codes.

- **401 Unauthorized**: "Hold up! You need to be logged in to do that." (or Invalid Credentials)
- **404 Not Found**: "Oops! We couldn't find what you were looking for."
- **422 Unprocessable Entity**: Validation errors (e.g., password too short, invalid email).
- **500 Internal Server Error**: "Oh no! Something went wrong on our end."
