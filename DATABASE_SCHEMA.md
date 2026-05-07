# ELD Database Schema

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌──────────────┐                                                       │
│  │    Driver    │                                                       │
│  ├──────────────┤                                                       │
│  │ id (PK)      │                                                       │
│  │ user_id (FK) │──────┐                                                │
│  │ license_num  │      │                                                │
│  │ vehicle_num  │      │                                                │
│  │ max_hours    │      │                                                │
│  └──────────────┘      │                                                │
│        │               │                                                │
│        │ (1:M)         └─────┐                                          │
│        │                     │                                          │
│        │                ┌────┴────────────────┐                        │
│        │                │ User (Django)       │                        │
│        │                ├─────────────────────┤                        │
│        │                │ id (PK)             │                        │
│        │                │ username            │                        │
│        │                │ email               │                        │
│        │                │ password            │                        │
│        │                └─────────────────────┘                        │
│        │                                                                │
│        └─────────────────────┬────────────────────┐                   │
│                              │ (1:M)              │ (1:M)              │
│                              ▼                    ▼                     │
│                        ┌──────────────┐   ┌──────────────────┐         │
│                        │    Trip      │   │   DailyLog       │         │
│                        ├──────────────┤   ├──────────────────┤         │
│                        │ id (PK)      │   │ id (PK)          │         │
│                        │ driver_id (FK)   │ driver_id (FK)   │         │
│                        │ status       │   │ trip_id (FK)     │         │
│                        │ current_loc  │   │ log_date         │         │
│                        │ pickup_loc   │   │ total_hours      │         │
│                        │ dropoff_loc  │   │ hours_available  │         │
│                        │ cycle_hours  │   │ status           │         │
│                        │ distance     │   └──────────────────┘         │
│                        └──────────────┘          │                     │
│                              │                  │ (1:M)               │
│                              │ (1:M)            │                     │
│                              ▼                  ▼                     │
│                        ┌──────────────┐   ┌──────────────────┐        │
│                        │    Stop      │   │   LogEntry       │        │
│                        ├──────────────┤   ├──────────────────┤        │
│                        │ id (PK)      │   │ id (PK)          │        │
│                        │ trip_id (FK) │   │ daily_log_id (FK)│        │
│                        │ stop_type    │   │ log_type         │        │
│                        │ location     │   │ start_time       │        │
│                        │ arrival_time │   │ end_time         │        │
│                        │ departure_tm │   │ duration_hours   │        │
│                        │ duration_min │   │ location         │        │
│                        │ notes        │   │ odometer_start   │        │
│                        └──────────────┘   │ odometer_end     │        │
│                                           │ notes            │        │
│                                           │ is_editable      │        │
│                                           └──────────────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Table Definitions

### Driver
```sql
CREATE TABLE product_driver (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL REFERENCES auth_user(id),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_state VARCHAR(2) NOT NULL,
    vehicle_number VARCHAR(20) NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    max_hours_per_day INTEGER DEFAULT 11,
    max_hours_per_week INTEGER DEFAULT 60,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW
);
```

### Trip
```sql
CREATE TABLE producto_trip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL REFERENCES producto_driver(id),
    status VARCHAR(20) DEFAULT 'planned',
    -- Locations (latitude/longitude for mapping)
    current_location_lat FLOAT NOT NULL,
    current_location_lng FLOAT NOT NULL,
    current_location_name VARCHAR(255),
    pickup_location_lat FLOAT NOT NULL,
    pickup_location_lng FLOAT NOT NULL,
    pickup_location_name VARCHAR(255) NOT NULL,
    dropoff_location_lat FLOAT NOT NULL,
    dropoff_location_lng FLOAT NOT NULL,
    dropoff_location_name VARCHAR(255) NOT NULL,
    -- Hours
    current_cycle_used_hours FLOAT NOT NULL,
    -- Timing
    start_datetime DATETIME AUTO_NOW_ADD,
    estimated_end_datetime DATETIME,
    actual_end_datetime DATETIME,
    -- Distance
    estimated_distance_miles FLOAT,
    actual_distance_miles FLOAT,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW,
    INDEX (driver_id),
    INDEX (status)
);
```

### Stop
```sql
CREATE TABLE producto_stop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL REFERENCES producto_trip(id),
    stop_type VARCHAR(20) NOT NULL,  -- fuel, rest, pickup, dropoff, sleeper, etc.
    location_name VARCHAR(255) NOT NULL,
    location_lat FLOAT NOT NULL,
    location_lng FLOAT NOT NULL,
    arrival_time DATETIME NOT NULL,
    departure_time DATETIME,
    duration_minutes INTEGER,
    notes TEXT,
    created_at DATETIME AUTO_NOW_ADD,
    INDEX (trip_id),
    INDEX (arrival_time)
);
```

### DailyLog
```sql
CREATE TABLE producto_dailylog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL REFERENCES producto_driver(id),
    trip_id INTEGER REFERENCES producto_trip(id),
    log_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, submitted, certified
    -- Hour tracking
    total_driving_hours FLOAT DEFAULT 0,
    total_on_duty_hours FLOAT DEFAULT 0,
    total_off_duty_hours FLOAT DEFAULT 0,
    total_sleeper_berth_hours FLOAT DEFAULT 0,
    -- Compliance tracking
    hours_available_driving FLOAT DEFAULT 11,
    hours_available_on_duty FLOAT DEFAULT 14,
    -- Vehicle data
    vehicle_odometer_start INTEGER,
    vehicle_odometer_end INTEGER,
    notes TEXT,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW,
    UNIQUE(driver_id, log_date),
    INDEX (driver_id),
    INDEX (log_date)
);
```

### LogEntry
```sql
CREATE TABLE producto_logentry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daily_log_id INTEGER NOT NULL REFERENCES producto_dailylog(id),
    log_type VARCHAR(3) NOT NULL,  -- OFF, SB, D, ON
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    duration_hours FLOAT NOT NULL,
    location VARCHAR(255),
    odometer_start INTEGER,
    odometer_end INTEGER,
    notes TEXT,
    is_editable BOOLEAN DEFAULT TRUE,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW,
    INDEX (daily_log_id),
    INDEX (log_type),
    INDEX (start_time)
);
```

## Key Relationships

### One-to-Many (1:M)
1. **User → Driver** - One user has one driver profile
2. **Driver → Trip** - One driver has many trips
3. **Driver → DailyLog** - One driver has many daily logs
4. **Trip → Stop** - One trip has many stops
5. **DailyLog → LogEntry** - One daily log has many log entries

### Field Mappings

| API Input | Database | Model |
|-----------|----------|-------|
| Current Location | current_location_lat, current_location_lng, current_location_name | Trip |
| Pickup Location | pickup_location_lat, pickup_location_lng, pickup_location_name | Trip |
| Dropoff Location | dropoff_location_lat, dropoff_location_lng, dropoff_location_name | Trip |
| Current Cycle Used Hours | current_cycle_used_hours | Trip |
| **Outputs** | | |
| Map Route | Coordinates from Trip & Stops | Trip, Stop |
| Stops/Rests | Stop table with type and timing | Stop |
| Daily Logs | DailyLog & LogEntry tables | DailyLog, LogEntry |

## Data Flow

```
React Frontend
      ↓
API Request (JSON)
      ↓
Django ViewSet
      ↓
Serializer (Validation)
      ↓
Django ORM
      ↓
SQLite Database
      ↓
Query Result
      ↓
Serializer (JSON)
      ↓
API Response
      ↓
React Frontend (Display)
```

## Query Examples

### Get All Trips for a Driver
```sql
SELECT t.* FROM producto_trip t 
WHERE t.driver_id = 1 
ORDER BY t.start_datetime DESC;
```

### Get Today's Log with Entries
```sql
SELECT l.* FROM producto_dailylog l
WHERE l.driver_id = 1 AND l.log_date = '2026-05-06';

SELECT e.* FROM producto_logentry e
WHERE e.daily_log_id = 1
ORDER BY e.start_time;
```

### Get Stops for a Trip (Ordered by Arrival)
```sql
SELECT s.* FROM producto_stop s
WHERE s.trip_id = 1
ORDER BY s.arrival_time;
```

### Calculate Total Hours Used
```sql
SELECT 
    SUM(CASE WHEN log_type='D' THEN duration_hours ELSE 0 END) as driving_hours,
    SUM(CASE WHEN log_type='ON' THEN duration_hours ELSE 0 END) as on_duty_hours
FROM producto_logentry
WHERE daily_log_id = 1;
```

## Indexes for Performance

```
Driver:
- PRIMARY KEY (id)
- UNIQUE (user_id)
- UNIQUE (license_number)

Trip:
- PRIMARY KEY (id)
- FOREIGN KEY (driver_id)
- INDEX (driver_id)
- INDEX (status)

Stop:
- PRIMARY KEY (id)
- FOREIGN KEY (trip_id)
- INDEX (trip_id)
- INDEX (arrival_time)

DailyLog:
- PRIMARY KEY (id)
- UNIQUE (driver_id, log_date)
- FOREIGN KEY (driver_id)
- INDEX (driver_id)
- INDEX (log_date)

LogEntry:
- PRIMARY KEY (id)
- FOREIGN KEY (daily_log_id)
- INDEX (daily_log_id)
- INDEX (log_type)
- INDEX (start_time)
```

## Constraints & Validations

### Data Types
- **Latitude/Longitude**: Float (±180 degrees, 6 decimal places for ~0.1m precision)
- **Hours**: Float (supports fractional hours like 8.5)
- **Timestamps**: DateTime with timezone support
- **Status Fields**: VARCHAR with predefined choices

### Business Rules
1. One user = One driver (unique)
2. One driver + one date = One daily log (unique)
3. Driving hours ≤ 11 hours per day
4. On-duty window ≤ 14 hours
5. Off-duty must be ≥ 10 hours
6. Log entries must fit within 24 hours

### Cascade Behavior
- Deleting Driver → Deletes all Trips and DailyLogs
- Deleting Trip → Deletes all Stops
- Deleting DailyLog → Deletes all LogEntries

## Storage Estimates

For 1000 drivers with 100 trips each:
- Drivers: ~100 KB
- Trips: ~500 KB
- Stops (5 per trip): ~2.5 MB
- DailyLogs (1 per day per trip): ~5 MB
- LogEntries (5 per log): ~25 MB
- **Total**: ~33 MB (SQLite suitable)

For production with millions of logs, migrate to PostgreSQL.

---

**Database Ready:** ✅ All tables created and normalized
**Schema Optimized:** ✅ Indexed for common queries
**Ready for API:** ✅ Relationships established
