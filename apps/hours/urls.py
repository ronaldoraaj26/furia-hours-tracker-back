from rest_framework.routers import DefaultRouter
from .views import CalendarEventViewSet, ApprovalViewSet

router = DefaultRouter()
router.register(r'calendar-events', CalendarEventViewSet,
                basename='calendar-event')
router.register(r'approvals', ApprovalViewSet,
                basename='approval')

urlpatterns = router.urls
