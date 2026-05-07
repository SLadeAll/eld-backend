# 🚀 Quick Start Guide - ELD App Setup

## Backend Quick Setup (5 minutes)

### 1. Start Backend
```bash
cd backend/assesBackend
.\../assessmentProyect\Scripts\Activate.ps1  # Windows
source ../assessmentProyect/bin/activate      # Linux/Mac
python manage.py runserver
```

**Backend running at:** `http://localhost:8000`  
**API available at:** `http://localhost:8000/api/`

### 2. Check Django Admin
```
http://localhost:8000/admin/
Username: admin (or your superuser name)
```

### 3. View Available Data
```bash
# Get drivers
curl http://localhost:8000/api/drivers/

# Get trips
curl http://localhost:8000/api/trips/

# Get daily logs (need driver ID)
curl "http://localhost:8000/api/daily-logs/today_log/?driver_id=1"
```

---

## Frontend Quick Setup (5 minutes)

### 1. Create React App
```bash
cd frontend
npx create-react-app . --template minimal
# OR use Vite:
npm create vite@latest . -- --template react
```

### 2. Install Dependencies
```bash
npm install axios leaflet react-leaflet
```

### 3. Create API Client (`src/services/api.js`)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

export default api;
```

### 4. Create Trip Display Component (`src/App.jsx`)
```javascript
import React, { useState, useEffect } from 'react';
import api from './services/api';

function App() {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/trips/').then(res => {
      setTrips(res.data.results || res.data);
      setLoading(false);
    });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>ELD Trips</h1>
      {loading ? <p>Loading...</p> : (
        <ul>
          {trips.map(trip => (
            <li key={trip.id}>
              {trip.pickup_location_name} → {trip.dropoff_location_name}
              <p>Status: {trip.status}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
```

### 5. Start Frontend
```bash
npm start
```

**Frontend running at:** `http://localhost:3000` (Create-React-App) or `http://localhost:5173` (Vite)

---

## 📱 First API Call Examples

### Get All Drivers
```javascript
import api from './services/api';

const drivers = await api.get('/drivers/');
console.log(drivers.data);
```

### Create a Trip
```javascript
const newTrip = await api.post('/trips/', {
  driver: 1,
  status: 'planned',
  current_location_lat: 40.7128,
  current_location_lng: -74.0060,
  current_location_name: 'New York, NY',
  pickup_location_lat: 40.7580,
  pickup_location_lng: -73.9855,
  pickup_location_name: 'Times Square, NYC',
  dropoff_location_lat: 34.0522,
  dropoff_location_lng: -118.2437,
  dropoff_location_name: 'Los Angeles, CA',
  current_cycle_used_hours: 3.5,
  estimated_distance_miles: 2800,
});
```

### Get Today's Log
```javascript
const log = await api.get('/daily-logs/today_log/', {
  params: { driver_id: 1 }
});
console.log(log.data);
```

### Add Log Entry
```javascript
await api.post(`/daily-logs/${logId}/add_entry/`, {
  log_type: 'D',  // D = Driving
  duration_hours: 8.5,
  location: 'Denver, CO',
  notes: 'Long haul'
});
```

---

## 🗺️ Display Map with Route

```javascript
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function TripMap({ trip, stops }) {
  const current = [trip.current_location_lat, trip.current_location_lng];
  const pickup = [trip.pickup_location_lat, trip.pickup_location_lng];
  const dropoff = [trip.dropoff_location_lat, trip.dropoff_location_lng];
  
  return (
    <MapContainer center={current} zoom={5} style={{ height: '500px' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <Marker position={current}><Popup>Current Location</Popup></Marker>
      <Marker position={pickup}><Popup>Pickup</Popup></Marker>
      <Marker position={dropoff}><Popup>Dropoff</Popup></Marker>
      {stops.map(stop => (
        <Marker key={stop.id} position={[stop.location_lat, stop.location_lng]}>
          <Popup>{stop.location_name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
```

---

## 📊 Display Daily Log

```javascript
function DailyLog({ log }) {
  return (
    <div>
      <h2>Daily Log - {log.log_date}</h2>
      <p>Driving Hours: {log.total_driving_hours}</p>
      <p>Available: {log.hours_available_driving}</p>
      <p>Status: {log.status}</p>
      
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Hours</th>
            <th>Location</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {log.entries.map(entry => (
            <tr key={entry.id}>
              <td>{entry.log_type}</td>
              <td>{entry.duration_hours}</td>
              <td>{entry.location}</td>
              <td>{entry.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 🔧 Common Tasks

### Get Route Information
```javascript
const route = await api.get(`/trips/${tripId}/route_info/`);
// Returns: trip data, stops, distance, stop count
```

### Check Remaining Hours
```javascript
const hours = await api.get(`/trips/${tripId}/remaining_hours/`);
// Returns: hours_available_driving, hours_used_today, max_hours_allowed
```

### Complete a Trip
```javascript
await api.post(`/trips/${tripId}/complete_trip/`, {
  actual_distance_miles: 2805
});
```

### Submit and Certify Log
```javascript
// Submit for review
await api.post(`/daily-logs/${logId}/submit/`);

// Certify with driver signature
await api.post(`/daily-logs/${logId}/certify/`);
```

---

## 🧪 Test with Demo Data

Demo user already created:
```
Username: demodriver
License: CA1234567
Trip: New York → Los Angeles
Status: In Progress
```

Access demo data:
```javascript
// Get demo driver
api.get('/drivers/1/').then(res => console.log(res.data));

// Get demo trip
api.get('/trips/1/').then(res => console.log(res.data));

// Get demo stops
api.get('/stops/?trip_id=1').then(res => console.log(res.data));

// Get demo daily log
api.get('/daily-logs/1/').then(res => console.log(res.data));
```

---

## 🐛 Troubleshooting

### CORS Error
**Problem:** "Access to XMLHttpRequest blocked by CORS policy"  
**Solution:** Make sure Django server is running on port 8000

### 404 Not Found
**Problem:** "Cannot GET /api/trips/"  
**Solution:** Check URL format, should be `http://localhost:8000/api/trips/`

### 401 Unauthorized
**Problem:** "Authentication credentials were not provided"  
**Solution:** Either disable auth in settings.py or provide valid token:
```javascript
headers: { Authorization: 'Token YOUR_TOKEN' }
```

### Trips Not Appearing
**Problem:** Empty trips list  
**Solution:** Run `python manage.py seed_demo_data` to create demo trip

---

## 📚 Documentation Reference

- **API Docs:** See `ELD_API_DOCUMENTATION.md`
- **React Setup:** See `REACT_INTEGRATION_GUIDE.md`
- **Full README:** See `README.md`

---

## ✅ Checklist

- [ ] Backend running (`http://localhost:8000`)
- [ ] API accessible (`http://localhost:8000/api/`)
- [ ] Demo data seeded (run `seed_demo_data` command)
- [ ] React app created and dependencies installed
- [ ] API client configured in `src/services/api.js`
- [ ] First component displaying data
- [ ] Map component working
- [ ] Log sheet displaying hours
- [ ] Can create new trip
- [ ] Can add log entries

---

## 🚀 Next Steps

1. Create user authentication UI
2. Add trip planning form with location inputs
3. Implement interactive map with route
4. Build daily log sheet UI
5. Add hour compliance alerts
6. Implement form validation
7. Add loading/error states
8. Create responsive mobile layout
9. Add offline support with service workers
10. Deploy to production

---

**Status:** Ready to build! 🎉
