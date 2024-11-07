from rest_framework import serializers
from .models import Employee, Task, Schedule, Skill


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'skills']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'skill', 'date', 'estimated_hours', 'assigned_hours']

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ['employee', 'task', 'date', 'hour']

class SkillModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class EmployeeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name']

class TaskModelSerializer(serializers.ModelSerializer):
    skill = SkillModelSerializer()
    class Meta:
        model = Task
        fields = ['title', 'skill', 'date', 'estimated_hours', 'assigned_hours']

class ScheduleModelSerializer(serializers.ModelSerializer):
    employee = EmployeeModelSerializer()
    class Meta:
        model = Schedule
        fields = ['employee', 'date', 'hour']

class ReportSerializer(serializers.Serializer):
    task_title = serializers.CharField(max_length=200)
    task_estimated_hours = serializers.IntegerField()
    task_skill = serializers.CharField(max_length=200)
    employee_name = serializers.CharField(max_length=200)
    execution_day = serializers.DateField()
    execution_hour_utc = serializers.IntegerField()
    assigned_at = serializers.DateTimeField()

class AssignmentSerializer(serializers.Serializer):
    task = TaskModelSerializer()
    schedules = ScheduleModelSerializer(many=True)