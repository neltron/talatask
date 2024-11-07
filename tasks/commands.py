from .classes import TaskAssigner, AssignmentByEmployeeAvailability
from .models import Task

def assign_pending_tasks():
    # Obtiene todas las tareas que cumplan con:
    # - Tengan horas pendientes de asignar
    # - Tengan fecha de ejecución mayor o igual a hoy
    # Priorización:
    # - Primero las con fecha más próxima
    # - Primero las que lleve más horas resolver
    tasks = list(Task.objects.unassigned().current().order_by('date', '-estimated_hours'))

    # Se crea el asignador, con la estrategia seleccionada, es acá que podrían desarrollarse diferentes métodos
    # que ejecuten las distintas estrategias, o tal vez, una estrategia diferente por tipo de tarea u otro.
    assigner = TaskAssigner(AssignmentByEmployeeAvailability())

    tasks_results = []

    for task in tasks:
        tasks_results.append({
            'task': task,
            'schedules': assigner.assign_task(task)
        })
    
    return tasks_results
