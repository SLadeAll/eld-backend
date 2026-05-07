from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# User Registration Model

class UserProfile(models.Model):
    """User profile for non-admin users registering through the API"""
    USER_ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('dispatcher', 'Dispatcher'),
        ('manager', 'Manager'),
        ('user', 'Regular User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# ELD (Electronic Logging Device) Models

class Driver(models.Model):
    """Driver profile for ELD system"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    license_state = models.CharField(max_length=2)
    vehicle_number = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    max_hours_per_day = models.IntegerField(default=11)  # Hours
    max_hours_per_week = models.IntegerField(default=60)  # Hours
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"


class Trip(models.Model):
    """Main trip record"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Location inputs
    current_location_lat = models.FloatField()
    current_location_lng = models.FloatField()
    pickup_location_lat = models.FloatField()
    pickup_location_lng = models.FloatField()
    dropoff_location_lat = models.FloatField()
    dropoff_location_lng = models.FloatField()
    
    # Location names (for display)
    current_location_name = models.CharField(max_length=255, blank=True)
    pickup_location_name = models.CharField(max_length=255)
    dropoff_location_name = models.CharField(max_length=255)
    
    # Cycle information
    current_cycle_used_hours = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    
    # Trip metadata
    start_datetime = models.DateTimeField(auto_now_add=True)
    estimated_end_datetime = models.DateTimeField(null=True, blank=True)
    actual_end_datetime = models.DateTimeField(null=True, blank=True)
    estimated_distance_miles = models.FloatField(null=True, blank=True)
    actual_distance_miles = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trip from {self.pickup_location_name} to {self.dropoff_location_name}"


class Stop(models.Model):
    """Route stops and rest breaks"""
    STOP_TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('fuel', 'Fuel Stop'),
        ('rest', 'Rest/Meal Break'),
        ('sleeper', 'Sleeper Berth'),
        ('inspection', 'Vehicle Inspection'),
        ('other', 'Other Stop'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    stop_type = models.CharField(max_length=20, choices=STOP_TYPE_CHOICES)
    
    location_name = models.CharField(max_length=255)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_stop_type_display()} at {self.location_name}"


class DailyLog(models.Model):
    """Daily ELD Log Sheet"""
    LOG_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('certified', 'Certified'),
    ]

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='daily_logs')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    
    log_date = models.DateField()
    status = models.CharField(max_length=20, choices=LOG_STATUS_CHOICES, default='draft')
    
    # Cycle tracking
    total_driving_hours = models.FloatField(default=0)
    total_on_duty_hours = models.FloatField(default=0)
    total_off_duty_hours = models.FloatField(default=0)
    total_sleeper_berth_hours = models.FloatField(default=0)
    
    # Regulations compliance
    hours_available_driving = models.FloatField(default=11)  # Remaining hours
    hours_available_on_duty = models.FloatField(default=14)  # Remaining hours in 14-hour window
    
    vehicle_odometer_start = models.IntegerField(null=True, blank=True)
    vehicle_odometer_end = models.IntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Log for {self.driver.user.get_full_name()} - {self.log_date}"

    class Meta:
        unique_together = ('driver', 'log_date')

    def _update_totals(self):
        """Update total hours from all entries"""
        entries = self.entries.all()
        
        self.total_driving_hours = sum(
            e.duration_hours for e in entries if e.log_type == 'D'
        )
        self.total_on_duty_hours = sum(
            e.duration_hours for e in entries if e.log_type == 'ON'
        )
        self.total_off_duty_hours = sum(
            e.duration_hours for e in entries if e.log_type == 'OFF'
        )
        self.total_sleeper_berth_hours = sum(
            e.duration_hours for e in entries if e.log_type == 'SB'
        )
        
        # Calculate remaining hours
        self.hours_available_driving = max(
            0, self.driver.max_hours_per_day - self.total_driving_hours
        )
        self.hours_available_on_duty = max(
            0, 14 - (self.total_driving_hours + self.total_on_duty_hours)
        )


class LogEntry(models.Model):
    """Individual log entries (driving, on-duty, off-duty, sleeper berth)"""
    LOG_TYPE_CHOICES = [
        ('OFF', 'Off Duty'),
        ('SB', 'Sleeper Berth'),
        ('D', 'Driving'),
        ('ON', 'On Duty'),
    ]

    daily_log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='entries')
    
    log_type = models.CharField(max_length=3, choices=LOG_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.FloatField()
    
    location = models.CharField(max_length=255, blank=True)
    odometer_start = models.IntegerField(null=True, blank=True)
    odometer_end = models.IntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    is_editable = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_log_type_display()} - {self.start_time} to {self.end_time}"