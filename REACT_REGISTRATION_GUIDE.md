# Quick Start: React Registration Integration

## API Base URL
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## Registration Service (React Hook/Service)

```javascript
// userService.js or authService.js
export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register/register/`, {
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
        phone_number: userData.phoneNumber || '',
        company_name: userData.companyName || '',
      }),
    });

    if (response.status === 201) {
      return await response.json();
    } else {
      const errors = await response.json();
      throw new Error(JSON.stringify(errors));
    }
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

export const checkUsernameAvailable = async (username) => {
  const response = await fetch(
    `${API_BASE_URL}/auth/register/check_username/?username=${username}`
  );
  const data = await response.json();
  return data.available;
};

export const checkEmailAvailable = async (email) => {
  const response = await fetch(
    `${API_BASE_URL}/auth/register/check_email/?email=${email}`
  );
  const data = await response.json();
  return data.available;
};

export const getUserProfile = async (userId) => {
  const response = await fetch(`${API_BASE_URL}/profiles/${userId}/`);
  if (response.ok) {
    return await response.json();
  }
  throw new Error('Failed to fetch profile');
};
```

---

## Registration Component Example

```jsx
import React, { useState } from 'react';
import { registerUser, checkUsernameAvailable, checkEmailAvailable } from './userService';

function RegistrationForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    passwordConfirm: '',
    role: 'driver',
    phoneNumber: '',
    companyName: '',
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username) newErrors.username = 'Username is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.firstName) newErrors.firstName = 'First name is required';
    if (!formData.lastName) newErrors.lastName = 'Last name is required';
    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    if (formData.password !== formData.passwordConfirm) {
      newErrors.passwordConfirm = 'Passwords do not match';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);

    try {
      // Check availability before submitting
      const usernameAvailable = await checkUsernameAvailable(formData.username);
      const emailAvailable = await checkEmailAvailable(formData.email);

      if (!usernameAvailable) {
        setErrors({ username: 'Username already taken' });
        setLoading(false);
        return;
      }

      if (!emailAvailable) {
        setErrors({ email: 'Email already registered' });
        setLoading(false);
        return;
      }

      // Register user
      const result = await registerUser(formData);
      setSuccess(true);
      console.log('User registered:', result);
      
      // Redirect or clear form
      setTimeout(() => {
        // window.location.href = '/login';
        setFormData({
          username: '',
          email: '',
          firstName: '',
          lastName: '',
          password: '',
          passwordConfirm: '',
          role: 'driver',
          phoneNumber: '',
          companyName: '',
        });
      }, 2000);
    } catch (error) {
      console.error('Registration failed:', error);
      if (error.message.includes('username')) {
        setErrors({ username: 'Registration failed' });
      } else {
        setErrors({ submit: 'Registration failed. Please try again.' });
      }
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return <div className="success-message">Registration successful! Redirecting...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="registration-form">
      <h2>Create Your Account</h2>

      <div className="form-group">
        <label>Username *</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleInputChange}
          placeholder="Enter username"
        />
        {errors.username && <span className="error">{errors.username}</span>}
      </div>

      <div className="form-group">
        <label>Email *</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          placeholder="Enter email"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>First Name *</label>
          <input
            type="text"
            name="firstName"
            value={formData.firstName}
            onChange={handleInputChange}
            placeholder="First name"
          />
          {errors.firstName && <span className="error">{errors.firstName}</span>}
        </div>

        <div className="form-group">
          <label>Last Name *</label>
          <input
            type="text"
            name="lastName"
            value={formData.lastName}
            onChange={handleInputChange}
            placeholder="Last name"
          />
          {errors.lastName && <span className="error">{errors.lastName}</span>}
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Password * (min 8 characters)</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            placeholder="Enter password"
          />
          {errors.password && <span className="error">{errors.password}</span>}
        </div>

        <div className="form-group">
          <label>Confirm Password *</label>
          <input
            type="password"
            name="passwordConfirm"
            value={formData.passwordConfirm}
            onChange={handleInputChange}
            placeholder="Confirm password"
          />
          {errors.passwordConfirm && (
            <span className="error">{errors.passwordConfirm}</span>
          )}
        </div>
      </div>

      <div className="form-group">
        <label>Role</label>
        <select name="role" value={formData.role} onChange={handleInputChange}>
          <option value="user">Regular User</option>
          <option value="driver">Driver</option>
          <option value="dispatcher">Dispatcher</option>
          <option value="manager">Manager</option>
        </select>
      </div>

      <div className="form-group">
        <label>Phone Number</label>
        <input
          type="tel"
          name="phoneNumber"
          value={formData.phoneNumber}
          onChange={handleInputChange}
          placeholder="Phone number (optional)"
        />
      </div>

      <div className="form-group">
        <label>Company Name</label>
        <input
          type="text"
          name="companyName"
          value={formData.companyName}
          onChange={handleInputChange}
          placeholder="Company name (optional)"
        />
      </div>

      {errors.submit && <div className="error-message">{errors.submit}</div>}

      <button type="submit" disabled={loading}>
        {loading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}

export default RegistrationForm;
```

---

## Real-time Validation Hook

```javascript
import { useState, useEffect, useCallback } from 'react';
import { checkUsernameAvailable, checkEmailAvailable } from './userService';

export const useFormValidation = () => {
  const [availability, setAvailability] = useState({
    username: null,
    email: null,
  });

  const [checking, setChecking] = useState({
    username: false,
    email: false,
  });

  const checkUsername = useCallback(async (username) => {
    if (username.length < 3) return;
    
    setChecking((prev) => ({ ...prev, username: true }));
    try {
      const available = await checkUsernameAvailable(username);
      setAvailability((prev) => ({ ...prev, username: available }));
    } finally {
      setChecking((prev) => ({ ...prev, username: false }));
    }
  }, []);

  const checkEmail = useCallback(async (email) => {
    if (!email.includes('@')) return;
    
    setChecking((prev) => ({ ...prev, email: true }));
    try {
      const available = await checkEmailAvailable(email);
      setAvailability((prev) => ({ ...prev, email: available }));
    } finally {
      setChecking((prev) => ({ ...prev, email: false }));
    }
  }, []);

  return { availability, checking, checkUsername, checkEmail };
};
```

---

## CSS Styling Example

```css
.registration-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.registration-form h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.error {
  color: #d32f2f;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
  font-weight: 500;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
```

---

## Setup Checklist

- [ ] Backend running: `python manage.py runserver`
- [ ] API URL configured: `http://localhost:8000/api`
- [ ] CORS enabled in Django settings
- [ ] React app running on port 3000 (or configured port)
- [ ] Environment variables set (if needed)
- [ ] API service file created (`userService.js`)
- [ ] Registration form component created
- [ ] Form validation implemented
- [ ] Error handling in place
- [ ] Success redirect configured

---

## Common Issues & Solutions

### Issue: CORS Error
**Solution:** Enable CORS in Django settings:
```python
INSTALLED_APPS = ['corsheaders', ...]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
```

### Issue: 404 Not Found
**Solution:** Verify API URL is correct and Django server is running

### Issue: Password Validation Fails
**Solution:** Password must be minimum 8 characters and passwords must match

### Issue: Username Already Exists
**Solution:** Check availability before submitting or use real-time validation

---

## Testing Registration

1. Fill out the form with valid data
2. Verify username/email are checked before submission
3. Confirm success message appears
4. Check admin panel (`/admin`) to verify user was created
5. Verify user has no admin privileges (is_staff=False)

**You're ready to integrate!** 🚀
