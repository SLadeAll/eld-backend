from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta

from producto.models import (
    Producto, Driver, Trip, Stop, DailyLog, LogEntry, UserProfile
)
from producto.api.serilizers import (
    productoSerializer, DriverSerializer, TripSerializer,
    StopSerializer, DailyLogSerializer, LogEntrySerializer,
    UserRegistrationSerializer, UserProfileSerializer,
    UserLoginSerializer, UserLoginResponseSerializer,
    RouteAnalysisRequestSerializer,
)
from producto.route_analysis import segment_route
from producto.pdf_generator import build_pdf


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = productoSerializer


# User Registration ViewSet

class UserRegistrationViewSet(viewsets.ViewSet):
    """Handle user registration for non-admin users"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check_username(self, request):
        """Check if username is available"""
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        exists = UserProfile.objects.filter(user__username=username).exists()
        return Response({'available': not exists})

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check_email(self, request):
        """Check if email is available"""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        exists = UserProfile.objects.filter(user__email=email).exists()
        return Response({'available': not exists})


class UserProfileViewSet(viewsets.ModelViewSet):
    """View and manage user profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# User Login ViewSet

class UserLoginViewSet(viewsets.ViewSet):
    """Handle user login and authentication"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Authenticate user with username and password"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            response_serializer = UserLoginResponseSerializer(user)
            return Response({
                'token': token.key,
                'user': response_serializer.data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def logout(self, request):
        """Logout and delete token"""
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

# ELD ViewSets

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    @action(detail=True, methods=['get'])
    def trip_history(self, request, pk=None):
        """Get trip history for a driver"""
        driver = self.get_object()
        trips = driver.trips.all().order_by('-start_datetime')
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def current_cycle(self, request, pk=None):
        """Get current hours for driver's cycle"""
        driver = self.get_object()
        today = timezone.now().date()
        log = DailyLog.objects.filter(driver=driver, log_date=today).first()
        if log:
            return Response({
                'total_driving_hours': log.total_driving_hours,
                'total_on_duty_hours': log.total_on_duty_hours,
                'hours_available_driving': log.hours_available_driving,
                'hours_available_on_duty': log.hours_available_on_duty,
            })
        return Response({
            'total_driving_hours': 0,
            'total_on_duty_hours': 0,
            'hours_available_driving': driver.max_hours_per_day,
            'hours_available_on_duty': 14,
        })


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @action(detail=True, methods=['post'])
    def create_stops(self, request, pk=None):
        """Create stops for a trip (route planning)"""
        trip = self.get_object()
        stops_data = request.data.get('stops', [])
        
        for stop_data in stops_data:
            Stop.objects.create(
                trip=trip,
                **stop_data
            )
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def route_info(self, request, pk=None):
        """Get route information and stops"""
        trip = self.get_object()
        stops = trip.stops.all().order_by('arrival_time')
        return Response({
            'trip': TripSerializer(trip).data,
            'stops': StopSerializer(stops, many=True).data,
            'total_distance_miles': trip.actual_distance_miles or trip.estimated_distance_miles,
            'stop_count': stops.count(),
        })

    @action(detail=True, methods=['post'])
    def complete_trip(self, request, pk=None):
        """Mark trip as completed"""
        trip = self.get_object()
        trip.status = 'completed'
        trip.actual_end_datetime = timezone.now()
        trip.actual_distance_miles = request.data.get('actual_distance_miles')
        trip.save()
        return Response(TripSerializer(trip).data)

    @action(detail=True, methods=['get'])
    def remaining_hours(self, request, pk=None):
        """Calculate remaining driving hours based on current cycle"""
        trip = self.get_object()
        driver = trip.driver
        
        hours_used = trip.current_cycle_used_hours
        hours_remaining = driver.max_hours_per_day - hours_used
        
        return Response({
            'hours_available_driving': max(0, hours_remaining),
            'hours_used_today': hours_used,
            'max_hours_allowed': driver.max_hours_per_day,
        })


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer

    def get_queryset(self):
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            return Stop.objects.filter(trip_id=trip_id).order_by('arrival_time')
        return Stop.objects.all()


class DailyLogViewSet(viewsets.ModelViewSet):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer

    @action(detail=True, methods=['post'])
    def add_entry(self, request, pk=None):
        """Add a log entry to daily log"""
        daily_log = self.get_object()
        
        log_type = request.data.get('log_type')
        start_time = timezone.now()
        duration_hours = request.data.get('duration_hours', 0)
        end_time = start_time + timedelta(hours=duration_hours)
        
        entry = LogEntry.objects.create(
            daily_log=daily_log,
            log_type=log_type,
            start_time=start_time,
            end_time=end_time,
            duration_hours=duration_hours,
            location=request.data.get('location', ''),
            odometer_start=request.data.get('odometer_start'),
            odometer_end=request.data.get('odometer_end'),
            notes=request.data.get('notes', ''),
        )
        
        # Update daily log totals
        daily_log._update_totals()
        
        serializer = DailyLogSerializer(daily_log)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today_log(self, request):
        """Get or create today's log for logged-in driver"""
        driver_id = request.query_params.get('driver_id')
        if not driver_id:
            return Response({'error': 'driver_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        today = timezone.now().date()
        log, created = DailyLog.objects.get_or_create(
            driver_id=driver_id,
            log_date=today
        )
        
        serializer = DailyLogSerializer(log)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit daily log for certification"""
        daily_log = self.get_object()
        daily_log.status = 'submitted'
        daily_log.save()
        return Response(DailyLogSerializer(daily_log).data)

    @action(detail=True, methods=['post'])
    def certify(self, request, pk=None):
        """Certify daily log (driver signature)"""
        daily_log = self.get_object()
        daily_log.status = 'certified'
        daily_log.save()
        return Response(DailyLogSerializer(daily_log).data)

    @action(detail=True, methods=['post'])
    def update_totals(self, request, pk=None):
        """Recalculate totals from entries"""
        daily_log = self.get_object()
        daily_log._update_totals()
        daily_log.save()
        return Response(DailyLogSerializer(daily_log).data)


class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

    def get_queryset(self):
        daily_log_id = self.request.query_params.get('daily_log_id')
        if daily_log_id:
            return LogEntry.objects.filter(daily_log_id=daily_log_id).order_by('start_time')
        return LogEntry.objects.all()


class RouteAnalysisViewSet(viewsets.ViewSet):
    """Segmenta una ruta en tramos para análisis de territorio mexicano."""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def analyze(self, request):
        """
        Recibe coordenadas de ruta y referencias viales, devuelve los tramos
        segmentados con trazo/topografía y puntos de referencia.
        """
        serializer = RouteAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        coordinates    = serializer.validated_data['coordinates']
        references     = serializer.validated_data.get('references', [])
        vehicle_config = serializer.validated_data.get('vehicle_config', {})

        result = segment_route(coordinates, references, vehicle_config)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='export-pdf')
    def export_pdf(self, request):
        """
        Accepts the same payload as /analyze/, generates a full PDF report
        (cover + per-tramo map + PROCESO table + OS profile) and returns it
        as an application/pdf download.
        """
        serializer = RouteAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        coordinates    = serializer.validated_data['coordinates']
        references     = serializer.validated_data.get('references', [])
        vehicle_config = serializer.validated_data.get('vehicle_config', {})
        route_label    = request.data.get('route_label', '')

        result = segment_route(coordinates, references, vehicle_config)
        tramos = result.get('tramos', [])

        try:
            pdf_bytes = build_pdf(tramos, route_label=route_label)
        except Exception as exc:
            return Response(
                {'error': f'Error generando PDF: {exc}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        date_str  = datetime.now().strftime('%Y%m%d_%H%M')
        safe_name = ''.join(c if c.isalnum() or c in '-_' else '_' for c in route_label)[:40]
        filename  = f"analisis_riesgos_{safe_name}_{date_str}.pdf" if safe_name else f"analisis_riesgos_{date_str}.pdf"

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny],
        url_path='extract-indications',
    )
    def extract_indications_view(self, request):
        """
        Automatically extract road indications (traffic signals, toll booths,
        fuel stations, speed bumps, etc.) from the OSM Overpass API for the
        route bounding box.

        Accepts: { "coordinates": [{lat, lon, elevation?}, ...] }
        Returns: { "indications": [{lat, lon, type, label, metadata?}], "total": int }

        Results are cached in-memory per bounding box for 1 hour.
        """
        coordinates = request.data.get('coordinates', [])
        if not coordinates or len(coordinates) < 2:
            return Response(
                {'error': 'coordinates array with at least 2 points required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Normalise to {lat, lon} dicts
        normalised = []
        for c in coordinates:
            if isinstance(c, dict) and 'lat' in c and 'lon' in c:
                try:
                    normalised.append({'lat': float(c['lat']), 'lon': float(c['lon'])})
                except (TypeError, ValueError):
                    pass

        if len(normalised) < 2:
            return Response(
                {'error': 'coordinates must be objects with numeric lat and lon fields'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from producto.indication_extractor import extract_indications
        indications = extract_indications(normalised)

        return Response(
            {'indications': indications, 'total': len(indications)},
            status=status.HTTP_200_OK,
        )
