from django.test import TestCase
from tasks.models import Skill, Employee, Task, Schedule
from .factories import SkillFactory, EmployeeFactory, ScheduleFactory

class SkillModelTest(TestCase):
    def setUp(self) -> None:
        self.skill = SkillFactory()

    def test_name_max_length(self):
        max_length = self.skill._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

class EmployeeModelTest(TestCase):
    def setUp(self) -> None:
        skill = SkillFactory()
        self.employee = EmployeeFactory.create(skills=(skill, ))
    
    def test_name_max_length(self):
        max_length = self.employee._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)
    
    def test_get_all_by_skill(self):
        skill = Skill.objects.get(id=1)
        employee = Employee.objects.get(id=1)
        employee_list = Employee.get_all_by_skill(skill)
        self.assertEqual(employee.id, employee_list[0].id)

