# User Login API Documentation

## Overview
Login endpoint for user authentication. Returns an authentication token for subsequent API requests.

## Base URL
```
http://localhost:8000/api
```

---

## Login Endpoint

### 1. User Login
**Endpoint:** `POST /auth/login/login/`

**Description:** Authenticate user with username and password, receive authentication token.

**Request Body:**
```json
{
  "username": "OscarPrueba",
  "password": "ozcar16990"
}
```

**Required Fields:**
- `username` - User's username
- `password` - User's password

**Success Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbea6d3356",
  "user": {
    "id": 5,
    "username": "OscarPrueba",
    "email": "oscar@example.com",
    "first_name": "Oscar",
    "last_name": "Prueba",
    "profile": {
      "id": 5,
      "username": "OscarPrueba",
      "email": "oscar@example.com",
      "first_name": "Oscar",
      "last_name": "Prueba",
      "role": "driver",
      "phone_number": "+1-555-123-4567",
      "company_name": "ABC Logistics",
      "is_verified": false,
      "created_at": "2026-05-06T10:30:00Z",
      "updated_at": "2026-05-06T10:30:00Z"
    }
  },
  "message": "Login successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid username or password."]
}
```

---

### 2. User Logout
**Endpoint:** `POST /auth/login/logout/`

**Description:** Logout user and invalidate their authentication token.

**Headers Required:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6d3356
```

**Success Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "User not authenticated"
}
```

---

## Authentication Token Usage

After login, use the token to access protected endpoints:

**All API Requests:**
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6d3356" \
  http://localhost:8000/api/profiles/
```

**JavaScript/Fetch:**
```javascript
fetch('http://localhost:8000/api/profiles/', {
  method: 'GET',
  headers: {
    'Authorization': 'Token ' + token,
    'Content-Type': 'application/json',
  },
})
```

---

## React Integration Example

### Login Component
```javascript
import React, { useState } from 'react';

function LoginForm({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Save token to localStorage
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        if (onLoginSuccess) {
          onLoginSuccess(data);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.non_field_errors?.[0] || 'Login failed');
      }
    } catch (error) {
      setError('An error occurred. Please try again.');
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      
      {error && <div className="error">{error}</div>}
      
      <div className="form-group">
        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}

export default LoginForm;
```

### Using Token for API Requests
```javascript
// authService.js
export const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

export const isAuthenticated = () => {
  return !!getAuthToken();
};

export const logout = async () => {
  const token = getAuthToken();
  
  try {
    await fetch('http://localhost:8000/api/auth/login/logout/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  }
};

export const fetchWithAuth = async (url, options = {}) => {
  const token = getAuthToken();
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    },
  });
};
```

### Protected Component
```javascript
import React, { useEffect, useState } from 'react';
import { fetchWithAuth, getAuthToken } from './authService';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      const token = getAuthToken();
      if (!token) {
        // Redirect to login
        return;
      }

      try {
        const response = await fetchWithAuth('http://localhost:8000/api/profiles/');
        if (response.ok) {
          const data = await response.json();
          setProfile(data);
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (!profile) return <div>No profile found</div>;

  return (
    <div>
      <h1>Welcome, {profile.first_name}!</h1>
      <p>Email: {profile.email}</p>
      <p>Role: {profile.profile.role}</p>
    </div>
  );
}

export default Dashboard;
```

---

## Complete Login Flow (React)

1. **User enters credentials**
2. **POST to `/api/auth/login/login/`**
3. **Receive token and user data**
4. **Save token to localStorage**
5. **Use token in Authorization header for all requests**
6. **On logout, call `/api/auth/login/logout/`**
7. **Clear token from localStorage**

---

## Testing with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "OscarPrueba",
    "password": "ozcar16990"
  }'
```

### Logout
```bash
curl -X POST http://localhost:8000/api/auth/login/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6d3356"
```

### Use token in request
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6d3356" \
  http://localhost:8000/api/profiles/
```

---

## Error Codes

| Status | Description |
|--------|-------------|
| 200 OK | Login successful |
| 400 Bad Request | Invalid credentials or missing fields |
| 401 Unauthorized | Token invalid or expired |
| 404 Not Found | Endpoint not found |

---

## Token Storage Best Practices

### localStorage
```javascript
// Save token
localStorage.setItem('authToken', token);

// Get token
const token = localStorage.getItem('authToken');

// Remove token
localStorage.removeItem('authToken');
```

### Environment Variables
```javascript
// .env
REACT_APP_API_URL=http://localhost:8000/api

// Usage
const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/login/login/`, {...})
```

---

## Security Notes

- **Never expose tokens** in public repositories
- **Use HTTPS** in production (not HTTP)
- **Store tokens securely** (httpOnly cookies preferred over localStorage)
- **Implement token refresh** for long-lived sessions
- **Log out on sensitive operations** to invalidate tokens
- **Use environment variables** for API URLs

---

## Next Steps

1. Test login with your credentials
2. Store the token securely in your React app
3. Add Authorization header to all authenticated requests
4. Implement logout functionality
5. Handle token expiration/refresh if needed
