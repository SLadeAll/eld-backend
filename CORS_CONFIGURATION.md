# CORS Configuration - Registration API

## ✅ CORS is now enabled and configured

### Allowed Origins
Your React frontend can request from any of these addresses:

- `http://localhost:3000` (default React dev server)
- `http://localhost:5174` (Vite dev server)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5174`
- `http://localhost:8000` (same server for testing)
- `http://127.0.0.1:8000`
- `https://assessment-front-end-neon.vercel.app` (production frontend)
- `https://assessment-front-end-*.vercel.app` (all Vercel preview deployments)

---

## Configuration Details

### CORS Settings (settings.py)

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://assessment-front-end-neon.vercel.app",
]

# Matches all Vercel preview deployments automatically
CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://assessment-front-end.*\.vercel\.app$',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
]
```

### REST Framework Default Permissions

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
```

---

## What This Means

✅ **Registration endpoint is publicly accessible**
- No authentication required to register
- CORS headers are sent with responses
- React frontend can make POST requests

✅ **Credentials are supported**
- Cookies and credentials can be sent
- Sessions work across origins

✅ **Required headers are allowed**
- Content-Type: application/json
- Authorization headers for future authentication
- CSRF tokens for security

---

## Testing CORS from React

### Test Registration Request
```javascript
const response = await fetch('http://localhost:8000/api/auth/register/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    password: 'testpass123',
    password_confirm: 'testpass123',
  }),
});
```

### Check CORS Response Headers
If CORS is working, you should see these headers in the response:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: content-type, authorization, ...
```

---

## Troubleshooting

### Issue: CORS Error in Browser Console
**Solution:** Verify your React app is running on one of the allowed origins

### Issue: Preflight Request (OPTIONS) Fails
**Solution:** Django automatically handles OPTIONS requests with CORS headers

### Issue: Still Getting CORS Error
1. Clear browser cache
2. Check Network tab in DevTools for CORS headers
3. Verify React app URL matches allowed origins exactly
4. Restart Django development server

---

## Adding More Origins (For Production)

To add more allowed origins, edit `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",        # Add production domain
    "https://assessment-front-end-neon.vercel.app",  # No trailing slash
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r'^https://assessment-front-end.*\.vercel\.app$',  # All preview deployments
]
```

Then restart the Django server:
```bash
python manage.py runserver
```

---

## Security Notes

- In production, list specific domains only
- Never use wildcard (`*`) for `CORS_ALLOWED_ORIGINS` in production
- `CORS_ALLOW_CREDENTIALS = True` requires explicit origin (not wildcard)
- Always use HTTPS in production

---

## Ready to Use!

Your registration API is now fully CORS-enabled and ready for React frontend integration.

Start your servers:
1. **Backend:** `python manage.py runserver` (runs on `http://localhost:8000`)
2. **React:** `npm start` or `npm run dev` (runs on port 3000 or 5174)

Then make requests to:
```
http://localhost:8000/api/auth/register/register/
```
