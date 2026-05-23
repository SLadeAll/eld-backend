from rest_framework import serializers
from django.contrib.auth.models import User
from producto.models import Producto, Driver, Trip, Stop, DailyLog, LogEntry, UserProfile


# User Registration Serializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(required=False, default='user')
    phone_number = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 
                  'password_confirm', 'role', 'phone_number', 'company_name']
        read_only_fields = ['id']

    def validate(self, data):
        """Validate that passwords match"""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def validate_username(self, value):
        """Check if username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        """Check if email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        """Create a new user without admin privileges"""
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        role = validated_data.pop('role', 'user')
        phone_number = validated_data.pop('phone_number', '')
        company_name = validated_data.pop('company_name', '')

        # Create user with is_staff and is_superuser set to False
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=False,
            is_superuser=False
        )

        # Create user profile with role and additional info
        UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=phone_number if phone_number else None,
            company_name=company_name if company_name else None
        )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                  'phone_number', 'company_name', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']


# User Login Serializer

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        data['user'] = user
        return data


class UserLoginResponseSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class productoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


# ELD Serializers

class DriverSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id', 'user', 'user_name', 'user_email', 'license_number', 
            'license_state', 'vehicle_number', 'company_name', 
            'max_hours_per_day', 'max_hours_per_week', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = [
            'id', 'trip', 'stop_type', 'location_name', 'location_lat', 
            'location_lng', 'arrival_time', 'departure_time', 'duration_minutes', 
            'notes', 'created_at'
        ]
        read_only_fields = ['created_at']


class TripSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True, read_only=True)
    driver_name = serializers.CharField(source='driver.user.get_full_name', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'driver', 'driver_name', 'status',
            'current_location_lat', 'current_location_lng', 'current_location_name',
            'pickup_location_lat', 'pickup_location_lng', 'pickup_location_name',
            'dropoff_location_lat', 'dropoff_location_lng', 'dropoff_location_name',
            'current_cycle_used_hours', 'start_datetime', 'estimated_end_datetime',
            'actual_end_datetime', 'estimated_distance_miles', 'actual_distance_miles',
            'stops', 'created_at', 'updated_at'
        ]
        read_only_fields = ['start_datetime', 'created_at', 'updated_at']


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = [
            'id', 'daily_log', 'log_type', 'start_time', 'end_time', 
            'duration_hours', 'location', 'odometer_start', 'odometer_end', 
            'notes', 'is_editable', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DailyLogSerializer(serializers.ModelSerializer):
    entries = LogEntrySerializer(many=True, read_only=True)
    driver_name = serializers.CharField(source='driver.user.get_full_name', read_only=True)

    class Meta:
        model = DailyLog
        fields = [
            'id', 'driver', 'driver_name', 'trip', 'log_date', 'status',
            'total_driving_hours', 'total_on_duty_hours', 'total_off_duty_hours',
            'total_sleeper_berth_hours', 'hours_available_driving',
            'hours_available_on_duty', 'vehicle_odometer_start', 'vehicle_odometer_end',
            'notes', 'entries', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ── Análisis de Ruta — Territorio Mexicano ────────────────────────────────────

class CoordinateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    elevation = serializers.FloatField(required=False, allow_null=True)


class ReferencePointSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    type = serializers.ChoiceField(choices=['caseta', 'paradero', 'rampa', 'gasolinera'])
    name = serializers.CharField(max_length=255)


class VehicleConfigSerializer(serializers.Serializer):
    vehicle_type = serializers.ChoiceField(
        choices=['double_trailer'],
        default='double_trailer',
    )
    first_delivery_coord_index = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0,
        help_text=(
            "Índice (0-based) de la coordenada donde ocurre la primera entrega. "
            "Los tramos cuyo seg_start >= este índice se marcan como Media Carga."
        ),
    )


class RouteAnalysisRequestSerializer(serializers.Serializer):
    coordinates = CoordinateSerializer(many=True)
    references = ReferencePointSerializer(many=True, required=False, default=list)
    vehicle_config = VehicleConfigSerializer(required=False, default=dict)

    def validate_coordinates(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Se requieren al menos 2 coordenadas para analizar la ruta."
            )
        return value