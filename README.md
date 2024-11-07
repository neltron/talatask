# TalaTasks - Prueba técnica
Implementación de algoritmo de asignación de tareas.

## Instalación
### Requisitos previos:
Necesita tener estos programas instalados en su máquina local:
* Docker
* GIT

### Pasos para la instalación
1. Clonar repositorio Github
2. Crear .env en base a .env.example utilizando los siguientes datos:
   ```sh
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=talatask_db
    DB_USER=talatask
    DB_PASSWORD=talatask_passwd
   ```
3. Ejecutar Docker Compose (desde una shell, ubicado en la carpeta del proyecto)
   ```sh
    docker compose up --build
   ```
4. Crear usuario administrador, para esto necesita ejecutar los siguientes comandos:
   ```sh
    docker exec -it talatask-backend-1 bash

    python manage.py createsuperuser --username admin --email admin@example.com
   ```
   Luego de ejecutado pedirá ingresar Password, recomendamos utilizar estos datos a modo de prueba:
   - Password: talana
   
   Estos dato serán necesarios para interactuar con la interfaz API más adelante.

## Modelo de datos implementado
[![](https://mermaid.ink/img/pako:eNpdkM8KwjAMxl-l5Oz2AL2JKyhOFKYHoSBhjdvQttJ1h7Hu3e2ciJpT_vy-jyQDlFYRcCCXNVg51NKwGGJ3yPdnIdgY0jQMrNhu8pxxVmN70Wj6PyqEJJmo1Vpkp1zM4Mwcl8U2usR5-Hb5Gk5i-yPGtm0qQwoWoMlpbFTccJgkEnxNmiTwmCp0NwnSjJHDztuiNyVw7zpagLNdVQO_4r2NVfdQ6Ol94adLqvHW7eYHvP4wPgE55lWe?type=png)](https://mermaid.live/edit#pako:eNpdkM8KwjAMxl-l5Oz2AL2JKyhOFKYHoSBhjdvQttJ1h7Hu3e2ciJpT_vy-jyQDlFYRcCCXNVg51NKwGGJ3yPdnIdgY0jQMrNhu8pxxVmN70Wj6PyqEJJmo1Vpkp1zM4Mwcl8U2usR5-Hb5Gk5i-yPGtm0qQwoWoMlpbFTccJgkEnxNmiTwmCp0NwnSjJHDztuiNyVw7zpagLNdVQO_4r2NVfdQ6Ol94adLqvHW7eYHvP4wPgE55lWe)

| Modelo | Campos | Descripción |
|------|-------|---------|
| Skill | name | Listado de habilidades necesarios para satisfacer las tareas del sistema, estos también representan a las habilidades que tiene cada Empleado |
| Employee | name | Listado de Empleados que a su vez tienen relación con muchos Skills y muchas Schedule |
| Task | title, date (fecha en la que se debe ejecutar la tarea), estimated_hours (cantidad de horas que se estima se necesitarán para ejecutar la tarea), assigned_hours (cantidad de horas que ya han sido asignas para la resolución de esta tarea) | Listado de tareas que se necesita ejecutar, se consideró que una Task puede estar asociada solo a un Skill |
| Schedule | date (día en el que se habilita hora de disponibilidad), hour (hora del día en que se ejecutará la tarea), last_assignment_date (fecha/hora de la última vez que se asignó este espacio de trabajo a una Task específica) | Representa a un espacio de tiempo de 1 hora, en un día específico, donde un Employee podrá ser asignado a una Task específica |

### Algunas consideraciones que se tomaron para simplificar la implementación:
* Un Employee puede tener muchas habilidades (Skill)
* Una Task puede pertenecer a una sola habilidad (Skill)
* Un Schedule puede o no estar asignado a un Task y cada vez que es asignada a una, se actualiza el valor de Schedule.last_assignment_date, esto último para dar control de tiempos al reporte solicitado y para evitar crear otra tabla que mantuviera dicha relación.

## API y endpoints creados
Se habilitaron los endpoints CRUD para los modelos mencionados anteriormente, estos se pueden acceder desde las siguientes URL:
* Skills: http://localhost:8000/skills/
* Employees: http://localhost:8000/employees/
* Tasks: http://localhost:8000/tasks/
* Schedule: http://localhost:8000/schedule/

Se habilitó un endpoit para obtener el reporte de asignaciones:
* http://localhost:8000/report/

Dicho reporte muestra todas las asignaciones históricas que se han realizado, ordenadas por Schedule.date y Schedule.hour, las columnas consideradas fueron las siguientes:
* **task_title**: Nombre de la tarea asignada
* **task_estimated_hours**: Cantidad de horas original que se estimó que la tarea demoraría en desarrollarse
* **task_skill**: Nombre de la habilidad que se necesitaba para realizar esta tarea
* **employee_name**: Nombre del empleado al que se le asignó la tarea
* **execution_day**: Fecha del día en que se asignó para ejecutar dicha tarea
* **execution_hour_utc**: Hora del día (UTC) en el que se asignó para ejecutar la tarea
* **assigned_at**: Fecha y hora (UTC) en que se asignó la tarea

Y también se habilitó un endpoint para ejecutar el comando de asignaciones, mostrando el resultado de esta:
* http://localhost:8000/assignment/

Este endpoint retorna un listado de las Tasks pendientes de asignación y el listado de Schedules que le fueron asignadas en esa ejecución, con este formato:
* **task**: información del Task que tomó el script
* **schedules**: listado de Schedules que fueron asignadas al Task correspondiente

Estos endpoints se pueden ejecutar tanto de la interfaz web (necesita autenticar con los datos creados anteriormente), como también mediante Postman o utilizando el comando curl, con la siguiente sintaxis:
```sh
curl -u admin -H 'Accept: application/json; indent=4' [ENDPOINT_URL]
```
Por ejemplo, para obtener el reporte:
```sh
curl -u admin -H 'Accept: application/json; indent=4' http://localhost:8000/report/
```

## Implementación de algoritmo de asignación:
Para realizar la asignación de horarios disponibles a una tarea, se utilizó el Patrón de diseño **Strategy**, que permite implementar distintas lógicas de asignación de una manera limpia y ordenada, permitiendo futuras implementaciones dependiendo de la necesidad de la empresa, más detalles se pueden encontrar directamente en el código Tasks.classes.