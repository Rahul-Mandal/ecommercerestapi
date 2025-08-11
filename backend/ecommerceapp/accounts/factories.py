# accounts/factories.py
# from django.conf import settings

# from .models import User

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerceapp.settings")
django.setup()

from django.contrib.auth import get_user_model

class UserFactory:
    @staticmethod
    def create_user(role, **kwargs):
        User = get_user_model()
        if role == 'admin':
            return User.objects.create_superuser(**kwargs)
        elif role == 'vendor':
            return User.objects.create_user(is_staff=True, **kwargs)
        elif role == 'customer':
            return User.objects.create_user(**kwargs)
        else:
            raise ValueError("Invalid role")


user = UserFactory.create_user(
    role='vendor',
    email='vendor@example.com',
    password='securepass'
)


class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Invalid animal type")

# Usage
factory = AnimalFactory()
animal = factory.create_animal("dog")
print(animal.speak())  # Woof!



# settings/models.py

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100)
    maintenance_mode = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.pk = 1  # force only one row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]




