from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from talatask.models import TimeStampModel
from datetime import date
from django.utils import timezone


class Skill(TimeStampModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class EmployeeQuerySet(models.QuerySet):
    def has_skill(self, skill: Skill):
        return self.filter(skills__id=skill.id)
    
    def has_availability(self, date: date):
        return self.filter(schedule__date=date)

    def with_schedule_count(self):
        return self.annotate(
            schedule_count=models.Count(
                models.Case(models.When(
                    schedule__task_id__isnull=True, then=1
                ),
                output_field=models.IntegerField(),
            ))
        ).order_by('schedule_count')

# Supuestos para los colaboradores
# - Un colaborador puede tener muchas habilidades
class Employee(TimeStampModel):
    name = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skill)

    objects = EmployeeQuerySet.as_manager()

    @staticmethod
    def get_all_by_skill(skill: Skill):
        return list(Employee.objects.all().has_skill(skill))

    @staticmethod
    def get_all_availability_by_date(date: date):
        return Employee.objects.has_availability(date).with_schedule_count()
    
    def __str__(self):
        return self.name


class TaskQuerySet(models.QuerySet):
    def unassigned(self):
        return self.filter(estimated_hours__gt=models.F('assigned_hours'))
    
    def current(self):
        return self.filter(date__gte=date.today())
    
    def with_schedule_count(self):
        return self.annotate(schedule_count=models.Count('schedule__id'))
    
# Supuestos para las tareas
# - Una tarea puede tener un solo Skill asociado, con sus horas estimadas para resolverse
# - estimated_hours considera horas completas solamente, siendo su menor valor 1
# - assigned_hours guarda las horas que han sigo asignadas a la Task, según las Assignment relacionadas
# - Si assigned_hours == assigned_hours se considera que dicha tarea ya está asignada por completo
class Task(TimeStampModel):
    skill = models.ForeignKey(Skill, on_delete=models.RESTRICT)
    title = models.CharField(max_length=128)
    date = models.DateField()
    estimated_hours = models.PositiveIntegerField(validators=[MaxValueValidator(24), MinValueValidator(1)])
    assigned_hours = models.PositiveIntegerField(default=0)
    
    objects = TaskQuerySet.as_manager()

    # Actualiza el campo Task.assigned_hours según la cantidad de Schedule.task corresponda
    def update_assigned_hours(self):
        current_assigned_hours = list(Task.objects.filter(id=self.id).values('id').with_schedule_count())
        self.assigned_hours = current_assigned_hours[0]['schedule_count']
        self.save()

    @staticmethod
    def get_current_unassigned_tasks():
        return Task.objects.all().unassigned().current()

    def __str__(self):
        return f'{self.title} - {self.skill.name} ({self.date})'


class ScheduleQuerySet(models.QuerySet):
    def unassigned(self):
        return self.filter(task__isnull=True)
    
    def assigned(self):
        return self.filter(task__isnull=False)

    def current(self):
        return self.filter(date__gte=date.today())

    def by_date(self, date):
        return self.filter(date=date)

    def by_employee(self, employee):
        return self.filter(employee=employee)


# Supuestos para los Horarios
# - Se considera un registro como una hora de X día, por ende, si el colaborador tiene 4 horas 
#   disponibles el mismo día, tendrá 4 registros con las horas correspondientes para el mismo día
# - Solo se puede crear 1 hora para el mismo día para el mismo usuario
# - Si la llave foránea con Task es null, se considera que el Schedule está disponible para ser asignado
# - Se considera Hour el valor de la hora correspondiente según el uso horario UTC
class Schedule(TimeStampModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    last_assignment_date = models.DateTimeField(null=True, blank=True)
    date = models.DateField()
    hour = models.PositiveIntegerField(validators=[MaxValueValidator(23), MinValueValidator(0)])

    objects = ScheduleQuerySet.as_manager()

    class Meta:
        ordering = ('date', 'hour')
        constraints = [models.UniqueConstraint(
            fields=['employee', 'date', 'hour'],
            name='unique_hour_per_day_per_employee',
        )]
    
    def assign_task(self, task: Task):
        self.task = task
        self.last_assignment_date = timezone.now()
        self.save()

    @staticmethod
    def get_assignment_report():
        report = []
        row = {}
        assignments = list(Schedule.objects.assigned().order_by('date', 'hour'))
        for assignment in assignments:
            row = {
                'task_title': assignment.task.title,
                'task_estimated_hours': assignment.task.estimated_hours,
                'task_skill': assignment.task.skill.name,
                'employee_name': assignment.employee.name,
                'execution_day': assignment.date,
                'execution_hour_utc': assignment.hour,
                'assigned_at': assignment.last_assignment_date
            }
            report.append(row)
        
        return report

    def __str__(self):
        return f'{self.date} {self.hour}:00 - {self.employee.name}'