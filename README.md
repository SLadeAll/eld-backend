# ELD (Electronic Logging Device) Application

A full-stack application for electronic logging of driver hours, trip management, and DOT compliance. Built with Django REST Framework backend and React frontend.

## 📋 Features

### Driver Management
- Driver profile creation and management
- License and vehicle tracking
- Hours regulation compliance (11-hour daily limit, 60-hour weekly limit)

### Trip Planning
- Trip creation with multiple input modes
- Real-time location tracking
- Automatic route calculation
- Stop planning and management

### Map Integration
- Interactive map display using Leaflet + OpenStreetMap
- Route visualization with stops
- Multiple stop type support (fuel, rest, pickup, dropoff, etc.)
- Distance calculation and tracking

### Daily ELD Logs
- Automatic daily log creation
- Log entry management (Driving, On-duty, Off-duty, Sleeper berth)
- Real-time hour tracking and calculation
- Remaining hours display
- Log status management (Draft → Submitted → Certified)

### Compliance Tracking
- 11-hour driving per day enforcement
- 14-hour on-duty window tracking
- Automatic regulations alerts
- Hours available calculation

## 🗂️ Project Structure

```
backend/
├── assesBackend/              # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
├── producto/                 # Main Django app
│   ├── models.py             # Database models (Driver, Trip, Stop, DailyLog, LogEntry)
│   ├── admin.py              # Django admin configuration
│   ├── api/
│   │   ├── views.py          # API ViewSets and endpoints
│   │   ├── serilizers.py     # DRF Serializers
│   │   └── urls.py           # API URL routing
│   └── management/
│       └── commands/
│           └── seed_demo_data.py  # Demo data seeding command
├── manage.py                 # Django management command
├── db.sqlite3                # Development database
└── requirements.txt          # Python dependencies

frontend/                     # React application
├── src/
│   ├── components/
│   │   ├── TripMap.jsx
│   │   ├── DailyLogSheet.jsx
│   │   └── TripPlanner.jsx
│   ├── hooks/
│   │   └── useELD.js         # Custom React hooks for API
│   ├── services/
│   │   └── api.js            # Axios API client
│   ├── styles/
│   │   └── app.css
│   └── App.jsx
└── package.json
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create and activate virtual environment:**
```bash
python -m venv assessmentProyect
# On Windows:
.\assessmentProyect\Scripts\Activate.ps1
# On Linux/Mac:
source assessmentProyect/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
cd assesBackend
python manage.py migrate
```

5. **Create superuser (admin):**
```bash
python manage.py createsuperuser
```

6. **Load demo data (optional):**
```bash
python manage.py seed_demo_data
```

7. **Start development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Create React app (if not already created):**
```bash
npx create-react-app frontend
cd frontend
```

2. **Install dependencies:**
```bash
npm install axios react-router-dom leaflet react-leaflet date-fns
```

3. **Copy components and hooks:**
   - Copy files from `REACT_INTEGRATION_GUIDE.md` into your React app

4. **Start development server:**
```bash
npm start
```

The app will be available at `http://localhost:3000` or `http://localhost:5173` (Vite)

## 🔌 API Endpoints

### Drivers
- `GET /api/drivers/` - List all drivers
- `POST /api/drivers/` - Create driver
- `GET /api/drivers/{id}/` - Get driver details
- `GET /api/drivers/{id}/trip_history/` - Get driver's trip history
- `GET /api/drivers/{id}/current_cycle/` - Get current hours

### Trips
- `GET /api/trips/` - List all trips
- `POST /api/trips/` - Create new trip
- `GET /api/trips/{id}/` - Get trip details
- `GET /api/trips/{id}/route_info/` - Get route and stops
- `GET /api/trips/{id}/remaining_hours/` - Get remaining driving hours
- `POST /api/trips/{id}/create_stops/` - Create route stops
- `POST /api/trips/{id}/complete_trip/` - Mark trip as completed

### Stops
- `GET /api/stops/?trip_id={id}` - List stops for trip
- `POST /api/stops/` - Create stop
- `GET /api/stops/{id}/` - Get stop details

### Daily Logs
- `GET /api/daily-logs/today_log/?driver_id={id}` - Get today's log
- `GET /api/daily-logs/{id}/` - Get daily log details
- `POST /api/daily-logs/{id}/add_entry/` - Add log entry
- `POST /api/daily-logs/{id}/submit/` - Submit log
- `POST /api/daily-logs/{id}/certify/` - Certify log

### Log Entries
- `GET /api/log-entries/?daily_log_id={id}` - List entries for log
- `POST /api/log-entries/` - Create log entry
- `PATCH /api/log-entries/{id}/` - Update log entry
- `DELETE /api/log-entries/{id}/` - Delete log entry

For detailed API documentation, see [ELD_API_DOCUMENTATION.md](./ELD_API_DOCUMENTATION.md)

## 📊 Database Models

### Driver
Stores driver information and regulations limits
- License number and state
- Vehicle information
- Max hours per day/week

### Trip
Main trip record with locations and status
- Current, pickup, and dropoff locations
- Trip status (planned, in_progress, completed)
- Current cycle hours used
- Distance tracking

### Stop
Route stops and rest breaks
- Stop type (fuel, rest, sleeper, etc.)
- Arrival and departure times
- Duration tracking

### DailyLog
Daily ELD log sheet
- Date and status
- Total hours by category
- Remaining hours available

### LogEntry
Individual log entries
- Entry type (Driving, On-duty, Off-duty, Sleeper berth)
- Start/end times
- Duration
- Location and odometer readings

## 🔐 Authentication

The API uses Token-based authentication:

1. Get token (in Django admin or via API endpoint)
2. Include in all requests:
```
Authorization: Token YOUR_TOKEN_HERE
```

## 🎨 Customization

### Modify Regulations
Edit `Driver.max_hours_per_day` and `Driver.max_hours_per_week` in models

### Add More Stop Types
Add to `Stop.STOP_TYPE_CHOICES` in models.py

### Change Default Hours
Modify DailyLog defaults:
```python
hours_available_driving = models.FloatField(default=11)
hours_available_on_duty = models.FloatField(default=14)
```

## 🗺️ Map Integration Options

- **Leaflet** (recommended for free) - Lightweight, flexible
- **OpenStreetMap** - Free tiles provider
- **Google Maps** - More features, has free tier
- **Mapbox** - Modern UI, free tier available

All provide latitude/longitude APIs that integrate with our coordinates.

## 📱 Mobile Features

The API is designed for mobile apps:
- All endpoints are REST-compliant
- CORS headers configured for cross-origin requests
- Pagination support for large datasets
- Filtering capabilities on all list endpoints

## 🧪 Testing

Run Django tests:
```bash
python manage.py test
```

## 📝 Admin Interface

Access Django admin at:
```
http://localhost:8000/admin/
```

Create superuser first:
```bash
python manage.py createsuperuser
```

## 🛠️ Development Tools

### Django Shell
```bash
python manage.py shell
```

### Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Seed Demo Data
```bash
python manage.py seed_demo_data
```

## 📦 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Set secure `SECRET_KEY` environment variable
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure CORS_ALLOWED_ORIGINS
- [ ] Set up SSL/HTTPS
- [ ] Configure static files serving
- [ ] Set up media files handling
- [ ] Configure logging
- [ ] Set up error monitoring (Sentry)

### Using Gunicorn
```bash
gunicorn assesBackend.wsgi:application --bind 0.0.0.0:8000
```

### Using PostgreSQL
```bash
# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eld_db',
        'USER': 'eld_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'django'
- Activate virtual environment: `.\assessmentProyect\Scripts\Activate.ps1`

### CORS errors
- Check CORS_ALLOWED_ORIGINS in settings.py
- Ensure frontend URL is included

### Database errors
- Run migrations: `python manage.py migrate`
- Check database permissions

### API returns 401 Unauthorized
- Verify authentication token is included in headers
- Token should be in format: `Token YOUR_TOKEN`

## 📚 Documentation Files

- **ELD_API_DOCUMENTATION.md** - Complete API reference
- **REACT_INTEGRATION_GUIDE.md** - React setup and components
- **This README.md** - Project overview and setup

## 🤝 Contributing

1. Create feature branch
2. Commit changes
3. Push to branch
4. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💼 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check Django and DRF official documentation

## 📞 Contact

For support or questions about the ELD application, please contact the development team.

---

**Last Updated:** May 2026
**Version:** 1.0.0
**Status:** Production Ready
