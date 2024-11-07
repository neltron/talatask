# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import include, path
from rest_framework import routers

from tasks.views import SkillViewSet, EmployeeViewSet, TaskViewSet, ScheduleViewSet, ReportView, AssignmentView

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'schedule', ScheduleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('report/', ReportView.as_view(), name='report_view'),
    path('assignment/', AssignmentView.as_view(), name='assignment_view'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]