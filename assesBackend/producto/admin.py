from django.contrib import admin
from .models import Producto, UserProfile, Driver, Trip, Stop, DailyLog, LogEntry

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'created_at', 'updated_at']
    search_fields = ['nombre', 'descripcion']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'license_number', 'company_name', 'created_at']
    list_filter = ['company_name', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_driver_name(self, obj):
        return obj.user.get_full_name()
    get_driver_name.short_description = 'Driver Name'


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['get_driver', 'status', 'pickup_location_name', 'dropoff_location_name', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['driver__user__first_name', 'pickup_location_name', 'dropoff_location_name']
    readonly_fields = ['start_datetime', 'created_at', 'updated_at']
    
    def get_driver(self, obj):
        return obj.driver.user.get_full_name()
    get_driver.short_description = 'Driver'


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['stop_type', 'location_name', 'arrival_time', 'departure_time']
    list_filter = ['stop_type', 'arrival_time']
    search_fields = ['location_name', 'notes']
    readonly_fields = ['created_at']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['get_driver', 'log_date', 'status', 'total_driving_hours']
    list_filter = ['status', 'log_date']
    search_fields = ['driver__user__first_name', 'driver__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_driver(self, obj):
        return obj.driver.user.get_full_name()
    get_driver.short_description = 'Driver'


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'start_time', 'end_time', 'duration_hours', 'location']
    list_filter = ['log_type', 'start_time']
    search_fields = ['location', 'notes']
    readonly_fields = ['created_at', 'updated_at']