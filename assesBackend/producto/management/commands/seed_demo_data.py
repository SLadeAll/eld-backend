from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from producto.models import Driver, Trip, Stop, DailyLog, LogEntry


class Command(BaseCommand):
    help = 'Seed database with demo ELD data'

    def handle(self, *args, **options):
        self.stdout.write('Starting demo data seeding...')

        # Create demo user if doesn't exist
        user, created = User.objects.get_or_create(
            username='demodriver',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@trucking.com'
            }
        )
        self.stdout.write(f'{"Created" if created else "Using existing"} user: {user.get_full_name()}')

        # Create driver profile
        driver, created = Driver.objects.get_or_create(
            user=user,
            defaults={
                'license_number': 'CA1234567',
                'license_state': 'CA',
                'vehicle_number': 'TRUCK-001',
                'company_name': 'Express Trucking Co',
                'max_hours_per_day': 11,
                'max_hours_per_week': 60,
            }
        )
        self.stdout.write(f'{"Created" if created else "Using existing"} driver: {driver.license_number}')

        # Create sample trip
        trip, created = Trip.objects.get_or_create(
            driver=driver,
            status='in_progress',
            pickup_location_name='New York, NY',
            dropoff_location_name='Los Angeles, CA',
            defaults={
                'current_location_lat': 40.7128,
                'current_location_lng': -74.0060,
                'current_location_name': 'New York, NY',
                'pickup_location_lat': 40.7580,
                'pickup_location_lng': -73.9855,
                'dropoff_location_lat': 34.0522,
                'dropoff_location_lng': -118.2437,
                'current_cycle_used_hours': 3.5,
                'estimated_distance_miles': 2800,
                'estimated_end_datetime': timezone.now() + timedelta(days=3),
            }
        )
        self.stdout.write(f'{"Created" if created else "Using existing"} trip: {trip.pickup_location_name} -> {trip.dropoff_location_name}')

        # Create sample stops
        stops_data = [
            {
                'stop_type': 'fuel',
                'location_name': 'Shell Gas Station, Denver, CO',
                'location_lat': 39.7392,
                'location_lng': -104.9903,
                'arrival_time': timezone.now() + timedelta(hours=8),
                'departure_time': timezone.now() + timedelta(hours=8.5),
                'duration_minutes': 30,
                'notes': 'Fuel up and brief rest',
            },
            {
                'stop_type': 'rest',
                'location_name': 'Rest Area, Kansas',
                'location_lat': 38.5266,
                'location_lng': -97.2469,
                'arrival_time': timezone.now() + timedelta(hours=12),
                'departure_time': timezone.now() + timedelta(hours=13),
                'duration_minutes': 60,
                'notes': 'Mandatory 1-hour rest break',
            },
            {
                'stop_type': 'fuel',
                'location_name': 'Loves Travel Stop, Texas',
                'location_lat': 30.2672,
                'location_lng': -97.7431,
                'arrival_time': timezone.now() + timedelta(hours=18),
                'departure_time': timezone.now() + timedelta(hours=19),
                'duration_minutes': 45,
                'notes': 'Fuel and meal break',
            },
            {
                'stop_type': 'sleeper',
                'location_name': 'Motel 6, New Mexico',
                'location_lat': 35.0845,
                'location_lng': -106.6504,
                'arrival_time': timezone.now() + timedelta(hours=22),
                'departure_time': timezone.now() + timedelta(days=1, hours=8),
                'duration_minutes': 600,  # 10 hours
                'notes': 'Overnight rest at motel',
            },
        ]

        for stop_data in stops_data:
            stop, created = Stop.objects.get_or_create(
                trip=trip,
                location_name=stop_data['location_name'],
                defaults=stop_data
            )
            if created:
                self.stdout.write(f'  Created stop: {stop.location_name}')

        # Create daily log
        today = timezone.now().date()
        log, created = DailyLog.objects.get_or_create(
            driver=driver,
            log_date=today,
            defaults={
                'trip': trip,
                'status': 'draft',
            }
        )
        self.stdout.write(f'{"Created" if created else "Using existing"} daily log for {today}')

        # Create sample log entries if this is new log
        if created:
            current_time = timezone.now().replace(hour=6, minute=0, second=0, microsecond=0)

            entries_data = [
                {
                    'log_type': 'ON',
                    'start_time': current_time,
                    'end_time': current_time + timedelta(hours=0.5),
                    'duration_hours': 0.5,
                    'location': 'New York, NY',
                    'notes': 'Pre-trip inspection',
                },
                {
                    'log_type': 'D',
                    'start_time': current_time + timedelta(hours=0.5),
                    'end_time': current_time + timedelta(hours=8),
                    'duration_hours': 7.5,
                    'location': 'New York to Denver, CO',
                    'odometer_start': 45000,
                    'odometer_end': 45600,
                    'notes': 'Long haul driving',
                },
                {
                    'log_type': 'OFF',
                    'start_time': current_time + timedelta(hours=8),
                    'end_time': current_time + timedelta(hours=9),
                    'duration_hours': 1,
                    'location': 'Denver, CO',
                    'notes': 'Fuel and meal break',
                },
                {
                    'log_type': 'D',
                    'start_time': current_time + timedelta(hours=9),
                    'end_time': current_time + timedelta(hours=14),
                    'duration_hours': 5,
                    'location': 'Denver, CO to Kansas City',
                    'odometer_start': 45600,
                    'odometer_end': 45950,
                    'notes': 'Afternoon driving',
                },
            ]

            for entry_data in entries_data:
                entry = LogEntry.objects.create(
                    daily_log=log,
                    **entry_data
                )
                self.stdout.write(f'  Created log entry: {entry.get_log_type_display()}')

            # Update log totals
            log._update_totals()
            log.save()
            self.stdout.write(f'  Updated log totals')

        self.stdout.write(self.style.SUCCESS('✓ Demo data seeding completed!'))
        self.stdout.write(f'\nDemo credentials:')
        self.stdout.write(f'  Username: demodriver')
        self.stdout.write(f'  Driver License: {driver.license_number}')
        self.stdout.write(f'  Trip: {trip.pickup_location_name} → {trip.dropoff_location_name}')
