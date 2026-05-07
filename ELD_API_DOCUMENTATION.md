# ELD (Electronic Logging Device) API Documentation

## Overview
This API provides endpoints for managing electronic logging of driver hours, trips, and vehicle logs for compliance with DOT regulations.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints require authentication. Include token in header:
```
Authorization: Token YOUR_AUTH_TOKEN
```

---

## 1. DRIVERS ENDPOINTS

### List All Drivers
```
GET /drivers/
```

### Create Driver
```
POST /drivers/
Content-Type: application/json

{
    "user": 1,
    "license_number": "DL123456",
    "license_state": "CA",
    "vehicle_number": "TRUCK-001",
    "company_name": "Your Trucking Co",
    "max_hours_per_day": 11,
    "max_hours_per_week": 60
}
```

### Get Driver Details
```
GET /drivers/{id}/
```

### Get Driver Trip History
```
GET /drivers/{id}/trip_history/
```
Returns: List of all trips for the driver ordered by most recent

### Get Driver Current Cycle Hours
```
GET /drivers/{id}/current_cycle/
```
Returns:
```json
{
    "total_driving_hours": 5.5,
    "total_on_duty_hours": 8.0,
    "hours_available_driving": 5.5,
    "hours_available_on_duty": 6.0
}
```

---

## 2. TRIPS ENDPOINTS

### List All Trips
```
GET /trips/
```

### Create New Trip
```
POST /trips/
Content-Type: application/json

{
    "driver": 1,
    "status": "planned",
    "current_location_lat": 40.7128,
    "current_location_lng": -74.0060,
    "current_location_name": "New York, NY",
    "pickup_location_lat": 40.7580,
    "pickup_location_lng": -73.9855,
    "pickup_location_name": "Times Square, NYC",
    "dropoff_location_lat": 34.0522,
    "dropoff_location_lng": -118.2437,
    "dropoff_location_name": "Los Angeles, CA",
    "current_cycle_used_hours": 3.5,
    "estimated_distance_miles": 2800,
    "estimated_end_datetime": "2026-05-10T15:30:00Z"
}
```

### Get Trip Details
```
GET /trips/{id}/
```

### Get Trip Route Information & Stops
```
GET /trips/{id}/route_info/
```
Returns:
```json
{
    "trip": { ...trip data... },
    "stops": [ ...list of stops... ],
    "total_distance_miles": 2800,
    "stop_count": 5
}
```

### Get Remaining Hours for Trip
```
GET /trips/{id}/remaining_hours/
```
Returns:
```json
{
    "hours_available_driving": 7.5,
    "hours_used_today": 3.5,
    "max_hours_allowed": 11
}
```

### Create Stops for Trip (Route Planning)
```
POST /trips/{id}/create_stops/
Content-Type: application/json

{
    "stops": [
        {
            "stop_type": "fuel",
            "location_name": "Shell Gas Station",
            "location_lat": 39.7392,
            "location_lng": -104.9903,
            "arrival_time": "2026-05-07T08:00:00Z",
            "notes": "Fuel up and rest"
        },
        {
            "stop_type": "rest",
            "location_name": "Rest Area, Ohio",
            "location_lat": 39.9500,
            "location_lng": -82.9988,
            "arrival_time": "2026-05-07T12:00:00Z",
            "duration_minutes": 60,
            "notes": "Mandatory 1-hour rest"
        }
    ]
}
```

### Complete Trip
```
POST /trips/{id}/complete_trip/
Content-Type: application/json

{
    "actual_distance_miles": 2805
}
```
Updates trip status to "completed" and records actual end time.

---

## 3. STOPS ENDPOINTS

### List Stops for a Trip
```
GET /stops/?trip_id=1
```

### Get Stop Details
```
GET /stops/{id}/
```

### Create Stop
```
POST /stops/
Content-Type: application/json

{
    "trip": 1,
    "stop_type": "rest",
    "location_name": "Rest Area, PA",
    "location_lat": 40.2206,
    "location_lng": -76.8719,
    "arrival_time": "2026-05-07T14:30:00Z",
    "departure_time": "2026-05-07T15:30:00Z",
    "duration_minutes": 60,
    "notes": "Mandatory rest break"
}
```

---

## 4. DAILY LOGS ENDPOINTS

### Get Today's Log (for Driver)
```
GET /daily-logs/today_log/?driver_id=1
```
Automatically creates log if it doesn't exist for today.

### Get Specific Daily Log
```
GET /daily-logs/{id}/
```

### Add Log Entry to Daily Log
```
POST /daily-logs/{id}/add_entry/
Content-Type: application/json

{
    "log_type": "D",  // Options: "OFF" (Off Duty), "SB" (Sleeper Berth), "D" (Driving), "ON" (On Duty)
    "duration_hours": 8.5,
    "location": "Los Angeles, CA",
    "odometer_start": 45000,
    "odometer_end": 45650,
    "notes": "Cross-country run"
}
```

### Update Daily Log Totals
```
POST /daily-logs/{id}/update_totals/
```
Recalculates all totals from log entries.

### Submit Daily Log
```
POST /daily-logs/{id}/submit/
```
Changes status from "draft" to "submitted".

### Certify Daily Log (Driver Signature)
```
POST /daily-logs/{id}/certify/
```
Changes status from "submitted" to "certified". This finalizes the log.

---

## 5. LOG ENTRIES ENDPOINTS

### List Entries for a Daily Log
```
GET /log-entries/?daily_log_id=1
```

### Get Log Entry Details
```
GET /log-entries/{id}/
```

### Create Log Entry
```
POST /log-entries/
Content-Type: application/json

{
    "daily_log": 1,
    "log_type": "D",
    "start_time": "2026-05-07T06:00:00Z",
    "end_time": "2026-05-07T14:30:00Z",
    "duration_hours": 8.5,
    "location": "Starting from Denver, CO",
    "odometer_start": 50000,
    "odometer_end": 50680,
    "notes": "Heavy traffic in morning"
}
```

### Update Log Entry
```
PATCH /log-entries/{id}/
Content-Type: application/json

{
    "notes": "Updated notes"
}
```

### Delete Log Entry
```
DELETE /log-entries/{id}/
```
Only if `is_editable` is true.

---

## LOG_TYPE Reference
```
'OFF' = Off Duty (Not on duty, not driving)
'SB'  = Sleeper Berth (In sleeper berth, not on duty)
'D'   = Driving (Operating vehicle)
'ON'  = On Duty (Not driving, performing duties)
```

---

## STOP_TYPE Reference
```
'pickup'      = Pickup location
'dropoff'     = Dropoff location
'fuel'        = Fuel stop
'rest'        = Rest/meal break
'sleeper'     = Sleeper berth location
'inspection'  = Vehicle inspection
'other'       = Other type of stop
```

---

## TRIP STATUS Reference
```
'planned'     = Trip is planned
'in_progress' = Trip is currently being driven
'completed'   = Trip has been completed
'cancelled'   = Trip was cancelled
```

---

## Common Workflow

### 1. Create a Driver (one-time setup)
```
POST /drivers/
```

### 2. Start a New Trip
```
POST /trips/
```

### 3. Plan Route with Stops
```
POST /trips/{trip_id}/create_stops/
```

### 4. Get Today's Log
```
GET /daily-logs/today_log/?driver_id={driver_id}
```

### 5. Add Log Entries Throughout the Day
```
POST /daily-logs/{log_id}/add_entry/
```

### 6. Check Remaining Hours
```
GET /trips/{trip_id}/remaining_hours/
```

### 7. Complete Trip
```
POST /trips/{trip_id}/complete_trip/
```

### 8. Submit and Certify Daily Log
```
POST /daily-logs/{log_id}/submit/
POST /daily-logs/{log_id}/certify/
```

---

## Sample Response: Complete Trip with Stops

```json
{
    "id": 1,
    "driver": 1,
    "driver_name": "John Doe",
    "status": "in_progress",
    "current_location_lat": 40.7128,
    "current_location_lng": -74.0060,
    "current_location_name": "New York, NY",
    "pickup_location_lat": 40.7580,
    "pickup_location_lng": -73.9855,
    "pickup_location_name": "Times Square, NYC",
    "dropoff_location_lat": 34.0522,
    "dropoff_location_lng": -118.2437,
    "dropoff_location_name": "Los Angeles, CA",
    "current_cycle_used_hours": 3.5,
    "start_datetime": "2026-05-07T05:00:00Z",
    "estimated_end_datetime": "2026-05-10T15:30:00Z",
    "actual_end_datetime": null,
    "estimated_distance_miles": 2800,
    "actual_distance_miles": null,
    "stops": [
        {
            "id": 1,
            "trip": 1,
            "stop_type": "fuel",
            "location_name": "Shell Gas Station, Denver",
            "location_lat": 39.7392,
            "location_lng": -104.9903,
            "arrival_time": "2026-05-07T08:00:00Z",
            "departure_time": "2026-05-07T08:30:00Z",
            "duration_minutes": 30,
            "notes": "Fuel up"
        },
        {
            "id": 2,
            "trip": 1,
            "stop_type": "rest",
            "location_name": "Rest Area, Kansas",
            "location_lat": 38.5266,
            "location_lng": -97.2469,
            "arrival_time": "2026-05-07T12:00:00Z",
            "departure_time": "2026-05-07T13:00:00Z",
            "duration_minutes": 60,
            "notes": "Mandatory 1-hour rest"
        }
    ],
    "created_at": "2026-05-07T05:00:00Z",
    "updated_at": "2026-05-07T12:00:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "driver_id required"
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Map Integration

For the React frontend, use free mapping APIs:
- **Leaflet** (free) - Excellent for interactive maps
- **OpenStreetMap** (free) - Tile provider for Leaflet
- **Google Maps** (free tier available) - More features
- **Mapbox** (free tier) - Modern, beautiful maps

The API returns latitude/longitude for all locations that can be plotted on any map provider.

---

## Pagination

All list endpoints support pagination:
```
GET /drivers/?page=1&limit=50
```

Default page size: 50 items

---

## Created By
Generated for ELD Compliance Application
