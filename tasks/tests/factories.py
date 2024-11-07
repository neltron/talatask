import factory
from datetime import date


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'tasks.Skill'
    
    name = factory.Faker('name')

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'tasks.Employee'
    
    name = factory.Faker('name')

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for skill in extracted:
                self.skills.add(skill)

class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'tasks.Schedule'
    
    title = factory.Faker('name')

