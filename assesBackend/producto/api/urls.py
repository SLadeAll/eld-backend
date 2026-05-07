from rest_framework.routers import DefaultRouter
from producto.api.views import (
    ProductoViewSet, UserRegistrationViewSet, UserLoginViewSet, UserProfileViewSet,
    DriverViewSet, TripViewSet, 
    StopViewSet, DailyLogViewSet, LogEntryViewSet
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'auth/register', UserRegistrationViewSet, basename='register')
router.register(r'auth/login', UserLoginViewSet, basename='login')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'stops', StopViewSet, basename='stop')
router.register(r'daily-logs', DailyLogViewSet, basename='daily-log')
router.register(r'log-entries', LogEntryViewSet, basename='log-entry')

urlpatterns = router.urls
