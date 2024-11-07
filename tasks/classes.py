# Implementación del Patrón de Diseño "Strategy" que permitirá encapsular la lógica de asignación de Tasks 
# a los diferentes Schedule disponibles en diferentes estrategias para que se puedan seleccionar y aplicar
# de manera flexible.

from abc import ABC, abstractmethod
from .models import Employee, Schedule

class AssignmentStrategy(ABC):
    @abstractmethod
    def assignment(self, task):
        pass


# Estrategia 1: Asignar priorizando la disponibilidad de los Employee
# Asigna primero a los empleados que tengan más horas disponibles la fecha que corresponda a la tarea
# Supuestos:
# - Se asignarán Employees a la Task, hasta que Task.assigned_hours == Task.estimated_hours
class AssignmentByEmployeeAvailability(AssignmentStrategy):
    def assignment(self, task):
        # Lista de horas que se asignarán a cada tarea.
        assigned_hours = []

        # 1. Obtener Employees que tengan el Skill requerido y disponibilidad según la Task
        employees = list(Employee.objects.all().has_skill(task.skill).has_availability(task.date).with_schedule_count())

        # 2. Actualizo Task.assigned_hours para asegurarme que los datos sean correctos
        task.update_assigned_hours()

        # 3. Por cada Employee (si es que existe alguno que cumpla la condición), obtengo sus Schedule disponibles 
        # y las asigno hasta cumplir con las horas pendientes de revisión
        pending_hours = task.estimated_hours - task.assigned_hours
        for employee in employees:
            # Obtiene las horas disponibles, ordenadas de menor a mayor
            hours = Schedule.objects.by_employee(employee).by_date(task.date).unassigned().order_by('hour')
            for hour in hours:
                if pending_hours > 0:
                    hour.assign_task(task)
                    assigned_hours.append(hour)
                    pending_hours -= 1
            
            # Si se asignaron todas las horas, se sale del ciclo
            if pending_hours == 0:
                continue
        
        # 4. Actualizo Task.assigned_hours nuevamente
        task.update_assigned_hours()

        return assigned_hours

# Otras posibles estrategias:
# - Asignar Task solo a un Employee que tenga las horas necesarias disponibles en la fecha correspondiente
# - Asignar Task a múltiples Employee distribuyendo las horas equitativamente
# - Asignar Task a múltiples Employee que tengan disponibilidad más temprano, para priorizar la pronta realización de la Task


# Asignador de tareas, que se encarga de ejecutar la estrategia seleccionada
class TaskAssigner:
    def __init__(self, strategy: AssignmentStrategy):
        self.strategy = strategy

    def assign_task(self, task):
        return self.strategy.assignment(task)
