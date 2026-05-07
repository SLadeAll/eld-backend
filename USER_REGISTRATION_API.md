# User Registration API Documentation

## Overview
This API provides endpoints for user registration without admin privileges. New users can create accounts that will have limited access to the system.

## Base URL
```
http://localhost:8000/api
```

---

## Endpoints

### 1. Register a New User
**Endpoint:** `POST /auth/register/register/`

**Description:** Create a new non-admin user account with optional role and profile information.

**Request Body:**
```json
{
  "username": "john_driver",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "role": "driver",
  "phone_number": "+1-555-123-4567",
  "company_name": "ABC Logistics"
}
```

**Required Fields:**
- `username` - Unique username (must not exist)
- `email` - Unique email address (must not exist)
- `password` - Minimum 8 characters
- `password_confirm` - Must match password

**Optional Fields:**
- `first_name` - User's first name
- `last_name` - User's last name
- `role` - User role (default: "user")
  - Options: `driver`, `dispatcher`, `manager`, `user`
- `phone_number` - Contact phone number
- `company_name` - Company/Organization name

**Success Response (201 Created):**
```json
{
  "id": 5,
  "username": "john_driver",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "username": ["Username already exists."],
  "email": ["Email already registered."],
  "password": ["Passwords must match."]
}
```

---

### 2. Check Username Availability
**Endpoint:** `GET /auth/register/check_username/?username=john_driver`

**Description:** Check if a username is available for registration.

**Query Parameters:**
- `username` (required) - Username to check

**Response:**
```json
{
  "available": true
}
```

---

### 3. Check Email Availability
**Endpoint:** `GET /auth/register/check_email/?email=john@example.com`

**Description:** Check if an email is available for registration.

**Query Parameters:**
- `email` (required) - Email address to check

**Response:**
```json
{
  "available": true
}
```

---

### 4. Get User Profile
**Endpoint:** `GET /profiles/{id}/`

**Description:** Retrieve a specific user profile by ID.

**Response:**
```json
{
  "id": 5,
  "username": "john_driver",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "driver",
  "phone_number": "+1-555-123-4567",
  "company_name": "ABC Logistics",
  "is_verified": false,
  "created_at": "2026-05-06T10:30:00Z",
  "updated_at": "2026-05-06T10:30:00Z"
}
```

---

### 5. List All User Profiles
**Endpoint:** `GET /profiles/`

**Description:** List all user profiles (paginated).

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "role": "driver",
      "is_verified": true,
      "created_at": "2026-05-01T10:00:00Z",
      "updated_at": "2026-05-01T10:00:00Z"
    },
    ...
  ]
}
```

---

### 6. Update User Profile
**Endpoint:** `PATCH /profiles/{id}/`

**Description:** Update user profile information (role, phone_number, company_name).

**Request Body:**
```json
{
  "role": "dispatcher",
  "phone_number": "+1-555-987-6543"
}
```

**Response:**
```json
{
  "id": 5,
  "username": "john_driver",
  "email": "john@example.com",
  "role": "dispatcher",
  "phone_number": "+1-555-987-6543",
  "company_name": "ABC Logistics",
  "is_verified": false,
  "created_at": "2026-05-06T10:30:00Z",
  "updated_at": "2026-05-06T11:45:00Z"
}
```

---

## User Roles

| Role | Description |
|------|-------------|
| `driver` | Driver accessing ELD system for logging hours |
| `dispatcher` | Dispatcher managing driver routes and trips |
| `manager` | Manager with administrative access |
| `user` | Standard user with limited access (default) |

---

## Security Notes

1. **No Admin Privileges**: All registered users have `is_staff=False` and `is_superuser=False`
2. **Password Requirements**: Minimum 8 characters
3. **Email Verification**: `is_verified` field tracks if email has been verified (default: false)
4. **CORS Configuration**: Ensure CORS is properly configured in settings.py for React frontend

---

## Error Codes

| Status | Description |
|--------|-------------|
| 200 OK | Successful GET request |
| 201 Created | User successfully created |
| 400 Bad Request | Invalid input data |
| 404 Not Found | Resource not found |
| 500 Internal Server Error | Server error |

---

## Example React Integration

### Registration Form
```javascript
// Example: Register a new user
async function registerUser(userData) {
  try {
    const response = await fetch('http://localhost:8000/api/auth/register/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: userData.username,
        email: userData.email,
        first_name: userData.firstName,
        last_name: userData.lastName,
        password: userData.password,
        password_confirm: userData.passwordConfirm,
        role: userData.role || 'user',
        phone_number: userData.phoneNumber,
        company_name: userData.companyName,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('User registered successfully:', data);
      return data;
    } else {
      const errors = await response.json();
      console.error('Registration failed:', errors);
      return null;
    }
  } catch (error) {
    console.error('Error during registration:', error);
    return null;
  }
}
```

### Username Availability Check
```javascript
async function checkUsernameAvailability(username) {
  try {
    const response = await fetch(
      `http://localhost:8000/api/auth/register/check_username/?username=${username}`
    );
    const data = await response.json();
    return data.available;
  } catch (error) {
    console.error('Error checking username:', error);
    return false;
  }
}
```

### Get User Profile
```javascript
async function getUserProfile(userId) {
  try {
    const response = await fetch(`http://localhost:8000/api/profiles/${userId}/`);
    if (response.ok) {
      const profile = await response.json();
      return profile;
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
    return null;
  }
}
```

---

## Testing with cURL

### Register a user
```bash
curl -X POST http://localhost:8000/api/auth/register/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_driver",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "role": "driver",
    "phone_number": "+1-555-123-4567",
    "company_name": "ABC Logistics"
  }'
```

### Check username availability
```bash
curl http://localhost:8000/api/auth/register/check_username/?username=john_driver
```

### Get user profile
```bash
curl http://localhost:8000/api/profiles/5/
```

---

## Database Schema

### UserProfile Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User model |
| role | CharField | User role (driver, dispatcher, manager, user) |
| phone_number | CharField | Contact phone number |
| company_name | CharField | Company/Organization name |
| is_verified | Boolean | Email verification status |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

---

## Setup Instructions

1. **Enable CORS** (if needed for React frontend):
   ```python
   # settings.py
   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]
   
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",  # React development server
       "http://localhost:8000",
   ]
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access Admin Panel**:
   Navigate to `http://localhost:8000/admin` to manage users and profiles

---

## Additional Notes

- Users registered through the API cannot access the Django admin panel
- User profiles are automatically created when a user registers
- Email addresses and usernames must be unique across the system
- Passwords are hashed and never stored in plain text
- The registration endpoint is public and requires no authentication
