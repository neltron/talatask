from django.shortcuts import render
from rest_framework import permissions, viewsets, generics, status
from rest_framework.response import Response

from .serializers import SkillSerializer, EmployeeSerializer, TaskSerializer, ScheduleSerializer, ReportSerializer, AssignmentSerializer
from .models import Skill, Employee, Task, Schedule
from .commands import assign_pending_tasks

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()
    serializer_class = ReportSerializer

    def get(self, request):
        report = Schedule.get_assignment_report()
        serializer = ReportSerializer(report, many=True)
        return Response(serializer.data)
    
class AssignmentView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()
    serializer_class = AssignmentSerializer

    def get(self, request):
        assignments = assign_pending_tasks()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)