# React Frontend Integration Guide for ELD App

## Setup Instructions

### 1. Install Required Dependencies

```bash
npm install axios react-router-dom
npm install leaflet react-leaflet  # For mapping
npm install date-fns              # For date handling
npm install zustand              # State management (optional but recommended)
```

### 2. Configure API Client

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;
```

### 3. Create API Service Hooks

Create `src/hooks/useELD.js`:

```javascript
import { useState, useCallback } from 'react';
import api from '../services/api';

export const useDriver = () => {
  const [driver, setDriver] = useState(null);
  const [loading, setLoading] = useState(false);

  const getDriver = useCallback(async (driverId) => {
    setLoading(true);
    try {
      const response = await api.get(`/drivers/${driverId}/`);
      setDriver(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch driver:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const getCurrentCycle = useCallback(async (driverId) => {
    try {
      const response = await api.get(`/drivers/${driverId}/current_cycle/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch current cycle:', error);
      throw error;
    }
  }, []);

  return { driver, loading, getDriver, getCurrentCycle };
};

export const useTrip = () => {
  const [trip, setTrip] = useState(null);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(false);

  const createTrip = useCallback(async (tripData) => {
    setLoading(true);
    try {
      const response = await api.post('/trips/', tripData);
      setTrip(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to create trip:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const getTrip = useCallback(async (tripId) => {
    setLoading(true);
    try {
      const response = await api.get(`/trips/${tripId}/`);
      setTrip(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch trip:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const getRouteInfo = useCallback(async (tripId) => {
    try {
      const response = await api.get(`/trips/${tripId}/route_info/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch route info:', error);
      throw error;
    }
  }, []);

  const getRemainingHours = useCallback(async (tripId) => {
    try {
      const response = await api.get(`/trips/${tripId}/remaining_hours/`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch remaining hours:', error);
      throw error;
    }
  }, []);

  const createStops = useCallback(async (tripId, stops) => {
    try {
      const response = await api.post(`/trips/${tripId}/create_stops/`, { stops });
      setTrip(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to create stops:', error);
      throw error;
    }
  }, []);

  const completeTrip = useCallback(async (tripId, actualDistance) => {
    try {
      const response = await api.post(`/trips/${tripId}/complete_trip/`, {
        actual_distance_miles: actualDistance,
      });
      setTrip(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to complete trip:', error);
      throw error;
    }
  }, []);

  return {
    trip,
    trips,
    loading,
    createTrip,
    getTrip,
    getRouteInfo,
    getRemainingHours,
    createStops,
    completeTrip,
  };
};

export const useDailyLog = () => {
  const [log, setLog] = useState(null);
  const [loading, setLoading] = useState(false);

  const getTodayLog = useCallback(async (driverId) => {
    setLoading(true);
    try {
      const response = await api.get(`/daily-logs/today_log/?driver_id=${driverId}`);
      setLog(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch today log:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const addEntry = useCallback(async (logId, entryData) => {
    try {
      const response = await api.post(`/daily-logs/${logId}/add_entry/`, entryData);
      setLog(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to add log entry:', error);
      throw error;
    }
  }, []);

  const submitLog = useCallback(async (logId) => {
    try {
      const response = await api.post(`/daily-logs/${logId}/submit/`);
      setLog(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to submit log:', error);
      throw error;
    }
  }, []);

  const certifyLog = useCallback(async (logId) => {
    try {
      const response = await api.post(`/daily-logs/${logId}/certify/`);
      setLog(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to certify log:', error);
      throw error;
    }
  }, []);

  return {
    log,
    loading,
    getTodayLog,
    addEntry,
    submitLog,
    certifyLog,
  };
};
```

### 4. Create Map Component

Create `src/components/TripMap.jsx`:

```javascript
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export const TripMap = ({ trip, stops }) => {
  if (!trip) return <div>Loading map...</div>;

  const currentLocation = [trip.current_location_lat, trip.current_location_lng];
  const pickupLocation = [trip.pickup_location_lat, trip.pickup_location_lng];
  const dropoffLocation = [trip.dropoff_location_lat, trip.dropoff_location_lng];

  // Create route line through stops
  const routePath = [
    currentLocation,
    ...stops.map(stop => [stop.location_lat, stop.location_lng]),
    dropoffLocation
  ];

  return (
    <MapContainer center={currentLocation} zoom={5} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      
      {/* Route line */}
      <Polyline positions={routePath} color="blue" weight={2} />

      {/* Current Location */}
      <Marker position={currentLocation}>
        <Popup>
          <strong>Current Location</strong><br />
          {trip.current_location_name}
        </Popup>
      </Marker>

      {/* Pickup Location */}
      <Marker position={pickupLocation}>
        <Popup>
          <strong>Pickup</strong><br />
          {trip.pickup_location_name}
        </Popup>
      </Marker>

      {/* Stops */}
      {stops.map((stop, idx) => (
        <Marker key={stop.id} position={[stop.location_lat, stop.location_lng]}>
          <Popup>
            <strong>{stop.stop_type.toUpperCase()}</strong><br />
            {stop.location_name}<br />
            {stop.duration_minutes && `${stop.duration_minutes} min`}
          </Popup>
        </Marker>
      ))}

      {/* Dropoff Location */}
      <Marker position={dropoffLocation}>
        <Popup>
          <strong>Dropoff</strong><br />
          {trip.dropoff_location_name}
        </Popup>
      </Marker>
    </MapContainer>
  );
};
```

### 5. Create Daily Log Sheet Component

Create `src/components/DailyLogSheet.jsx`:

```javascript
import React, { useEffect, useState } from 'react';
import { format } from 'date-fns';
import { useDailyLog } from '../hooks/useELD';

export const DailyLogSheet = ({ driverId }) => {
  const { log, getTodayLog, addEntry } = useDailyLog();
  const [newEntry, setNewEntry] = useState({
    log_type: 'D',
    duration_hours: 0,
    location: '',
    notes: '',
  });

  useEffect(() => {
    getTodayLog(driverId);
  }, [driverId, getTodayLog]);

  const handleAddEntry = async (e) => {
    e.preventDefault();
    await addEntry(log.id, newEntry);
    setNewEntry({ log_type: 'D', duration_hours: 0, location: '', notes: '' });
  };

  if (!log) return <div>Loading log sheet...</div>;

  const logTypes = {
    OFF: 'Off Duty',
    SB: 'Sleeper Berth',
    D: 'Driving',
    ON: 'On Duty',
  };

  return (
    <div className="log-sheet">
      <h2>Daily Log Sheet - {format(new Date(log.log_date), 'MMMM dd, yyyy')}</h2>

      <div className="hours-summary">
        <div className="hour-box">
          <label>Driving Hours</label>
          <div className="hour-value">{log.total_driving_hours.toFixed(1)}h</div>
          <div className="hour-available">Available: {log.hours_available_driving.toFixed(1)}h</div>
        </div>
        <div className="hour-box">
          <label>On Duty Hours</label>
          <div className="hour-value">{log.total_on_duty_hours.toFixed(1)}h</div>
        </div>
        <div className="hour-box">
          <label>Off Duty Hours</label>
          <div className="hour-value">{log.total_off_duty_hours.toFixed(1)}h</div>
        </div>
        <div className="hour-box">
          <label>Sleeper Berth</label>
          <div className="hour-value">{log.total_sleeper_berth_hours.toFixed(1)}h</div>
        </div>
      </div>

      <form onSubmit={handleAddEntry} className="add-entry-form">
        <h3>Add Log Entry</h3>
        <select
          value={newEntry.log_type}
          onChange={(e) => setNewEntry({ ...newEntry, log_type: e.target.value })}
        >
          {Object.entries(logTypes).map(([key, label]) => (
            <option key={key} value={key}>{label}</option>
          ))}
        </select>

        <input
          type="number"
          step="0.5"
          min="0"
          max="24"
          placeholder="Duration (hours)"
          value={newEntry.duration_hours}
          onChange={(e) => setNewEntry({ ...newEntry, duration_hours: parseFloat(e.target.value) })}
          required
        />

        <input
          type="text"
          placeholder="Location"
          value={newEntry.location}
          onChange={(e) => setNewEntry({ ...newEntry, location: e.target.value })}
        />

        <input
          type="text"
          placeholder="Notes"
          value={newEntry.notes}
          onChange={(e) => setNewEntry({ ...newEntry, notes: e.target.value })}
        />

        <button type="submit">Add Entry</button>
      </form>

      <table className="entries-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Type</th>
            <th>Location</th>
            <th>Duration</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {log.entries && log.entries.map((entry) => (
            <tr key={entry.id}>
              <td>{format(new Date(entry.start_time), 'HH:mm')}</td>
              <td>{logTypes[entry.log_type]}</td>
              <td>{entry.location}</td>
              <td>{entry.duration_hours.toFixed(1)}h</td>
              <td>{entry.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="log-status">
        <p>Status: <strong>{log.status.toUpperCase()}</strong></p>
      </div>
    </div>
  );
};
```

### 6. Create Trip Planning Component

Create `src/components/TripPlanner.jsx`:

```javascript
import React, { useState } from 'react';
import { useTrip } from '../hooks/useELD';

export const TripPlanner = ({ driverId }) => {
  const { createTrip, createStops } = useTrip();
  const [tripData, setTripData] = useState({
    driver: driverId,
    current_location_lat: 40.7128,
    current_location_lng: -74.0060,
    current_location_name: 'New York, NY',
    pickup_location_lat: 0,
    pickup_location_lng: 0,
    pickup_location_name: '',
    dropoff_location_lat: 0,
    dropoff_location_lng: 0,
    dropoff_location_name: '',
    current_cycle_used_hours: 0,
  });

  const handleCreateTrip = async (e) => {
    e.preventDefault();
    const trip = await createTrip(tripData);
    console.log('Trip created:', trip);
    // Redirect or show success message
  };

  return (
    <form onSubmit={handleCreateTrip} className="trip-planner">
      <h2>Plan New Trip</h2>

      <label>Pickup Location</label>
      <input
        type="text"
        placeholder="City, State"
        value={tripData.pickup_location_name}
        onChange={(e) => setTripData({ ...tripData, pickup_location_name: e.target.value })}
        required
      />

      <label>Dropoff Location</label>
      <input
        type="text"
        placeholder="City, State"
        value={tripData.dropoff_location_name}
        onChange={(e) => setTripData({ ...tripData, dropoff_location_name: e.target.value })}
        required
      />

      <label>Current Cycle Hours Used</label>
      <input
        type="number"
        step="0.5"
        min="0"
        max="24"
        value={tripData.current_cycle_used_hours}
        onChange={(e) => setTripData({ ...tripData, current_cycle_used_hours: parseFloat(e.target.value) })}
      />

      <button type="submit">Create Trip</button>
    </form>
  );
};
```

### 7. Create Main Trip App Component

Create `src/App.jsx`:

```javascript
import React, { useState, useEffect } from 'react';
import { useTrip, useDailyLog } from './hooks/useELD';
import { TripMap } from './components/TripMap';
import { DailyLogSheet } from './components/DailyLogSheet';
import { TripPlanner } from './components/TripPlanner';

function App() {
  const [driverId] = useState(1); // Get from auth context
  const { trip, getTrip, getRouteInfo } = useTrip();
  const { log, getTodayLog } = useDailyLog();
  const [routeInfo, setRouteInfo] = useState(null);
  const [currentView, setCurrentView] = useState('plan'); // 'plan', 'map', 'log'

  useEffect(() => {
    // Load initial data
    getTodayLog(driverId);
  }, [driverId, getTodayLog]);

  useEffect(() => {
    if (trip) {
      getRouteInfo(trip.id).then(setRouteInfo);
    }
  }, [trip, getRouteInfo]);

  return (
    <div className="app">
      <header>
        <h1>ELD - Electronic Logging Device</h1>
        <nav>
          <button 
            className={currentView === 'plan' ? 'active' : ''} 
            onClick={() => setCurrentView('plan')}
          >
            Plan Trip
          </button>
          <button 
            className={currentView === 'map' ? 'active' : ''} 
            onClick={() => setCurrentView('map')}
          >
            Map & Route
          </button>
          <button 
            className={currentView === 'log' ? 'active' : ''} 
            onClick={() => setCurrentView('log')}
          >
            Daily Log
          </button>
        </nav>
      </header>

      <main>
        {currentView === 'plan' && <TripPlanner driverId={driverId} />}
        {currentView === 'map' && trip && routeInfo && (
          <TripMap trip={trip} stops={routeInfo.stops} />
        )}
        {currentView === 'log' && <DailyLogSheet driverId={driverId} />}
      </main>
    </div>
  );
}

export default App;
```

### 8. CSS Styling

Create `src/styles/app.css`:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  background-color: #f5f5f5;
}

.app {
  min-height: 100vh;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

header h1 {
  margin-bottom: 15px;
}

header nav {
  display: flex;
  gap: 10px;
}

header button {
  background-color: #34495e;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

header button:hover {
  background-color: #1a252f;
}

header button.active {
  background-color: #e74c3c;
}

main {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.hours-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.hour-box {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.hour-box label {
  display: block;
  color: #7f8c8d;
  font-weight: 600;
  margin-bottom: 10px;
}

.hour-value {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 5px;
}

.hour-available {
  font-size: 12px;
  color: #27ae60;
}

.add-entry-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-entry-form h3 {
  margin-bottom: 15px;
}

.add-entry-form select,
.add-entry-form input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 14px;
}

.add-entry-form button {
  width: 100%;
  padding: 12px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

.add-entry-form button:hover {
  background-color: #229954;
}

.entries-table {
  width: 100%;
  background: white;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.entries-table th {
  background-color: #34495e;
  color: white;
  padding: 12px;
  text-align: left;
  font-weight: 600;
}

.entries-table td {
  padding: 12px;
  border-bottom: 1px solid #ecf0f1;
}

.entries-table tr:hover {
  background-color: #f8f9fa;
}

.log-status {
  margin-top: 20px;
  padding: 15px;
  background-color: #ecf0f1;
  border-radius: 4px;
  text-align: center;
}

.trip-planner {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.trip-planner h2 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.trip-planner label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #2c3e50;
}

.trip-planner input,
.trip-planner select {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 14px;
}

.trip-planner button {
  width: 100%;
  padding: 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
}

.trip-planner button:hover {
  background-color: #2980b9;
}
```

## Environment Variables

Create `.env`:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Running the Application

1. Start Django backend:
```bash
python manage.py runserver
```

2. Start React frontend:
```bash
npm start
```

3. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

4. Access admin dashboard:
```
http://localhost:8000/admin/
```

## Features Implemented

✅ Trip planning with location inputs
✅ Route display on interactive map
✅ Real-time stop management
✅ Daily ELD log sheets
✅ Automatic hour tracking and compliance
✅ Log entry management (Driving, On-duty, Off-duty, Sleeper berth)
✅ Trip completion tracking
✅ Hours remaining calculations

## Next Steps

1. Add map integration with geocoding (Google Maps API or Nominatim)
2. Add route optimization
3. Add geofencing for automatic stop detection
4. Add offline mode with sync when online
5. Add digital signature capture for log certification
6. Add analytics dashboard
7. Add export to PDF for reports
8. Add mobile app version
